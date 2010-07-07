package main

import (
	"reflect"
	"fmt"
)

func ToChan(myfunc *reflect.FuncValue) chan []reflect.Value {
	funcasval := reflect.NewValue(myfunc)
	newfunc := new(reflect.FuncValue)
	newfunc.SetValue(funcasval)
	vallist := make([]reflect.Value, 0)
	mychan := make(chan []reflect.Value)
	go func() { mychan <- newfunc.Call(vallist) }()
	return mychan
}

func return3() uint { return 3 }

func main() {
	theval := reflect.NewValue(return3)
	thefunc := new(reflect.FuncValue)
	thefunc.SetValue(theval)
	mchan := ToChan(thefunc)
	 fmt.Println(<-mchan)
}

