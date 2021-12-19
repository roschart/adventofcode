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

func explode(current, root *Number, deep, Max_deep int) bool {
	if deep == Max_deep && current.Id == Pair {
		fmt.Printf("Explosion at.Current %s, deep %d\n", current.String(), deep)

		sumToExtrems(current, root)
		current = &Number{Id: Value, Value: 0}
		return true
	}
	if current.Id == Pair {
		el := explode(current.Left, root, deep+1, Max_deep)
		if !el {
			return explode(current.Right, root, deep+1, Max_deep)
		}

	}
	return false
}

func sumToExtrems(current, root *Number) {
	fmt.Println("SumExtrems", current, root)
	vs := flat(root)
	a := current.Left
	b := current.Right
	i := 0
	for ; i < len(vs); i++ {
		if vs[i] == b {
			if i-2 >= 0 {
				n := vs[i-2]
				n.Value += a.Value
			}
			if i+1 < len(vs) {
				vs[i+1].Value += b.Value
			}
		}
	}
	*current = Number{Id: Value, Value: 0}
}

func flat(n *Number) (result []*Number) {
	switch n.Id {
	case Pair:
		result = append(result, flat(n.Left)...)
		result = append(result, flat(n.Right)...)
	case Value:
		return []*Number{n}
	}
	return result
}

func AddToRight(n *Number, i int) {
	fmt.Println("Add to Righ")
	if n == nil {
		return
	}
	switch n.Id {
	case Pair:
		AddToRight(n.Right, i)
	case Value:
		n.Value += i

	}
}

func AddToLeft(n *Number, i int) {
	if n == nil {
		return
	}
	switch n.Id {
	case Pair:
		AddToLeft(n.Left, i)
	case Value:
		n.Value += i

	}
}

func TestParse(t *testing.T) {
	cases := []struct {
		line      string
		magnitude int
	}{
		{"[9,1]", 29},
		{"[[9,1],1]", 89},
		{"[9,[1,1]]", 37},
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

func TestExplode(t *testing.T) {
	cases := []struct {
		line     string
		deep     int
		expected string
	}{
		{"[1,[9,2]]", 2, "[10,0]"},
		{"[[[[[9,8],1],2],3],4]", 5, "[[[[0,9],2],3],4]"},
		{"[7,[6,[5,[4,[3,2]]]]]", 5, "[7,[6,[5,[7,0]]]]"},
		{"[[6,[5,[4,[3,2]]]],1]", 5, "[[6,[5,[7,0]]],3]"},
		{"[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", 5, "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"},
		{"[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", 5, "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"},
	}

	for _, c := range cases {
		_, n := ParseNum(c.line)
		explode(n, n, 1, c.deep)

		if c.expected != n.String() {
			t.Errorf("Expected %s, got %s", c.expected, n.String())
		}
	}
}
