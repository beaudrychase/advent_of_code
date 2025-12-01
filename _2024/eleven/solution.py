from functools import lru_cache

from .utils import input_multiline


def solution(input_value: str):
    stones = make_initial_stones(input_value)
    total = sum((count_stones(s, 25) for s in stones))
    return str(total)


def make_initial_stones(input_value: str):
    return [int(s) for s in input_value.strip().split(" ")]


@lru_cache(maxsize=None)
def count_stones(stone: int, steps: int) -> int:
    if steps == 0:
        return 1

    remaining_steps = steps - 1
    if stone == 0:
        return count_stones(1, remaining_steps)

    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        stone_1 = int(stone_str[0 : len(stone_str) // 2])
        stone_2 = int(stone_str[len(stone_str) // 2 :])
        return count_stones(stone_1, remaining_steps) + count_stones(
            stone_2, remaining_steps
        )
    return count_stones(stone * 2024, remaining_steps)


def solution_two(input_value: str):
    stones = make_initial_stones(input_value)
    total = sum((count_stones(s, 75) for s in stones))
    return str(total)


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
