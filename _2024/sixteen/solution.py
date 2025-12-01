from dataclasses import dataclass
from typing import NamedTuple

import networkx as nx
import sympy as sympy

from .utils import Direction, Pos, input_multiline


# G.add_edge(2, 3, weight=5)
class Node(NamedTuple):
    dir: Direction
    pos: Pos


@dataclass
class Grid:
    start: Pos
    end: Pos
    nodes: set[Node]


dir_to_move = {
    Direction.UP: Pos(0, -1),
    Direction.DOWN: Pos(0, 1),
    Direction.RIGHT: Pos(1, 0),
    Direction.LEFT: Pos(-1, 0),
}

dir_90_deg = {
    Direction.UP: [Direction.RIGHT, Direction.LEFT],
    Direction.DOWN: [Direction.RIGHT, Direction.LEFT],
    Direction.RIGHT: [Direction.UP, Direction.DOWN],
    Direction.LEFT: [Direction.UP, Direction.DOWN],
}


def solution(input_value: str):
    graph = nx.Graph()
    grid = make_grid(input_value)
    graph.add_nodes_from(grid.nodes)
    for n in graph.nodes:
        graph.add_edges_from(
            ((n, Node(d, n.pos), {"weight": 1000}) for d in dir_90_deg[n.dir])
        )
        if Node(n.dir, n.pos + dir_to_move[n.dir]) in graph.nodes:
            graph.add_edge(n, Node(n.dir, n.pos + dir_to_move[n.dir]), weight=1)
    x = min(
        (
            nx.shortest_path_length(
                graph,
                Node(Direction.RIGHT, grid.start),
                Node(d, grid.end),
                weight="weight",
            )
            for d in Direction
        )
    )
    return str(x)


def make_grid(input: str):
    grid = [[c for c in line] for line in input.splitlines()]
    start: Pos
    nodes: set[Node] = set()
    end: Pos
    for y, line in enumerate(grid):
        for x, c in enumerate(line):
            pos = Pos(x, y)
            match c:
                case ".":
                    nodes.update({Node(d, Pos(x, y)) for d in Direction})
                case "S":
                    start = Pos(x, y)
                    nodes.update({Node(d, Pos(x, y)) for d in Direction})
                case "E":
                    end = Pos(x, y)
                    nodes.update({Node(d, Pos(x, y)) for d in Direction})
    return Grid(start, end, nodes)


def solution_two(input_value: str):
    graph = nx.DiGraph()
    grid = make_grid(input_value)
    graph.add_nodes_from(grid.nodes)
    for n in graph.nodes:
        graph.add_edges_from(
            ((n, Node(d, n.pos), {"weight": 1000}) for d in dir_90_deg[n.dir])
        )
        if Node(n.dir, n.pos + dir_to_move[n.dir]) in graph.nodes:
            graph.add_edge(n, Node(n.dir, n.pos + dir_to_move[n.dir]), weight=1)
    shortest_path_len = min(
        (
            nx.shortest_path_length(
                graph,
                Node(Direction.RIGHT, grid.start),
                Node(d, grid.end),
                weight="weight",
            )
            for d in Direction
        )
    )
    dir = {
        x
        for x in Direction
        if nx.shortest_path_length(
            graph,
            Node(Direction.RIGHT, grid.start),
            Node(x, grid.end),
            weight="weight",
        )
        == shortest_path_len
    }
    paths = list()
    positions: set[Pos] = set()
    for d in dir:
        found_paths = nx.all_shortest_paths(
            graph,
            Node(Direction.RIGHT, grid.start),
            Node(d, grid.end),
            weight="weight",
        )
        i = 0
        for p in found_paths:
            positions.update({x.pos for x in p})
            i += 1

    for p in paths:
        positions.update({x.pos for x in p})
    return str(len(positions))


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
