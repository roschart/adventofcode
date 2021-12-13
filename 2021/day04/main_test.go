package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

type board = []int

func secondStar(filename string) int {
	var lastwinner board
	var lastNumber int
	numbers, boards := parserFile(filename)
	for _, n := range numbers {
		bs := boards[:]
		boards = nil
		for i := 0; i < len(bs); i++ {
			b := bs[i]
			wins := mark(b, n)
			if wins {
				lastwinner = b
				lastNumber = n
			} else {
				boards = append(boards, b)
			}
		}
	}

	return puntuation(lastwinner, lastNumber)
}

func firstStar(filename string) int {
	numbers, boards := parserFile(filename)
	for _, n := range numbers {
		for _, b := range boards {
			wins := mark(b, n)
			if wins {
				return puntuation(b, n)
			}
		}
	}
	return -1
}

func puntuation(b board, n int) int {
	sum := 0
	for _, v := range b {
		if v != -1 {
			sum += v
		}
	}
	return sum * n
}

func mark(b board, n int) bool {
	for i, v := range b {
		if v == n {
			b[i] = -1
			if isRow(b, i) || isColumn(b, i) {
				return true
			}
			break
		}
	}
	return false
}

func isColumn(b board, pos int) bool {
	col := pos % 5
	for i := 0; i < 5; i++ {
		if b[i*5+col] != -1 {
			return false
		}
	}
	return true
}

func isRow(b []int, pos int) bool {
	row := pos / 5
	for i := 0; i < 5; i++ {
		if b[row*5+i] != -1 {
			return false
		}
	}
	return true
}

func parserFile(filename string) (numbers []int, boards []board) {
	file, err := os.Open(filename)

	var pointer int
	var current board
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	i := 0
	for scanner.Scan() {
		if i == 0 {
			numbers = readNumbers(scanner.Text())
		} else {
			line := scanner.Text()
			//If line is empty create new board
			if line == "" {
				b := make(board, 25)
				current = b
				boards = append(boards, current)
				pointer = 0
			} else {
				row := getRow(line)
				for _, n := range row {
					current[pointer] = n
					pointer++
				}
			}
		}
		i++

	}
	return numbers, boards
}

func getRow(line string) []int {
	var row []int
	fields := strings.Fields(line)
	for _, f := range fields {
		n, _ := strconv.Atoi(f)
		row = append(row, n)
	}
	return row

}

func readNumbers(s string) (numbers []int) {
	ns := strings.Split(s, ",")

	for _, n := range ns {
		d, _ := strconv.Atoi(n)
		numbers = append(numbers, d)
	}
	return
}

func TestExample(t *testing.T) {
	result := firstStar("example")
	expected := 4512

	if expected != result {
		t.Errorf("Expected %d,  got %d", expected, result)
	}
}

func TestCollumn(t *testing.T) {
	result := firstStar("example2")
	expected := 2450

	if expected != result {
		t.Errorf("Expected %d,  got %d", expected, result)
	}
}

func TestFirstStar(t *testing.T) {
	result := firstStar("input")
	expected := 64084

	if expected != result {
		t.Errorf("Expected %d,  got %d", expected, result)
	}
}

func TestExampleSecondStar(t *testing.T) {
	result := secondStar("example")
	expected := 1924

	if expected != result {
		t.Errorf("Expected %d,  got %d", expected, result)
	}
}

func TestSecondtStar(t *testing.T) {
	result := secondStar("input")
	expected := 64084

	if expected != result {
		t.Errorf("Expected %d,  got %d", expected, result)
	}
}
