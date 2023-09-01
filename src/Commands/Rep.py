from Structures.MBR import *
from Structures.EBR import *
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
            self.__reportMBR()
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

    def __reportMBR(self):
        if self.params['id'][3:] in disks:
            diskPath = disks[self.params['id'][3:]]
            absolutePath = os.path.abspath(diskPath)
            if not os.path.exists(absolutePath):
                self.printError(' -> Error rep: No existe el disco para reportar.')
                return
            with open(absolutePath, 'rb') as file:
                readed_bytes = file.read(127)
                mbr = MBR.decode(readed_bytes)
                colors = [
                    ["#FFFFFF", "#FFFFFF"],
                    ["#E8DAEF", "#F5B7B1"]
                ]
                dot = 'digraph Disk{\n\tnode [shape=plaintext];'
                dot += '\n\ttabla[label=<\n\t\t<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
                dot += '\n\t\t\t<TR>\n\t\t\t\t<TD BORDER="1">\n\t\t\t\t\t<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">'
                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD COLSPAN="2" BGCOLOR="#4A235A"><FONT COLOR="white">{self.params["id"][3:]}</FONT></TD>\n\t\t\t\t\t\t</TR>'
                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#4A235A"><FONT COLOR="white">MBR</FONT></TD>\n\t\t\t\t\t\t\t<TD COLSPAN="2" BGCOLOR="#4A235A"></TD>\n\t\t\t\t\t\t</TR>'
                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">mbr_tamano</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{mbr.size}</TD>\n\t\t\t\t\t\t</TR>'
                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#E8DAEF">mbr_fecha_creacion</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#E8DAEF">{mbr.date}</TD>\n\t\t\t\t\t\t</TR>'
                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">mbr_fecha_creacion</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{mbr.date}</TD>\n\t\t\t\t\t\t</TR>'
                for i in range(len(mbr.partitions)):
                    if mbr.partitions[i].status:
                        dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#4A235A"><FONT COLOR="white">Particion</FONT></TD>\n\t\t\t\t\t\t\t<TD COLSPAN="2" BGCOLOR="#4A235A"></TD>\n\t\t\t\t\t\t</TR>'
                        dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_status</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{mbr.partitions[i].status}</TD>\n\t\t\t\t\t\t</TR>'
                        dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#E8DAEF">part_type</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#E8DAEF">{mbr.partitions[i].type}</TD>\n\t\t\t\t\t\t</TR>'
                        dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_fit</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{mbr.partitions[i].fit}</TD>\n\t\t\t\t\t\t</TR>'
                        dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#E8DAEF">part_start</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#E8DAEF">{mbr.partitions[i].start}</TD>\n\t\t\t\t\t\t</TR>'
                        dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_size</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{mbr.partitions[i].size}</TD>\n\t\t\t\t\t\t</TR>'
                        dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#E8DAEF">part_name</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#E8DAEF">{mbr.partitions[i].name.strip()}</TD>\n\t\t\t\t\t\t</TR>'
                        if mbr.partitions[i].type == 'E':
                            file.seek(mbr.partitions[i].start)
                            ebr = EBR.decode(file.read(30))
                            while ebr.status:
                                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F08080"><FONT COLOR="white">Particion Logica</FONT></TD>\n\t\t\t\t\t\t\t<TD COLSPAN="2" BGCOLOR="#F08080"></TD>\n\t\t\t\t\t\t</TR>'
                                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_status</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{ebr.status}</TD>\n\t\t\t\t\t\t</TR>'
                                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F5B7B1">part_next</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#F5B7B1">{ebr.next}</TD>\n\t\t\t\t\t\t</TR>'
                                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_fit</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{ebr.fit}</TD>\n\t\t\t\t\t\t</TR>'
                                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F5B7B1">part_start</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#F5B7B1">{ebr.start}</TD>\n\t\t\t\t\t\t</TR>'
                                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_size</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{ebr.size}</TD>\n\t\t\t\t\t\t</TR>'
                                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F5B7B1">part_name</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#F5B7B1">{ebr.name.strip()}</TD>\n\t\t\t\t\t\t</TR>'
                                if ebr.next != -1:
                                    file.seek(ebr.next)
                                    ebr = EBR.decode(file.read(30))
                                    continue
                                break
                dot += '\n\t\t\t\t\t</TABLE>\n\t\t\t\t</TD>\n\t\t\t</TR>'
                dot += '\n\t\t</TABLE>\n\t>];'
                dot += '\n}'
                self.__generateFile(dot)
        else:
            self.printError(' -> Error rep: No existe el disco para reportarlo.')

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
                lastNoEmptyByte = 126
                dotParts = ''
                occupiedCells = 10
                extendedParts = ''
                for i in range(len(mbr.partitions)):
                    if mbr.partitions[i].status:
                        if mbr.partitions[i].start - lastNoEmptyByte > 1:
                            space = round(((mbr.partitions[i].start - (lastNoEmptyByte + 1)) / mbr.size) * 200, 2)
                            occupiedCells += int(space)
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                        space = round((mbr.partitions[i].size / mbr.size) * 200, 2)
                        if mbr.partitions[i].type == 'P':
                            occupiedCells += int(space)
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">{mbr.partitions[i].name.strip()}<BR/>Primaria<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                        elif mbr.partitions[i].type == 'E':
                            extendedParts = '\n\t\t\t<TR>'
                            file.seek(mbr.partitions[i].start)
                            ebr = EBR.decode(file.read(30))
                            lastNoEmptyByteExt = mbr.partitions[i].start + 30
                            occupiedExtend = 0
                            if ebr.status:
                                while True:
                                    extendedParts += '\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="5">EBR</TD>'
                                    space = round((ebr.size / mbr.size) * 200, 2)
                                    extendedParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="5">{mbr.partitions[i].name.strip()}<BR/>Logica<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                                    lastNoEmptyByteExt = ebr.start + ebr.size - 1
                                    occupiedExtend += 10 + int(space)
                                    if ebr.next == -1:
                                        break
                                    file.seek(ebr.next)
                                    ebr = EBR.decode(file.read(30))
                            else:
                                occupiedExtend += 10
                                extendedParts += '\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="5">EBR</TD>'
                            if lastNoEmptyByteExt < mbr.partitions[i].start + mbr.partitions[i].size:
                                space = round(((mbr.partitions[i].start + mbr.partitions[i].size - (lastNoEmptyByteExt + 1)) / mbr.size) * 200, 2)
                                extendedParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="5">Libre<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                                occupiedExtend += int(space)
                            extendedParts += '\n\t\t\t</TR>'
                            occupiedCells += occupiedExtend
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{occupiedExtend}" ROWSPAN="1">{mbr.partitions[i].name.strip()}<BR/>Extendida</TD>'
                        lastNoEmptyByte = mbr.partitions[i].start + mbr.partitions[i].size - 1
                if lastNoEmptyByte < mbr.size:
                    space = round(((mbr.size - (lastNoEmptyByte + 1)) / mbr.size) * 200, 2)
                    dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                    occupiedCells += int(space)

                dot = 'digraph Disk{\n\tnode [shape=plaintext];'
                dot += '\n\ttabla[label=<\n\t\t<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="2" CELLPADDING="4">'
                dot += f'\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="{occupiedCells}">{self.params["id"][3:]}</TD>\n\t\t\t</TR>'
                dot += '\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="6">MBR</TD>'
                dot += dotParts
                dot += '\n\t\t\t</TR>'
                dot += extendedParts
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
        os.system(f'dot -T{extension} "{absolutePathDot}" -o "{absolutePath}"')
        # os.remove(absolutePath.replace(extension, "dot"))
        self.printSuccess(self.params['name'].lower(), self.params['id'][3:])

    def porcentaje(self, number : float) -> int or float:
        num = number - int(number)
        if num > 0:
            return number
        return int(number)

    def printError(self, text):
        print(f"\033[{31}m{text}\033[0m")

    def printSuccess(self, type, diskname):
        print(f"\033[{35}m -> rep: Reporte generado exitosamente. '{type}' {diskname}\033[0m")

    def __str__(self) -> str:
        return 'Rep'