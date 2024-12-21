from enum import Enum, auto
from typing import NamedTuple


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


DIR_TO_MOVE: dict[Direction, Pos] = {
    Direction.UP: Pos(0, -1),
    Direction.DOWN: Pos(0, 1),
    Direction.RIGHT: Pos(1, 0),
    Direction.LEFT: Pos(-1, 0),
}


def input_multiline() -> str:
    contents = []
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return "\n".join(contents)


def create_input_list_pair(file_data: str) -> tuple[list[int], list[int]]:
    lines = file_data.splitlines()
    left = list()
    right = list()
    for line in lines:
        l, r = line.split("   ")
        left.append(int(l))
        right.append(int(r))
    return left, right


def create_input_list_of_list(file_data: str) -> list[list[int]]:
    lines = file_data.splitlines()
    result = list()
    for line in lines:
        result.append([int(x) for x in line.split()])
    return result
