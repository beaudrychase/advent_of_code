from typing import NamedTuple

from .utils import input_multiline


class Position(NamedTuple):
    x: int
    y: int


class TrailMap:

    heights: dict[Position, int]
    next_steps: dict[Position, frozenset[Position]]

    def __init__(self, grid: list[list[int]]):
        self.heights = dict()
        self.next_steps = dict()
        for y, row in enumerate(grid):
            for x, height in enumerate(row):
                position = Position(x, y)
                self.heights[position] = height

        for position, height in self.heights.items():

            adjacent_positions = {
                Position(position.x - 1, position.y),
                Position(position.x + 1, position.y),
                Position(position.x, position.y - 1),
                Position(position.x, position.y + 1),
            }
            filtered_adjacent = frozenset(
                {
                    x
                    for x in adjacent_positions
                    if x in self.heights and self.heights[x] == height + 1
                }
            )
            self.next_steps[position] = filtered_adjacent

    def count_trail_terminals(self) -> int:
        start_candidates = {pos for pos, height in self.heights.items() if height == 0}
        result = 0

        for c in start_candidates:
            result += len(self.get_terminals(c))

        return result

    def get_terminals(self, position: Position) -> set[Position]:
        if self.heights[position] == 9:
            return {position}

        result = set()
        for x in self.next_steps[position]:
            result.update(self.get_terminals(x))
        return result

    def get_all_paths(
        self,
    ) -> set[tuple[Position, ...]]:
        start_candidates = {pos for pos, height in self.heights.items() if height == 0}
        result = set()

        for c in start_candidates:
            result.update(self.get_paths_from_position(c, list(), set()))

        return result

    def get_paths_from_position(
        self,
        position: Position,
        visited: list[Position],
        acc: set[tuple[Position, ...]],
    ):
        if self.heights[position] == 9:
            visited.append(position)
            acc.add(tuple(visited))
            visited.pop()
            return acc

        for x in self.next_steps[position]:
            visited.append(position)
            self.get_paths_from_position(x, visited, acc)
            visited.pop()
        return acc


def solution(input_value: str):
    grid = [[int(c) for c in line.strip()] for line in input_value.splitlines()]
    map = TrailMap(grid)
    total = map.count_trail_terminals()

    return str(total)


def solution_two(input_value: str):
    grid = [[int(c) for c in line.strip()] for line in input_value.splitlines()]
    map = TrailMap(grid)
    paths = map.get_all_paths()

    return str(len(paths))


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
