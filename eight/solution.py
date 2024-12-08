import re
from collections import defaultdict
from typing import NamedTuple

from .utils import input_multiline

reg = re.compile(r"\d+")


class Position(NamedTuple):
    x: int
    y: int


def solution(input_value: str):
    grid = [[c for c in line] for line in input_value.splitlines()]
    antinodes: set[Position] = set()
    beacons: defaultdict[str, list[Position]] = defaultdict(list)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != ".":
                beacons[c].append(Position(x, y))

    for antennas in beacons.values():
        for a in antennas:
            anti = [
                Position(a.x + (a.x - other.x), a.y + (a.y - other.y))
                for other in antennas
                if other != a
            ]
            for x in anti:
                antinodes.add(x)
    antinodes = {
        x
        for x in antinodes
        if x.x >= 0 and x.y >= 0 and x.x < len(grid[0]) and x.y < len(grid)
    }
    return str(len(antinodes))


def solution_two(input_value: str):
    grid = [[c for c in line] for line in input_value.splitlines()]
    antinodes: set[Position] = set()
    beacons: defaultdict[str, list[Position]] = defaultdict(list)
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            if c != ".":
                beacons[c].append(Position(x, y))

    for antennas in beacons.values():
        for a in antennas:
            differences = {
                Position((a.x - other.x), (a.y - other.y))
                for other in antennas
                if other != a
            }
            multiplied = list()
            for d in differences:
                x = a.x
                y = a.y
                while x >= 0 and y >= 0 and x < len(grid[0]) and y < len(grid):
                    multiplied.append(Position(x, y))
                    x += d.x
                    y += d.y

            for x in multiplied:
                antinodes.add(x)
    antinodes = {
        x
        for x in antinodes
        if x.x >= 0 and x.y >= 0 and x.x < len(grid[0]) and x.y < len(grid)
    }
    return str(len(antinodes))


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
    print(solution_two(input_value))
