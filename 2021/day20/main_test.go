package main

import (
	"bufio"
	"fmt"
	"os"
	"testing"
)

type IEA string //image enhancement algorithm.

type Point struct {
	X, Y int
}
type Range struct {
	//ranges [)
	Min, Max int
}
type Limit struct {
	X Range
	Y Range
}
type Image struct {
	Lights      map[Point]bool //Set of lighs
	Limits      Limit
	OutOfLimits int //1 tru, 0 false (int to use as mask)
}

func NewImage() (result Image) {
	result.Lights = make(map[Point]bool)
	return result
}

func (i Image) Count() (sum int) {
	return len(i.Lights)
}

func TestFisrtStar(t *testing.T) {
	cases := []struct {
		filename string
		loop     int
		expected int
	}{
		{"example", 2, 35},
		{"input", 2, 4964},
		{"example", 50, 3351},
		{"input", 50, 0},
	}
	for _, c := range cases {
		got := firstStar(c.filename, c.loop)
		if c.expected != got {
			t.Errorf("\nFor %s, Expected %d, got %d\n", c.filename, c.expected, got)
		}
	}
}

func firstStar(filename string, repeat int) int {
	iea, image := parseFile(filename)
	for i := 0; i < repeat; i++ {
		image = applyIEA(iea, image)
	}
	return image.Count()
}

// func printImage(image Image) {
// 	for y := image.Limits.Y.Min; y < image.Limits.Y.Max; y++ {
// 		for x := image.Limits.X.Min; x < image.Limits.X.Max; x++ {
// 			v := image.Lights[Point{X: x, Y: y}]
// 			if v {
// 				fmt.Printf("#")
// 			} else {
// 				fmt.Printf(".")
// 			}
// 		}
// 		fmt.Println()
// 	}
// 	fmt.Println()
// }

func applyIEA(iea IEA, image Image) Image {
	newImage := NewImage()
	for y := image.Limits.Y.Min - 1; y < image.Limits.Y.Max+1; y++ {
		for x := image.Limits.X.Min - 1; x < image.Limits.X.Max+1; x++ {
			p := Point{X: x, Y: y}
			if calculatePoint(iea, image, p) {
				newImage.Lights[p] = true
			}
		}
	}
	if image.OutOfLimits == 0 {
		if iea[0] == '#' {
			newImage.OutOfLimits = 1
		} else {
			newImage.OutOfLimits = 0
		}
	} else {
		if iea[len(iea)-1] == '#' {
			newImage.OutOfLimits = 1
		} else {
			newImage.OutOfLimits = 0
		}
	}
	newImage.Limits.X.Min = image.Limits.X.Min - 1
	newImage.Limits.X.Max = image.Limits.X.Max + 1
	newImage.Limits.Y.Min = image.Limits.Y.Min - 1
	newImage.Limits.Y.Max = image.Limits.Y.Max + 1

	return newImage
}

func calculatePoint(iea IEA, image Image, point Point) bool {
	position := 0
	for i := 0; i < 3; i++ {
		for x := point.X - 1; x <= point.X+1; x++ {
			y := point.Y + i - 1
			p := Point{X: x, Y: y}
			position = position << 1
			isOutOfLimit := p.X < image.Limits.X.Min || p.X >= image.Limits.X.Max || p.Y < image.Limits.Y.Min || p.Y >= image.Limits.Y.Max
			if isOutOfLimit {
				position = position | image.OutOfLimits
			} else {
				if _, ok := image.Lights[p]; ok {
					position = position | 1
				}
			}
		}
	}
	result := iea[position] == '#'
	return result
}

func parseFile(filename string) (IEA, Image) {
	image := NewImage()
	var iea IEA
	file, err := os.Open(filename)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	for i := 0; scanner.Scan(); i++ {
		line := scanner.Text()
		switch i {
		case 0:
			iea = IEA(line)
		case 1:
			image.Lights = make(map[Point]bool)
		default:
			image.Limits.Y.Max = i - 1
			image.Limits.X.Max = len(line)
			for j, c := range line {
				if c == '#' {
					p := Point{X: j, Y: i - 2}
					image.Lights[p] = true
				}
			}
		}
	}
	if err := scanner.Err(); err != nil {
		fmt.Println(err)
	}
	return iea, image
}

func TestParseFile(t *testing.T) {
	cases := []struct {
		filename    string
		imageLimits Limit
		lenIEA      int
		countBit    int
	}{
		{"example", Limit{X: Range{Min: 0, Max: 5}, Y: Range{Min: 0, Max: 5}}, 512, 10},
	}
	for _, c := range cases {
		iea, image := parseFile(c.filename)
		if len(iea) != c.lenIEA || image.Limits != c.imageLimits || image.Count() != c.countBit {
			t.Errorf("Reading %s: len %d, %+v, %d", c.filename, len(iea), image.Limits, image.Count())
		}
	}
}
