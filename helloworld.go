package main

import "fmt" // Package implementing formatted I/O.
import "big"

func main() {
	b := big.NewInt(43)
	c := big.NewInt(56)
	d := b + c
	fmt.Printf("%v\n", b)
//	fmt.Printf("Hello, world; or Καλημέρα κόσμε; or こんにちは 世界\n")
}

