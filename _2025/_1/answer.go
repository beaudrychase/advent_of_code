package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)

const DIAL_SIZE = 100
const DIAL_STARTING_POSITION = 50

type Dial struct {
	position int
}

func makeDial() *Dial {
	return &Dial{DIAL_STARTING_POSITION}
}

func rotateDial(dial *Dial, command *Command) int {
	clicks := 0
	degrees := command.magnitude % DIAL_SIZE
	if command.isRightTurn {
		clicks = (dial.position + command.magnitude) / DIAL_SIZE
		dial.position += degrees
	} else {
		counterClockwisePosition := ((DIAL_SIZE - dial.position) % DIAL_SIZE)
		clicks = (counterClockwisePosition + command.magnitude) / DIAL_SIZE
		dial.position += DIAL_SIZE - degrees
	}
	dial.position = dial.position % DIAL_SIZE

	return clicks
}

type Command struct {
	isRightTurn bool
	magnitude   int
}

func makeCommand(input string) *Command {
	firstChar := string(input[0])
	magnitude, _ := strconv.Atoi(input[1:])
	return &Command{firstChar == "R", magnitude}
}

func part1() {
	dial := makeDial()
	countOfZeroPosition := 0
	// test()

	file, err := os.Open("real.in")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		command := makeCommand(scanner.Text())
		rotateDial(dial, command)
		isZeroPosition := dial.position == 0
		if isZeroPosition {
			countOfZeroPosition = countOfZeroPosition + 1
		}
	}
	fmt.Printf("%v\n", countOfZeroPosition)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

func part2() {
	dial := makeDial()
	totalClicks := 0

	file, err := os.Open("real.in")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		command := makeCommand(scanner.Text())
		clicks := rotateDial(dial, command)
		totalClicks = totalClicks + clicks
	}
	fmt.Printf("%v\n", totalClicks)

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

func main() {
	part1()
	part2()
}
