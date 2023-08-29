from Structures.MBR import *
from Env.Env import *
import os

class Rep:
    def setParams(self, params : dict):
        self.params = params

    def exec(self):
        if not ('name' in self.params and 'path' in self.params and 'id' in self.params):
            self.printError(' -> Error rep: Faltan parámetros obligatorios para generar el reporte.')
            return
        self.params['path'] = self.params['path'].replace('"','')
        if self.params['name'].lower() == 'mbr':
            return
        if self.params['name'].lower() == 'disk':
            self.__reportDisk()
            return
        if self.params['name'].lower() == 'inode':
            return
        if self.params['name'].lower() == 'journaling':
            return
        if self.params['name'].lower() == 'block':
            return
        if self.params['name'].lower() == 'bm_inode':
            return
        if self.params['name'].lower() == 'bm_block':
            return
        if self.params['name'].lower() == 'tree':
            return
        if self.params['name'].lower() == 'sb':
            return
        if self.params['name'].lower() == 'file':
            return
        if self.params['name'].lower() == 'ls':
            return

    def __reportDisk(self):
        if self.params['id'][3:] in disks:
            diskPath = disks[self.params['id'][3:]]
            absolutePath = os.path.abspath(diskPath)
            if not os.path.exists(absolutePath):
                self.printError(' -> Error rep: No existe el disco para reportar.')
                return
            with open(absolutePath, 'rb') as file:
                readed_bytes = file.read(127)
                mbr = MBR.decode(readed_bytes)
                isThereEmpty = False
                lastNoEmptyByte = 126
                dotParts = ''
                ocuppedCells = 10
                for i in range(len(mbr.partitions)):
                    if mbr.partitions[i].status:
                        if isThereEmpty or mbr.partitions[i].start - lastNoEmptyByte > 1:
                            space = round(((mbr.partitions[i].start - (lastNoEmptyByte + 1)) / mbr.size) * 200, 2)
                            ocuppedCells += int(space)
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                        space = round((mbr.partitions[i].size / mbr.size) * 200, 2)
                        ocuppedCells += int(space)
                        if mbr.partitions[i].type == 'P':
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">{mbr.partitions[i].name.strip()}<BR/>Primaria<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                        elif mbr.partitions[i].type == 'M':
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">{mbr.partitions[i].name.strip()}<BR/>Extendida<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                        lastNoEmptyByte = mbr.partitions[i].start + mbr.partitions[i].size - 1
                        isThereEmpty = False
                    else:
                        isThereEmpty = True
                if lastNoEmptyByte < mbr.size:
                    space = round(((mbr.size - (lastNoEmptyByte + 1)) / mbr.size) * 200, 2)
                    dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                    ocuppedCells += int(space)

                dot = 'digraph Disk{\n\tnode [shape=plaintext];'
                dot += '\n\ttabla[label=<\n\t\t<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="2" CELLPADDING="4">'
                dot += f'\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="{ocuppedCells}">Disk1</TD>\n\t\t\t</TR>'
                dot += '\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="6">MBR</TD>'
                dot += dotParts
                dot += '\n\t\t\t</TR>'
                dot += '\n\t\t</TABLE>\n\t>];'
                dot += '\n}'
                self.__generateFile(dot)
        else:
            self.printError(' -> Error rep: No existe el disco para reportarlo.')

    def __generateFile(self, dot):
        absolutePath = os.path.abspath(self.params['path'])
        destdir = os.path.dirname(absolutePath)
        extension = os.path.basename(absolutePath).split('.')[1]
        absolutePathDot = absolutePath.replace(extension, 'dot')
        if not os.path.exists(destdir):
            os.makedirs(destdir)
        with open(absolutePathDot, 'w') as file:
            file.write(dot)
        os.system(f'dot -T{extension} {absolutePathDot} -o {absolutePath}')
        os.remove(absolutePath.replace(extension, "dot"))

    def porcentaje(self, number : float) -> int or float:
        num = number - int(number)
        if num > 0:
            return number
        return int(number)

    def printError(self, text):
        print(f"\033[{31}m{text}\033[0m")

    def __str__(self) -> str:
        return 'Rep'