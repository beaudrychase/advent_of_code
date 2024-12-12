from pytest import mark


def file_input(*file_names: str):
    return mark.parametrize("testcase", file_names, indirect=True)


def shared_input(solution_number: int, *file_names: str):
    args = [(file_name, solution_number) for file_name in file_names]
    return mark.parametrize("shared_testcase", args, indirect=True, ids=file_names)


def part_1_cases(*file_names: str):
    return shared_input(1, *file_names)


def part_2_cases(*file_names: str):
    return shared_input(2, *file_names)
