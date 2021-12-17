package main

import (
	"testing"
)

type Velocity struct {
	X, Y int
}

type Point struct {
	X, Y int
}

type Range struct {
	Min, Max int
}
type Limit struct {
	X Range
	Y Range
}

func TestFindHighest(t *testing.T) {
	cases := []struct {
		l      Limit
		result int
	}{
		{l: Limit{X: Range{Min: 20, Max: 30}, Y: Range{Min: -10, Max: -5}}, result: 45},
		{l: Limit{X: Range{Min: 248, Max: 285}, Y: Range{Min: -85, Max: -56}}, result: 3570},
	}
	for _, c := range cases {
		got := findHighest(c.l)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}

func findHighest(l Limit) (result int) {
	for x := 1; x < l.X.Max; x++ {
		for y := 0; y < 500; y++ {
			v := Velocity{X: x, Y: y}
			if ok, y_max := isImpact(v, l); ok {
				if y_max > result {
					result = y_max
				}
			}
		}
	}
	return result
}

func TestIsImpact(t *testing.T) {
	cases := []struct {
		v         Velocity
		l         Limit
		is_impact bool
		y_max     int
	}{
		{v: Velocity{6, -2}, l: Limit{X: Range{Min: 6, Max: 10}, Y: Range{Min: -2, Max: 0}}, is_impact: true, y_max: 0},
		{v: Velocity{6, 9}, l: Limit{X: Range{Min: 20, Max: 30}, Y: Range{Min: -10, Max: -5}}, is_impact: true, y_max: 45},
	}
	for _, c := range cases {
		i, m := isImpact(c.v, c.l)
		if i != c.is_impact || m != c.y_max {
			t.Errorf("Expected %v, %d,  got %v, %d", c.is_impact, c.y_max, i, m)

		}
	}
}

func isImpact(v Velocity, l Limit) (bool, int) {
	pased := false
	is_impact := false
	p := Point{}
	y_max := 0
	y_tentative := 0

	for !pased {
		p.X += v.X
		p.Y += v.Y
		if v.X > 0 {
			v.X--
		}
		v.Y = v.Y - 1
		if p.Y > y_tentative {
			y_tentative = p.Y
		}
		impact := p.X <= l.X.Max && p.X >= l.X.Min && p.Y <= l.Y.Max && p.Y >= l.Y.Min
		if impact {
			is_impact = true
			if y_tentative > y_max {
				y_max = y_tentative
			}
		}
		if p.X > l.X.Max || p.Y < l.Y.Min {
			pased = true
		}
	}
	return is_impact, y_max
}
