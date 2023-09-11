from Structures.ListEBR import ListEBR
from io import BufferedRandom
from Structures.MBR import *
from Structures.EBR import *
from Env.Env import *
import os
import re

class Rep:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, params : dict):
        self.params = params

    def exec(self):
        if not ('name' in self.params and 'path' in self.params and 'id' in self.params):
            self.__printError(' -> Error rep: Faltan parámetros obligatorios para generar el reporte.')
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
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            diskPath = disks[match.group(2)]['path']
            absolutePath = os.path.abspath(diskPath)
            if not os.path.exists(absolutePath):
                self.__printError(' -> Error rep: No existe el disco para reportar.')
                return
            with open(absolutePath, 'rb') as file:
                readed_bytes = file.read(127)
                mbr = MBR.decode(readed_bytes)
                dot = 'digraph MBR{\n\tnode [shape=plaintext];'
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
                            iterEBR : list[EBR] = self.__getListEBR(mbr.partitions[i].start, mbr.partitions[i].size, file).getIterable()
                            for ebr in iterEBR:
                                if ebr.status:
                                    dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F08080"><FONT COLOR="white">Particion Logica</FONT></TD>\n\t\t\t\t\t\t\t<TD COLSPAN="2" BGCOLOR="#F08080"></TD>\n\t\t\t\t\t\t</TR>'
                                    dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_status</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{ebr.status}</TD>\n\t\t\t\t\t\t</TR>'
                                    dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F5B7B1">part_next</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#F5B7B1">{ebr.next}</TD>\n\t\t\t\t\t\t</TR>'
                                    dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_fit</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{ebr.fit}</TD>\n\t\t\t\t\t\t</TR>'
                                    dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F5B7B1">part_start</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#F5B7B1">{ebr.start}</TD>\n\t\t\t\t\t\t</TR>'
                                    dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">part_size</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{ebr.size}</TD>\n\t\t\t\t\t\t</TR>'
                                    dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#F5B7B1">part_name</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#F5B7B1">{ebr.name.strip()}</TD>\n\t\t\t\t\t\t</TR>'
                dot += '\n\t\t\t\t\t</TABLE>\n\t\t\t\t</TD>\n\t\t\t</TR>'
                dot += '\n\t\t</TABLE>\n\t>];'
                dot += '\n}'
                self.__generateFile(dot, match.group(2))
        else:
            self.__printError(' -> Error rep: No existe el disco para reportarlo.')

    def __reportDisk(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            diskPath = disks[match.group(2)]['path']
            absolutePath = os.path.abspath(diskPath)
            if not os.path.exists(absolutePath):
                self.__printError(' -> Error rep: No existe el disco para reportar.')
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
                            space = self.__calculateSpace(mbr.partitions[i].start, lastNoEmptyByte + 1, mbr.size)
                            occupiedCells += int(space)
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.__percentage(mbr.partitions[i].start, lastNoEmptyByte + 1, mbr.size)} %</TD>'
                        space = self.__calculateSpace(mbr.partitions[i].size, 0, mbr.size)
                        if mbr.partitions[i].type == 'P':
                            occupiedCells += int(space)
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">{mbr.partitions[i].name.strip()}<BR/>Primaria<BR/>{self.__percentage(mbr.partitions[i].size, 0, mbr.size)} %</TD>'
                        elif mbr.partitions[i].type == 'E':
                            extendedParts = '\n\t\t\t<TR>'
                            lastNoEmptyByteExt = mbr.partitions[i].start - 1
                            occupiedExtend = 0
                            iterEBR : list[EBR] = self.__getListEBR(mbr.partitions[i].start, mbr.partitions[i].size, file).getIterable()
                            if iterEBR[0].status:
                                for ebr in iterEBR:
                                    if ebr.start - lastNoEmptyByteExt > 1:
                                        space = self.__calculateSpace(ebr.start, lastNoEmptyByteExt + 1, mbr.size)
                                        occupiedExtend += int(space)
                                        extendedParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="5">Libre<BR/>{self.__percentage(ebr.start, lastNoEmptyByteExt + 1, mbr.size)} %</TD>'
                                    extendedParts += '\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="5">EBR</TD>'
                                    space = self.__calculateSpace(ebr.size, 0, mbr.size)
                                    extendedParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="5">{ebr.name.strip()}<BR/>Logica<BR/>{self.__percentage(ebr.size, 0, mbr.size)} %</TD>'
                                    lastNoEmptyByteExt = ebr.start + ebr.size - 1
                                    occupiedExtend += 10 + int(space)
                            elif iterEBR[0].next != -1:
                                occupiedExtend += 10
                                extendedParts += '\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="5">EBR</TD>'
                                for e in range(1, len(iterEBR)):
                                    if iterEBR[e].start - lastNoEmptyByteExt > 1:
                                        space = self.__calculateSpace(iterEBR[e].start, lastNoEmptyByteExt + 1, mbr.size)
                                        occupiedExtend += int(space)
                                        extendedParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="5">Libre<BR/>{self.__percentage(iterEBR[e].start, lastNoEmptyByteExt + 1, mbr.size)} %</TD>'
                                    extendedParts += '\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="5">EBR</TD>'
                                    space = self.__calculateSpace(iterEBR[e].size, 0, mbr.size)
                                    extendedParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="5">{iterEBR[e].name.strip()}<BR/>Logica<BR/>{self.__percentage(iterEBR[e].size, 0, mbr.size)} %</TD>'
                                    lastNoEmptyByteExt = iterEBR[e].start + iterEBR[e].size - 1
                                    occupiedExtend += 10 + int(space)
                            else:
                                occupiedExtend += 10
                                extendedParts += '\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="5">EBR</TD>'
                            if mbr.partitions[i].start + mbr.partitions[i].size - lastNoEmptyByteExt > 1:
                                space = self.__calculateSpace(mbr.partitions[i].start + mbr.partitions[i].size, lastNoEmptyByteExt + 1, mbr.size)
                                occupiedExtend += int(space)
                                extendedParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="5">Libre<BR/>{self.__percentage(mbr.partitions[i].start + mbr.partitions[i].size, lastNoEmptyByteExt + 1, mbr.size)} %</TD>'
                            extendedParts += '\n\t\t\t</TR>'
                            occupiedCells += occupiedExtend
                            dotParts += f'\n\t\t\t\t<TD COLSPAN="{occupiedExtend}" ROWSPAN="1">{mbr.partitions[i].name.strip()}<BR/>Extendida</TD>'
                        lastNoEmptyByte = mbr.partitions[i].start + mbr.partitions[i].size - 1
                if mbr.size - lastNoEmptyByte > 1:
                    space = self.__calculateSpace(mbr.size, lastNoEmptyByte + 1, mbr.size)
                    dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.__percentage(mbr.size, lastNoEmptyByte + 1, mbr.size)} %</TD>'
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
                self.__generateFile(dot, match.group(2))
        else:
            self.__printError(' -> Error rep: No existe el disco para reportarlo.')

    def __getListEBR(self, start : int, size : int, file : BufferedRandom) -> ListEBR:
        listEBR : ListEBR = ListEBR(start, size)
        file.seek(start)
        ebr = EBR.decode(file.read(30))
        listEBR.insert(ebr)
        while ebr.next != -1:
            file.seek(ebr.next)
            ebr = EBR.decode(file.read(30))
            listEBR.insert(ebr)
        return listEBR

    def __generateFile(self, dot, diskname):
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
        self.__printSuccess(self.params['name'].lower(), diskname)

    def __percentage(self, start, firstEmptyByte, size) -> int or float:
        number = round(((start - firstEmptyByte) / size) * 100, 2)
        num = number - int(number)
        if round(num, 2) > 0:
            return number
        return int(number)

    def __calculateSpace(self, start, firstEmptyByte, size):
        num = round(((start - firstEmptyByte) / size) * 200, 2)
        if num >= 1:
            return num
        return 1

    def __printError(self, text):
        print(f"\033[{31}m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccess(self, type, diskname):
        print(f"\033[{35}m -> rep: Reporte generado exitosamente. '{type}' {diskname} [{self.line}:{self.column}]\033[0m")

    def __str__(self) -> str:
        return 'Rep'