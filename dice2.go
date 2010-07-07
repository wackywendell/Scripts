package main

import "fmt"

type fRollStruc struct {
	ndie   uint
	nsides uint
	rolls  []uint64
}

func (fr *fRollStruc) Sides() uint { return fr.nsides }

func (fr *fRollStruc) Die() uint { return fr.ndie }

func (fr *fRollStruc) Getroll(n uint) uint64 { return fr.rolls[n-fr.ndie] }

func (fr *fRollStruc) Limits() (uint, uint) {
	first := fr.ndie
	last := fr.ndie * fr.nsides
	return first, last
}

func (fr *fRollStruc) String() string {
	mystring := fmt.Sprintf("%d Die, %d Sides: [", fr.ndie, fr.nsides)
	low, high := fr.Limits()
	for i := low; i < high; i++ {
		mystring += fmt.Sprintf("%d,", fr.Getroll(i))
	}
	mystring += fmt.Sprintf("%d]", fr.Getroll(high))
	return mystring
}

func NewRolls(ndie uint, nsides uint) *fRollStruc {
	arraysize := ndie*nsides - ndie + 1
	struc := &fRollStruc{ndie, nsides, make([]uint64, arraysize)}
	return struc
}

func GetRolls(ndie uint, nsides uint) *fRollStruc {
	struc := NewRolls(ndie, nsides)
	if ndie <= 1 {
		for i := 0; i < len(struc.rolls); i++ {
			//			fmt.Print(i)
			struc.rolls[i] = 1
		}
		return struc
	}

	smallstruc := GetRolls(ndie-1, nsides)
	lowbound, highbound := smallstruc.Limits()
	value := uint(0)
	for i := lowbound; i <= highbound; i++ {
		for j := uint(1); j <= nsides; j++ {
			value = i + j
			struc.rolls[value-ndie] += smallstruc.Getroll(i)
			fmt.Printf("%d,%d: Setting rolls[%d], now %d\n", i, j, value-ndie, struc.rolls[value-ndie])
		}
	}
	return struc
}

func getval(n uint) (uint, bool) {
	if n < 10 {
		return 3, true
	}
	return 4, false
}

//func getval(n uint) (uint){
//	n, _ := getval(n)
//	return n
//}


func main() {
	//	f := fRollStruc{1, 6, []uint64{1, 1, 1, 1, 1, 1}}
	//	f := NewRolls(1, 6)
	//	fmt.Printf("%#v\n", f)
	//	fmt.Println(f.Getroll(6))
	fmt.Println(GetRolls(4, 6))
	//	newn, _ := getval(3)
	//	val, _ := fmt.Println(newn)
	//	fmt.Println(val)
}

