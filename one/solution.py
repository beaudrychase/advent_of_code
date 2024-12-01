from collections import Counter

from .utils import create_input_lists, input_multiline


def solution(input: str):
    left: list[int]
    right: list[int]
    left, right = create_input_lists(input)
    left.sort()
    right.sort()
    distance = sum((abs(l - r) for l, r in zip(left, right)))
    return str(distance)


def solution_two(input: str):
    left: list[int]
    right: list[int]
    left, right = create_input_lists(input)
    count_in_right = Counter(right)
    similarity = sum((l * count_in_right[l] for l in left))
    return str(similarity)


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
