from Structures.Tree import *
from Structures.MBR import *
from Env.Env import *
import datetime
import os

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
                    if len(self.params['name']) <= 10:
                        with open(currentLogged['PathDisk'], 'rb') as file:
                            readed_bytes = file.read(127)
                            mbr = MBR.decode(readed_bytes)
                            for i in range(len(mbr.partitions)):
                                if mbr.partitions[i].status and mbr.partitions[i].name.strip() == currentLogged['Partition']:
                                    file.seek(mbr.partitions[i].start)
                                    superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                                    tree: Tree = Tree(superBlock, file)
                                    content, exists = tree.readFile('/users.txt')
                                    if exists:
                                        groups = tree.getGroups(content)
                                        newGroup: str = '{},G,{:<10}\n'.format(len(groups) + 1, self.params['name'])
                                        tree.writeFile('/users.txt', currentLogged['PathDisk'], mbr.partitions[i].start, newGroup)
                                        if superBlock.filesystem_type == 3:
                                            file.seek(mbr.partitions[i].start + SuperBlock.sizeOf())
                                            for r in range(superBlock.inodes_count):
                                                readed_bytes = file.read(Journal.sizeOf())
                                                if readed_bytes == Journal.sizeOf() * b'\x00':
                                                    with open(currentLogged['PathDisk'], 'r+b') as file:
                                                        file.seek(mbr.partitions[i].start + SuperBlock.sizeOf() + r * Journal.sizeOf())
                                                        file.write(Journal('mkgrp', '', f'{self.params["name"]}', datetime.datetime.now()).encode())
                                                        break
                                        self.__printSuccess(' -> mkgrp: Grupo {:<10} creado exitosamente. ({}: {})'.format(self.params['name'], currentLogged['Partition'], os.path.basename(currentLogged['PathDisk']).split('.')[0]))
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