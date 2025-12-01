from collections import defaultdict
from typing import NamedTuple

import sympy as sympy

from .utils import input_multiline


class Key(NamedTuple):
    p_1: int
    p_2: int
    p_3: int
    p_4: int
    p_5: int


class Lock(NamedTuple):
    p_1: int
    p_2: int
    p_3: int
    p_4: int
    p_5: int


# Heights range from 0 through 5 inclusive.
# lock pin height of 0 accepts all key heights


def solution(input: str):
    sections = input.split("\n\n")
    locks: set[Lock] = set()
    keys: list[Key] = list()
    for section in sections:
        col_order = zip(*section.splitlines())
        pins = ["".join(x).count("#") - 1 for x in col_order]
        if section[0] == "#":
            locks.add(Lock(*pins))
        else:
            keys.append(Key(*pins))

    keys_with_pin_compatible: dict[int, dict[int, set[Key]]] = defaultdict(
        lambda: defaultdict(set)
    )
    for key in keys:
        for i, pin in enumerate(key):
            for key_pin_height in range(0, 6):
                if (pin + key_pin_height) <= 5:
                    keys_with_pin_compatible[i][key_pin_height].add(key)
    total = 0
    for lock in locks:
        candidates = set(keys)
        for i, key_pin in enumerate(lock):
            candidates = keys_with_pin_compatible[i][key_pin] & candidates
            if not candidates:
                break
        total += len(candidates)

    return str(total)


def solution_two(input: str):
    return ""


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
