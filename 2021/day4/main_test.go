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

func TestExampe(t *testing.T) {
	numbers, boards := parserFile("example")
	t.Log(numbers, boards)
	t.Fail()
}
