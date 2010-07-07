package main

import (
	"fmt"
	"maps"
	"container/list"
)

type RollVal uint64
type SpecInt uint32

type RollSpec struct {
	ndie   SpecInt
	nsides SpecInt
}

func (rs RollSpec) Hash() maps.Value {
	var retval uint64 = uint64(rs.ndie)<<32 + uint64(rs.nsides)
	return retval
}

type RollArray struct {
	spec  RollSpec
	rolls []RollVal
}

func newRollArray(spec RollSpec) *RollArray {
	retval := new(RollArray)
	retval.spec = spec
	ndie := spec.ndie
	nsides := spec.nsides
	retval.rolls = make([]RollVal, ndie*nsides-ndie+1)
	if ndie == 1 {
		for i, _ := range retval.rolls {
			retval.rolls[i] = 1
		}
	}
	return retval
}

func (fr *RollArray) mult(other *RollArray) *RollArray {
	nsides := fr.spec.nsides
	ndie := fr.spec.ndie + other.spec.ndie
	newarr := newRollArray(RollSpec{ndie, nsides})

	for l1, v1 := range fr.rolls {
		for l2, v2 := range other.rolls {
			//			fmt.Println(l1, v1, l2, v2)
			newarr.rolls[l1+l2] += v1 * v2
		}
	}

	return newarr
}

// takes two RollArrays, checks if they've been created before, and then either
// uses the old one or multiplies them together and adds them to
func worker(in1 chan *RollArray, in2 chan *RollArray, goal SpecInt, procchan chan chan *RollArray) {
	//	fmt.Println("Worker started")
	arr1 := <-in1
	in1 <- arr1
	arr2 := <-in2
	in2 <- arr2

	n := arr1.spec.ndie + arr2.spec.ndie
	rs := RollSpec{n, arr1.spec.nsides}
	val, existed := bigMap.Get(rs)
	var storechan chan *RollArray = val.(chan *RollArray)
	var newarr *RollArray
	if !existed {
		//		fmt.Println("Multiplying")
		newarr = arr1.mult(arr2)
		//		fmt.Println("Multiplying Finished:", newarr)
	} else {
		//		fmt.Println("Waiting")
		newarr = <-storechan
		//		fmt.Println("Received:", newarr)
	}
	storechan <- newarr
	procchan <- storechan
	if newarr.spec.ndie == goal {
		close(procchan)
	}
}

func mydeffunc(indx maps.Value) maps.Value {
	var indxspec RollSpec = indx.(RollSpec)
	valchan := make(chan *RollArray, 1)
	if indxspec.ndie == 1 {
		basecase := newRollArray(indxspec)
		valchan <- basecase
	}
	var v maps.Value = valchan
	return v
}

var bigHashMap maps.Map = maps.NewHash()
var bigDefMap maps.Map = maps.ToDefault(&bigHashMap, mydeffunc)
var bigMap maps.Map = maps.ToSafe(&bigDefMap)

func processor(goal SpecInt, procchan chan chan *RollArray) (final *RollArray) {
	var last chan *RollArray = nil
	for i := range procchan {
		if last == nil {
			last = i
		} else {
			//			fmt.Println("Starting worker\n")
			go worker(last, i, goal, procchan)
			last = nil
		}
	}
	final = <-last
	return final
}

func getn(l *list.List, n SpecInt) (nextn SpecInt) {
	var curhigh SpecInt = 1
	for e := l.Front(); e != nil; e = e.Next() {
		//		fmt.Println("Got value", e)
		uval := e.Value.(SpecInt)
		//		fmt.Println("Converted type", e.Value)
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

func starter(s RollSpec, procchan chan chan *RollArray) {
	l := list.New()
	ndie := s.ndie
	nsides := s.nsides
	//	fmt.Printf("getting keys!\n")
	ks := bigMap.Keys()
	//	fmt.Printf("got key chan!\n")
	for k := range ks {
		kasspec := k.(RollSpec)
		//		fmt.Println("getting key!", k)
		if kasspec.nsides == s.nsides {
			l.PushBack(kasspec.ndie)
		}
	}
	//	fmt.Println("list made!:", l)

	curn := ndie
	for curval := getn(l, curn); curn > 0; curval = getn(l, curn) {
		curn -= curval
		//		fmt.Printf("pushing %d, now at %d\n", curval, curn)
		c, _ := bigMap.Get(RollSpec{curval, nsides})
		//		fmt.Println("Got", c, ok)
		procchan <- c.(chan *RollArray)
	}
}

func GetRolls(ndie SpecInt, nsides SpecInt) *RollArray {
	procchan := make(chan chan *RollArray, 30)
	go starter(RollSpec{ndie, nsides}, procchan)
	//	fmt.Println("starter returned \n")
	retval := processor(ndie, procchan)
	return retval
}

func maptester() {
	f := func(v maps.Value) maps.Value { return RollSpec{0, 0} }
	hm := maps.NewHash()
	dm := maps.ToDefault(&hm, f)
	m := maps.ToSafe(&dm)
	//	m := maps.NewSafe()
	m.Put(RollSpec{1, 2}, RollSpec{1, 3})
	m.Put(RollSpec{2, 2}, RollSpec{2, 3})
	m.Put(RollSpec{1, 1}, RollSpec{1, 2})
	val, ok := m.Get(RollSpec{1, 2})
	fmt.Println("Getting 1,2", val, ok)
	val, ok = m.Get(RollSpec{2, 2})
	fmt.Println("Getting 2,2", val, ok)
	val, ok = m.Get(RollSpec{3, 3})
	fmt.Println("Getting 3,3", val, ok)
	val, ok = m.Get(RollSpec{3, 3})
	fmt.Println("Getting 3,3", val, ok)
	m.Put(RollSpec{34, 2}, RollSpec{34, 2})
	for k := range m.Keys() {
		val, ok = m.Get(k)
		fmt.Println("Got key", k, val, ok)
	}
	fmt.Println("Got keys")
}

func main() {
	//	maptester()
	fr := GetRolls(3000, 6)
	fmt.Println(fr.rolls[1500])
	for k := range bigMap.Keys() {
		fmt.Println(k)
	}
}

