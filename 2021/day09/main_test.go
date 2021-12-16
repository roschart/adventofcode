package main

import (
	"bufio"
	"fmt"
	"os"
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
	sum := 0
	for _, v := range basins {
		sum += v + 1
	}
	return sum
}

func getBasins(cave Cave, lowPoints Points) []int {

	panic("Pending to implement")
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
			for _, v1 := range getNeigbors(cave, x, y) {
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

func getNeigbors(cave Cave, x, y int) (neigbors Points) {
	neigbors = make(Points)
	near := [][]int{
		{-1, 0},
		{1, 0},
		{0, -1},
		{0, 1},
	}
	for _, n := range near {
		j := y + n[0]
		i := x + n[1]
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

func TestSolution(t *testing.T) {
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
