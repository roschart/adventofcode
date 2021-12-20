package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"testing"
)

type Cave [][]int

func (c Cave) String() (result string) {
	result = ""
	for _, row := range c {
		for _, v := range row {
			result += fmt.Sprintf("%d", v)
		}
		result += fmt.Sprintln()
	}
	return result
}

func (c Cave) allFlash() bool {
	for _, row := range c {
		for _, v := range row {
			if v != 0 {
				return false
			}
		}
	}
	return true
}

func solution(filename string, repeat int) (int, int) {
	first_all_flash := -1
	cave := parseFile(filename)
	sum := 0
	i := 0
	for ; i < repeat; i++ {
		sum += step(cave)
		if cave.allFlash() {
			first_all_flash = i
		}
	}

	for first_all_flash < 0 {
		step(cave)
		i = i + 1
		if cave.allFlash() {
			first_all_flash = i
		}
	}

	return sum, first_all_flash
}

func parseFile(filename string) (cave Cave) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		var row []int
		for _, c := range line {
			n, _ := strconv.Atoi(string(c))
			row = append(row, n)
		}
		cave = append(cave, row)
	}
	return cave
}

func step(cave Cave) int {
	addOneToAll(cave)
	return executeFlashes(cave)

}

func addOneToAll(cave Cave) {
	for j, row := range cave {
		for i, v := range row {
			cave[j][i] = v + 1
		}
	}
}

func executeFlashes(cave Cave) int {
	flashes := 0
	must_loop := true
	for must_loop {
		must_loop = false
		for j, row := range cave {
			for i, v := range row {
				if v > 9 {
					flashes++
					cave[j][i] = 0

					if addOneToNeibors(cave, j, i) {
						must_loop = true
					}
				}
			}
		}
	}
	return flashes
}

func addOneToNeibors(cave Cave, j, i int) bool {
	flash := false
	neigbors := [][]int{
		{-1, -1},
		{-1, 0},
		{-1, 1},
		{0, -1},
		{0, 1},
		{1, -1},
		{1, 0},
		{1, 1},
	}
	for _, n := range neigbors {
		y := j + n[0]
		x := i + n[1]
		if x >= 0 && y >= 0 && y < len(cave) && x < len(cave[0]) {
			if cave[y][x] > 0 {
				cave[y][x] += 1
				if cave[y][x] > 9 {
					flash = true
				}
			}
		}
	}
	return flash
}

func TestSolution(t *testing.T) {
	cases := []struct {
		filename        string
		repeat          int
		num_flashes     int
		first_all_flash int
	}{
		{"example", 100, 1656, 195},
		{"input", 100, 1665, 235},
	}
	for _, c := range cases {
		flash, first := solution(c.filename, c.repeat)
		expected := c.num_flashes
		if expected != flash {
			t.Errorf("Expected %d,  got %d", expected, flash)
		}
		if c.first_all_flash != first {
			t.Errorf("Expected %d,  got %d", c.first_all_flash, first)
		}
	}
}
