from test_utils import file_input

from .solution import solution, solution_two


@file_input("a", "first_easy", "first_hard")
def test_example(testcase):
    sample_data, expected_out = testcase

    result = solution(sample_data)

    assert result == expected_out


@file_input("b", "second_easy", "second_hard")
def test_example_2(testcase):
    sample_data, expected_out = testcase

    result = solution_two(sample_data)

    assert result == expected_out
