from Structures.ListEBR import ListEBR
from Structures.SuperBlock import *
from Structures.InodesTable import *
from Structures.BlockFolder import *
from Structures.BlockFile import *
from Structures.BlockPointers import *
from Structures.Journal import *
from Structures.MBR import *
from Structures.EBR import *
from io import BufferedRandom
from typing import List
from Env.Env import *
import datetime
import os
import re

class Mkfs:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, params: dict):
        self.params = params

    def exec(self):
        if self.__validateParams():
            self.__mkfs()
        else:
            self.__printError(' -> Error mkfs: Faltan parámetros obligatorios para formatear la partición')

    def __mkfs(self):
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
                            if self.params['fs'] == '2fs':
                                self.__ext2(absolutePath, mbr.partitions[i])
                            else:
                                self.__ext3(absolutePath, mbr.partitions[i])
                            self.__printSuccess(match.group(2), namePartition, self.params['id'], mbr.partitions[i].type, self.params['fs'])
                            return
            else:
                self.__printError(f' -> Error mkfs: No existe el código de partición {self.params["id"]} para formatear en el disco {match.group(2)}.')
        else:
            self.__printError(f' -> Error mkfs: No existe el disco {match.group(2)} para formatear la partición.')

    def __ext2(self, absolutePath: str, partition: Partition):
        n: int = int(((partition.size - SuperBlock.sizeOf()) / (4 + InodesTable.sizeOf() + 3 * BlockFolder.sizeOf())) // 1)
        superBlock: SuperBlock = SuperBlock()
        superBlock.filesystem_type = 2 if self.params['fs'] == '2fs' else 3
        superBlock.inodes_count = n
        superBlock.blocks_count = 3 * n
        superBlock.free_inodes_count = n - 2
        superBlock.free_blocks_count = 3 * n - 2
        superBlock.mtime = None
        superBlock.umtime = None
        superBlock.mnt_count = 0
        superBlock.magic = 0xEF53
        superBlock.inode_s = InodesTable.sizeOf()
        superBlock.block_s = BlockFolder.sizeOf()
        superBlock.first_ino = 2
        superBlock.first_blo = 2
        superBlock.bm_inode_start = partition.start + SuperBlock.sizeOf()
        superBlock.bm_block_start = superBlock.bm_inode_start + n
        superBlock.inode_start = superBlock.bm_block_start + 3 * n
        superBlock.block_start = superBlock.inode_start + n * InodesTable.sizeOf()

        inode0: InodesTable = InodesTable(block = [-1 for i in range(15)], perm = 777)
        inode0.block[0] = 0

        blockFolder: BlockFolder = BlockFolder()
        blockFolder.content[0] = Content('.'.ljust(12), 0)
        blockFolder.content[1] = Content('..'.ljust(12), 0)
        blockFolder.content[2] = Content('users.txt'.ljust(12), 1)

        userstxt: str = '1,G,root      \n1,U,root      ,root        ,123       \n'
        inode1: InodesTable = InodesTable(type = '1', size = len(userstxt), block = [-1 for i in range(15)], perm = 777)
        inode1.block[0] = 1

        blockFile: BlockFile = BlockFile(['' for i in range(64)])
        for c in range(len(userstxt)):
            blockFile.content[c] = userstxt[c]

        with open(absolutePath, 'r+b') as file:
            file.seek(partition.start)
            file.write(superBlock.encode())
            file.seek(superBlock.bm_inode_start)
            file.write('1'.encode('utf-8') * 2 + '0'.encode('utf-8') * (n - 2) + '1'.encode('utf-8') * 2 + '0'.encode('utf-8') * (3 * n - 2))
            file.seek(superBlock.inode_start)
            file.write(inode0.encode() + inode1.encode())
            file.seek(superBlock.block_start)
            file.write(blockFolder.encode() + blockFile.encode())

    def __ext3(self, absolutePath: str, partition: Partition):
        n: int = int(((partition.size - SuperBlock.sizeOf()) / (4 + Journal.sizeOf() + InodesTable.sizeOf() + 3 * BlockFolder.sizeOf())) // 1)
        superBlock: SuperBlock = SuperBlock()
        superBlock.filesystem_type = 3
        superBlock.inodes_count = n
        superBlock.blocks_count = 3 * n
        superBlock.free_inodes_count = n - 2
        superBlock.free_blocks_count = 3 * n - 2
        superBlock.mtime = None
        superBlock.umtime = None
        superBlock.mnt_count = 0
        superBlock.magic = 0xEF53
        superBlock.inode_s = InodesTable.sizeOf()
        superBlock.block_s = BlockFolder.sizeOf()
        superBlock.first_ino = 2
        superBlock.first_blo = 2
        superBlock.bm_inode_start = partition.start + SuperBlock.sizeOf() + n * Journal.sizeOf()
        superBlock.bm_block_start = superBlock.bm_inode_start + n
        superBlock.inode_start = superBlock.bm_block_start + 3 * n
        superBlock.block_start = superBlock.inode_start + n * InodesTable.sizeOf()

        inode0: InodesTable = InodesTable(block = [-1 for i in range(15)], perm = 777)
        inode0.block[0] = 0

        blockFolder: BlockFolder = BlockFolder()
        blockFolder.content[0] = Content('.'.ljust(12), 0)
        blockFolder.content[1] = Content('..'.ljust(12), 0)
        blockFolder.content[2] = Content('users.txt'.ljust(12), 1)

        userstxt: str = '1,G,root      \n1,U,root      ,root        ,123       \n'
        inode1: InodesTable = InodesTable(type = '1', size = len(userstxt), block = [-1 for i in range(15)], perm = 777)
        inode1.block[0] = 1

        blockFile: BlockFile = BlockFile(['' for i in range(64)])
        for c in range(len(userstxt)):
            blockFile.content[c] = userstxt[c]

        journal1: Journal = Journal('mkdir', '/', '', datetime.datetime.now())
        journal2: Journal = Journal('mkfile', 'users.txt', userstxt, datetime.datetime.now())

        with open(absolutePath, 'r+b') as file:
            file.seek(partition.start)
            file.write(superBlock.encode())
            file.seek(partition.start + SuperBlock.sizeOf())
            file.write(journal1.encode() + journal2.encode())
            file.seek(superBlock.bm_inode_start)
            file.write('1'.encode('utf-8') * 2 + '0'.encode('utf-8') * (n - 2) + '1'.encode('utf-8') * 2 + '0'.encode('utf-8') * (3 * n - 2))
            file.seek(superBlock.inode_start)
            file.write(inode0.encode() + inode1.encode())
            file.seek(superBlock.block_start)
            file.write(blockFolder.encode() + blockFile.encode())

    def __getListEBR(self, start: int, size: int, file: BufferedRandom) -> ListEBR:
        listEBR: ListEBR = ListEBR(start, size)
        file.seek(start)
        ebr = EBR.decode(file.read(30))
        listEBR.insert(ebr)
        while ebr.next != -1:
            file.seek(ebr.next)
            ebr = EBR.decode(file.read(30))
            listEBR.insert(ebr)
        return listEBR

    def __getExtended(self, partitions: List[Partition]):
        for i in range(len(partitions)):
            if partitions[i].type == 'E':
                return i
        return -1

    def __validateParams(self):
        if 'id' in self.params:
            return True
        return False

    def __printError(self, text):
        print(f"\033[31m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccess(self, diskname, name, ID, typePart, typeFs):
        typePart = "PRIMARIA " if typePart == 'P' else ("EXTENDIDA" if typePart == 'E' else "LOGICA   ")
        typeFs = "EXT2" if typeFs == '2fs' else "EXT3"
        print(f"\033[96m -> mkfs: Partición formateada ({typeFs}) exitosamente en {diskname}. {typePart} ({name}: {ID}) [{self.line}:{self.column}]\033[0m")