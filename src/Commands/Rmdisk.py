from Env.Env import *
import os

class Rmdisk:
    def __init__(self, path : str = None):
        self.path = path.replace('"', '')

    def exec(self):
        if not self.path:
            self.printError(' ->  Error rmdisk: No se especificó el disoc que quiere eliminar.')
            return
        absolutePath = os.path.abspath(self.path)
        if not os.path.exists(absolutePath):
            self.printError(' ->  Error rmdisk: No existe el disco que quiere eliminar.')
            return
        while True:
            confirm = input('Eliminar el disco (y/n): ')
            if confirm.lower() == 'y':
                break
            elif confirm.lower() == 'n':
                return
        del disks[os.path.basename(self.path).split('.')[0]]
        os.remove(self.path)


    def printError(self, text):
        print(f"\033[{31}m{text}\033[0m")