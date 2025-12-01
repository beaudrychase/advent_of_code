from collections import defaultdict
from functools import cache
from typing import NamedTuple

import networkx as nx

from .utils import input_multiline


class LogicGate(NamedTuple):
    wire_1: str
    wire_2: str
    operator: str
    output: str


def solution(input: str):
    lookup: dict[str, int] = dict()
    wire_part, logic_part = input.split("\n\n")
    wires: set[str] = set()
    for line in wire_part.splitlines():
        name, val = line.split(": ")
        lookup[name] = int(val)
        wires.add(name)

    logic_gates: set[LogicGate] = set()
    for line in logic_part.splitlines():
        parts = line.split(" ")
        wire_1, operator, wire_2, _, output = parts

        wires.update([wire_1, wire_2, output])
        logic_gates.add(LogicGate(wire_1, wire_2, operator, output))

    logic_gates_by_output = {x.output: x for x in logic_gates}

    wires_by_first_character: dict[str, set[str]] = defaultdict(set)
    for w in wires:
        wires_by_first_character[w[0]].add(w)

    for z_wire in wires_by_first_character["z"]:
        find_value_of_wire(z_wire, lookup, logic_gates_by_output)

    return str(make_number("z", lookup))


@cache
def do_op(op: str, wire_1: int, wire_2: int) -> int:
    match op:
        case "XOR":
            return wire_1 ^ wire_2
        case "OR":
            return wire_1 | wire_2
        case _:
            return wire_1 & wire_2


def find_value_of_wire(
    wire: str, lookup: dict[str, int], logic_gates_by_output: dict[str, LogicGate]
):
    if wire in lookup:
        return lookup[wire]
    logic_gate = logic_gates_by_output[wire]
    res = do_op(
        logic_gate.operator,
        find_value_of_wire(logic_gate.wire_1, lookup, logic_gates_by_output),
        find_value_of_wire(logic_gate.wire_2, lookup, logic_gates_by_output),
    )
    lookup[wire] = res
    return res


def make_number(character: str, lookup: dict[str, int]) -> int:
    output_wires = list()
    for x in lookup:
        if x.startswith(character):
            output_wires.append(x)
    output_wires.sort(reverse=True)
    binary_str = "".join([str(lookup[x]) for x in output_wires])
    res = int(binary_str, 2)
    return res


# x = 18460186568099
# y = 34461222108877
# z = 52921408676976
# correct then current
# 1100000010 0 0011 011 10011 100 001111100 1000 1110000
# 1100000010 1 0011 100 10011 011 001111100 0111 1110000
def solution_two(input: str):
    lookup: dict[str, int] = dict()
    wire_part, logic_part = input.split("\n\n")
    wires: set[str] = set()
    for line in wire_part.splitlines():
        name, val = line.split(": ")
        lookup[name] = int(val)
        wires.add(name)

    logic_gates: set[LogicGate] = set()
    for line in logic_part.splitlines():
        parts = line.split(" ")
        wire_1, operator, wire_2, _, output = parts

        wires.update([wire_1, wire_2, output])
        logic_gates.add(LogicGate(wire_1, wire_2, operator, output))

    logic_gates_by_output = {x.output: x for x in logic_gates}

    graph = make_graph(wires, lookup, logic_gates_by_output)

    return str("")


def make_graph(
    wires: set[str], lookup: dict[str, int], logic_gates_by_output: dict[str, LogicGate]
):
    graph = nx.DiGraph()
    for wire in wires:
        find_value_of_wire(wire, lookup, logic_gates_by_output)
    for logic_gate in logic_gates_by_output.values():
        graph.add_edge(logic_gate.output, logic_gate.wire_1)
        graph.add_edge(logic_gate.output, logic_gate.wire_2)
        graph.nodes[logic_gate.output]["op"] = logic_gate.operator

    for wire in wires:
        if wire.startswith("z"):
            graph.add_edge(f"out_{wire}", wire)

    return graph


def swap(graph: nx.DiGraph, n_1, n_2):
    for pred in graph.pred[n_1]:
        graph.remove_edge(pred, n_1)
        graph.add_edge(pred, n_2)

    for pred in graph.pred[n_2]:
        graph.remove_edge(pred, n_2)
        graph.add_edge(pred, n_1)


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
