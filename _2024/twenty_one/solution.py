from enum import StrEnum
from itertools import product, tee
from typing import NamedTuple

import networkx as nx
import sympy as sympy

from .utils import Pos, input_multiline


class Command(StrEnum):
    UP = "^"
    LEFT = "<"
    DOWN = "v"
    RIGHT = ">"
    ENTER = "A"


class State(NamedTuple):
    num: str
    d_2: Command
    d_1: Command


PathLookup = dict[str, dict[str, tuple[Command, ...]]]


def solution(input: str):
    num_pad: dict[Pos, str] = {
        Pos(0, 0): "7",
        Pos(1, 0): "8",
        Pos(2, 0): "9",
        Pos(0, 1): "4",
        Pos(1, 1): "5",
        Pos(2, 1): "6",
        Pos(0, 2): "1",
        Pos(1, 2): "2",
        Pos(2, 2): "3",
        Pos(1, 3): "0",
        Pos(2, 3): "A",
    }
    direction_pad: dict[Pos, str] = {
        Pos(1, 0): Command.UP,
        Pos(2, 0): Command.ENTER,
        Pos(0, 1): Command.LEFT,
        Pos(1, 1): Command.DOWN,
        Pos(2, 1): Command.RIGHT,
    }
    num_pad_graph = make_graph(num_pad)
    d_pad_graph = make_graph(direction_pad)
    big = make_big_graph(num_pad_graph, d_pad_graph)
    total = 0
    for line in input.splitlines():
        x = sol(line, big)
        total += x * int(line[:-1])
    return str(total)


def make_big_graph(num_pad: nx.DiGraph, d_pad: nx.DiGraph):
    big_graph = nx.DiGraph()
    for num_pad_hand in num_pad.nodes:
        for n_adjacent in d_pad.nodes:
            for d_1 in d_pad.nodes:
                big_graph.add_node(State(num_pad_hand, n_adjacent, d_1))
    t = tee(d_pad.nodes, 25)
    lst = list(product(*t))
    for num_pad_hand in num_pad.nodes:
        for d_pad_2_hand in d_pad.nodes:
            for d_pad_1_hand in d_pad.nodes:
                big_graph.add_edges_from(
                    [
                        (
                            State(num_pad_hand, d_pad_2_hand, d_pad_1_hand),
                            State(num_pad_hand, d_pad_2_hand, adj),
                            attr,
                        )
                        for adj, attr in d_pad.adj[d_pad_1_hand].items()
                    ]
                )

                big_graph.add_edges_from(
                    [
                        (
                            State(num_pad_hand, d_pad_2_hand, d_pad_1_hand),
                            State(num_pad_hand, adj, d_pad_1_hand),
                            {"dir": Command.ENTER},
                        )
                        for adj, attr in d_pad.adj[d_pad_2_hand].items()
                        if attr["dir"] == d_pad_1_hand
                    ]
                )
                big_graph.add_edges_from(
                    [
                        (
                            State(num_pad_hand, d_pad_2_hand, d_pad_1_hand),
                            State(adj, d_pad_2_hand, d_pad_1_hand),
                            {"dir": Command.ENTER},
                        )
                        for adj, attr in num_pad.adj[num_pad_hand].items()
                        if attr["dir"] == d_pad_2_hand and d_pad_1_hand == Command.ENTER
                    ]
                )
                # can human send enter
    return big_graph


def sol(input: str, big_graph: nx.DiGraph):
    prev = "A"
    total = 0
    for c in input:
        path = nx.shortest_path(
            big_graph,
            State(prev, Command.ENTER, Command.ENTER),
            State(c, Command.ENTER, Command.ENTER),
        )
        total += len(path)
        edges = [big_graph.edges[(x, y)]["dir"] for x, y in zip(path, path[1:])]
        prev = c
    return total


def make_graph(pad: dict[Pos, str]):
    graph = nx.DiGraph()
    graph.add_nodes_from(pad.values())
    for pos, button in pad.items():
        neighbors: list[tuple[str, Command]] = [
            (pad[p + pos], dir)
            for p, dir in [
                (Pos(1, 0), Command.RIGHT),
                (Pos(-1, 0), Command.LEFT),
                (Pos(0, -1), Command.UP),
                (Pos(0, 1), Command.DOWN),
            ]
            if p + pos in pad
        ]
        graph.add_edges_from(
            ((button, o_button, {"dir": dir})) for o_button, dir in neighbors
        )
    return graph


def solution_two(input: str):
    return ""


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
