import re

import networkx as nx
import sympy as sympy

from .utils import Pos, input_multiline

reg = re.compile(r"(\d+),(\d+)", re.MULTILINE)


def solution(input: str):
    max_x = 70
    max_y = 70
    positions = {Pos(x, y) for x in range(max_x + 1) for y in range(max_y + 1)}
    it = reg.finditer(input)
    corrupt: set[Pos] = set()
    for i in range(1024):
        x, y = next(it).groups()
        corrupt.add(Pos(int(x), int(y)))

    positions.difference_update(corrupt)
    graph = nx.Graph()
    graph.add_nodes_from(positions)
    for p in positions:
        graph.add_edges_from(
            {
                (p, x + p)
                for x in [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)]
                if x + p in positions
            }
        )
    x = nx.shortest_path_length(graph, Pos(0, 0), Pos(70, 70))

    return str(x)


def solution_two(input: str):
    max_x = 70
    max_y = 70
    positions = {Pos(x, y) for x in range(max_x + 1) for y in range(max_y + 1)}
    graph = nx.Graph()
    graph.add_nodes_from(positions)
    for p in positions:
        graph.add_edges_from(
            {
                (p, x + p)
                for x in [Pos(1, 0), Pos(-1, 0), Pos(0, 1), Pos(0, -1)]
                if x + p in positions
            }
        )
    corrupt = reg.finditer(input)
    i: Pos
    while nx.has_path(graph, Pos(0, 0), Pos(70, 70)):
        x, y = next(corrupt).groups()
        new_corrupt = Pos(int(x), int(y))
        if new_corrupt in graph.nodes:
            graph.remove_node(new_corrupt)
        i = new_corrupt

    return str(f"{i.x},{i.y}")


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
