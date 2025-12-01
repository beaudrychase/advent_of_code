import re
from typing import NamedTuple

from .utils import input_multiline

reg = re.compile(r"\d", re.MULTILINE)

SPACE = -1


def solution(input_value: str):
    memory_layout = make_memory_layout(input_value)
    move_data_forward(memory_layout)

    total = 0
    for i, x in enumerate(memory_layout):
        if x != SPACE:
            total += i * x
    return str(total)


def make_memory_layout(input: str):
    res = list()
    id = 0
    file = True
    for c in input.strip():
        section_length = int(c)
        if file:
            res.extend([id for _ in range(section_length)])
            id += 1
        else:
            res.extend([SPACE for _ in range(section_length)])
        file = not file
    return res


def move_data_forward(memory_layout: list[int]):
    free_block_idx = 0
    for i in range(len(memory_layout) - 1, -1, -1):
        data = memory_layout[i]
        space = memory_layout[free_block_idx]
        while space != SPACE and free_block_idx < i:
            free_block_idx += 1
            space = memory_layout[free_block_idx]

        if space == SPACE:
            memory_layout[free_block_idx] = data
            memory_layout[i] = SPACE
        else:
            break


def solution_two(input_value: str):
    memory = Memory(input_value)
    memory.move_whole_files()

    answer = memory.get_answer()

    return str(answer)


class File(NamedTuple):
    id: int
    index: int
    size: int

    def calculate_answer_part(self):
        return sum((self.id * i for i in range(self.index, self.index + self.size)))


class Space(NamedTuple):
    index: int
    size: int


class Memory:
    files: list[File]
    spaces: list[Space]

    def __init__(self, input: str):
        last_allocated_idx = 0
        files: list[File] = list()
        spaces: list[Space] = list()
        id = 0
        file = True
        for x in input:
            match_length = int(x)
            if file:
                files.append(File(id, last_allocated_idx, match_length))
                id += 1
            else:
                spaces.append(Space(last_allocated_idx, match_length))
            last_allocated_idx += match_length
            file = not file

        self.files = files
        self.spaces = spaces

    def move_whole_files(self):
        files, spaces = (self.files, self.spaces)
        for i in range(len(files) - 1, -1, -1):
            file = files[i]
            j = 0
            space = spaces[j]
            while (
                space.size < file.size and space.index < file.index and j < len(spaces)
            ):
                j += 1
                space = spaces[j]

            if space.index > file.index:
                continue
            elif space.size == file.size:
                files[i] = File(file.id, space.index, file.size)
                del spaces[j]
            elif space.size > file.size:
                files[i] = File(file.id, space.index, file.size)
                spaces[j] = Space(space.index + file.size, space.size - file.size)

    def get_answer(self) -> int:
        total = 0
        for file in self.files:
            total += file.calculate_answer_part()
        return total


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
