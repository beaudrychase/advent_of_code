package main

import (
	"fmt"
	"math/big"
	"os"
	"regexp"
	"sort"
	"strconv"
	"strings"
)

type Range struct {
	start int64
	end   int64
}

type Inventory struct {
	fresh_ids   []Range
	ingredients []int64
}

func parseInput(input string) Inventory {
	parts := strings.Split(input, "\n\n")
	pat := regexp.MustCompile(`(\d+)-(\d+)`)
	matches := pat.FindAllStringSubmatch(parts[0], -1)
	fresh_ids := []Range{}
	for i := 0; i < len(matches); i++ {
		start, _ := strconv.ParseInt(matches[i][1], 10, 64)
		end, _ := strconv.ParseInt(matches[i][2], 10, 64)
		fresh_ids = append(fresh_ids, Range{start, end})
	}

	pat = regexp.MustCompile(`(\d+)`)
	matches = pat.FindAllStringSubmatch(parts[1], -1)
	ingredients := []int64{}
	for _, match := range matches {
		id, _ := strconv.ParseInt(match[0], 10, 64)
		ingredients = append(ingredients, id)
	}

	return Inventory{coalesceRanges(fresh_ids), ingredients}
}

func coalesceRanges(ranges []Range) []Range {
	sort.Slice(ranges, func(i int, j int) bool {
		return ranges[i].start < ranges[j].start
	})
	updated_ranges := []Range{}

	for i := 0; i < len(ranges); i++ {
		cand := Range{ranges[i].start, ranges[i].end}
		for j := i + 1; j < len(ranges) && ranges[j].start <= cand.end; j++ {
			cand.end = max(ranges[j].end, cand.end)
			i = j
		}
		updated_ranges = append(updated_ranges, cand)
	}

	return updated_ranges

}

func part1(input string) string {
	inventory := parseInput(input)
	fresh := 0
	for _, food := range inventory.ingredients {
		for _, r := range inventory.fresh_ids {
			if food >= r.start && food <= r.end {
				fresh++
				break
			}
		}
	}
	result := strconv.Itoa(fresh)
	return result
}

func part2(input string) string {
	inventory := parseInput(input)
	total := big.NewInt(0)
	for _, r := range inventory.fresh_ids {
		total.Add(total, big.NewInt((r.end-r.start)+1))
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
