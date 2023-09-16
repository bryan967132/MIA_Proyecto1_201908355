from Env.Env import *

class Rmusr:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, params: dict):
        self.params = params

    def exec(self):
        if currentLogged['User']:
            if currentLogged['User'].name == 'root':
                print(currentLogged['User'])
            else:
                self.__printError(f" -> Error rmusr: Solo el usuario 'root' puede eliminar usuarios.")
        else:
            self.__printError(f" -> Error rmusr: No hay ningún usuario loggeado actualmente.")

    def __printError(self, text):
        print(f"\033[31m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccess(self, text):
        print(f"\033[32m{text} [{self.line}:{self.column}]\033[0m")