package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

type command struct {
	Order string
	Size  int
}

func parserFile(filename string) []command {
	var result []command
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		words := strings.Split(line, " ")
		order := words[0]
		size, _ := strconv.Atoi(words[1])
		result = append(result, command{order, size})

	}
	return result
}

func fistStar(commands []command) (position int, depth int) {
	for _, c := range commands {
		switch c.Order {
		case "forward":
			position += c.Size
		case "down":
			depth += c.Size
		case "up":
			depth -= c.Size
		}
	}
	return
}

func secondStar(commands []command) (position int, depth int) {
	aim := 0
	for _, c := range commands {
		switch c.Order {
		case "forward":
			position += c.Size
			depth += c.Size * aim
		case "down":
			aim += c.Size
		case "up":
			aim -= c.Size
		}
	}
	return
}

func TestExampe(t *testing.T) {
	data := parserFile("example")
	p, d := fistStar(data)
	pe := 15
	de := 10

	if p != pe || d != de {
		t.Errorf("Expected p=%d, d=%d, got %d, %d", pe, de, p, d)

	}
}

func TestFirstStar(t *testing.T) {
	data := parserFile("input")
	p, d := fistStar(data)
	expected := 2120749
	got := p * d

	if expected != got {
		t.Errorf("Expected %d, , got %d", expected, got)
	}
}

func TestExampe2(t *testing.T) {
	data := parserFile("example")
	p, d := secondStar(data)
	pe := 15
	de := 60

	if p != pe || d != de {
		t.Errorf("Expected p=%d, d=%d, got %d, %d", pe, de, p, d)

	}
}

func TestSecondtStar(t *testing.T) {
	data := parserFile("input")
	p, d := secondStar(data)
	expected := 2138382217
	got := p * d

	if expected != got {
		t.Errorf("Expected %d, , got %d", expected, got)
	}
}
