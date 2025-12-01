import networkx as nx
import sympy as sympy

from .utils import input_multiline


def solution(input: str):
    graph = nx.Graph()
    for line in input.splitlines():
        c1, c2 = line.split("-")
        graph.add_edge(c1, c2)
    sol = set()
    for cycle in nx.simple_cycles(graph, 3):
        for n in cycle:
            if n.startswith("t"):
                sol.add(frozenset(cycle))

    return str(len(sol))


def solution_two(input: str):
    graph = nx.Graph()
    for line in input.splitlines():
        c1, c2 = line.split("-")
        graph.add_edge(c1, c2)

    bi = nx.make_clique_bipartite(graph)
    n = -1
    max_found = list()
    while n in bi:
        if len(bi.adj[n]) > len(max_found):
            max_found = list(bi.adj[n].keys())
        n -= 1
    max_found.sort()
    return ",".join(max_found)


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
