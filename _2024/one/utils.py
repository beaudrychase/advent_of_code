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


def create_input_lists(file_data: str) -> tuple[list[int], list[int]]:
    lines = file_data.splitlines()
    left = list()
    right = list()
    for line in lines:
        l, r = line.split("   ")
        left.append(int(l))
        right.append(int(r))
    return left, right
