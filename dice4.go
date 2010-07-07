package main

import (
	"fmt"
	"maps"
)

var logval int = 3

func logPln(imp int, v ...) {
	if imp >= logval {
		fmt.Println(v)
	}
}

func logPr(imp int, v ...) {
	if imp >= logval {
		fmt.Print(v)
	}
}

func logPrf(imp int, format string, v ...) {
	if imp >= logval {
		fmt.Printf(format, v)
	}
}

type RollVal uint64

type RollArray struct {
	ndie   uint
	nsides uint
	rolls  []RollVal
}

type Empty interface{}
type singleArgFunc func(Empty)

//func (myfunc singleArgFunc) gofunc(arg Empty, chan){
//
//
//}

func (fr *RollArray) Sides() uint { return fr.nsides }

func (fr *RollArray) Die() uint { return fr.ndie }

func (fr *RollArray) Getroll(n uint) RollVal { return fr.rolls[n-fr.ndie] }

func ArraySize(ndie uint, nsides uint) uint { return ndie*nsides - ndie + 1 }

func (fr *RollArray) Limits() (uint, uint) {
	first := fr.ndie
	last := fr.ndie * fr.nsides
	return first, last
}

func newRollArray(ndie uint, nsides uint) *RollArray {
	retval := new(RollArray)
	retval.ndie = ndie
	retval.nsides = nsides
	retval.rolls = make([]RollVal, ndie*nsides-ndie+1)
	if ndie == 1 {
		for i, _ := range retval.rolls {
			retval.rolls[i] = 1
		}
	}
	return retval
}

func (fr *RollArray) mult(other *RollArray) *RollArray {
	nsides := fr.nsides
	ndie := fr.ndie + other.ndie
	newarr := newRollArray(ndie, nsides)

	for l1, v1 := range fr.rolls {
		for l2, v2 := range other.rolls {
			fmt.Println(l1, v1, l2, v2)
//			newval := v1 * v2
			newarr.rolls[l1+l2] += v1 * v2
		}
	}

	return newarr
}


type maprolls map[uint]*RollArray
type mapmap map[uint]*maprolls
type safemap chan *mapmap

func NewSafeMap() safemap {
	thesafemap := make(safemap, 1)
	themap := make(mapmap)
	thesafemap <- &themap
	return thesafemap
}

func (sm safemap) Get(ndie uint, nsides uint) (rolls *RollArray, success bool) {
	mymap := <-sm
	//	var ok bool
	//	var retval *RollArray
	innermap, ok := (*mymap)[nsides]
	if !ok {
		//		fmt.Println("Making map")
		newmap := make(maprolls)
		innermap = &newmap
		(*mymap)[nsides] = innermap
		retval := newRollArray(1, nsides)
		(*innermap)[1] = retval
		logPln(0, (*innermap)[1])
	}

	logPln(1, "Fetching rollarray")
	retval, ok := (*innermap)[ndie]
	logPln(0, retval, ok)
	logPln(1, "returning rollarray")
	sm <- mymap
	return retval, ok
}

func (sm safemap) Put(rolls *RollArray) {
	ndie := rolls.ndie
	nsides := rolls.ndie
	mymap := <-sm
	innermap, ok := (*mymap)[nsides]
	if !ok {
		newmap := make(maprolls)
		innermap = &newmap
		(*mymap)[nsides] = innermap
	}
	(*innermap)[ndie] = rolls
	sm <- mymap
}

func getn(l *list.List, n uint) (nextn uint){
	var curhigh uint = 1
	for e := l.Front(); e != nil; e = e.Next() {
		uval := e.Value.(uint)
		if uval > n {
			l.Remove(e)
			continue
		}
		if uval > curhigh {
			curhigh = uval
		}
	}
	return curhigh
}

type arrchmap map[uint](RollArray)
type safearrchmap chan arrchmap
func (safemp *safearrchmap) Get(n uint) (retval chan *RollArray, made bool){
	mp := <- safemp
	val, ok := mp[n]
	if !ok{
		val = make(chan *RollArray, 1)
		mp[n] = val
	}
	safemp <- mp
	return val, !ok
}

func NewSafeArrMap() safemap {
	thesafemap := make(safearrchmap, 1)
	themap := make(arrchmap)
	thesafemap <- &themap
	return thesafemap
}

func worker(in1 chan *RollArray, in2 chan *RollArray, 
			mp safearrchmap, procchan chan *RollArray){
	arr1 := <- in1
	in1 <- arr1
	
	arr2 := <- in2
	in2 <- arr2
	
	n := arr1.ndie + arr2.ndie
	storechan, made := mp.Get(n)
	var newarr *RollArray
	if made{
		newarr = arr1.mult(arr2)
	} else {
		newarr = <-storechan
	}
	
	procchan <- newarr
}

func GetRolls(ndie uint, nsides uint){
	l := list.New()
	theBigMap.Get(1, nsides) // make sure the inner map is made,
	                         // and that it has a 1 in it
	
	outermap := <-theBigMap
	innermap, _ := (*outermap)[nsides]
	fmt.Printf("%#v\n", innermap)
	for k, _ := range (*innermap){
		l.PushBack(k)
	}
	theBigMap <- outermap

	// make all the subchans
	chanmap := newSafeArrMap()
	processchan := make(chan *RollArray, 50)
	
	curn := ndie
	for curval := getn(l, curn); curval != ndie; curval = getn(l, curn){
		curn -= curval
		fmt.Printf("pushing %d, now at %d\n",curval, curn)
		arr, ok = theBigMap.Get(curval, nsides)
		if !ok{
			fmt.Printf("COULDN'T GET '%v'\n", curval)
		}
		curchan, _ := chanmap.Get(curval)
		curchan <- arr
		processchan <- curchan
	}
	
func processstarter(processchan chan *RollArray, mp safearrchmap) {
	var lastpulled *RollArray = nil
	for i := range processchan {
		val := <- i
		if val.ndie == ndie{
			return val
		}
		i <- val
		if lastpulled != nil{
			worker(lastpulled, i, mp, processchan)
		}
	}
	return nil
}

var theBigMap safemap = NewSafeMap()

func main() {
	GetRolls(2,6)
//	f1 := newRollArray(1, 6)
//	for v1 := range f1.rolls {
//		fmt.Printf("%v\n", v1)
//	}

//	f2 := f1.mult(f1)
//	fmt.Println(f2.mult(f2))
}

