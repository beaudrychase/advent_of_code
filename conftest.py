from pathlib import Path

from pytest import fixture


@fixture
def testcase(request):
    requestor_directory = Path(request.module.__file__).parent
    with open(Path(requestor_directory, "tests", f"{request.param}.in")) as file:
        input = file.read()
    with open(Path(requestor_directory, "tests", f"{request.param}.out")) as file:
        expected_out = file.read()
    return (input, expected_out)
