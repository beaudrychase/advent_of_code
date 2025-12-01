import re
from typing import NamedTuple

import sympy as sympy

from .utils import input_multiline

reg = re.compile(r"^p=(\d+),(\d+) v=(-?\d+),(-?\d+)$")

WIDTH = 101
HEIGHT = 103


class Pos(NamedTuple):
    x: int
    y: int


class Vel(NamedTuple):
    x: int
    y: int


class Robot(NamedTuple):
    pos: Pos
    vel: Vel


def solution(input_value: str):
    robots = make_robots(input_value)
    robot_final_pos = get_final_pos(robots, 100)

    quadrants = make_quadrants()
    counts = [0] * 4
    for pos in robot_final_pos:
        for i, quadrant in enumerate(quadrants):
            if pos in quadrant:
                counts[i] += 1

    safety = 1
    for v in counts:
        safety *= v
    return str(safety)


def make_robots(input: str) -> list[Robot]:
    lines = input.splitlines()
    robots: list[Robot] = list()
    for line in lines:
        match = reg.match(line)
        assert match is not None
        groups = match.groups()
        x, y, v_x, v_y = groups
        robots.append(Robot(Pos(int(x), int(y)), Vel(int(v_x), int(v_y))))

    return robots


def make_quadrants() -> list[frozenset[Pos]]:
    quadrants: list[frozenset[Pos]] = list()
    quad_1_ranges = (range(0, 50), range(0, 51))
    quad_2_ranges = (range(51, 101), range(0, 51))
    quad_3_ranges = (range(0, 50), range(52, 103))
    quad_4_ranges = (range(51, 101), range(52, 103))
    ranges = (quad_1_ranges, quad_2_ranges, quad_3_ranges, quad_4_ranges)
    for r in ranges:
        x_range, y_range = r
        quadrants.append(frozenset({Pos(x, y) for x in x_range for y in y_range}))

    return quadrants


def get_final_pos(robots: list[Robot], steps: int):
    result: list[Pos] = list()
    for robot in robots:
        result.append(
            Pos(
                simulate(robot.pos.x, robot.vel.x, WIDTH, steps),
                simulate(robot.pos.y, robot.vel.y, HEIGHT, steps),
            )
        )
    return result


def simulate(init: int, vel: int, max: int, steps: int) -> int:
    return (init + (vel * steps)) % max


def solution_two(input_value: str):
    robots = make_robots(input_value)

    with open("x.out", "w") as file:
        for i in range(1, 10000):
            positions: set[Pos] = set(get_final_pos(robots, i))

            grid = [[" " for _ in range(WIDTH)] for _ in range(HEIGHT)]
            for p in positions:
                grid[p.y][p.x] = "*"
            populated_grid = "\n".join(["".join(x) for x in grid])

            file.writelines([f"{i}\n", populated_grid, "\n-------------\n"])

    return ""


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
