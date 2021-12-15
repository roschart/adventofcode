package main

import (
	"bufio"
	"fmt"
	"math"
	"os"
	"strconv"
	"testing"
)

type Cave [][]int
type Node struct {
	X, Y, G, H, Value, X_p, Y_p int
}

func (n *Node) Hash() string {
	return fmt.Sprintf("x:%d,y:%d", n.X, n.Y)
}

func NewNode(x, y int, parent Node, cave Cave) Node {
	len_x := len(cave[0])
	len_y := len(cave)

	n := Node{
		X:     x,
		Y:     y,
		Value: cave[x][y],
		X_p:   parent.X,
		Y_p:   parent.Y,
	}
	n.H = len_x - n.X + len_y - n.Y - 2
	n.G = parent.G + n.Value
	return n
}

func firstStar(filename string) int {
	cave := parseFile(filename)
	lastNode := getPath(cave)
	return lastNode.G
}

func getPath(cave Cave) Node {
	open := make(map[string]Node)
	close := make(map[string]Node)
	n := NewNode(0, 0, Node{}, cave)
	n.G = 0
	open[n.Hash()] = n
	for len(open) > 0 {
		n = getLessCost(open)

		delete(open, n.Hash())
		ns := neighbor(n, cave)
		for _, ne := range ns {
			if isGoal(ne, cave) {
				return ne
			}
			if no, ok := open[ne.Hash()]; ok {
				if no.G+no.H < ne.G+ne.H {
					continue
				}
			}
			if no, ok := close[ne.Hash()]; ok {
				if no.G+no.H < ne.G+ne.H {
					continue
				}
			}
			open[ne.Hash()] = ne
		}
		close[n.Hash()] = n
	}
	return Node{}
}

func isGoal(n Node, cave Cave) bool {
	return n.X == len(cave[0])-1 && n.Y == len(cave)-1
}

func neighbor(n Node, cave Cave) (ns []Node) {
	if n.X-1 >= 0 {
		nn := NewNode(n.X-1, n.Y, n, cave)
		ns = append(ns, nn)
	}
	if n.X+1 < len(cave[0]) {
		nn := NewNode(n.X+1, n.Y, n, cave)
		ns = append(ns, nn)
	}
	if n.Y-1 >= 0 {
		nn := NewNode(n.X, n.Y-1, n, cave)
		ns = append(ns, nn)
	}
	if n.Y+1 < len(cave) {
		nn := NewNode(n.X, n.Y+1, n, cave)
		ns = append(ns, nn)
	}
	return ns
}

func getLessCost(ns map[string]Node) Node {
	lest_cost := math.MaxInt32
	var result Node
	for _, n := range ns {
		c := n.G + n.H
		if c < lest_cost {
			lest_cost = c
			result = n
		}
	}
	return result
}

func parseFile(filename string) (cave Cave) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		var row []int
		for _, c := range line {
			n, _ := strconv.Atoi(string(c))
			row = append(row, n)
		}
		cave = append(cave, row)
	}
	return cave
}

func TestFirstStar(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"example", 40},
		{"input", 0},
	}
	for _, c := range cases {
		got := firstStar(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
