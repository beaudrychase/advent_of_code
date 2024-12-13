from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple

from .utils import input_multiline


class Pos(NamedTuple):
    x: int
    y: int

    def get_adjacent_pos(self):
        return {
            Pos(self.x + c.x, self.y + c.y)
            for c in {(Pos(0, 1)), Pos(0, -1), Pos(1, 0), Pos(-1, 0)}
        }


class Direction(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


class Perimeter(NamedTuple):
    pos: Pos
    direction: Direction


@dataclass
class Section:
    positions: set[Pos]
    perimeters: set[Perimeter]


class Plots:
    plants: dict[Pos, str]
    sections: list[Section]

    def __init__(self, input: str):
        grid = [[c for c in line] for line in input.strip().splitlines()]
        plants: dict[Pos, str] = dict()
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                plants[Pos(x, y)] = c
        self.plants = plants
        self.make_sections()

    def make_sections(self):
        unassigned = set(self.plants)

        def find_section(
            section_plant: str, pos: Pos, section: set[Pos], perimeter: set[Pos]
        ):
            if pos in section:
                return
            if pos not in self.plants or self.plants[pos] != section_plant:
                perimeter.add(pos)
                return

            unassigned.remove(pos)
            section.add(pos)
            for c in pos.get_adjacent_pos():
                if c in self.plants:
                    find_section(section_plant, c, section, perimeter)
                else:
                    perimeter.add(c)

        sections: list[Section] = list()
        while len(unassigned) > 0:
            pos = unassigned.pop()
            unassigned.add(pos)
            section = set()
            perimeter = set()
            find_section(self.plants[pos], pos, section, perimeter)
            res = self.make_perimeter_with_direction(section, perimeter)
            sections.append(
                Section(
                    section,
                    res,
                )
            )
        self.sections = sections

    def make_perimeter_with_direction(self, positions: set[Pos], perimeters: set[Pos]):
        res: set[Perimeter] = set()
        for s in positions:
            res.update(
                {
                    Perimeter(x, dir)
                    for x, dir in {
                        (Pos(s.x + 1, s.y), Direction.RIGHT),
                        (Pos(s.x - 1, s.y), Direction.LEFT),
                        (Pos(s.x, s.y + 1), Direction.DOWN),
                        (Pos(s.x, s.y - 1), Direction.UP),
                    }
                    if x in perimeters
                }
            )
        return res


def solution(input_value: str):
    plots = Plots(input_value)

    total = sum(
        (len(section.positions) * len(section.perimeters) for section in plots.sections)
    )
    return str(total)


def solution_two(input_value: str):
    plots = Plots(input_value)
    total = 0
    for section in plots.sections:
        sides = get_sides(section.perimeters)
        total += len(section.positions) * len(sides)
    return str(total)


def get_sides(perimeter: set[Perimeter]) -> list[set[Perimeter]]:
    sides: list[set[Perimeter]] = list()
    unsided_perimeter: set[Perimeter] = set(perimeter)

    while len(unsided_perimeter) > 0:
        first = unsided_perimeter.pop()
        unsided_perimeter.add(first)
        side = make_side(unsided_perimeter, first)

        sides.append(side)
    return sides


def make_side(unsided_perimeter: set[Perimeter], perimeter: Perimeter):
    side = set()
    side_edge = set([perimeter])
    while len(side_edge) > 0:
        cur = side_edge.pop()
        unsided_perimeter.remove(cur)
        side.add(cur)
        unallocated_and_shares_side = {
            x for x in get_adjacent_side_perimeters(cur) if x in unsided_perimeter
        }

        side_edge.update(unallocated_and_shares_side)
    return side


def get_adjacent_side_perimeters(perimeter: Perimeter):
    if perimeter.direction in {Direction.LEFT, Direction.RIGHT}:
        return {
            Perimeter(Pos(perimeter.pos.x, perimeter.pos.y + 1), perimeter.direction),
            Perimeter(Pos(perimeter.pos.x, perimeter.pos.y - 1), perimeter.direction),
        }

    else:
        return {
            Perimeter(Pos(perimeter.pos.x + 1, perimeter.pos.y), perimeter.direction),
            Perimeter(Pos(perimeter.pos.x - 1, perimeter.pos.y), perimeter.direction),
        }


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
