from Structures.Tree import *
from Structures.MBR import *
from Env.Env import *
import datetime
import os

class Mkdir:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, params: dict):
        self.params = params

    def exec(self):
        if currentLogged['User']:
            if self.__validateParams():
                with open(currentLogged['PathDisk'], 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == currentLogged['Partition']:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            tree: Tree = Tree(superBlock, file)
                            if tree.searchdir(self.params['path']):
                                self.__printError(f" -> Error mkdir: No pueden crearse la carpeta {self.params['path']} porque ya existe.")
                                return
                            if not self.params['r'] and len([i for i in self.params['path'].split('/') if i != '']) > 1:
                                self.__printError(f" -> Error mkdir: No se creó la carpeta {self.params['path']}, no existe la ruta donde intentó crearse.")
                                return
                            if self.params['r']:
                                dir = [i for i in self.params['path'].split('/') if i != '']
                                c = 0
                                while c < len(dir) - 1:
                                    tmpDir = [dir[i] for i in range(c + 1)]
                                    tree.mkdir('/' + '/'.join(tmpDir), currentLogged['PathDisk'], mbr.partitions[i].start)
                                    c += 1
                            tree.mkdir(self.params['path'], currentLogged['PathDisk'], mbr.partitions[i].start)
                            self.__printSuccess(f' -> mkdir: Nueva carpeta creada exitosamente \'{self.params["path"]}\'')
            else:
                self.__printError(f" -> Error mkdir: Faltan parámetros obligatorios para crear un directorio.")
        else:
            self.__printError(f" -> Error mkdir: No hay ningún usuario loggeado actualmente.")

    def __validateParams(self):
        if 'path' in self.params:
            self.params['path'] = self.params['path'].replace('"', '')
            return True
        return False

    def __printError(self, text):
        print(f"\033[31m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccess(self, text):
        print(f"\033[32m{text} [{self.line}:{self.column}]\033[0m")