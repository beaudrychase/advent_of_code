package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
)

type Range struct {
	start int
	end   int
}

func parseInput(input string) []Range {
	pat := regexp.MustCompile(`(\d+)`)
	matches := pat.FindAllStringSubmatch(input, -1)
	result := []Range{}
	for i := 0; i < len(matches); i += 2 {
		start, _ := strconv.Atoi(matches[i][0])
		end, _ := strconv.Atoi(matches[i+1][0])
		result = append(result, Range{start, end})
	}
	return result
}

func isNumberRepeatedTwice(id int) bool {
	converted_id := strconv.Itoa(id)
	split_size := len(converted_id) / 2
	if len(converted_id) != 1 || len(converted_id)%split_size == 0 {
		if converted_id[:split_size] == converted_id[split_size:] {
			return true
		}
	}
	return false
}

func isNumberRepeatedTwiceOrMore(id int) bool {
	converted_id := strconv.Itoa(id)
	for split_size := len(converted_id) / 2; split_size > 0; split_size -= 1 {
		if len(converted_id)%split_size == 0 {
			is_only_repeats := true
			for i := split_size; i < len(converted_id); i += split_size {
				if converted_id[:split_size] != converted_id[i:i+split_size] {
					is_only_repeats = false
					break
				}
			}
			if is_only_repeats {
				return true
			}

		}
	}
	return false
}

func part1(input string) string {
	ranges := parseInput(input)
	sum := 0
	for _, _range := range ranges {
		for i := _range.start; i <= _range.end; i++ {
			if isNumberRepeatedTwice(i) {
				sum += i
			}
		}
	}

	result := strconv.Itoa(sum)
	return result
}

func part2(input string) string {
	ranges := parseInput(input)
	sum := 0
	for _, _range := range ranges {
		for i := _range.start; i <= _range.end; i++ {
			if isNumberRepeatedTwiceOrMore(i) {
				sum += i
			}
		}
	}

	result := strconv.Itoa(sum)
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
