from dataclasses import dataclass
from enum import Enum, auto
from typing import NamedTuple

import sympy as sympy

from .utils import input_multiline


class Pos(NamedTuple):
    x: int
    y: int

    def __add__(self, addvalue: "Pos"):
        return Pos(self.x + addvalue.x, self.y + addvalue.y)


class Direction(Enum):
    UP = auto()
    LEFT = auto()
    DOWN = auto()
    RIGHT = auto()


dir_to_move = {
    Direction.UP: Pos(0, -1),
    Direction.DOWN: Pos(0, 1),
    Direction.RIGHT: Pos(1, 0),
    Direction.LEFT: Pos(-1, 0),
}

instruction_to_dir = {
    "^": Direction.UP,
    "v": Direction.DOWN,
    ">": Direction.RIGHT,
    "<": Direction.LEFT,
}


@dataclass
class Map:
    robot: Pos
    walls: set[Pos]
    boxes: set[Pos]


def solution(input_value: str):
    grid_block, instruction_block = input_value.split("\n\n")
    instructions = make_instructions(instruction_block)
    map = make_map(grid_block)
    for inst in instructions:
        process_intruction(inst, map)

    total = 0
    for b in map.boxes:
        total += b.x + b.y * 100
    return str(total)


def process_intruction(instruction: Direction, map: Map):
    move = dir_to_move[instruction]
    check_pos = map.robot + move
    boxes_to_move = set()
    while check_pos in map.boxes or check_pos in map.walls:
        if check_pos in map.walls:
            return
        if check_pos in map.boxes:
            boxes_to_move.add(check_pos)
        check_pos = check_pos + move
    map.robot = map.robot + move
    map.boxes.difference_update(boxes_to_move)
    map.boxes.update({x + move for x in boxes_to_move})


def make_map(input: str) -> Map:
    grid = [[c for c in line] for line in input.splitlines()]
    robot: Pos
    walls: set[Pos] = set()
    boxes: set[Pos] = set()
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            pos = Pos(x, y)
            match c:
                case "#":
                    walls.add(pos)
                case "O":
                    boxes.add(pos)
                case "@":
                    robot = pos

    return Map(robot, walls, boxes)


def make_instructions(input: str) -> list[Direction]:
    result = list()
    input = input.replace("\n", "")
    for c in input:
        result.append(instruction_to_dir[c])
    return result


@dataclass
class WideMap:
    robot: Pos
    walls: set[Pos]
    left_boxes: set[Pos]
    right_boxes: set[Pos]


def solution_two(input_value: str):
    grid_block, instruction_block = input_value.split("\n\n")
    instructions = make_instructions(instruction_block)
    map = make_wide_map(grid_block)
    for inst in instructions:
        process_wide_intruction(inst, map)

    total = 0
    for b in map.left_boxes:
        total += b.x + b.y * 100
    return str(total)


def make_wide_map(input: str) -> WideMap:
    input = (
        input.replace("#", "##")
        .replace("O", "[]")
        .replace(".", "..")
        .replace("@", "@.")
    )
    grid = [[c for c in line] for line in input.splitlines()]
    robot: Pos
    walls: set[Pos] = set()
    left_boxes: set[Pos] = set()
    right_boxes: set[Pos] = set()
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            pos = Pos(x, y)
            match c:
                case "#":
                    walls.add(pos)
                case "[":
                    left_boxes.add(pos)
                case "]":
                    right_boxes.add(pos)
                case "@":
                    robot = pos

    return WideMap(robot, walls, left_boxes, right_boxes)


def process_wide_intruction(instruction: Direction, map: WideMap):
    move: Pos = dir_to_move[instruction]
    check_pos: set[Pos] = {map.robot + move}
    left_boxes_to_move: set[Pos] = set()
    right_boxes_to_move: set[Pos] = set()
    checked_already: set[Pos] = set()
    while (
        check_pos & map.left_boxes or check_pos & map.right_boxes
    ) or check_pos & map.walls:
        if check_pos & map.walls:
            return
        new_left = set()
        new_right = set()
        if check_pos & map.left_boxes:
            new_left.update(check_pos & map.left_boxes)
            new_right.update({x + Pos(1, 0) for x in check_pos & map.left_boxes})

        if check_pos & map.right_boxes:
            new_right.update(check_pos & map.right_boxes)
            new_left.update({x + Pos(-1, 0) for x in check_pos & map.right_boxes})

        left_boxes_to_move.update(new_left)
        right_boxes_to_move.update(new_right)
        checked_already.update(check_pos)
        check_pos = {x + move for x in (new_left | new_right)} - checked_already

    map.robot = map.robot + move

    map.left_boxes.difference_update(left_boxes_to_move)
    map.left_boxes.update({x + move for x in left_boxes_to_move})

    map.right_boxes.difference_update(right_boxes_to_move)
    map.right_boxes.update({x + move for x in right_boxes_to_move})


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
