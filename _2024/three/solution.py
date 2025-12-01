import re

from .utils import input_multiline

pattern = re.compile(r"mul\((\d+),(\d+)\)", re.MULTILINE)


def solution(input_value: str):
    total = get_sum_of_commands(input_value)
    return str(total)


def get_sum_of_commands(input: str):
    total = 0
    for match in pattern.finditer(input):
        left, right = match.groups()
        total += int(left) * int(right)
    return total


do_filter = re.compile(r"(do\(\)|^)(.*?)(don't\(\)|$)", re.MULTILINE)


def solution_two(input_value: str):
    input_value = input_value.replace("\n", " ")
    result = 0
    for do_enabled_section in do_filter.finditer(input_value):
        _, command_section, _ = do_enabled_section.groups()
        result += get_sum_of_commands(command_section)
    return str(result)


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
    print(solution_two(input_value))
