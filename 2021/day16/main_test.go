package main

import (
	"fmt"
	"strconv"
	"testing"
)

type Package struct {
	Version     int
	Type        int
	SubPackages []Package
	literal     int
}

func parse(s string) Package {
	var binString string
	for _, c := range s {
		d, _ := strconv.ParseInt(string(c), 16, 0)
		binString = fmt.Sprintf("%s%.4b", binString, d)
	}
	binString, v := readInt(binString, 3)
	binString, t := readInt(binString, 3)
	binString, l := readLiteral(binString)
	fmt.Println(binString, v, t, l, len(binString))
	return Package{Version: v, Type: t, literal: l}
}

func readLiteral(binString string) (string, int) {
	last := false
	i := 0
	literal := ""
	for !last {
		var c string
		binString, c = readString(binString, 1)
		i = i + 1
		if c == "0" {
			last = true
		}

		binString, c = readString(binString, 4)
		i = i + 4
		literal = literal + c
	}
	//read the ceros
	binString, _ = readString(binString, i%4)
	d, _ := strconv.ParseInt(string(literal), 2, 0)
	return binString, int(d)
}

func readString(binString string, bits int) (string, string) {
	return binString[bits:], binString[0:bits]
}

func readInt(binString string, bits int) (string, int) {
	c := binString[0:bits]
	d, _ := strconv.ParseInt(string(c), 2, 0)
	return binString[bits:], int(d)

}

func calculateFistStar(pack Package) int {
	panic("unimplemented")
}

// func parseFile(filename string) (cave Cave) {
// 	file, err := os.Open(filename)
// 	if err != nil {
// 		fmt.Println(err)
// 	}
// 	defer file.Close()
// 	scanner := bufio.NewScanner(file)
// 	for scanner.Scan() {
// 		line := scanner.Text()
// 		var row []int
// 		for _, c := range line {
// 			n, _ := strconv.Atoi(string(c))
// 			row = append(row, n)
// 		}
// 		cave = append(cave, row)
// 	}
// 	return cave
// }

func TestParse(t *testing.T) {
	cases := []struct {
		code   string
		result int
	}{{"D2FE28", 4},
		{"8A004A801A8002F478", 16},
		{"620080001611562C8802118E34", 12},
		{"C0015000016115A2E0802F182340", 23},
		{"A0016C880162017C3686B18A3D4780", 31},
	}
	for _, c := range cases {
		pack := parse(c.code)
		got := calculateFistStar(pack)
		expected := c.result
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}
}
