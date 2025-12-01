import re
from typing import NamedTuple

import sympy as sympy

from .utils import input_multiline

case_reg = re.compile(
    r"Button A: X\+(\d+), Y\+(\d+) Button B: X\+(\d+), Y\+(\d+) Prize: X=(\d+), Y=(\d+)",
    re.MULTILINE,
)
button_b = re.compile(r"Button B: X\+(\d+), Y\+(\d+)")
prize = re.compile(r"Prize: X\+(\d+), Y\+(\d+)")


class Button(NamedTuple):
    x: int
    y: int
    cost: int


class Prize(NamedTuple):
    x: int
    y: int


class Crane(NamedTuple):
    x_efficient: Button
    x_inefficient: Button
    y_efficient: Button
    y_inefficient: Button


class Situation(NamedTuple):
    crane: Crane
    prize: Prize


def solution(input_value: str):
    block = " ".join(input_value.splitlines())
    situations: list[Situation] = list()
    for match in case_reg.finditer(block):
        button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y = (
            match.groups()
        )
        button_a = Button(int(button_a_x), int(button_a_y), 3)
        button_b = Button(int(button_b_x), int(button_b_y), 1)
        prize = Prize(int(prize_x), int(prize_y))
        x_efficient, x_inefficient = (
            (button_a, button_b)
            if button_a.x / button_a.cost > button_b.x / button_b.cost
            else (button_b, button_a)
        )
        y_efficient, y_inefficient = (
            (button_a, button_b)
            if button_a.y / button_a.cost > button_b.y / button_b.cost
            else (button_b, button_a)
        )
        crane = Crane(x_efficient, x_inefficient, y_efficient, y_inefficient)
        situations.append(Situation(crane, prize))

    total = 0
    for sit in situations:
        total += minimum_cost_solution(sit)

    return str(int(total))


def minimum_cost_solution(situation: Situation):
    prize = situation.prize
    crane = situation.crane
    x_solution = linear_algebra_cost(prize, crane.x_efficient, crane.x_inefficient)

    if x_solution != -1:
        return x_solution
    return 0


def cost(prize: Prize, efficient: Button, inefficient: Button):
    y_remaining = prize.y
    x_remaining = prize.x
    acc_cost = 0
    while y_remaining > 0 and x_remaining > 0:

        if (
            y_remaining % efficient.y == 0
            and x_remaining % efficient.x == 0
            and y_remaining / efficient.y == x_remaining / efficient.x
        ):
            return acc_cost + (y_remaining / efficient.y * efficient.cost)
        acc_cost += inefficient.cost
        y_remaining -= inefficient.y
        x_remaining -= inefficient.x
    if y_remaining == 0 and x_remaining == 0:
        return acc_cost
    return -1


def linear_algebra_cost(prize: Prize, efficient: Button, inefficient: Button):
    x = sympy.Symbol("x", integer=True, negative=False)
    y = sympy.Symbol("y", integer=True, negative=False)
    aug_matrix = sympy.Matrix(
        [[efficient.x, inefficient.x, prize.x], [efficient.y, inefficient.y, prize.y]]
    )
    eq_1 = sympy.Eq(x * efficient.x + y * inefficient.x, prize.x)  # type: ignore
    eq_2 = sympy.Eq(x * efficient.y + y * inefficient.y, prize.y)  # type: ignore
    sol = sympy.solve((eq_1, eq_2), x, y)
    if sol:
        return sol[x] * efficient.cost + sol[y] * inefficient.cost
    return -1


def solution_two(input_value: str):
    block = " ".join(input_value.splitlines())
    situations: list[Situation] = list()
    for match in case_reg.finditer(block):
        button_a_x, button_a_y, button_b_x, button_b_y, prize_x, prize_y = (
            match.groups()
        )
        button_a = Button(int(button_a_x), int(button_a_y), 3)
        button_b = Button(int(button_b_x), int(button_b_y), 1)
        prize = Prize(10000000000000 + int(prize_x), 10000000000000 + int(prize_y))
        x_efficient, x_inefficient = (
            (button_a, button_b)
            if button_a.x / button_a.cost > button_b.x / button_b.cost
            else (button_b, button_a)
        )
        y_efficient, y_inefficient = (
            (button_a, button_b)
            if button_a.y / button_a.cost > button_b.y / button_b.cost
            else (button_b, button_a)
        )
        crane = Crane(x_efficient, x_inefficient, y_efficient, y_inefficient)
        situations.append(Situation(crane, prize))

    total = 0
    for sit in situations:
        total += minimum_cost_solution(sit)

    return str(int(total))


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
