from Structures.MBR import *
from Env.Env import *
import os

class Mkdisk:
    def setParams(self, params : dict):
        self.params = params

    def exec(self):
        if self.__validateParams():
            self.params['unit'] = self.params['unit'].upper()
            self.params['fit'] = self.params['fit'].upper()
            if self.params['size'] < 0:
                self.printError(' ->  Error: El tamaño de la partición debe ser mayor que cero')
                return
            k = 1
            if self.params['unit'] == 'M':
                k = 1024 * 1024
            elif self.params['unit'] == 'K':
                k = 1024
            else:
                self.printError(' ->  Error mkdisk: Unidad de Bytes Incorrecta')
                return
            self.params['path'] = self.params['path'].replace('"', '')
            absolutePath = os.path.abspath(self.params['path'])
            directory = os.path.dirname(absolutePath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            self.params['fit'] = self.params['fit'][:1]
            mbr = MBR(size = self.params['size'] * k, fit = self.params['fit'])
            disks[os.path.basename(self.params['path']).split('.')[0]] = os.path.abspath(self.params['path'])
            with open(self.params['path'], 'wb') as file:
                byte = b'\x00'
                for i in range(self.params['size']):
                    file.write(byte * k)
            with open(self.params['path'], 'r+b') as file:
                file.seek(0)
                file.write(mbr.encode())
        else:
            self.printError(' ->  Error mkdisk: Faltan Parámetros Obligatorios.')

    def __validateParams(self):
        size = False
        path = False
        for k in self.params:
            if k == 'size':
                self.params[k] = int(self.params[k])
                size = True
            elif k == 'path':
                path = True
        return size and path

    def printError(self, text):
        print(f"\033[{31}m{text}\033[0m")

    def __str__(self) -> str:
        return 'Mkdisk'