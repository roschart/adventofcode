package main

import (
	"bufio"
	"fmt"
	"os"
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

func firstStart(filename string) int {
	lines := parseFile(filename)
	_, acc := ParseNum(lines[0])

	for i := 1; i < len(lines); i++ {
		_, n := ParseNum(lines[i])
		acc = reduce(acc, n)
	}
	return acc.magnitude()
}

func parseFile(filename string) (lines []string) {
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		lines = append(lines, line)
	}
	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}
	return lines
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

func explode(current, root *Number, deep int) []*Number {
	const Max_deep = 5
	if deep >= Max_deep && current.Id == Pair {
		if current.Left.Id == Value || current.Right.Id == Value {
			fmt.Println("Exploding", current)
			affected := sumToExtrems(current, root)
			current = &Number{Id: Value, Value: 0}
			fmt.Println("After Explode:", root)
			for _, a := range affected {
				if a.Value > 9 {
					split(a, root)
				}
			}
			return affected
		}

	}
	if current.Id == Pair {
		affected := explode(current.Left, root, deep+1)
		if len(affected) > 0 {
			return affected
		}
		if len(affected) == 0 {
			return explode(current.Right, root, deep+1)
		}

	}
	return make([]*Number, 0)
}

func sumToExtrems(current, root *Number) (affected []*Number) {
	vs := flat(root)
	a := current.Left
	b := current.Right
	i := 0
	for ; i < len(vs); i++ {
		if vs[i] == b {
			if i-2 >= 0 {
				n := vs[i-2]
				n.Value += a.Value
				affected = append(affected, n)
			}
			if i+1 < len(vs) {
				n := vs[i+1]
				n.Value += b.Value
				affected = append(affected, n)
			}
		}
	}
	*current = Number{Id: Value, Value: 0}
	return affected
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

func split(n, root *Number) {
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

func reduce(a, b *Number) *Number {
	r := adition(a, b)
	fmt.Println("After adition: ", r)
	reduceNum(r)
	return r
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
		expected string
	}{
		// {"[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"},
		// {"[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"},
		// {"[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"},
		// {"[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]"},
		// {"[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"},
		{"[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", "[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]"},
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
		split(n, n)

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

func TestReduce(t *testing.T) {
	cases := []struct {
		a, b     string
		expected string
	}{
		// {"[[[[4,3],4],4],[7,[[8,4],9]]]", "[1,1]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"},
		{"[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]", "[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]", "[[[[4,0],[5,4]],[[7,7],[6,0]]],[[8,[7,7]],[[7,9],[5,0]]]]"},
	}
	for _, c := range cases {
		_, na := ParseNum(c.a)
		_, nb := ParseNum(c.b)
		got := reduce(na, nb)

		if c.expected != got.String() {
			t.Errorf("Expected %s, got %s", c.expected, got.String())
		}
	}
}

func TestReduceMultiline(t *testing.T) {
	cases := []struct {
		lines    []string
		expected string
	}{
		{lines: []string{
			"[1,1]",
			"[2,2]",
			"[3,3]",
			"[4,4]",
		},
			expected: "[[[[1,1],[2,2]],[3,3]],[4,4]]",
		}, {lines: []string{
			"[1,1]",
			"[2,2]",
			"[3,3]",
			"[4,4]",
			"[5,5]",
		},
			expected: "[[[[3,0],[5,3]],[4,4]],[5,5]]",
		},
		{lines: []string{
			"[1,1]",
			"[2,2]",
			"[3,3]",
			"[4,4]",
			"[5,5]",
			"[6,6]",
		},
			expected: "[[[[5,0],[7,4]],[5,5]],[6,6]]",
		},
		{lines: []string{
			"[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]",
			"[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]",
			"[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]",
			"[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]",
			"[7,[5,[[3,8],[1,4]]]]",
			"[[2,[2,2]],[8,[8,1]]]",
			"[2,9]",
			"[1,[[[9,3],9],[[9,0],[0,7]]]]",
			"[[[5,[7,4]],7],1]",
			"[[[[4,2],2],6],[8,7]]",
		},
			expected: "[[[[8,7],[7,7]],[[8,6],[7,7]]],[[[0,7],[6,6]],[8,7]]]",
		},
	}
	for _, c := range cases {
		_, acc := ParseNum(c.lines[0])

		for i := 1; i < len(c.lines); i++ {
			_, n := ParseNum(c.lines[i])
			acc = reduce(acc, n)
		}
		if c.expected != acc.String() {
			t.Errorf("Expected %s, got %s", c.expected, acc.String())
		}
	}
}

func TestFirstStar(t *testing.T) {
	cases := []struct {
		filename string
		result   int
	}{
		{"example", 4140},
	}
	for _, c := range cases {
		got := firstStart(c.filename)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}

func TestReduce2(t *testing.T) {
	cases := []struct {
		n        string
		expected string
	}{
		{"[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]"},
		{"[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]"},
		{"[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]"},
		{"[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"},
		{"[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]", "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]"},
	}
	for _, c := range cases {
		_, got := ParseNum(c.n)
		reduceNum(got)

		if c.expected != got.String() {
			t.Errorf("Expected %s, got %s", c.expected, got.String())
		}
	}
}

func reduceNum(root *Number) {
	executed := executeAction(root, root, 1)
	for executed {
		executed = executeAction(root, root, 1)
	}
}

func executeAction(current, root *Number, deep int) bool {
	switch current.Id {
	case Pair:
		if current.Left.Id == Value && current.Right.Id == Value && deep >= 5 {
			sumToExtrems(current, root)
			current = &Number{Id: Value, Value: 0}
			fmt.Println("After Explode: ", root)
			return true
		} else {
			el := executeAction(current.Left, root, deep+1)
			if el {
				return true
			}
			er := executeAction(current.Right, root, deep+1)

			return er
		}
	case Value:
		if current.Value > 9 {
			split(current, root)
			fmt.Println("After Split:   ", root)
			return true
		}
	}
	return false
}
