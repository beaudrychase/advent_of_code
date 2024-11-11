from pathlib import Path

from pytest import fixture, mark

from day_template.solution import solution


@fixture
def testcase(request):
    requestor_directory = Path(request.module.__file__).parent
    with open(Path(requestor_directory, "tests", f"{request.param}.in")) as file:
        input = file.read()
    with open(Path(requestor_directory, "tests", f"{request.param}.out")) as file:
        expected_out = file.read()
    return (input, expected_out)


def file_input(*file_names: str):
    return mark.parametrize("testcase", file_names, indirect=True)


@file_input("a", "b")
def test_example2(testcase):
    sample_data, expected_out = testcase

    result = solution(sample_data)

    assert result == expected_out
