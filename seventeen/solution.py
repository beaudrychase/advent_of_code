import re
from enum import IntEnum
from typing import NamedTuple

import sympy as sympy

from .utils import input_multiline

reg = re.compile(r"\d", re.MULTILINE)


class Instruction(IntEnum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


class Program:
    inst_pointer: int
    reg_a: int
    reg_b: int
    reg_c: int
    memory: list[int]
    output: list[int]

    def __init__(self, memory: list[int], reg_a: int, reg_b: int, reg_c: int):
        self.inst_pointer = 0
        self.reg_a = reg_a
        self.reg_b = reg_b
        self.reg_c = reg_c
        self.memory = memory
        self.output = list()

    def process(self):
        while self.inst_pointer < len(self.memory) - 1:
            self.process_instruction()

    def process_instruction(self):
        lit = self.memory[self.inst_pointer + 1]
        instruction = Instruction(self.memory[self.inst_pointer])
        match instruction:
            case Instruction.ADV:
                self.adv(lit)
            case Instruction.BXL:
                self.bxl(lit)
            case Instruction.BST:
                self.bst(lit)
            case Instruction.JNZ:
                self.jnz(lit)
            case Instruction.BXC:
                self.bxc(lit)
            case Instruction.OUT:
                self.out(lit)
            case Instruction.BDV:
                self.bdv(lit)
            case Instruction.CDV:
                self.cdv(lit)
        self.inst_pointer += 2

    def adv(self, lit: int):
        num = self.reg_a
        div = 2 ** self.combo(lit)
        self.reg_a = int(num / div)

    def bxl(self, lit: int):
        self.reg_b = self.reg_b ^ lit

    def bst(self, lit: int):
        self.reg_b = self.combo(lit) % 8

    def jnz(self, lit: int):
        if self.reg_a != 0:
            self.inst_pointer = lit - 2

    def bxc(self, lit: int):
        self.reg_b = self.reg_b ^ self.reg_c

    def out(self, lit: int):
        self.output.append(self.combo(lit) % 8)

    def bdv(self, lit: int):
        num = self.reg_a
        div = 2 ** self.combo(lit)
        self.reg_b = int(num / div)

    def cdv(self, lit: int):
        num = self.reg_a
        div = 2 ** self.combo(lit)
        self.reg_c = int(num / div)

    def combo(self, lit: int) -> int:
        match lit:
            case 0 | 1 | 2 | 3:
                return lit
            case 4:
                return self.reg_a
            case 5:
                return self.reg_b
            case _:
                return self.reg_c


def solution(input_value: str):
    register_input, program_input = input_value.split("\n\n")
    registers = list()
    for line in register_input.splitlines():
        registers.append(int(line.split(" ")[-1]))
    memory = list()
    for x in reg.finditer(program_input):
        memory.append(int(x.group()))

    prog = Program(memory, *registers)
    prog.process()
    return ",".join([str(x) for x in prog.output])


def solution_two(input_value: str):
    register_input, program_input = input_value.split("\n\n")
    registers = list()
    for line in register_input.splitlines():
        registers.append(int(line.split(" ")[-1]))
    memory = list()
    for x in reg.finditer(program_input):
        memory.append(int(x.group()))

    reversed_memory = list(reversed(memory))
    a = rec(0, memory, len(memory) - 1)
    return str(a)


def rec(previous_a: int, whole_solution: list, idx: int):
    if idx < 0:
        return previous_a
    this_a = previous_a * 8
    for x in range(0, 18):
        res = list()
        a = this_a + x
        res = my_program_only_a(a, res)
        if res == whole_solution[idx:]:
            idx -= 1
            final_a = rec(a, whole_solution, idx)
            if final_a != -1:
                return final_a
            idx += 1
    return -1


def my_program(a: int):
    # bst 4
    b = a % 8
    # bxl 7
    b = b ^ 7
    # cdv 7
    c = int(a / (2**b))
    # bxc 1
    b = b ^ c
    # bxl 4
    b = b ^ 4
    # out 5
    output = b % 8
    # adv 3
    a = int(a / (8))

    print(output)
    if a == 0:
        return
    my_program(a)


def my_program_only_a(a: int, out: list):
    # bst 4
    # bxl 7
    # cdv 7
    # bxc 1
    # bxl 4
    # out 5
    output = (((a % 8) ^ 7) ^ int(a / (2 ** ((a % 8) ^ 7))) ^ 4) % 8
    # adv 3
    a = int(a / (8))
    out.append(output)
    if a == 0:
        return out
    return my_program_only_a(a, out)


class Snapshot(NamedTuple):
    reg_a: int
    reg_b: int
    reg_c: int
    instruction_pointer: int


class Command(NamedTuple):
    instruction: Instruction
    literal: int


class ProgramTwo(Program):

    correct_a: int
    visited_states: set

    def __init__(self, memory: list[int], reg_a: int, reg_b: int, reg_c: int):
        super().__init__(memory, reg_a, reg_b, reg_c)
        self.reg_a = 0
        self.correct_a = 0
        self.visited_states = set()

    def process(self):
        # new number if the last elements aren't equal
        # return if lists have same length and elements are equal
        # need to detect infinite loops
        res = list()
        commands = [
            Command(Instruction(self.memory[i]), self.memory[i + 1])
            for i in range(0, len(self.memory) - 1, 2)
        ]
        for d in reversed(self.memory):

            for a in range(1, 1000):
                self.reset()
                self.reg_a = a
                while self.inst_pointer < len(self.memory) - 1:
                    self.process_instruction()
                    snapshot = self.make_snapshot()

                    if snapshot in self.visited_states:
                        break
                    self.visited_states.add(snapshot)
                    last_idx_of_output = len(self.output) - 1
                    if (last_idx_of_output >= 0) or len(self.output) == len(
                        self.memory
                    ):
                        break

                if [d] == self.output:
                    res.append(a)
                    break
        return res

    def my_program(self):
        # bst 4
        self.reg_b = self.reg_a % 8
        # bxl 7
        self.reg_b = self.reg_b ^ 7
        # cdv 7
        self.reg_c = int(self.reg_a / (2**self.reg_b))
        # bxc 1
        self.reg_b = self.reg_b ^ self.reg_c
        # bxl 1
        self.reg_b = self.reg_b ^ 1
        # out 5
        output = self.reg_b % 8
        # adv 3
        self.reg_a = int(self.reg_a / (8))

    def reset(self):
        self.inst_pointer = 0
        self.output = list()
        self.visited_states = set()
        self.reg_a = 0
        self.reg_b = 0
        self.reg_c = 0

    def make_snapshot(self):
        return Snapshot(self.reg_a, self.reg_b, self.reg_c, self.inst_pointer)


if __name__ == "__main__":
    input = input_multiline()
    print(solution(input))
    print(solution_two(input))
