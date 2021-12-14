package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
	"testing"
)

func secondStar(filename string) int {
	positions := parseFile(filename)
	fuel := 0 //With only one elmente fuel needed is 0
	value := positions[0]
	for i := 1; i < len(positions); i++ {
		fuel, value = calculateNext(positions, i, value)
	}
	return fuel
}

func calculateNext(positions []int, n, value int) (fuel, nvalue int) {
	fuel = calculateFuel(positions, n, value)
	p := positions[n]

	if p == value {
		return calculateFuel(positions, n, value), value
	}
	step := 1
	if p < value {
		step = -1
	}
	nvalue = value + step
	nfuel := calculateFuel(positions, n, nvalue)
	for nfuel < fuel {
		nvalue += step
		fuel = nfuel
		nfuel = calculateFuel(positions, n, nvalue)
	}
	return fuel, nvalue - step
}

func calculateFuel(positions []int, n, value int) int {
	fuel := 0
	for i := 0; i <= n; i++ {
		a := positions[i]
		d := a - value
		if d < 0 {
			d = -d
		}
		spend := d * (d + 1) / 2
		fuel += spend
	}
	return fuel
}

func firstStar(filename string) int {

	positions := parseFile(filename)

	position := calculateMedian(positions)
	solution := calcuateFuel(positions, position)

	return solution
}

func calcuateFuel(positions []int, position int) (fuel int) {
	for _, p := range positions {
		f := p - position
		if f < 0 {
			f = -f
		}
		fuel += f
	}
	return fuel
}

func calculateMedian(positions []int) int {

	sort.Ints(positions)
	median := len(positions) / 2
	return positions[median]
}

func parseFile(filename string) (positions []int) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		ss := strings.Split(line, ",")
		for _, s := range ss {
			n, _ := strconv.Atoi(s)
			positions = append(positions, n)
		}
	}
	return positions
}

func TestExample(t *testing.T) {
	cases := []struct{ result int }{
		{37},
	}
	for _, c := range cases {
		got := firstStar("example")
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}

func TestFirst(t *testing.T) {
	cases := []struct{ result int }{
		{356958},
	}
	for _, c := range cases {
		got := firstStar("input")
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}

func TestSecond(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"test", 13},
		{"example", 168},
		{"input", 105461913},
	}
	for _, c := range cases {
		got := secondStar(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
