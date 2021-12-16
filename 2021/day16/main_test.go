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
	var p Package
	_, p = readPackage(binString)

	return p
}

func readPackage(binString string) (string, Package) {
	var p Package
	var d int
	binString, d = readInt(binString, 3)
	p.Version = d
	binString, d = readInt(binString, 3)
	p.Type = d
	if d == 4 {
		binString, d = readLiteral(binString)
		p.literal = d
	} else {
		var os []Package
		binString, os = readoperator(binString)
		p.SubPackages = os
	}

	return binString, p
}

func readoperator(binString string) (string, []Package) {
	var s string
	var subs []Package
	binString, s = readString(binString, 1)
	if s == "0" {
		binString, subs = readSubPackagesByLength(binString)
	} else {
		binString, subs = readSubPackagesByNum(binString)
	}

	return binString, subs
}

func readSubPackagesByNum(binString string) (string, []Package) {
	var length int
	var subs []Package
	var p Package
	binString, length = readInt(binString, 11)
	for i := 0; i < length; i++ {
		binString, p = readPackage(binString)
		subs = append(subs, p)
	}
	return binString, subs
}

func readSubPackagesByLength(binString string) (string, []Package) {
	var length int
	var subs []Package
	var p Package
	binString, length = readInt(binString, 15)
	for length > 0 {
		l := len(binString)
		binString, p = readPackage(binString)
		subs = append(subs, p)
		l2 := len(binString)
		length = length + l2 - l
	}

	return binString, subs

}

func readLiteral(binString string) (string, int) {
	last := false
	i := 6
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
	//binString, _ = readString(binString, i%4)
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

func calculateFistStar(p Package) int {
	sum := p.Version

	for _, x := range p.SubPackages {
		sum += calculateFistStar(x)
	}
	return sum
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
	}{
		{"EE00D40C823060", 14},
		{"38006F45291200", 9},
		{"D2FE28", 6},
		{"8A004A801A8002F478", 16},
		{"620080001611562C8802118E34", 12},
		{"C0015000016115A2E0802F182340", 23},
		{"A0016C880162017C3686B18A3D4780", 31},
		{"E20D72805F354AE298E2FCC5339218F90FE5F3A388BA60095005C3352CF7FBF27CD4B3DFEFC95354723006C401C8FD1A23280021D1763CC791006E25C198A6C01254BAECDED7A5A99CCD30C01499CFB948F857002BB9FCD68B3296AF23DD6BE4C600A4D3ED006AA200C4128E10FC0010C8A90462442A5006A7EB2429F8C502675D13700BE37CF623EB3449CAE732249279EFDED801E898A47BE8D23FBAC0805527F99849C57A5270C064C3ECF577F4940016A269007D3299D34E004DF298EC71ACE8DA7B77371003A76531F20020E5C4CC01192B3FE80293B7CD23ED55AA76F9A47DAAB6900503367D240522313ACB26B8801B64CDB1FB683A6E50E0049BE4F6588804459984E98F28D80253798DFDAF4FE712D679816401594EAA580232B19F20D92E7F3740D1003880C1B002DA1400B6028BD400F0023A9C00F50035C00C5002CC0096015B0C00B30025400D000C398025E2006BD800FC9197767C4026D78022000874298850C4401884F0E21EC9D256592007A2C013967C967B8C32BCBD558C013E005F27F53EB1CE25447700967EBB2D95BFAE8135A229AE4FFBB7F6BC6009D006A2200FC3387D128001088E91121F4DED58C025952E92549C3792730013ACC0198D709E349002171060DC613006E14C7789E4006C4139B7194609DE63FEEB78004DF299AD086777ECF2F311200FB7802919FACB38BAFCFD659C5D6E5766C40244E8024200EC618E11780010B83B09E1BCFC488C017E0036A184D0A4BB5CDD0127351F56F12530046C01784B3FF9C6DFB964EE793F5A703360055A4F71F12C70000EC67E74ED65DE44AA7338FC275649D7D40041E4DDA794C80265D00525D2E5D3E6F3F26300426B89D40094CCB448C8F0C017C00CC0401E82D1023E0803719E2342D9FB4E5A01300665C6A5502457C8037A93C63F6B4C8B40129DF7AC353EF2401CC6003932919B1CEE3F1089AB763D4B986E1008A7354936413916B9B080", 0},
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

func TestReadPackage(t *testing.T) {
	cases := []struct {
		code   string
		result int
	}{
		{"11010001010", 10},
	}

	for _, c := range cases {
		s, pack := readPackage(c.code)
		got := pack.literal
		expected := c.result
		fmt.Println(s)
		if expected != got {
			t.Errorf("Expected %d,  got %d", expected, got)
		}
	}

}
