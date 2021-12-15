package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"testing"
)

type Entry struct {
	Digits []string
	Value  []string
}

func secondStar(filename string) int {

	entries := parseFile(filename)
	sum := 0
	for _, e := range entries {
		sum += decodeEntry(e)
	}
	return sum
}

func decodeEntry(e Entry) int {
	codes, numbers := decodeUniquesSizes(e)
	decodeThree(codes, numbers, e)
	decodeTwoFive(codes, numbers, e)
	decodeNineSixCero(codes, numbers, e)
	decodeNineSixCero(codes, numbers, e)
	if len(codes) != 10 || len(numbers) != 10 {
		panic(fmt.Sprintln("No funded all codes for ", e))
	}
	return getMeasure(codes, e)
}

func getMeasure(codes map[string]int, e Entry) int {
	result := getValue(codes, e.Value[0]) * 1000
	result += getValue(codes, e.Value[1]) * 100
	result += getValue(codes, e.Value[2]) * 10
	result += getValue(codes, e.Value[3])
	return result
}

func getValue(codes map[string]int, s string) int {
	for c, v := range codes {
		if contains(c, s) && contains(s, c) {
			return v
		}
	}
	panic(fmt.Sprintln("Not value matched for ", s))
}

func decodeNineSixCero(codes map[string]int, numbers map[int]string, e Entry) {
	//1+3+4=9
	one, tree, four := numbers[1], numbers[3], numbers[4]
	s := one + tree + four
	for _, d := range e.Digits {
		if len(d) == 6 {
			if contains(s, d) {
				addCodeNumber(codes, numbers, d, 9)
			} else { //can be 0 or 6
				if contains(d, one) {
					addCodeNumber(codes, numbers, d, 0)
				} else {
					addCodeNumber(codes, numbers, d, 6)
				}
			}
		}
	}
}

func decodeThree(codes map[string]int, numbers map[int]string, e Entry) {
	//3 share with 1 de left
	for _, d := range e.Digits {
		if len(d) == 5 {
			if contains(d, numbers[1]) {
				addCodeNumber(codes, numbers, d, 3)
				return
			}
		}
	}
}

func decodeTwoFive(codes map[string]int, numbers map[int]string, e Entry) {
	for _, d := range e.Digits {
		if len(d) == 5 {
			if d != numbers[3] {
				//3+4 contains 5
				s := numbers[3] + numbers[4]
				if contains(s, d) {
					addCodeNumber(codes, numbers, d, 5)
				} else {
					addCodeNumber(codes, numbers, d, 2)
				}
			}

		}
	}
}

func contains(secuence, sub string) bool {
	for _, c := range sub {
		finded := false
		for _, d := range secuence {
			if d == c {
				finded = true
				break
			}
		}
		if !finded {
			return false
		}
	}
	return true
}

func decodeUniquesSizes(e Entry) (codes map[string]int, numbers map[int]string) {
	codes = make(map[string]int)
	numbers = make(map[int]string)
	for _, d := range e.Digits {
		switch len(d) {
		case 2:
			addCodeNumber(codes, numbers, d, 1)
		case 3:
			addCodeNumber(codes, numbers, d, 7)
		case 4:
			addCodeNumber(codes, numbers, d, 4)
		case 7:
			addCodeNumber(codes, numbers, d, 8)
		}

	}
	return codes, numbers
}

func addCodeNumber(codes map[string]int, numbers map[int]string, d string, n int) {
	codes[d] = n
	numbers[n] = d
}

func firstStar(filename string) int {
	entries := parseFile(filename)
	solution := countSpecialDigits(entries)
	return solution
}

func countSpecialDigits(entries []Entry) int {
	sum := 0
	for _, e := range entries {
		for _, d := range e.Value {
			switch len(d) {
			case 2, 4, 3, 7:
				sum++
			}
		}
	}
	return sum
}

func parseFile(filename string) (entries []Entry) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		ss := strings.Split(line, " | ")
		entry := Entry{
			Digits: strings.Split(ss[0], " "),
			Value:  strings.Split(ss[1], " "),
		}
		entries = append(entries, entry)

	}
	return entries
}

func TestFirstStar(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"example", 26},
		{"input", 344},
	}
	for _, c := range cases {
		got := firstStar(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}

func TestSecondStar(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"test", 5353},
		{"example", 61229},
		{"input", 1048410},
	}
	for _, c := range cases {
		got := secondStar(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
