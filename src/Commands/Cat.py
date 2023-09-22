from Structures.Tree import *
from Structures.MBR import *
from Env.Env import *
import datetime
import os

class Cat:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, files: list):
        self.files = files

    def exec(self):
        if currentLogged['User']:
            if len(self.files) > 0:
                with open(currentLogged['PathDisk'], 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == currentLogged['Partition']:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            tree: Tree = Tree(superBlock, file)
                            print(f'\033[33m -> cat: \033[0m')
                            for i in self.files:
                                print('\033[53m\t -> ({})\n{:<20}\033[0m'.format(i[1], tree.readFile(i[1])[0]).replace('\n', '\n\t'))
                            return
            else:
                self.__printError(f' -> Error cat: No se incluyeron archivos.')
        else:
            self.__printError(f" -> Error cat: No hay ningún usuario loggeado actualmente.")

    def __printError(self, text):
        print(f"\033[31m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccess(self, text):
        print(f"\033[32m{text} [{self.line}:{self.column}]\033[0m")