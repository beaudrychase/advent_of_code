package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
)
const DIAL_SIZE = 100

type Dial struct{
	position int
}

func makeDial() *Dial {
	return &Dial{50}
}

func rotateDial(dial *Dial, command *Command) int {
	clicks := 0
	degrees := command.magnitude % DIAL_SIZE
	if command.is_right_turn {
		clicks = (dial.position + command.magnitude) / DIAL_SIZE
		dial.position += degrees
	} else {
		clicks = (((DIAL_SIZE - dial.position) % DIAL_SIZE) + command.magnitude) / DIAL_SIZE
		dial.position += DIAL_SIZE - degrees
	}
	dial.position = dial.position % DIAL_SIZE

	return clicks
}


type Command struct{
	is_right_turn bool
	magnitude int
}

func makeCommand(input string) *Command {
	firstChar := string(input[0])
	magnitude, _ := strconv.Atoi(input[1:])
	return &Command{firstChar == "R", magnitude}
}

func part_1() {
	dial := makeDial()
	count_of_zero_position := 0
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
		is_zero_position := dial.position == 0
		if is_zero_position {
			count_of_zero_position = count_of_zero_position + 1
		}
    }
	fmt.Printf("%v\n", count_of_zero_position)

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }
}

func part_2() {
	dial := makeDial()
	total_clicks := 0
	
	file, err := os.Open("real.in")
    if err != nil {
        log.Fatal(err)
    }
    defer file.Close()

    scanner := bufio.NewScanner(file)
    for scanner.Scan() {
        command := makeCommand(scanner.Text())
		clicks := rotateDial(dial, command)
		total_clicks = total_clicks + clicks
    }
	fmt.Printf("%v\n", total_clicks)

    if err := scanner.Err(); err != nil {
        log.Fatal(err)
    }
}

func main() {
	part_1()
	part_2()
}