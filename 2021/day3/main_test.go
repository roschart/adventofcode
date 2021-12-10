package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"testing"
)

type diagnostic = string
type generator int

const (
	Oxygen generator = iota
	CO2
)

func parserFile(filename string) (diagnostics []diagnostic) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		d := scanner.Text()
		diagnostics = append(diagnostics, d)

	}
	return diagnostics
}

func firstStar(diagnostics []diagnostic) (int, int) {
	n := len(diagnostics[0])
	gamma := make([]rune, n)
	epsilon := make([]rune, n)
	count := make([]int, n)
	for _, diag := range diagnostics {
		bits := strings.Split(diag, "")
		for i := 0; i < n; i++ {
			bit, _ := strconv.Atoi(bits[i])
			count[i] += bit
		}
	}
	size := len(diagnostics)
	for i := 0; i < n; i++ {
		if count[i] > size/2 {
			gamma[i] = '1'
			epsilon[i] = '0'
		} else {
			gamma[i] = '0'
			epsilon[i] = '1'
		}
	}
	g, _ := strconv.ParseInt(string(gamma), 2, 0)
	e, _ := strconv.ParseInt(string(epsilon), 2, 0)
	return int(g), int(e)
}

func secondStar(diagnostics []diagnostic, g generator) int {
	n := len(diagnostics[0])
	size := len(diagnostics)
	for pos := 0; pos < n && size > 1; pos++ {
		var ones, ceros int
		for _, diag := range diagnostics {
			if diag[pos] == '1' {
				ones++
			} else {
				ceros++
			}
		}
		//Chose the selector to filter
		var selec byte
		if (ones >= ceros && g == Oxygen) || ones < ceros && g == CO2 {
			selec = '1'
		} else {
			selec = '0'
		}

		//fiter with the selection
		var filter []diagnostic
		for _, d := range diagnostics {
			if d[pos] == selec {
				filter = append(filter, d)
			}
		}
		diagnostics = filter
		size = len(diagnostics)
	}
	result, _ := strconv.ParseInt(string(diagnostics[0]), 2, 0)
	return int(result)
}

func TestExampe(t *testing.T) {
	data := parserFile("example")
	g, e := firstStar(data)
	ge := 22
	ee := 9

	if g != ge || e != ee {
		t.Errorf("Expected p=%d, d=%d, got %d, %d", ge, ee, g, e)

	}
}

func TestFirstStar(t *testing.T) {
	data := parserFile("input")
	g, e := firstStar(data)
	expected := 2743844
	got := g * e

	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)

	}
}

func TestExampe2(t *testing.T) {
	data := parserFile("example")

	o := secondStar(data, Oxygen)
	oe := 23
	c := secondStar(data, CO2)
	ce := 10

	if o != oe || c != ce {
		t.Errorf("Expected p=%d, d=%d, got %d, %d", oe, ce, o, c)
	}
}

func TestSecondStar(t *testing.T) {
	data := parserFile("input")

	o := secondStar(data, Oxygen)
	c := secondStar(data, CO2)
	expected := 0
	got := c * o

	if expected != got {
		t.Errorf("Expected %d,  got %d", expected, got)
	}
}
