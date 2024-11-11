from day_template.solution import solution
from test_utils import file_input


@file_input("a", "b")
def test_example2(testcase):
    sample_data, expected_out = testcase

    result = solution(sample_data)

    assert result == expected_out
