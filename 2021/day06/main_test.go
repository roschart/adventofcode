package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

type Fish map[int]int

func firstStar(filename string, steps int) int {

	fish := parseFile(filename)

	for i := 0; i < steps; i++ {
		fish = makeStep(fish)
	}

	solution := countFishs(fish)
	return solution
}

func countFishs(fish Fish) int {
	sum := 0
	for _, v := range fish {
		sum += v
	}
	return sum
}

func makeStep(fish Fish) Fish {
	result := make(Fish)
	for k, v := range fish {
		if k == 0 {
			result[8] = v
			result[6] += v
		} else {
			result[k-1] += v
		}
	}
	return result
}

func parseFile(filename string) Fish {
	fish := make(map[int]int)
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
			fish[n] += 1
		}
	}
	return fish
}

func TestExample(t *testing.T) {
	cases := []struct{ step, result int }{
		{1, 5},
		{18, 26},
		{80, 5934},
		{256, 26984457539},
	}
	for _, c := range cases {
		got := firstStar("example", c.step)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}

}

func TestSolution(t *testing.T) {
	cases := []struct{ step, result int }{
		{80, 360268},
		{256, 0},
	}
	for _, c := range cases {
		got := firstStar("input", c.step)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}

}

func TestFirstStar(t *testing.T) {
	got := firstStar("input", 80)
	expected := 0
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}
