package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"testing"
)

type Cave [][]int

func solution(filename string) int {
	cave := parseFile(filename)
	lowPoints := getLowPoints(cave)
	sum := 0
	for _, v := range lowPoints {
		sum += v + 1
	}
	return sum
}

func getLowPoints(cave Cave) (lowPoints []int) {
	neibors := [][]int{
		{-1, 0},
		{1, 0},
		{0, -1},
		{0, 1},
	}
	for y, row := range cave {
		for x, v := range row {
			ismin := true
			for _, cn := range neibors {
				j := y + cn[0]
				i := x + cn[1]
				if i >= 0 && j >= 0 && i < len(cave[0]) && j < len(cave) {
					v1 := cave[j][i]
					if v1 <= v {
						ismin = false
						break
					}
				}
			}
			if ismin {
				lowPoints = append(lowPoints, v)
			}
		}
	}
	return lowPoints
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

func TestSolution(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"example", 15},
		{"input", 425},
	}
	for _, c := range cases {
		got := solution(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
