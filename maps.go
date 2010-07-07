package maps

import (
	"container/list"
)

type Value interface{}

type Map interface {
	Get(indx Value) (retval Value, ok bool)
	Put(indx Value, itm Value)
	Keys() (<-chan Value)
}

type simple map[Value]Value

func NewSimple() Map {
	s := make(simple)
	return s
}

func (m simple) Get(indx Value) (retval Value, ok bool) {
	v, ok := m[indx]
	return v, ok
}

func (m simple) Put(indx Value, itm Value) { m[indx] = itm }

func (m simple) iterate(c chan Value) {
	for k, _ := range m {
		c <- k
	}
	close(c)
}

func (m simple) Keys() (<-chan Value) {
	c := make(chan Value, 0)
	go m.iterate(c)
	return c
}

type safe chan *Map

func ToSafe(m *Map) Map {
	sm := make(safe, 1)
	sm <- m
	var mp Map = sm
	return mp
}

func NewSafe() Map{
	var themap Map = NewSimple()
	var m *Map = &themap
	return ToSafe(m)

}

func (sm safe) Get(indx Value) (retval Value, ok bool) {
	var m *Map = <-sm
	v, ok := m.Get(indx)
	sm <- m
	return v, ok
}

func (sm safe) Put(indx Value, itm Value) {
	m := <-sm
	m.Put(indx, itm)
	sm <- m
}

//takes a list, returns values one at a time, destroying the list as it goes
func listeater(l *list.List, c chan Value){
	var d *list.Element = nil
	for e := l.Front(); e != nil; e = e.Next() {
		if d != nil {l.Remove(d)}
		v := e.Value
		c <- v
		d = e
	}
	close(c)
}

func (sm safe) Keys() (<-chan Value) {
	m := <-sm
	inc := m.Keys()
	
	l := list.New()
	for i := range inc {
		l.PushBack(i)
	}
	sm <- m
	outchan := make(chan Value, 0)
	go listeater(l, outchan)
	return outchan
//	
//	return l.Iter()
}

type defaultfunc (func(indx Value) Value)

type defaultmap struct{
	inner *Map
	deffunc defaultfunc
}

func (m *defaultmap) Get(indx Value) (retval Value, existed bool){
	val, ok := m.inner.Get(indx)
	if ok {
		return val, true
	}
	val = m.deffunc(indx)
	m.inner.Put(indx, val)
	return val, false
}

func (m *defaultmap) Put(indx Value, itm Value){
	m.inner.Put(indx, itm)
}

func (m *defaultmap) Keys() (<- chan Value){
	return m.inner.Keys()
}

func ToDefault(mp *Map, deffunc defaultfunc) Map {
	d := defaultmap{mp, deffunc}
	return &d

}

func NewDefault(df defaultfunc) Map {
	simple := NewSimple()
	var mp Map = simple
	return ToDefault(&mp, df)
}

type Hashable interface {
	Hash() Value
}

type hashMap struct {
	inner *Map
	keymap map[Value] Hashable
}

func (h hashMap) Get(indx Value) (retval Value, ok bool){
	hash := (indx.(Hashable)).Hash()
	return h.inner.Get(hash)
}

func (h hashMap) Put(indx Value, itm Value){
	hash := (indx.(Hashable)).Hash()
	h.inner.Put(hash, itm)
	h.keymap[hash] = (indx.(Hashable))
}

func (h hashMap) iterate(c chan Value){
	for i := range h.inner.Keys(){
		c <- h.keymap[i]
	}
	close(c)
}

func (h hashMap) Keys() (<- chan Value){
	c := make(chan Value)
	go h.iterate(c)
	return c
}

func ToHash(mp *Map) Map {
	keymap := make(map[Value] Hashable)
	hmp := hashMap{mp, keymap}
	return hmp

}

func NewHash() Map {
	simple := NewSimple()
	var mp Map = simple
	return ToHash(&mp)
}
