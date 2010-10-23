package main

import (
	"fmt"
	"container/list"
	"flag"
	"big"
)

//func newRollVal(x uint64) RollVal { return RollVal(big.NewInt(int64(x))) }

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
	rolls [](*big.Int)
}

func newRollArray(spec RollSpec) *RollArray {
	retval := new(RollArray)
	retval.spec = spec
	ndie := spec.ndie
	nsides := spec.nsides
	retval.rolls = make([](*big.Int), ndie*nsides-ndie+1)
	for i, _ := range retval.rolls {
		if ndie == 1 {
			retval.rolls[i] = big.NewInt(1)
		} else {
			retval.rolls[i] = big.NewInt(0)
		}
	}
	return retval
}

func (fr *RollArray) mult(other *RollArray) *RollArray {
	nsides := fr.spec.nsides
	ndie := fr.spec.ndie + other.spec.ndie
	newarr := newRollArray(RollSpec{ndie, nsides})
//	fmt.Println("mult", fr.rolls, other.rolls)

	tmp := big.NewInt(0)

	for l1, v1 := range fr.rolls {
		for l2, v2 := range other.rolls {
			//			fmt.Println(l1, v1, l2, v2)
			oldval := newarr.rolls[l1+l2]
			//			fmt.Printf("Start:%v, %v, %v  ", oldval, v1, v2)
			newarr.rolls[l1+l2] = oldval.Add(oldval, tmp.Mul(v1, v2))
			//			fmt.Println("End:", oldval)
		}
	}
//	fmt.Println("mult finished", fr.rolls, other.rolls)

	return newarr
}

func (fr *RollArray) cmp(other *RollArray) (wins *big.Int, ties *big.Int, losses *big.Int){
	wins, ties, losses = big.NewInt(0), big.NewInt(0), big.NewInt(0)
	curnumrolls := big.NewInt(0)
	for l1, v1 := range fr.rolls{
		roll1 := fr.spec.ndie + SpecInt(l1)
		for l2, v2 := range other.rolls{
			roll2 := other.spec.ndie + SpecInt(l2)
			curnumrolls.Mul(v1, v2)
			if roll1 > roll2{
//			fmt.Println(roll1,"beats",roll2)
				wins.Add(wins, curnumrolls)
			} else if roll1 < roll2 {
//			fmt.Println(roll1,"loses",roll2)
				losses.Add(losses, curnumrolls)
			} else {
//			fmt.Println(roll1,"equals",roll2)
				ties.Add(ties, curnumrolls)
			}
		}
	}
	return wins, ties, losses
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
var divint SpecInt = 2

// For getting a power of divint. Assumes that it is a power of divint.
func getpower(spec RollSpec) *RollArray {
//	fmt.Println("getpower", spec)
	mapval, existed := bigMap.Get(spec)
	mapchan := mapval.(chan *RollArray)
	if existed || spec.ndie == 1 {
//		fmt.Println("getpower", spec, "existed")
		arr := <-mapchan
		mapchan <- arr
		return arr
	}
//	fmt.Println("getpower", spec.ndie)
	lwrspec := RollSpec{spec.ndie / divint, spec.nsides}
	lwr := getpower(lwrspec)
	for i := SpecInt(0); i < divint-1; i++ {
		lwr = lwr.mult(getpower(lwrspec))
	}
	mapchan <- lwr
	return lwr
}

func gopower(spec RollSpec, goal RollSpec, out chan *RollArray) {
	outarr := getpower(spec)
	out <- outarr
	if outarr.spec.ndie == goal.ndie {
		close(out)
	}
}

func worker(arr1 *RollArray, arr2 *RollArray, goal SpecInt, procchan chan *RollArray) {
	//	n := arr1.spec.ndie + arr2.spec.ndie
	newarr := arr1.mult(arr2)
//	fmt.Println("worker", newarr.spec.ndie)
	mapval, existed := bigMap.Get(newarr.spec)
	if !existed {
		mapchan := mapval.(chan *RollArray)
		mapchan <- newarr
	} else {
		fmt.Println("SHOULD NOT HAPPEN: worker remade:", newarr.spec.ndie)
	}
	procchan <- newarr
	if newarr.spec.ndie == goal {
		close(procchan)
	}
}

func GetRolls(ndie SpecInt, nsides SpecInt) *RollArray {
	procchan := make(chan *RollArray, 20)
	goalspec := RollSpec{ndie, nsides}
	go starter(goalspec, procchan)
	return processor(ndie, procchan)
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

func starter(s RollSpec, procchan chan *RollArray) {
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
	for i := SpecInt(1); i <= ndie; i *= divint {
		l.PushBack(i)
	}
	//	fmt.Println("list made!:", l)

	curn := ndie
	for curval := getn(l, curn); curn > 0; curval = getn(l, curn) {
		curn -= curval
		//		fmt.Printf("pushing %d, now at %d\n", curval, curn)
		go gopower(RollSpec{curval, nsides}, s, procchan)
//		fmt.Println("starter:", curval)
	}
}

//func oldstarter(spec RollSpec, procchan chan *RollArray) {
//	curn := spec.ndie
//	for i := SpecInt(0); curn > 0; i++ {
//		curpow := SpecInt(math.Pow(float64(divint), float64(i)))
//		curval := curn % (curpow * divint)
//		curpowamt := curval / curpow
//		curspec := RollSpec{curpow, spec.nsides}
//		for j := SpecInt(0); j < curpowamt; j++ {
//			go gopower(curspec, procchan)
//		}
//		curn -= curval
//	}
//}

func processor(goal SpecInt, procchan chan *RollArray) (final *RollArray) {
//	fmt.Println("Processor started\n")
	var last *RollArray = nil
	for i := range procchan {
		if last == nil {
//			fmt.Println("Processor pulled", i)
			last = i
		} else {
			//			fmt.Println("Starting worker\n")
			go worker(last, i, goal, procchan)
//			fmt.Println("Processor pulled, started worker")
			last = nil
		}
	}
//	fmt.Println("Processor finished\n")
	return last
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

var usePercent = flag.Bool("p", false, "Return percentages instead of exact integers")

func printrolls(fr *RollArray, usepercent bool) {

}

func main() {
	//	maptester()
//	var ndie SpecInt = 1
	fr := GetRolls(100, 6)
	other := GetRolls(101, 6)
	w,t,l := fr.cmp(other)
	fmt.Printf("%v\n\n%v\n\n%v\n",w,t,l)
//	fmt.Println(fr.rolls)
//	fmt.Println(other.rolls)
//	fmt.Println(fr.spec.ndie, fr.rolls[0], fr.rolls[1], fr.rolls[ndie/2].Len())
//		fr = GetRolls(ndie+1, 6)
//		fmt.Println(fr.spec.ndie, fr.rolls[0], fr.rolls[1], fr.rolls[ndie/2].Len())
	//	fmt.Println(float(fr.rolls[ndie/2])/float(math.MaxInt64))
//	n := 0
//	for _ = range bigMap.Keys() {
//		n += 1
//	}
//	fmt.Println("keys:", n)
}

