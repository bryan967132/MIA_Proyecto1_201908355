from Structures.ListEBR import ListEBR
from Structures.SuperBlock import *
from Structures.InodesTable import *
from Structures.BlockFolder import *
from Structures.BlockFile import *
from Structures.BlockPointers import *
from Structures.Journaling import *
from Structures.Tree import *
from Structures.MBR import *
from Structures.EBR import *
from io import BufferedRandom
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
            self.__reportInode()
            return
        if self.params['name'].lower() == 'block':
            self.__reportBlock()
            return
        if self.params['name'].lower() == 'journaling':
            self.__reportJournaling()
            return
        if self.params['name'].lower() == 'bm_inode':
            self.__reportBMInode()
            return
        if self.params['name'].lower() == 'bm_block':
            self.__reportBMBlock()
            return
        if self.params['name'].lower() == 'tree':
            self.__reportTree()
            return
        if self.params['name'].lower() == 'sb':
            self.__reportSb()
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
            with open(absolutePath, 'rb') as file:
                readed_bytes = file.read(127)
                mbr = MBR.decode(readed_bytes)
                dot = 'digraph MBR{\n\tnode [shape=plaintext];'
                dot += '\n\ttabla[label=<\n\t\t<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
                dot += '\n\t\t\t<TR>\n\t\t\t\t<TD BORDER="1">\n\t\t\t\t\t<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">'
                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD COLSPAN="2" BGCOLOR="#4A235A"><FONT COLOR="white">{match.group(2)}</FONT></TD>\n\t\t\t\t\t\t</TR>'
                dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#4A235A"><FONT COLOR="white">MBR</FONT></TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#4A235A"></TD>\n\t\t\t\t\t\t</TR>'
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
                self.__generateFile(dot, f'({match.group(2)})')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

    def __reportDisk(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            diskPath = disks[match.group(2)]['path']
            absolutePath = os.path.abspath(diskPath)
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
                dot += f'\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="{occupiedCells}">{match.group(2)}</TD>\n\t\t\t</TR>'
                dot += '\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="6">MBR</TD>'
                dot += dotParts
                dot += '\n\t\t\t</TR>'
                dot += extendedParts
                dot += '\n\t\t</TABLE>\n\t>];'
                dot += '\n}'
                self.__generateFile(dot, f'({match.group(2)})')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

    def __reportInode(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            if self.params['id'] in disks[match.group(2)]['ids']:
                absolutePath = disks[match.group(2)]['path']
                namePartition = disks[match.group(2)]['ids'][self.params['id']]
                with open(absolutePath, 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == namePartition:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            file.seek(superBlock.bm_inode_start)
                            bm_inodes = file.read(superBlock.inodes_count).decode('utf-8')
                            dot = 'digraph Inodes{\n\tnode [shape=box];\n\trankdir=LR;'
                            for i in range(len(bm_inodes)):
                                if bm_inodes[i] == '1':
                                    file.seek(superBlock.inode_start + i * InodesTable.sizeOf())
                                    inode = InodesTable.decode(file.read(InodesTable.sizeOf()))
                                    dot += f'''\n\tn{i}[label = <<TABLE BORDER="0">
        <TR><TD colspan="2">Inodo {i}</TD></TR>
        <TR><TD ALIGN="LEFT">uid:</TD><TD ALIGN="LEFT">{inode.uid}</TD></TR>
        <TR><TD ALIGN="LEFT">gid:</TD><TD ALIGN="LEFT">{inode.gid}</TD></TR>
        <TR><TD ALIGN="LEFT">size:</TD><TD ALIGN="LEFT">{inode.size}</TD></TR>
        <TR><TD ALIGN="LEFT">atime:</TD><TD ALIGN="LEFT">{inode.atime}</TD></TR>
        <TR><TD ALIGN="LEFT">ctime:</TD><TD ALIGN="LEFT">{inode.ctime}</TD></TR>
        <TR><TD ALIGN="LEFT">mtime:</TD><TD ALIGN="LEFT">{inode.mtime}</TD></TR>'''
                                    for i in range(len(inode.block)):
                                        dot += f'\n\t\t<TR><TD ALIGN="LEFT">apt{i + 1}:</TD><TD ALIGN="LEFT">{inode.block[i]}</TD></TR>'
                                    dot += f'''
        <TR><TD ALIGN="LEFT">type:</TD><TD ALIGN="LEFT">{inode.type}</TD></TR>
        <TR><TD ALIGN="LEFT">perm:</TD><TD ALIGN="LEFT">{inode.perm}</TD></TR>
    </TABLE>>];'''
                            dot += '\n'
                            nodes = ''
                            for i in range(len(bm_inodes)):
                                if bm_inodes[i] == '1':
                                    if nodes != '':
                                        nodes += ' -> '
                                    else:
                                        nodes += '\t'
                                    nodes += 'n' + str(i)
                            dot += nodes
                            dot += ';\n}'
                            self.__generateFile(dot, f'({namePartition}: {match.group(2)})')
                            return
            else:
                self.__printError(f' -> Error rep: No existe el código de partición {self.params["id"]} para desmontar en el disco {match.group(2)}.')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

    def __reportBlock(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            if self.params['id'] in disks[match.group(2)]['ids']:
                absolutePath = disks[match.group(2)]['path']
                namePartition = disks[match.group(2)]['ids'][self.params['id']]
                with open(absolutePath, 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == namePartition:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            file.seek(superBlock.bm_inode_start)
                            tree: Tree = Tree(superBlock, file)
                            blocks = tree.getBlocks()
                            dot = 'digraph Blocks{\n\tnode [shape=box];\n\trankdir=LR;'
                            for i in blocks:
                                dot += f'{i[1].getDotB(i[0])}'
                            blocksDot = ''
                            for i in blocks:
                                if blocksDot != '':
                                    blocksDot += ' -> '
                                blocksDot += f'n{i[0]}'
                            dot += '\n\t' + blocksDot
                            dot += ';\n}'
                            self.__generateFile(dot, f'({namePartition}: {match.group(2)})')
                            return
            else:
                self.__printError(f' -> Error rep: No existe el código de partición {self.params["id"]} para desmontar en el disco {match.group(2)}.')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

    def __reportJournaling(self):
        pass

    def __reportBMInode(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            if self.params['id'] in disks[match.group(2)]['ids']:
                absolutePath = disks[match.group(2)]['path']
                namePartition = disks[match.group(2)]['ids'][self.params['id']]
                with open(absolutePath, 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == namePartition:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            file.seek(superBlock.bm_inode_start)
                            bm_inodes = file.read(superBlock.inodes_count).decode('utf-8')
                            matriz: str = ''
                            i: int = 0
                            while i < len(bm_inodes):
                                matriz += bm_inodes[i] + '  '
                                if (i + 1) % 20 == 0:
                                    matriz += '\n'
                                i += 1
                            with open(os.path.abspath(self.params['path']), 'w') as file:
                                file.write(matriz)
                            self.__printSuccess(self.params['name'].lower(), f'({namePartition}: {match.group(2)})')
                            return
            else:
                self.__printError(f' -> Error rep: No existe el código de partición {self.params["id"]} para desmontar en el disco {match.group(2)}.')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

    def __reportBMBlock(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            if self.params['id'] in disks[match.group(2)]['ids']:
                absolutePath = disks[match.group(2)]['path']
                namePartition = disks[match.group(2)]['ids'][self.params['id']]
                with open(absolutePath, 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == namePartition:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            file.seek(superBlock.bm_block_start)
                            bm_blocks = file.read(superBlock.blocks_count).decode('utf-8')
                            matriz: str = ''
                            i: int = 0
                            while i < len(bm_blocks):
                                matriz += bm_blocks[i] + '  '
                                if (i + 1) % 20 == 0:
                                    matriz += '\n'
                                i += 1
                            with open(os.path.abspath(self.params['path']), 'w') as file:
                                file.write(matriz)
                            self.__printSuccess(self.params['name'].lower(), f'({namePartition}: {match.group(2)})')
                            return
            else:
                self.__printError(f' -> Error rep: No existe el código de partición {self.params["id"]} para desmontar en el disco {match.group(2)}.')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

    def __reportTree(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            if self.params['id'] in disks[match.group(2)]['ids']:
                absolutePath = disks[match.group(2)]['path']
                namePartition = disks[match.group(2)]['ids'][self.params['id']]
                with open(absolutePath, 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == namePartition:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            file.seek(superBlock.bm_inode_start)
                            tree: Tree = Tree(superBlock, file)
                            self.__generateFile(tree.getDot(), f'({namePartition}: {match.group(2)})')
                            return
            else:
                self.__printError(f' -> Error rep: No existe el código de partición {self.params["id"]} para desmontar en el disco {match.group(2)}.')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

    def __reportSb(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d*)', self.params['id'])
        if match.group(2) in disks:
            if self.params['id'] in disks[match.group(2)]['ids']:
                absolutePath = disks[match.group(2)]['path']
                namePartition = disks[match.group(2)]['ids'][self.params['id']]
                with open(absolutePath, 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == namePartition:
                            file.seek(mbr.partitions[i].start)
                            superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                            dot = 'digraph SuperBlock{\n\tnode [shape=plaintext];'
                            dot += '\n\ttabla[label=<\n\t\t<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0">'
                            dot += '\n\t\t\t<TR>\n\t\t\t\t<TD BORDER="1">\n\t\t\t\t\t<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" CELLPADDING="4">'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD COLSPAN="2" BGCOLOR="#145A32"><FONT COLOR="white">{match.group(2)}</FONT></TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#145A32"><FONT COLOR="white">SuperBlock</FONT></TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#145A32"><FONT COLOR="white">{namePartition}</FONT></TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">filesystem_type</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.filesystem_type}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">inodes_count</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.inodes_count}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">blocks_count</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.blocks_count}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">free_inodes_count</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.free_inodes_count}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">free_blocks_count</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.free_blocks_count}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">mtime</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.mtime}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">umtime</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.umtime}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">mnt_count</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.mnt_count}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">magic</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.magic}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">inode_size</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.inode_s}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">block_size</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.block_s}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">first_ino</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.first_ino}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">first_blo</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.first_blo}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">bm_inode_start</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.bm_inode_start}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">bm_block_start</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.bm_block_start}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#27AE60">inode_start</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#27AE60">{superBlock.inode_start}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += f'\n\t\t\t\t\t\t<TR>\n\t\t\t\t\t\t\t<TD BGCOLOR="#FFFFFF">inode_start</TD>\n\t\t\t\t\t\t\t<TD COLSPAN="1" BGCOLOR="#FFFFFF">{superBlock.inode_start}</TD>\n\t\t\t\t\t\t</TR>'
                            dot += '\n\t\t\t\t\t</TABLE>\n\t\t\t\t</TD>\n\t\t\t</TR>'
                            dot += '\n\t\t</TABLE>\n\t>];'
                            dot += '\n}'
                            self.__generateFile(dot, f'({namePartition}: {match.group(2)})')
                            return
            else:
                self.__printError(f' -> Error rep: No existe el código de partición {self.params["id"]} para reportar en el disco {match.group(2)}.')
        else:
            self.__printError(f' -> Error rep: No existe el disco {match.group(2)} para reportar.')

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
        #os.remove(absolutePath.replace(extension, "dot"))
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