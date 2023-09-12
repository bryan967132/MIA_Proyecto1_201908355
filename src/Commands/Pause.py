class Pause:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def exec(self):
        input(f"\033[33m -> pause \033[0m")