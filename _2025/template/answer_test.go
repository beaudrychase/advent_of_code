package main

import (
	"fmt"
	"os"
	"testing"
)

func read_string_from_file(file_name string) string {
	file_bytes, err := os.ReadFile(file_name)
	if err != nil {
		fmt.Print(err)
	}

	input := string(file_bytes)
	return input
}

func Test_1_1(t *testing.T) {
	input := read_string_from_file("1.in")

	got := part1(input)

	want := read_string_from_file("1.1.out")
	if got != want {
		t.Errorf("got %q, wanted %q", got, want)
	}
}

func Test_1_2(t *testing.T) {
	input := read_string_from_file("1.in")

	got := part2(input)

	want := read_string_from_file("1.2.out")
	if got != want {
		t.Errorf("got %q, wanted %q", got, want)
	}
}

func Test_Real_1(t *testing.T) {
	input := read_string_from_file("real.in")

	got := part1(input)

	want := read_string_from_file("real.1.out")
	if got != want {
		t.Errorf("got %q, wanted %q", got, want)
	}
}

func Test_Real_2(t *testing.T) {
	input := read_string_from_file("real.in")

	got := part2(input)

	want := read_string_from_file("real.2.out")
	if got != want {
		t.Errorf("got %q, wanted %q", got, want)
	}
}
