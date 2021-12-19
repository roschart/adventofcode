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

func explode(current, root *Number, deep int) bool {
	const Max_deep = 5
	if deep == Max_deep && current.Id == Pair {

		sumToExtrems(current, root)
		current = &Number{Id: Value, Value: 0}
		return true
	}
	if current.Id == Pair {
		el := explode(current.Left, root, deep+1)
		if !el {
			return explode(current.Right, root, deep+1)
		}

	}
	return false
}

func sumToExtrems(current, root *Number) {
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

func split(n *Number) {
	switch n.Id {
	case Pair:
		panic("Pairs not must be splited")
	case Value:
		a := n.Value
		var l, r int
		l = a / 2
		r = a / 2
		if a%2 == 1 {
			r = r + 1

		}
		*n = Number{
			Id:    Pair,
			Left:  &Number{Id: Value, Value: l},
			Right: &Number{Id: Value, Value: r},
		}
	}

}

func adition(a, b *Number) *Number {
	return &Number{Id: Pair, Left: a, Right: b}
}

// func reduce(a, b *Number) *Number {
// 	r := adition(a, b)
// 	explode(r, r, 1)
// 	return r
// }

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
		expected string
	}{
		{"[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"},
		{"[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"},
		{"[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"},
		{"[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"},
		{"[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"},
	}

	for _, c := range cases {
		_, n := ParseNum(c.line)
		explode(n, n, 1)

		if c.expected != n.String() {
			t.Errorf("Expected %s, got %s", c.expected, n.String())
		}
	}
}

func TestSplit(t *testing.T) {
	cases := []struct {
		n        Number
		expected string
	}{
		{Number{Id: Value, Value: 12}, "[6,6]"},
		{Number{Id: Value, Value: 13}, "[6,7]"},
	}
	for _, c := range cases {
		n := &c.n
		split(n)

		if c.expected != n.String() {
			t.Errorf("Expected %s, got %s", c.expected, n.String())
		}
	}
}

func TestAdition(t *testing.T) {
	cases := []struct {
		a, b     string
		expected string
	}{
		{"[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]"},
	}
	for _, c := range cases {
		_, na := ParseNum(c.a)
		_, nb := ParseNum(c.b)
		got := adition(na, nb)

		if c.expected != got.String() {
			t.Errorf("Expected %s, got %s", c.expected, got.String())
		}
	}
}
