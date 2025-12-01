import re
from dataclasses import dataclass

import sympy as sympy

from .utils import Pos, input_multiline

reg = re.compile(r"(/W+),?", re.MULTILINE)


@dataclass
class RaceTrack:
    start: Pos
    finish: Pos
    positions: dict[Pos, int]


def solution(input: str):
    grid = [[c for c in line] for line in input.splitlines()]
    race_track = make_race_track(grid)
    shortcuts: set[tuple[Pos, Pos]] = set()

    for x in race_track.positions:
        x_score = race_track.positions[x]
        candidates = {
            x + c
            for c in {
                Pos(2, 0),
                Pos(-2, 0),
                Pos(0, 2),
                Pos(0, -2),
                Pos(1, 1),
                Pos(1, -1),
                Pos(-1, -1),
                Pos(-1, 1),
            }
            if x + c in race_track.positions
        }
        for c in candidates:
            if race_track.positions[c] - (x_score + 2) >= 100:
                shortcuts.add((x, c))

    return str(len(shortcuts))


def make_race_track(grid: list[list[str]]):
    start: Pos
    finish: Pos
    positions: set[Pos] = set()
    for x, line in enumerate(grid):
        for y, c in enumerate(line):
            pos = Pos(x, y)
            match c:
                case "S":
                    start = pos
                    positions.add(pos)
                case "E":
                    finish = pos
                    positions.add(pos)
                case ".":
                    positions.add(pos)
    cur = start
    scored: dict[Pos, int] = dict()
    distance = 0
    while cur != finish:
        scored[cur] = distance
        candidates = {
            cur + x
            for x in [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)]
            if cur + x not in scored and cur + x in positions
        }
        if not candidates:
            break
        cur = candidates.pop()
        distance += 1
    scored[finish] = distance

    return RaceTrack(start, finish, scored)


def solution_two(input: str):
    grid = [[c for c in line] for line in input.splitlines()]
    race_track = make_race_track(grid)
    shortcuts: set[tuple[Pos, Pos]] = set()
    short_cut_paths = make_short_cut_paths()
    for x in race_track.positions:
        x_score = race_track.positions[x]
        candidates = {
            (x + c, d)
            for c, d in short_cut_paths.items()
            if x + c in race_track.positions
        }
        for c in candidates:
            if race_track.positions[c[0]] - (x_score + c[1]) >= 100:
                shortcuts.add((x, c[0]))

    return str(len(shortcuts))


def make_short_cut_paths():
    short_cut_paths: dict[Pos, int] = dict()
    for x in range(41):
        for y in range(41):
            distance = abs(abs(x) - 20) + abs(abs(y) - 20)
            if distance <= 20:
                short_cut_paths[Pos(x - 20, y - 20)] = distance
    del short_cut_paths[Pos(0, 0)]
    return short_cut_paths


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
