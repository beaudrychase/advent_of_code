from typing import Iterator, Literal, Optional

from .utils import create_input_list_of_list, input_multiline

Sign = Literal[1, -1]


def solution(input: str):
    reports: list[list[int]] = create_input_list_of_list(input)
    total_safe = 0
    for report in reports:
        if is_safe(report):
            total_safe += 1

    return str(total_safe)


def is_safe(report: list[int]):
    gradient = get_sign(report[-1] - report[0])
    is_safe = True

    report_iterator = iter(report)
    previous_level = try_get_next(report_iterator)
    level = try_get_next(report_iterator)
    while is_safe and level is not None:
        difference = level - previous_level

        is_safe = is_level_difference_safe(gradient, difference)

        previous_level = level
        level = try_get_next(report_iterator)

    return is_safe


def is_level_difference_safe(gradient: Sign, difference: int):
    MIN_DIFFERENCE = 1
    MAX_DIFFERENCE = 3

    difference_sign = get_sign(difference)
    abs_difference = abs(difference)

    return (
        difference_sign == gradient
        and abs_difference >= MIN_DIFFERENCE
        and abs_difference <= MAX_DIFFERENCE
    )


def get_sign(n: int) -> Sign:
    return 1 if n > 0 else -1


def try_get_next(iterator: Iterator[int]) -> Optional[int]:
    return next(iterator, None)


def solution_two(input: str):
    reports = create_input_list_of_list(input)
    total_safe = 0
    for report in reports:
        if is_safe(report) or is_dampened_safe(report):
            total_safe += 1

    return str(total_safe)


def is_dampened_safe(report: list[int]):
    for i in range(len(report)):
        removed = report.pop(i)
        if is_safe(report):
            return True
        report.insert(i, removed)

    return False


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
