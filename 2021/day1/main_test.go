package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"testing"
)

func fistStar() int {
	file, err := os.Open("input")
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	var previous int64
	result := 0
	i := 0

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		number, _ := strconv.ParseInt(scanner.Text(), 10, 0)
		if i > 0 && number > previous {
			result++
		}
		previous = number
		i++
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}
	return result
}

func secondStar() int {
	file, err := os.Open("input")
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	var a, b, c, d int64
	result := 0
	i := 0

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		d, _ = strconv.ParseInt(scanner.Text(), 10, 0)
		current := b + c + d
		previous := a + b + c
		if i >= 3 && current > previous {
			result++
		}
		fmt.Println(a, b, c, d, current, previous, result)
		a, b, c = b, c, d
		i++
	}

	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}
	return result
}

func count(data []int) int {
	previous := 0
	result := 0
	for i, v := range data {
		if i > 0 && v > previous {
			result++
		}
		previous = v
	}

	return result
}
func TestExample(t *testing.T) {
	data := []int{
		199,
		200,
		208,
		210,
		200,
		207,
		240,
		269,
		260,
		263,
	}
	result := count(data)
	if count(data) != 7 {
		t.Errorf("Count(data) = %d; want 7", result)
	}
}

func TestFirstStar(t *testing.T) {
	result := fistStar()
	expected := 1521
	if result != expected {
		t.Errorf("fistStar = %d; want %d", result, expected)
	}

}
func TestSecondStar(t *testing.T) {
	result := secondStar()
	expected := 1521
	if result != expected {
		t.Errorf("secondStar = %d; want %d", result, expected)
	}

}
