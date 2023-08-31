from Env.Env import *
import os

class Rmdisk:
    def __init__(self, path : str = None):
        self.path = path.replace('"', '')

    def exec(self):
        if not self.path:
            self.printError(' -> Error rmdisk: No se especificó el disoc que quiere eliminar.')
            return
        absolutePath = os.path.abspath(self.path)
        if not os.path.exists(absolutePath):
            self.printError(' -> Error rmdisk: No existe el disco que quiere eliminar.')
            return
        while True:
            confirm = input(f"\033[33m -> Eliminar disco {os.path.basename(absolutePath).split('.')[0]} (y/n): \033[0m")
            if confirm.lower() == 'y':
                break
            elif confirm.lower() == 'n':
                return
        del disks[os.path.basename(absolutePath).split('.')[0]]
        os.remove(self.path)
        self.printSuccess(f' -> rmdisk: Disco {os.path.basename(absolutePath).split(".")[0]} elminado exitosamente.')

    def printError(self, text):
        print(f"\033[{31}m{text}\033[0m")

    def printSuccess(self, text):
        print(f"\033[96m{text}\033[0m")