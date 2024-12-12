from collections import defaultdict
from enum import Enum, auto
from typing import NamedTuple

from .utils import input_multiline


class Pos(NamedTuple):
    x: int
    y: int


class Direction(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


class Perimeter(NamedTuple):
    pos: Pos
    direction: Direction


class Plots:
    positions: dict
    sections: list[tuple[set, dict[Pos, set[Perimeter]]]]

    def __init__(self, input: str):
        grid = [[c for c in line] for line in input.strip().splitlines()]
        positions = dict()
        for y, row in enumerate(grid):
            for x, c in enumerate(row):
                positions[Pos(x, y)] = c
        self.positions = positions
        self.make_sections()

    def make_sections(self):
        unassigned = set(self.positions)

        def find_section(cat: str, pos: Pos, section: set[Pos], perimeter: set[Pos]):
            if pos in section:
                return
            if pos not in self.positions or self.positions[pos] != cat:
                perimeter.add(pos)
                return
            else:
                unassigned.remove(pos)
                section.add(pos)
            candidates = {
                Pos(pos.x + c.x, pos.y + c.y)
                for c in {(Pos(0, 1)), Pos(0, -1), Pos(1, 0), Pos(-1, 0)}
            }
            for c in candidates:
                if c in self.positions:
                    find_section(cat, c, section, perimeter)
                else:
                    find_section("*", c, section, perimeter)

        sections: list[tuple[set, dict[Pos, set[Perimeter]]]] = list()
        while len(unassigned) > 0:
            pos = unassigned.pop()
            unassigned.add(pos)
            section = set()
            perimeter = set()
            find_section(self.positions[pos], pos, section, perimeter)
            res = self.make_perimeter_adjacents(section, perimeter)
            sections.append(
                (
                    section,
                    res,
                )
            )
        self.sections = sections

    def make_perimeter_adjacents(self, section: set[Pos], perimeter: set[Pos]):
        res = defaultdict(set)
        for s in section:
            res[s].update(
                {
                    Perimeter(x, dir)
                    for x, dir in {
                        (Pos(s.x + 1, s.y), Direction.RIGHT),
                        (Pos(s.x - 1, s.y), Direction.LEFT),
                        (Pos(s.x, s.y + 1), Direction.DOWN),
                        (Pos(s.x, s.y - 1), Direction.UP),
                    }
                    if x in perimeter
                }
            )
        return res


def solution(input_value: str):
    plots = Plots(input_value)

    total = sum((len(x) * sum(len(p) for p in y.values()) for x, y in plots.sections))
    return str(total)


def solution_two(input_value: str):
    plots = Plots(input_value)
    total = 0
    for _, perimeter in plots.sections:
        sides = count_sides(perimeter)
        total += len(perimeter) * len(sides)
    return str(total)


def count_sides(perimeter: dict[Pos, set[Perimeter]]):
    sides: list[set[Perimeter]] = list()
    all_perimeter: set[Perimeter] = set()
    for x in perimeter.values():
        all_perimeter.update(x)

    while len(all_perimeter) > 0:
        first = all_perimeter.pop()
        all_perimeter.add(first)
        side = set()
        search = set([first])
        while len(search) > 0:
            cur = search.pop()
            all_perimeter.remove(cur)
            side.add(cur)
            if cur.direction in {Direction.LEFT, Direction.RIGHT}:
                shares_side = {
                    x
                    for x in {
                        Perimeter(Pos(cur.pos.x, cur.pos.y + 1), cur.direction),
                        Perimeter(Pos(cur.pos.x, cur.pos.y - 1), cur.direction),
                    }
                    if x in all_perimeter
                }
            else:
                shares_side = {
                    x
                    for x in {
                        Perimeter(Pos(cur.pos.x + 1, cur.pos.y), cur.direction),
                        Perimeter(Pos(cur.pos.x - 1, cur.pos.y), cur.direction),
                    }
                    if x in all_perimeter
                }
            search.update(shares_side)

        sides.append(side)
    return sides


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
