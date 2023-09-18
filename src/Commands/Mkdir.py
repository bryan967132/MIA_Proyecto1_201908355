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
                            disk = disks[os.path.basename(currentLogged['PathDisk']).split('.')[0]]
                            dirExists = disk['ids'][currentLogged['IDPart']]['mkdirs']
                            if self.params['path'] in dirExists:
                                self.__printError(f" -> Error mkdir: No se creó la carpeta '{self.params['path']}' porque ya existe.")
                                return
                            if self.params['r']:
                                dir = [i for i in self.params['path'].split('/') if i != '']
                                c = 0
                                while c < len(dir):
                                    tmpDir = [dir[i] for i in range(c + 1)]
                                    if not tree.searchdir('/' + '/'.join(tmpDir)):
                                        tree.mkdir('/' + '/'.join(tmpDir), currentLogged['PathDisk'])
                                    c += 1
                            else:
                                dir = [i for i in self.params['path'].split('/') if i != '']
                                if len(dir) > 1:
                                    tmpDir = [dir[i] for i in range(len(dir) - 1)]
                                    if not tree.searchdir('/' + '/'.join(tmpDir)) and len([i for i in self.params['path'].split('/') if i != '']) > 1:
                                        self.__printError(f" -> Error mkdir: No se creó la carpeta '{self.params['path']}', no existe la ruta donde intentó crearse.")
                                        return
                                tree.mkdir(self.params['path'], currentLogged['PathDisk'])
                            if superBlock.filesystem_type == 3:
                                file.seek(mbr.partitions[i].start + SuperBlock.sizeOf())
                                for r in range(superBlock.inodes_count):
                                    readed_bytes = file.read(Journal.sizeOf())
                                    if readed_bytes == Journal.sizeOf() * b'\x00':
                                        with open(currentLogged['PathDisk'], 'r+b') as file:
                                            file.seek(mbr.partitions[i].start + SuperBlock.sizeOf() + r * Journal.sizeOf())
                                            file.write(Journal('mkdir', f'{self.params["path"]}', '', datetime.datetime.now()).encode())
                                            break
                            tree.writeInDisk(currentLogged['PathDisk'], mbr.partitions[i].start, superBlock.encode())
                            dirExists.append(self.params['path'])
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