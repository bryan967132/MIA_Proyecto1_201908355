from Structures.Tree import *
from Structures.MBR import *
from Env.Env import *

class Mkgrp:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, params: dict):
        self.params = params

    def exec(self):
        if currentLogged['User']:
            if currentLogged['User'].name == 'root':
                if self.__validateParams():
                    if len(self.params['name']) > 10:
                        with open(currentLogged['PathDisk'], 'rb') as file:
                            readed_bytes = file.read(127)
                            mbr = MBR.decode(readed_bytes)
                            for i in range(len(mbr.partitions)):
                                if mbr.partitions[i].status and mbr.partitions[i].name.strip() == currentLogged['Partition']:
                                    file.seek(mbr.partitions[i].start)
                                    superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                                    tree: Tree = Tree(superBlock, file)
                                    _, exists = tree.readFile('/users.txt')
                                    if exists:
                                        tree.writeFile('/users.txt', currentLogged['PathDisk'], self.params['name'])
                                    else:
                                        self.__printError(f" -> Error mkgrp: No existe el archivo /users.txt.")
                                    return
                    else:
                        self.__printError(f" -> Error mkgrp: El nombre de un grupo no puede contener más de 10 caracteres.")
                else:
                    self.__printError(f" -> Error mkgrp: Faltan parámetros obligatorios para crear un grupo.")
            else:
                self.__printError(f" -> Error mkgrp: Solo el usuario 'root' puede crear grupos.")
        else:
            self.__printError(f" -> Error mkgrp: No hay ningún usuario loggeado actualmente.")

    def __validateParams(self):
        if 'name' in self.params:
            return True
        return False

    def __printError(self, text):
        print(f"\033[31m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccess(self, text):
        print(f"\033[32m{text} [{self.line}:{self.column}]\033[0m")