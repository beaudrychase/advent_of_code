package main

import (
	"bufio"
	"fmt"
	"math/big"
	"os"
	"strconv"
	"strings"
)

func parseInput(input string) [][]int {
	scanner := bufio.NewScanner(strings.NewReader(input))
	result := [][]int{}
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 {
			break
		}

		number_line := []int{}
		for _, c := range line {
			n, _ := strconv.Atoi(string(c))
			number_line = append(number_line, n)
		}
		result = append(result, number_line)
	}
	return result
}

func part1(input string) string {
	escalators := parseInput(input)
	total := 0

	for _, escalator := range escalators {
		first_num := escalator[0]
		first_num_index := 0
		for i := 0; i < len(escalator)-1; i++ {
			if escalator[i] > first_num {
				first_num = escalator[i]
				first_num_index = i
			}
		}
		second_num := escalator[first_num_index+1]
		for i := first_num_index + 1; i < len(escalator); i++ {
			if escalator[i] > second_num {
				second_num = escalator[i]
			}
		}
		joltage := first_num*10 + second_num
		total += joltage
	}

	result := strconv.Itoa(total)
	return result
}

func part2Joltage(escalator []int) *big.Int {
	total := big.NewInt(0)
	next_start_idx := 0
	for i := range 12 {
		candidate := escalator[next_start_idx]
		next_start_idx += 1
		for j := next_start_idx; j < len(escalator)-(11-i); j++ {
			if escalator[j] > candidate {
				candidate = escalator[j]
				next_start_idx = j + 1
			}
		}
		total.Mul(total, big.NewInt(10)).Add(total, big.NewInt(int64(candidate)))
	}
	return total
}

func part2(input string) string {
	escalators := parseInput(input)
	total := big.NewInt(int64(0))

	for _, escalator := range escalators {
		total.Add(total, part2Joltage(escalator))
	}

	result := total.String()
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
