package main

import (
	"bufio"
	"fmt"
	"os"
	"sort"
	"testing"
)

func secondStar(filename string) int {
	lines := parseFile(filename)
	return scoreIncomplete(lines)
}

func scoreIncomplete(lines []string) int {
	var ss []int
	s := map[rune]int{
		')': 1,
		']': 2,
		'}': 3,
		'>': 4,
	}
	for _, l := range lines {
		_, i := isCorrupted(l)
		if i == "" {
			continue
		}
		sum := 0
		for _, c := range i {
			sum *= 5
			sum += s[c]
		}
		ss = append(ss, sum)
	}
	sort.Ints(ss)
	return ss[len(ss)/2]
}

func firstStar(filename string) int {
	lines := parseFile(filename)
	return scoreCorrupted(lines)
}

func scoreCorrupted(lines []string) (sum int) {
	s := map[rune]int{
		')': 3,
		']': 57,
		'}': 1197,
		'>': 25137,
	}
	for _, l := range lines {
		c, _ := isCorrupted(l)
		sum += s[c]
	}
	return sum
}

func isCorrupted(line string) (rune, string) {
	pairs := map[rune]rune{
		'(': ')',
		'[': ']',
		'{': '}',
		'<': '>',
	}
	var open []rune
	for _, r := range line {
		if c, ok := pairs[r]; ok {
			open = append(open, c)
		} else {
			var v rune
			open, v = pop(open)
			if r != v {
				return r, ""
			}
		}
	}
	return 0, reverse(open)
}

func reverse(rs []rune) (result string) {
	for _, v := range rs {
		result = string(v) + result
	}
	return
}

func pop(ls []rune) ([]rune, rune) {
	l := len(ls)
	v := ls[l-1]
	ls = ls[:l-1]
	return ls, v
}

func parseFile(filename string) (lines []string) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}

	return lines
}

func TestScoreIncomplete(t *testing.T) {
	cases := []struct {
		file   string
		result int
	}{
		{"example", 288957},
		{"input", 3354640192},
	}
	for _, c := range cases {
		got := secondStar(c.file)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
func TestScoreCorrupted(t *testing.T) {
	cases := []struct {
		file   string
		result int
	}{
		{"example", 26397},
		{"input", 413733},
	}
	for _, c := range cases {
		got := firstStar(c.file)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}

func TestCorrupted(t *testing.T) {
	cases := []struct {
		line   string
		result rune
	}{
		{"()", 0},
		{"[]", 0},
		{"{}", 0},
		{"<>", 0},
		{"([])", 0},
		{"(", 0},
		{"[", 0},
		{"([]", 0},
		{"(]", ']'},
		{"{()()()>", '>'},
		{"(((()))}", '}'},
		{"<([]){()}[{}])", ')'},
	}

	for _, c := range cases {
		got, _ := isCorrupted(c.line)
		expected := c.result
		if expected != got {
			t.Errorf("With %q: Expected %q,  got %q", c.line, expected, got)
		}
	}
}

func TestIncomplete(t *testing.T) {
	cases := []struct {
		line   string
		result string
	}{{"([", "])"},
		{"[({(<(())[]>[[{[]{<()<>>", "}}]])})]"},
		{"[(()[<>])]({[<{<<[]>>(", ")}>]})"},
		{"()", ""},
	}

	for _, c := range cases {
		_, got := isCorrupted(c.line)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %q,  got %q", expected, got)
		}
	}
}
