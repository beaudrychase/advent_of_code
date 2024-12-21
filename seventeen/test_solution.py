from test_utils import part_1_cases, part_2_cases

from .solution import solution, solution_two


@part_1_cases("a", "b", "c", "easy", "hard")
def test_part_1(shared_testcase):
    sample_data, expected_out = shared_testcase

    result = solution(sample_data)

    assert result == expected_out


@part_2_cases("a", "b", "hard")
def test_part_2(shared_testcase):
    sample_data, expected_out = shared_testcase

    result = solution_two(sample_data)

    assert result == expected_out
