def input_multiline() -> str:
    contents = []
    print("Enter/Paste your content. Ctrl-D or Ctrl-Z ( windows ) to save it.")
    while True:
        try:
            line = input()
        except EOFError:
            break
        contents.append(line)
    return "\n".join(contents)


def create_input_list_pair(file_data: str) -> tuple[list[int], list[int]]:
    lines = file_data.splitlines()
    left = list()
    right = list()
    for line in lines:
        l, r = line.split("   ")
        left.append(int(l))
        right.append(int(r))
    return left, right


def create_input_list_of_list(file_data: str):
    lines = file_data.splitlines()
    result = list()
    for line in lines:
        result.append([int(x) for x in line.split()])
    return result
