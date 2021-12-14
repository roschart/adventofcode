package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strings"
	"testing"
)

type Secuence = string
type Rules map[string]string
type Pairs map[string]int

func firstStar(filename string, steps int) int {

	secuence, rules := parseFile(filename)

	for i := 0; i < steps; i++ {
		secuence = makeStep(secuence, rules)
	}

	solution := countSecuence(secuence)
	return solution
}

func secondStar(filename string, steps int) int {
	secuence, rules := parseFile(filename)
	pairs := genPairs(secuence, rules)
	for i := 0; i < steps; i++ {
		pairs = nextStep(pairs, rules)
	}
	solution := countPairs(pairs, secuence[0:1])
	return solution
}

func countPairs(pairs Pairs, s string) int {
	stats := make(map[rune]int)
	stats[rune(s[0])] = 1 //First character
	for k, v := range pairs {
		c := k[1] //Take the second character
		stats[rune(c)] += v
	}
	max, min := getMaxMin(stats)
	return max - min
}

func nextStep(pairs Pairs, rules Rules) Pairs {
	result := make(Pairs)
	for k, v := range pairs {
		r := rules[k]
		pairA := k[0:1] + r
		pairB := r + k[1:2]
		result[pairA] += v
		result[pairB] += v
	}
	return result
}

func genPairs(secuence string, rules Rules) (pairs Pairs) {
	pairs = make(Pairs)
	for i := 0; i < len(secuence)-1; i++ {
		pair := secuence[i : i+2]
		pairs[pair] = pairs[pair] + 1
	}
	return pairs
}

func countSecuence(secuence string) int {
	stats := make(map[rune]int)

	for _, c := range secuence {
		if v, ok := stats[c]; ok {
			stats[c] = v + 1
		} else {
			stats[c] = 1
		}
	}
	max, min := getMaxMin(stats)
	return max - min
}

func getMaxMin(stats map[rune]int) (max int, min int) {
	max = 0
	min = math.MaxInt64
	for _, v := range stats {
		if v > max {
			max = v
		}
		if v < min {
			min = v
		}
	}
	return max, min
}

func makeStep(secuence string, rules Rules) (result Secuence) {

	for i := 0; i < len(secuence)-1; i++ {
		pair := secuence[i : i+2]
		r := rules[pair]
		result = result + pair[0:1] + r
	}
	result += secuence[len(secuence)-1:]
	return result

}

func parseFile(filename string) (secuence Secuence, rules Rules) {
	rules = make(Rules)
	state := "reading_secuence"
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if line == "" {
			state = "reading_rules"
			continue

		}
		if state == "reading_secuence" {
			secuence = line
		} else {
			ss := strings.Split(line, " -> ")
			rules[ss[0]] = ss[1]
		}
	}
	return secuence, rules
}

func TestExample(t *testing.T) {
	got := firstStar("example", 10)
	expected := 1588
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestFirstStar(t *testing.T) {
	got := firstStar("input", 10)
	expected := 3009
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestSecondStarExample(t *testing.T) {
	got := secondStar("example", 10)
	expected := 1588
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}

func TestSecondStar(t *testing.T) {
	got := secondStar("input", 40)
	expected := 1588
	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}
