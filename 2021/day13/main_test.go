package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

type axe = int

const (
	X int = iota
	Y
)

type dot struct {
	X int
	Y int
}

type fold struct {
	axe   axe
	value int
}

func firstStar(filename string) int {
	var dots []dot
	var folds []fold
	dots, folds = parseFile(filename)
	dots = makeFold(dots, folds[0])
	solution := countPoints(dots)
	return solution

}

func countPoints(dots []dot) int {
	panic("unimplemented")
}

func makeFold(dots []dot, fold fold) []dot {
	panic("unimplemented")
}

func parseFile(filename string) (dots []dot, folds []fold) {
	state := "reading_dots"
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			state = "reading_folds"
			continue

		}
		if state == "reading_dots" {
			dot := readDot(line)
			dots = append(dots, dot)
		} else {
			fold := readFold(line)
			folds = append(folds, fold)

		}
	}
	return dots, folds
}

func readDot(s string) dot {
	ns := strings.Split(s, ",")
	x, _ := strconv.Atoi(ns[0])
	y, _ := strconv.Atoi(ns[1])
	return dot{
		X: x,
		Y: y,
	}
}

func readFold(s string) fold {
	ns := strings.Split(s, "=")
	value, _ := strconv.Atoi(ns[1])
	dir := ns[0][len(ns[0])-1]
	if dir == 'y' {
		return fold{
			axe:   Y,
			value: value,
		}
	} else {
		return fold{
			axe:   X,
			value: value,
		}

	}

}

func TestExampe(t *testing.T) {
	got := firstStar("example")
	expected := 17
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}

}
