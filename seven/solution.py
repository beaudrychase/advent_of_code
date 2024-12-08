import re

from .utils import input_multiline

reg = re.compile(r"\d+")


def solution(input_value: str):
    result = 0
    for line in input_value.splitlines():
        x = [int(x) for x in reg.findall(line)]
        total = x[0]
        numbers = x[1:]

        def rec(idx, aggregate):
            if idx >= len(numbers):
                return aggregate == total
            for i in range(2):
                if i == 0:
                    test = numbers[idx] + aggregate
                    res = rec(idx + 1, test)
                else:
                    test = numbers[idx] * aggregate
                    res = rec(idx + 1, test)
                if res:
                    return True
            return False

        if rec(1, numbers[0]):
            result += total
    return str(result)


def solution_two(input_value: str):
    result = 0
    for line in input_value.splitlines():
        x = [int(x) for x in reg.findall(line)]
        total = x[0]
        numbers = x[1:]

        def rec(idx, aggregate):
            if idx >= len(numbers):
                return aggregate == total
            for i in range(3):
                if i == 0:
                    test = numbers[idx] + aggregate
                    res = rec(idx + 1, test)
                elif i == 1:
                    test = numbers[idx] * aggregate
                    res = rec(idx + 1, test)
                else:
                    test = int(str(aggregate) + str(numbers[idx]))
                    res = rec(idx + 1, test)
                if res:
                    return True
            return False

        if rec(1, numbers[0]):
            result += total
    return str(result)


if __name__ == "__main__":
    input_value = input_multiline()
    print(solution(input_value))
    print(solution_two(input_value))
