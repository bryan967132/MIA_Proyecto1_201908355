from Env.Env import *

class Logout:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def exec(self):
        if currentLogged['User']:
            print(f"\033[32m -> logout: Sesión finalizada exitosamente. ({currentLogged['User'].name}) [{self.line}:{self.column}]\033[0m")
            currentLogged['User'] = None
        else:
            print(f"\033[31m -> Error logout: No hay ningún usuario loggeado actualmente. [{self.line}:{self.column}]\033[0m")