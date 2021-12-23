package main

import (
	"fmt"
	"testing"
)

func TestFirstStar(t *testing.T) {
	cases := []struct {
		player1  int
		player2  int
		expected int
	}{
		{4, 8, 739785},
		{4, 9, 903630},
	}
	for _, c := range cases {
		got := firstStar(c.player1, c.player2)
		if c.expected != got {
			t.Errorf("\nFor %d, %d, Expected %d, got %d\n", c.player1, c.player2, c.expected, got)
		}
	}
}

func TestSecondStar(t *testing.T) {
	cases := []struct {
		position1 int
		position2 int
		limit     int
		win1      int
		win2      int
	}{
		{4, 8, 21, 0, 0},
		// {1, 1, 3, 5, 2},
		// {1, 1, 0, 0, 1}, // This is a corner case
		// {1, 1, 1, 3, 0},
		// {1, 1, 2, 3, 0},
		// {9, 9, 2, 5, 2},
	}
	for _, c := range cases {
		fmt.Printf("New test %v\n", c)
		win1, win2 := seconStart(c.position1, c.position2, c.limit)
		if c.win1 != win1 || c.win2 != win2 {
			t.Errorf("Expected %d, %d, got %d, %d\n", c.win1, c.win2, win1, win2)
		}
	}
}

type Node struct {
	Position1, Position2, Score1, Score2, Turn int
}

func fromNode(n Node) Node {
	return Node{
		Position1: n.Position1,
		Position2: n.Position2,
		Score1:    n.Score1,
		Score2:    n.Score2,
		Turn:      n.Turn ^ 1,
	}
}

func seconStart(position1, position2, limit int) (int, int) {
	var win1, win2 int
	open := make(map[Node]int)
	close := make(map[Node]int)
	current := Node{Position1: position1, Position2: position2, Score1: 0, Score2: 0, Turn: 0}
	open[current] = 1
	for len(open) > 0 {
		var count int
		current, count = getOne(open)
		if count > 1 {

			fmt.Printf("Nodes Open %d, current %v, with count %d\n", len(open), current, count)
		}
		close[current] = count
		isWinner := current.Score1 >= limit || current.Score2 >= limit
		if isWinner {
			if current.Turn == 0 {
				win2 += count
			} else {
				win1 += count
			}
		} else {
			ns := generateNext(current)
			for _, n := range ns {
				if c, ok := open[n]; ok {
					open[n] = c + count
				}
				if c, ok := close[n]; ok {
					close[n] = c + count
				} else {
					open[n] = count
				}
			}

		}
	}
	fmt.Println("Nodes analize ", len(close))
	return win1, win2
}

func generateNext(current Node) []Node {
	var ns []Node
	for i := 1; i < 4; i++ {
		n := fromNode(current)
		if current.Turn == 0 {
			p := calcuatePosition(n.Position1, i)
			n.Score1 += p
			n.Position1 = p
			ns = append(ns, n)
		} else {
			p := calcuatePosition(n.Position2, i)
			n.Position2 = p
			n.Score2 += p
			ns = append(ns, n)
		}
	}
	return ns
}

func getOne(open map[Node]int) (Node, int) {
	for k, v := range open {
		delete(open, k)
		return k, v
	}
	panic("getOne called on empty map: Chec len(map) before call")
}

func firstStar(playe1, player2 int) int {
	var puntuation [2]int
	position := [2]int{playe1, player2}
	player := 0 //0 or 1
	lastDicePuntuation := 0
	totalRolls := 0
	for puntuation[player] < 1000 {
		a := rollDice(lastDicePuntuation)
		b := rollDice(a)
		lastDicePuntuation = rollDice(b)
		totalRolls += 3
		total := a + b + lastDicePuntuation
		newPosition := calcuatePosition(position[player], total)
		position[player] = newPosition
		if puntuation[player]+newPosition >= 1000 {
			return puntuation[player^1] * totalRolls
		}
		puntuation[player] += newPosition
		player = player ^ 1 //0->1 1->0
	}
	panic("No arrive to solution")
}

func rollDice(p int) int {
	return (p % 100) + 1
}

func calcuatePosition(position, total int) int {
	np := position + total
	return (np-1)%10 + 1
}
