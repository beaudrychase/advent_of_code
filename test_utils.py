from pytest import mark


def file_input(*file_names: str):
    return mark.parametrize("testcase", file_names, indirect=True)
