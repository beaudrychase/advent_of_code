package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
)

type Coord struct {
	x int
	y int
}

const (
	ROLL  string = "@"
	EMPTY string = "."
	WALL  string = "X"
)

type Grid struct {
	layout map[Coord]string
	rows   int
	cols   int
}

func parseInputToGrid(input string) [][]string {
	result := [][]string{}
	scanner := bufio.NewScanner(strings.NewReader(input))
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 {
			break
		}
		number_line := []string{}
		for _, c := range line {
			number_line = append(number_line, string(c))
		}
		result = append(result, number_line)
	}

	return result
}

func parseInput(input string) Grid {
	grid := parseInputToGrid(input)
	result := map[Coord]string{}
	for y, row := range grid {
		for x, loc := range row {
			result[Coord{x, y}] = loc
		}
		result[Coord{-1, y}] = WALL
		result[Coord{len(row), y}] = WALL
	}
	for x, _ := range grid[0] {
		result[Coord{x, -1}] = WALL
		result[Coord{x, len(grid[0])}] = WALL
	}

	return Grid{result, len(grid[0]), len(grid)}
}

func getAdjacent(coord Coord) []Coord {
	return []Coord{
		{coord.x - 1, coord.y - 1},
		{coord.x, coord.y - 1},
		{coord.x + 1, coord.y - 1},
		{coord.x - 1, coord.y},
		{coord.x + 1, coord.y},
		{coord.x - 1, coord.y + 1},
		{coord.x, coord.y + 1},
		{coord.x + 1, coord.y + 1},
	}
}

func getRemovable(grid Grid) []Coord {
	removable := []Coord{}
	for x := range grid.rows {
		for y := range grid.cols {
			coord := Coord{x, y}
			if grid.layout[coord] == ROLL {
				adjacent_roll_count := 0
				for _, a := range getAdjacent(coord) {
					if grid.layout[a] == ROLL {
						adjacent_roll_count += 1
					}
				}
				if adjacent_roll_count < 4 {
					removable = append(removable, coord)
				}
			}
		}
	}
	return removable
}

func part1(input string) string {
	grid := parseInput(input)
	total := len(getRemovable(grid))

	result := strconv.Itoa(total)
	return result
}

func part2(input string) string {
	grid := parseInput(input)
	total := 0
	currently_removable := getRemovable(grid)
	for len(currently_removable) > 0 {
		total += len(currently_removable)
		for _, coord := range currently_removable {
			grid.layout[coord] = EMPTY
		}
		currently_removable = getRemovable(grid)

	}
	result := strconv.Itoa(total)
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
