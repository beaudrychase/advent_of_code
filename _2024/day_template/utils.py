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
