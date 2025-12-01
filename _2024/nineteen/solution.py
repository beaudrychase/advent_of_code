import re
from functools import lru_cache

import sympy as sympy

from .utils import input_multiline

reg = re.compile(r"(/W+),?", re.MULTILINE)


def solution(input: str):
    patterns_str, problems_str = input.split("\n\n")

    patterns: frozenset[str] = frozenset({x for x in patterns_str.split(", ")})

    total = 0
    for pro in problems_str.splitlines():
        is_solvable = rec(pro, patterns)
        if is_solvable:
            total += 1

    return str(total)


@lru_cache
def rec(pro: str, patterns: frozenset[str]) -> bool:
    if pro in patterns or pro == "":
        return True
    candidates = [pro[:i] for i in range(len(pro))]
    for x in candidates:
        if x in patterns:
            res = rec(pro[len(x) :], patterns)
            if res:
                return res
    return False


def solution_two(input: str):
    patterns_str, problems_str = input.split("\n\n")

    patterns: frozenset[str] = frozenset({x for x in patterns_str.split(", ")})

    total = 0
    max_len_in_patterns = max((len(x) for x in patterns))

    @lru_cache(maxsize=1000)
    def rec_2(pro: str) -> int:
        sol = 0
        if pro == "":
            return 1
        candidates = [pro[:i] for i in range(1, len(pro) + 1)]

        for x in candidates:
            if x in patterns:
                res = rec_2(pro[len(x) :])
                sol += res
        return sol

    for pro in problems_str.splitlines():
        is_solvable = rec_2(pro)
        if is_solvable:
            total += is_solvable

    return str(total)


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
