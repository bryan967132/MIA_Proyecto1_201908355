from Structures.MBR import *
from Env.Env import *
import os

class Mkdisk:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, params: dict):
        self.params = params

    def exec(self):
        if self.__validateParams():
            self.params['unit'] = self.params['unit'].upper()
            self.params['fit'] = self.params['fit'].upper()
            if self.params['size'] < 0:
                self.printError(' -> Error: El tamaño de la partición debe ser mayor que cero')
                return
            units = 1
            if self.params['unit'] == 'M':
                units = 1024 * 1024
            elif self.params['unit'] == 'K':
                units = 1024
            else:
                self.printError(' -> Error mkdisk: Unidad de Bytes Incorrecta')
                return
            self.params['path'] = self.params['path'].replace('"', '')
            absolutePath = os.path.abspath(self.params['path'])
            directory = os.path.dirname(absolutePath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.params['fit'] = self.params['fit'][:1]
            mbr = MBR(size = self.params['size'] * units, fit = self.params['fit'])
            disks[os.path.basename(self.params['path']).split('.')[0]] = os.path.abspath(self.params['path'])
            with open(self.params['path'], 'wb') as file:
                byte = b'\x00'
                for i in range(self.params['size']):
                    file.write(byte * units)
            with open(self.params['path'], 'r+b') as file:
                file.seek(0)
                file.write(mbr.encode())
            self.printSuccess(f' -> mkdisk: {os.path.basename(absolutePath).split(".")[0]} creado exitosamente. ({self.params["size"]} {self.params["unit"]}B)')
        else:
            self.printError(' -> Error mkdisk: Faltan Parámetros Obligatorios.')

    def __validateParams(self):
        if 'size' in self.params and 'path' in self.params:
            self.params['size'] = int(self.params['size'])
            return True
        return False

    def printError(self, text):
        print(f"\033[{31}m{text} [{self.line}:{self.column}]\033[0m")

    def printSuccess(self, text):
        print(f"\033[96m{text} [{self.line}:{self.column}]\033[0m")

    def __str__(self) -> str:
        return 'Mkdisk'