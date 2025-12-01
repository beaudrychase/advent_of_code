from functools import cache

import sympy as sympy

from .utils import input_multiline


def solution(input: str):
    total = 0
    for x in input.splitlines():
        val = int(x)
        for i in range(2000):
            val = next_number(val)
        total += val
    return str(total)


@cache
def next_number(input: int) -> int:
    mult = (lambda x: x * 64, lambda x: x // 32, lambda x: x * 2048)
    prune = 16777216
    res = input
    for f in mult:
        res = f(res) ^ res
        res = res % prune
    return res


def solution_two(input: str):
    prices = list()
    for x in input.splitlines():
        val = int(x)
        seq = [val]
        for i in range(2000):
            val = next_number(val)
            seq.append(val)
        prices.append([x % 10 for x in seq])

    seq_to_price: list[dict[tuple[int, int, int, int], int]] = list()
    for price in prices:
        seq = dict()
        for i, x in enumerate(price[4:]):
            prev = price[i : i + 5]
            dif = tuple(
                (
                    next - cur
                    for next, cur in zip(
                        prev[1:],
                        prev,
                    )
                )
            )
            if dif not in seq:
                seq[dif] = x
        seq_to_price.append(seq)

    possible_seq = set()
    for seq in seq_to_price:
        possible_seq.update(seq.keys())
    res = 0
    for k in possible_seq:
        possible_res = 0
        for seq in seq_to_price:
            if k in seq:
                possible_res += seq[k]
        if possible_res > res:
            res = possible_res

    return str(res)


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
