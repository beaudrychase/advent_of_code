import re

from .utils import input_multiline

xmas = re.compile(r"(XMAS)", re.MULTILINE)
samx = re.compile(r"(SAMX)", re.MULTILINE)


def solution(input_value: str):
    horizontal = input_value
    vertical = make_vertical(input_value)
    first_diagonal = make_diagonal(input_value)
    second_diagonal = make_perpendicular_axis_diagonal(input_value)
    together = [horizontal, vertical, first_diagonal, second_diagonal]

    result = sum((count_xmas_occurrences(block) for block in together))
    return str(result)


def make_vertical(block: str):
    lines = block.splitlines()
    split_by_character = [[c for c in line] for line in lines]
    vertical_lines = "\n".join(["".join(x) for x in zip(*split_by_character)])
    return vertical_lines


def make_diagonal(block: str):
    lines = block.splitlines()
    characters = [[c for c in line] for line in lines]
    return diagonal_of_2d(characters)


def diagonal_of_2d(two_d: list[list[str]]):
    rows = len(two_d[0])
    cols = len(two_d)
    result = list()
    for line_out in range(1, rows + cols):
        start_col = max(0, line_out - rows)
        length_of_line = min(line_out, (cols - start_col), rows)
        line = ""
        for y in range(length_of_line):
            line += two_d[min(rows, line_out) - y - 1][start_col + y]
        result.append(line)
    return "\n".join(result)


def make_perpendicular_axis_diagonal(block: str):
    lines = block.splitlines()
    reversed_characters = [[c for c in line[::-1]] for line in lines]
    return diagonal_of_2d(reversed_characters)


def count_xmas_occurrences(block: str):
    return len(re.findall(xmas, block) + re.findall(samx, block))


def solution_two(input_value: str):
    lines = input_value.splitlines()
    characters = [[c for c in line] for line in lines]

    rows = len(lines[0])
    cols = len(lines)
    total = 0
    for r in range(rows - 2):
        for c in range(cols - 2):
            if is_x_mas(
                top_left=characters[r][c],
                top_right=characters[r][c + 2],
                middle=characters[r + 1][c + 1],
                bottom_left=characters[r + 2][c],
                bottom_right=characters[r + 2][c + 2],
            ):
                total += 1

    return str(total)


def is_x_mas(
    top_left: str,
    top_right: str,
    middle: str,
    bottom_left: str,
    bottom_right: str,
):
    together = top_left + top_right + middle + bottom_left + bottom_right
    return together in {"MSAMS", "SMASM", "MMASS", "SSAMM"}


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
    print(solution_two(input_value))
