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
		player1 int
		player2 int
		limit   int
		score   Score
	}{
		{0, 0, 0, Score{0, 0}},
		{0, 0, 1, Score{3, 0}},
		// {0, 0, 2, Score{5, 2,}},
		// {0, 0, 3, Score{14, 7,},
		// {5, 5, 7, Score{5, 2},},
	}
	for _, c := range cases {
		score := seconStart(c.player1, c.player2, c.limit)
		if c.score.SA != score.SA || c.score.SB != score.SB {
			t.Errorf("Expected %d, %d, got %d, %d\n", c.score.SA, c.score.SB, score.SA, score.SB)
		}
	}
}

type Node struct {
	PA, PB int
}

type Score struct {
	SA, SB int
}

func seconStart(player1, player2, limit int) Score {
	open := make(map[Node]Score)
	close := make(map[Node]Score)
	turn := 0 //0 player1 1 player2
	current := Node{PA: player1, PB: player2}
	open[current] = Score{0, 0}
	for len(open) > 0 {
		fmt.Printf("Nodes Open %d\n", len(open))
		var score Score
		current, score = getOne(open)
		isWinner := current.PA >= limit
		if isWinner {
			close[current] = score
		} else {
			//Creating next nodes with interchengin player1 and plaer2
			ns := []Node{
				//winA: current.WinB, WinB: current.winA
				{PA: current.PB, PB: current.PA + 1},
				{PA: current.PB, PB: current.PA + 2},
				{PA: current.PB, PB: current.PA + 2},
			}
			for _, n := range ns {
				if n.PB >= limit { //isWinner
					score.SA += 1
				}
				if _, ok := open[n]; ok {
					panic("implement when in open")
				}
				if _, ok := close[n]; ok {
					panic("implement when in close")
				}
			}
			close[current] = score
		}
		turn = turn ^ 1
	}
	result := sum(close)
	if turn == 1 {
		return Score{result.SB, result.SA}
	}
	return Score{result.SB, result.SA}
}

func sum(close map[Node]Score) Score {
	result := Score{}
	for _, s := range close {
		result.SA += s.SA
		result.SB += s.SB
	}
	return result
}

func getOne(open map[Node]Score) (Node, Score) {
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
