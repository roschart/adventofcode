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

type Dot struct {
	X int
	Y int
}

type Fold struct {
	axe   axe
	value int
}

func firstStar(filename string) int {
	var dots []Dot
	var folds []Fold
	dots, folds = parseFile(filename)
	dots = makeFold(dots, folds[0])
	solution := countPoints(dots)
	return solution

}

func secondStar(filename string, nx int, ny int) {
	var dots []Dot
	var folds []Fold
	dots, folds = parseFile(filename)
	for _, f := range folds {
		dots = makeFold(dots, f)
	}
	printDots(dots, nx, ny)

}

func printDots(dots []Dot, nx int, ny int) {
	matrix := make([][]rune, nx)
	for i := range matrix {
		matrix[i] = make([]rune, ny)
		for j := range matrix[i] {
			matrix[i][j] = ' '
		}
	}

	for _, d := range dots {
		matrix[d.Y][d.X] = 'X'
	}

	for i := 0; i < nx; i++ {
		fmt.Println(string(matrix[i]))
	}
}

func countPoints(dots []Dot) int {
	return len(dots)
}

func makeFold(dots []Dot, fold Fold) []Dot {
	var result []Dot
	if fold.axe == Y {
		for _, d := range dots {
			if d.Y < fold.value {
				result = append(result, d)
			} else if d.Y > fold.value {
				// y1= 2f-y+1
				y1 := 2*fold.value - d.Y
				result = append(result, Dot{X: d.X, Y: y1})
			}
		}
	} else {
		for _, d := range dots {
			if d.X < fold.value {
				result = append(result, d)
			} else if d.X > fold.value {
				// x1= 2f-x+1
				x1 := 2*fold.value - d.X
				result = append(result, Dot{X: x1, Y: d.Y})
			}
		}
	}
	return deduplicate(result)
}

func deduplicate(dots []Dot) []Dot {
	const N = 10000
	m := make(map[int]Dot)
	for _, d := range dots {
		x := d.X*N + d.Y
		m[x] = d
	}
	var result []Dot
	for _, d := range m {
		result = append(result, d)
	}

	return result
}

func parseFile(filename string) (dots []Dot, folds []Fold) {
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

func readDot(s string) Dot {
	ns := strings.Split(s, ",")
	x, _ := strconv.Atoi(ns[0])
	y, _ := strconv.Atoi(ns[1])
	return Dot{
		X: x,
		Y: y,
	}
}

func readFold(s string) Fold {
	ns := strings.Split(s, "=")
	value, _ := strconv.Atoi(ns[1])
	dir := ns[0][len(ns[0])-1]
	if dir == 'y' {
		return Fold{
			axe:   Y,
			value: value,
		}
	} else {
		return Fold{
			axe:   X,
			value: value,
		}

	}

}

func TestExample(t *testing.T) {
	got := firstStar("example")
	expected := 17
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestFirstStar(t *testing.T) {
	got := firstStar("input")
	expected := 724
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestSecondStar(t *testing.T) {
	secondStar("input", 6, 40)
	t.Fail()

}
