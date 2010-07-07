package main

import (
	"fmt"
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

func (sm safemap) Put(ndie uint, nsides uint, rolls *RollArray) {
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

func strucToChan(struc *RollArray, outchan chan RollVal) {
	if outchan == nil {
		return
	}
	low, high := struc.Limits()
	for i := low; i <= high; i++ {
		outchan <- struc.Getroll(i)
	}
}

func calcNext(ndie uint, nsides uint, outchan chan RollVal) {
	logPln(2, "Calcnext, ndie", ndie)
	mystruc, ok := theBigMap.Get(ndie, nsides)
	if ok {
		strucToChan(mystruc, outchan)
		return
	}
	logPln(1, "Calcnext, struc not found")
	// At this point, the structure has never been created, so we need to create it.
	// First, we create the one before it:
	myinchan := make(chan RollVal)
	go calcNext(ndie-1, nsides, myinchan)
	//Create the structure we will need in the end:
	mystruc = newRollArray(ndie, nsides)
	// now we take rolls from the one below, process them
	totalincoming := ArraySize(ndie-1, nsides)
	for i := uint(0); i < totalincoming; i++ {
		value := <-myinchan
		for j := uint(0); j < nsides; j++ {
			mystruc.rolls[i+j] += value
			if outchan != nil && (j == 1 || i == totalincoming-1) {
				outchan <- mystruc.rolls[i+j]
			}
		}
	}

	// And store it for next time:
	theBigMap.Put(ndie, nsides, mystruc)
}

func GetRolls(ndie uint, nsides uint) *RollArray {
	calcNext(ndie, nsides, nil)
	retval, _ := theBigMap.Get(ndie, nsides)
	return retval
}

var theBigMap safemap = NewSafeMap()

func main() {

	retval := GetRolls(2000, 6)

	fmt.Println(retval)
	t := range retval.rolls
	fmt.Println(t)
}

/*
mapofmaps

main(){
	makeRolls(nsides, ndie)
}

channelthread:
	input:
		rolls
	output:
		rolls

global mapchan - Main must put an empty map there

structochan(rollstruc, outchan){
	put rolls into outchan
}

getstrucfrommap(nsides, ndie){
	acquire map from mapchan
	check if struc in map
	if it is, return it
	if not and ndie == 1{
		make struc
		put it in map
		return it
	}
	else return nothing
}

normalthread(nsides, ndie, outchan){
	mystruc = getstrucfrommap(nsides, ndie)
	if not exist and ndie == 1{
		make struc
		put struc in map
	}
	if struc exists{
		structochan(rollstruc, outchan)
		return
	}
	make inchan (buffered)
	go normalthread(nsides, ndie -1, inchan)
	take rolls from input
	process rolls into struc, (outchan if it exists)
	use mapchan to put struc in map
	return nothing
}

getrolls(nsides, ndie){
	run normalthread (NOT go)
	use mapchan to get struc
	return struc
}
*/
