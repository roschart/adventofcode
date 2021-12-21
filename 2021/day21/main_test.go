package main

import (
	"testing"
)

func TestFirstStar(t *testing.T) {
	cases := []struct {
		player1  int
		player2  int
		expected int
	}{
		{4, 8, 739785},
		{4, 9, 0},
	}
	for _, c := range cases {
		got := firstStar(c.player1, c.player2)
		if c.expected != got {
			t.Errorf("\nFor %d, %d, Expected %d, got %d\n", c.player1, c.player2, c.expected, got)
		}
	}
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
