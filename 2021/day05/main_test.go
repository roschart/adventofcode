package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

type Point struct {
	X, Y int
}

type Segment struct {
	A, B Point
}

type SegmentData struct {
	Segments []Segment
	Max_x    int
	Max_y    int
}

func firstStar(filename string) int {
	segmentsData := parseFile(filename)
	diagram := makeDiagram(segmentsData, false)
	return countDiagram(diagram)
}

func secondStar(filename string) int {
	segmentsData := parseFile(filename)
	diagram := makeDiagram(segmentsData, true)
	return countDiagram(diagram)
}

func printDiagram(diagram [][]int) {
	for _, line := range diagram {
		fmt.Println(line)
	}
}

func countDiagram(diagram [][]int) int {
	sum := 0
	for _, line := range diagram {
		for _, v := range line {
			if v > 1 {
				sum++
			}
		}
	}
	return sum
}

func makeDiagram(sd SegmentData, hasDiagonals bool) [][]int {
	diagram := make([][]int, sd.Max_y+1)
	for i := range diagram {
		diagram[i] = make([]int, sd.Max_x+1)
	}
	for _, s := range sd.Segments {
		if isVertical(s) || isHorizontal(s) {
			addPoints(diagram, s)
		}
		if hasDiagonals {
			if isDiagonal(s) {
				addPoints(diagram, s)
			}
		}
	}
	return diagram
}

func isDiagonal(s Segment) bool {
	x := s.A.X - s.B.X
	y := s.A.Y - s.B.Y
	return x*x == y*y
}

func addPoints(diagram [][]int, s Segment) {
	if isVertical(s) {
		addVerticalPoints(diagram, s)
	}
	if isHorizontal(s) {
		addHorizontalPoints(diagram, s)
	}
	if isDiagonal(s) {
		addDiagonalPoints(diagram, s)
	}
}

func addVerticalPoints(diagram [][]int, s Segment) {
	a := s.A.Y
	b := s.B.Y

	if b < a {
		a, b = b, a
	}
	for i := a; i <= b; i++ {
		diagram[i][s.A.X] += 1
	}

}
func addHorizontalPoints(diagram [][]int, s Segment) {
	a := s.A.X
	b := s.B.X

	if b < a {
		a, b = b, a
	}
	for i := a; i <= b; i++ {
		diagram[s.A.Y][i] += 1
	}

}

func addDiagonalPoints(diagram [][]int, s Segment) {
	vstep, hstep := 1, 1
	if s.B.X < s.A.X {
		hstep = -1
	}
	if s.B.Y < s.A.Y {
		vstep = -1
	}

	size := s.A.X - s.B.X
	if size < 0 {
		size = -size
	}
	i := s.A.X
	j := s.A.Y
	for k := 0; k <= size; k++ {
		diagram[j][i] += 1
		i += hstep
		j += vstep
	}

}

func isVertical(s Segment) bool {
	return s.A.X == s.B.X
}
func isHorizontal(s Segment) bool {
	return s.A.Y == s.B.Y
}

func parseFile(filename string) (sd SegmentData) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		segment := readSegment(line)
		if segment.A.X > sd.Max_x {
			sd.Max_x = segment.A.X
		}
		if segment.B.X > sd.Max_x {
			sd.Max_x = segment.B.X
		}
		if segment.A.Y > sd.Max_y {
			sd.Max_y = segment.A.Y
		}
		if segment.B.Y > sd.Max_y {
			sd.Max_y = segment.B.Y
		}
		sd.Segments = append(sd.Segments, segment)
	}
	return sd
}

func readSegment(s string) Segment {
	ns := strings.Split(s, " -> ")
	origin := strings.Split(ns[0], ",")
	x1, _ := strconv.Atoi(origin[0])
	y1, _ := strconv.Atoi(origin[1])
	dest := strings.Split(ns[1], ",")
	x2, _ := strconv.Atoi(dest[0])
	y2, _ := strconv.Atoi(dest[1])
	return Segment{
		A: Point{x1, y1},
		B: Point{x2, y2},
	}
}

func TestExample(t *testing.T) {
	got := firstStar("example")
	expected := 5
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestFirstStar(t *testing.T) {
	got := firstStar("input")
	expected := 8060
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestExampleSecondStar(t *testing.T) {
	got := secondStar("example")
	expected := 12
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestSecondStar(t *testing.T) {
	got := secondStar("input")
	expected := 21577
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}
