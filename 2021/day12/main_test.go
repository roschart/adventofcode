package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"testing"
)

type TypeCave int

const (
	Start TypeCave = iota
	End
	Small
	Big
)

type CaveId struct {
	TypeID TypeCave
	Code   string
}

func (c CaveId) String() string {
	return c.Code
}

func NewCaveId(code string) CaveId {
	caveId := CaveId{Code: code}
	switch {
	case code == "start":
		caveId.TypeID = Start
	case code == "end":
		caveId.TypeID = End
	case isBig(code):
		caveId.TypeID = Big
	case isSmall(code):
		caveId.TypeID = Small
	default:
		panic(fmt.Sprintf("Bad code cave %s", code))
	}
	return caveId
}

func isBig(code string) bool {
	c := code[0]
	return 'A' <= c && c <= 'Z'
}
func isSmall(code string) bool {
	c := code[0]
	return 'a' <= c && c <= 'z'
}

type Connections struct {
	//cave     CaveId
	conected []CaveId
}

type CaveMap map[CaveId]Connections //To simulate a set

func findPathsFromFile(filename string) int {
	cave := parseFile(filename)
	paths := findPaths(cave)
	return len(paths)
}

func findPaths(caveMap CaveMap) (paths [][]CaveId) {
	start := NewCaveId("start")
	open := [][]CaveId{
		{start},
	}
	var closed [][]CaveId

	for len(open) > 0 {
		path := open[0]
		open = open[1:]
		cave := path[len(path)-1]
		cs := caveMap[cave].conected
		if contains(path, NewCaveId("end")) {
			continue
		}
		for _, c := range cs {
			switch {
			case c.TypeID == End:
				ne := appendPath(path, c)
				closed = appendPaths(closed, ne)

			case c.TypeID == Big:
				nb := appendPath(path, c)
				open = appendPaths(open, nb)
			case c.TypeID == Small:
				if !contains(path, c) {
					nc := appendPath(path, c)
					open = appendPaths(open, nc)
				}
			}
		}
	}
	return closed
}

func appendPaths(paths [][]CaveId, ne []CaveId) [][]CaveId {
	result := make([][]CaveId, len(paths))
	copy(result, paths)
	return append(result, ne)
}

func appendPath(path []CaveId, c CaveId) []CaveId {
	result := make([]CaveId, len(path))
	copy(result, path)
	return append(result, c)

}

func contains(path []CaveId, c CaveId) bool {
	for _, v := range path {
		if v == c {
			return true
		}
	}
	return false
}

func parseFile(filename string) (caveMap CaveMap) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	caveMap = make(CaveMap)
	for scanner.Scan() {
		line := scanner.Text()
		ss := strings.Split(line, "-")
		a := NewCaveId(ss[0])
		b := NewCaveId(ss[1])
		connect(a, b, caveMap)
	}
	return caveMap
}

func connect(a, b CaveId, caveMap CaveMap) {
	ca := caveMap[a]
	cb := caveMap[b]
	if b.TypeID != Start {
		ca.conected = appendPath(ca.conected, b)
		caveMap[a] = ca
	}
	if a.TypeID != Start {
		cb.conected = appendPath(cb.conected, a)
		caveMap[b] = cb
	}
}

func TestFirstStar(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"example", 10},
		{"example2", 19},
		{"example3", 226},
		{"input", 4775},
	}
	for _, c := range cases {
		got := findPathsFromFile(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
