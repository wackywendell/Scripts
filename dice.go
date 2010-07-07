package main

import (
	"fmt"
	//	"container/list"
	"container/vector"
)

type roll struct {
	roll  uint
	value uint64
}

type fullroll struct {
	ndie   uint
	nsides uint
	rolls  []roll
}

var dicemap = map[uint]*vector.Vector{}

// maps number of sides to a list
// each list has 1 die, two die, three die, etc.

func initmap(nsides uint) {
	_, present := dicemap[nsides]
	if !present {
		l := new(vector.Vector)
		newrolls := make([]roll, uint(nsides))
		for i := uint(0); i < nsides; i++ {
			newrolls[i] = roll{i + 1, 1}
		}
		froll := fullroll{1, nsides, newrolls}
		l.Set(0, froll)
		dicemap[nsides] = l
	}
}

func GetRolls(nsides uint, ndie uint) fullroll {
	initmap(nsides)
	dielist := dicemap[nsides]
	minsize := dielist.Len()
	for i := uint(minsize + 1); i <= ndie; i++ {

	}

	return fullroll(dielist.At(0))
}

func main() {
	initmap(6)
	l, ok := dicemap[6]
	fmt.Println(ok)
	fr := l.At(0)
	fmt.Printf("%#v\n", fr)

	GetRolls(6, 1)
}

