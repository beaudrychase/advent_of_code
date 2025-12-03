package main

import (
	"fmt"
	"os"
)

func part1(input string) string {
	_ = input
	result := "x"
	return result
}

func part2(input string) string {
	_ = input
	result := "x"
	return result
}

func main() {
	file_bytes, err := os.ReadFile("real.in")
	if err != nil {
		fmt.Print(err)
	}

	input := string(file_bytes)
	part1_result := part1(input)
	part2_result := part2(input)

	fmt.Println(part1_result)
	fmt.Println(part2_result)
}
