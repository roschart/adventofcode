package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"testing"
)

type Cave [][]int

type Coord struct {
	X, Y int
}

type Points map[Coord]int

func solutionBasin(filename string) int {
	cave := parseFile(filename)
	lowPoints := getLowPoints(cave)
	basins := getBasins(cave, lowPoints)
	mult := 1
	sort.Ints(basins)
	basins = basins[len(basins)-3:]
	for _, v := range basins {
		mult *= v
	}
	return mult
}

func getBasins(cave Cave, lowPoints Points) (basins []int) {
	for c := range lowPoints {
		sum := 0
		//Create 2 sets
		open := make(map[Coord]bool)
		close := make(map[Coord]bool)
		open[c] = true
		for len(open) > 0 {
			sum++
			o := getOneElement(open)
			delete(open, o)
			close[o] = true
			ns := getNeigbors(cave, o)
			for c, v := range ns {
				if v != 9 {
					if _, ok := close[c]; !ok {
						open[c] = true
					}
				}
			}
		}
		basins = append(basins, sum)
	}
	return basins
}

func getOneElement(set map[Coord]bool) Coord {
	for c := range set {
		return c
	}
	panic("EmptyPoints")
}

func solutionLowPoints(filename string) int {
	cave := parseFile(filename)
	lowPoints := getLowPoints(cave)
	sum := 0
	for _, v := range lowPoints {
		sum += v + 1
	}
	return sum
}

func getLowPoints(cave Cave) (lowPoints Points) {
	lowPoints = make(Points)
	for y, row := range cave {
		for x, v := range row {
			ismin := true
			for _, v1 := range getNeigbors(cave, Coord{x, y}) {
				if v1 <= v {
					ismin = false
					break
				}
			}
			if ismin {
				lowPoints[Coord{x, y}] = v
			}
		}
	}
	return lowPoints
}

func getNeigbors(cave Cave, c Coord) (neigbors Points) {
	neigbors = make(Points)
	near := [][]int{
		{-1, 0},
		{1, 0},
		{0, -1},
		{0, 1},
	}
	for _, n := range near {
		j := c.Y + n[0]
		i := c.X + n[1]
		if i >= 0 && j >= 0 && i < len(cave[0]) && j < len(cave) {
			neigbors[Coord{i, j}] = cave[j][i]
		}
	}
	return neigbors
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

func TestSolutionLowPoints(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"example", 15},
		{"input", 425},
	}
	for _, c := range cases {
		got := solutionLowPoints(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}

func TestSolutionBasins(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"example", 1134},
		{"input", 1135260},
	}
	for _, c := range cases {
		got := solutionBasin(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
