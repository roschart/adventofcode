package main

import (
	"fmt"
	"testing"
)

type typeNumber int

const (
	Pair typeNumber = iota
	Value
)

type Number struct {
	Id     typeNumber
	Value  int
	Left   *Number
	Right  *Number
	Parent *Number
}

func (n *Number) magnitude() int {
	switch n.Id {
	case Pair:
		return n.Left.magnitude()*3 + n.Right.magnitude()*2
	case Value:
		return n.Value
	}
	panic("No all cases analize for manitude")
}

func (n *Number) String() string {
	switch n.Id {
	case Pair:
		return fmt.Sprintf("[%s,%s]", n.Left, n.Right)
	case Value:
		return fmt.Sprintf("%d", n.Value)
	}
	panic("No all cases analize for string")
}

func ParseNum(s string) (string, *Number) {
	c := s[0]
	rest := s[1:]
	switch c {
	case '[':
		n := Number{}
		n.Id = Pair
		rest, n.Left = ParseNum(rest)
		rest = ParseCharacter(rest) // this is the `,`
		rest, n.Right = ParseNum(rest)
		rest = ParseCharacter(rest) // this is the `]`
		return rest, &n
	case '0', '1', '2', '3', '4', '5', '6', '7', '8', '9':
		n := Number{Id: Value}
		n.Value = int(c - '0')
		return rest, &n
	}
	panic("Not al cases in parserNuber")
}

func ParseCharacter(rest string) string {
	return rest[1:]
}

func TestParse(t *testing.T) {
	cases := []struct {
		line      string
		magnitude int
	}{
		{"[9,1]", 29},
		{"[[9,1],1)", 89},
		{"[9,[1,1])", 37},
	}
	for _, c := range cases {
		_, n := ParseNum(c.line)
		got := n.magnitude()
		expect := c.magnitude
		if expect != got {
			t.Errorf("Expected %v, got %v adn n=%v", expect, got, n)
		}
	}
}
