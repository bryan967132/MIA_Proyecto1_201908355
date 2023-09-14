from Structures.SuperBlock import *
from Structures.SuperBlock import *
from Structures.InodesTable import *
from Structures.BlockFolder import *
from Structures.BlockFile import *
from Structures.BlockPointers import *
from Structures.Journal import *
from Structures.User import *
from Structures.Group import *
from io import BufferedRandom
from typing import List, Tuple
import math

class Tree:
    def __init__(self, superBlock: SuperBlock, file: BufferedRandom):
        self.superBlock: SuperBlock = superBlock
        self.file: BufferedRandom = file
        self.blocks = []
        self.fileBlocks = []

# ============================== GRAPH TREE ================================

    def getDot(self, diskname, partName) -> str:
        dot: str = 'digraph Tree{\n\tnode [shape=plaintext];\n\trankdir=LR;\n\t'
        dot += f'label="{diskname}: {partName}";\n\tlabelloc=t;\n\t'
        dot += self.__getDotInode(0)
        dot += '\n}'
        return dot

    def __getDotInode(self, i) -> str:
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        dot = inode.getDot(i)
        for p in range(len(inode.block)):
            if inode.block[p] != -1:
                if p < 12:
                    if inode.type == '0':
                        dot += '\n\t' + self.__getDotBlockFolder(inode.block[p])
                    else:
                        dot += '\n\t' + self.__getDotBlockFile(inode.block[p])
                elif p == 12:
                    dot += '\n\t' + self.__getDotBlockPointers(inode.block[p], inode.type, 1)
                elif p == 13:
                    dot += '\n\t' + self.__getDotBlockPointers(inode.block[p], inode.type, 2)
                elif p == 14:
                    dot += '\n\t' + self.__getDotBlockPointers(inode.block[p], inode.type, 3)
                dot += f'\n\tinode{i}:A{p} -> block{inode.block[p]}:B{inode.block[p]};'
        return dot

    def __getDotBlockPointers(self, i: int, inodeType: str, simplicity: int) -> str:
        self.file.seek(self.superBlock.block_start + i * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        dot = blockPointers.getDot(i)
        for p in range(len(blockPointers.pointers)):
            if blockPointers.pointers[p] != -1:
                if simplicity == 1:
                    if inodeType == '0':
                        dot += '\n\t' + self.__getDotBlockFile(blockPointers.pointers[p])
                    else:
                        dot += '\n\t' + self.__getDotBlockFile(blockPointers.pointers[p])                        
                else:
                    dot += '\n\t' + self.__getDotBlockPointers(blockPointers.pointers[p], inodeType, simplicity - 1)
                dot += f'\n\tblock{i}:A{p} -> block{blockPointers.pointers[p]}:B{blockPointers.pointers[p]};'
        return dot

    def __getDotBlockFolder(self, i) -> str:
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        dot = blockFolder.getDot(i)
        for p in range(len(blockFolder.content)):
            if not blockFolder.content[p].name.strip() in ['.', '..'] and blockFolder.content[p].inodo != -1:
                dot += '\n\t' + self.__getDotInode(blockFolder.content[p].inodo)
                dot += f'\n\tblock{i}:A{p} -> inode{blockFolder.content[p].inodo}:I{blockFolder.content[p].inodo};'
        return dot

    def __getDotBlockFile(self, i) -> str:
        self.file.seek(self.superBlock.block_start + i * BlockFile.sizeOf())
        blockFile: BlockFile = BlockFile.decode(self.file.read(BlockFile.sizeOf()))
        return blockFile.getDot(i)

# =================================== GET BLOCKS ==================================

    def getBlocks(self):
        self.__searchInInodes(0)
        if len(self.blocks) > 1:
            for i in range(1, len(self.blocks)):
                for j in range(i, 0, -1):
                    if self.blocks[j][0] < self.blocks[j - 1][0]:
                        self.blocks[j], self.blocks[j - 1] = self.blocks[j - 1], self.blocks[j]
                        continue
                    break
        return self.blocks

    def __searchInInodes(self, i):
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        for p in range(len(inode.block)):
            if inode.block[p] != -1:
                if inode.type == '0':
                    self.__searchInBlockFolder(inode.block[p])
                else:
                    self.__searchInBlockFile(inode.block[p])

    def __searchInBlockFolder(self, i):
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        self.blocks.append([i, blockFolder])
        for p in range(len(blockFolder.content)):
            if not blockFolder.content[p].name.strip() in ['.', '..'] and blockFolder.content[p].inodo != -1:
                self.__searchInInodes(blockFolder.content[p].inodo)

    def __searchInBlockFile(self, i):
        self.file.seek(self.superBlock.block_start + i * BlockFile.sizeOf())
        blockFile: BlockFile = BlockFile.decode(self.file.read(BlockFile.sizeOf()))
        self.blocks.append([i, blockFile])

# ================================== READ CONTENT ==================================

    def readFile(self, path: str) -> Tuple[str, bool]:
        dir = [i for i in path.split('/') if i != '']
        return self.__readFileInInodes(0, dir)

    def __readFileInInodes(self, i, path: List[str]) -> Tuple[str, bool]:
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        content = ''
        founded = False
        for p in range(len(inode.block)):
            if inode.block[p] != -1:
                if inode.type == '0':
                    content, founded = self.__readFileInBlockFolder(inode.block[p], path)
                else:
                    cont, founded = self.__readFileInBlockFile(inode.block[p])
                    content += cont
        return content, founded

    def __readFileInBlockFolder(self, i, path: List[str]) -> Tuple[str, bool]:
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        self.blocks.append([i, blockFolder])
        for p in range(len(blockFolder.content)):
            if not blockFolder.content[p].name.strip() in ['.', '..'] and blockFolder.content[p].inodo != -1 and blockFolder.content[p].name.strip() == path[0]:
                path.pop(0)
                return self.__readFileInInodes(blockFolder.content[p].inodo, path)
        return '', False

    def __readFileInBlockFile(self, i) -> Tuple[str, bool]:
        self.file.seek(self.superBlock.block_start + i * BlockFile.sizeOf())
        blockFile: BlockFile = BlockFile.decode(self.file.read(BlockFile.sizeOf()))
        return ''.join(blockFile.content), True

# ================================= WRITE FILE ===================================

    def writeFile(self, path: str, diskpath: str, partstart: int, newContent: str):
        dir = [i for i in path.split('/') if i != '']
        self.__writeGrpFileInInodes(0, dir, diskpath, newContent, partstart)

    def __writeGrpFileInInodes(self, i: int, path: List[str], pathdsk, newContent: str, partstart: int):
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        if inode.type == '0':
            for p in range(len(inode.block)):
                if inode.block[p] != -1:
                    self.__writeFileInBlockFolder(inode.block[p], path, pathdsk, newContent, partstart)
        else:
            blocksFile: Tuple[int, BlockFile]
            for p in range(len(inode.block)):
                if inode.block[p] != -1:
                    blocksFile = self.__writeFileInBlockFile(inode.block[p])
            num, block = blocksFile
            contents = [[r for r in block.content if r != '']]
            for z in newContent:
                if len(contents[-1]) < 64:
                    contents[-1].append(z)
                else:
                    contents.append([z])
            block.content = contents.pop(0)
            self.__writeInDisk(pathdsk, self.superBlock.block_start + num * BlockFile.sizeOf(), block.encode())
            newSizeInode = (num - 1) * 64 + len(block.content)
            while len(contents) > 0:
                newBlock: BlockFile = BlockFile(['' for i in range(64)])
                contenew = contents.pop(0)
                newSizeInode = (num - 1) * 64 + len(contenew)
                if len(newBlock.content) == len(contenew):
                    newBlock.content = contenew
                else:
                    for h in range(len(contenew)):
                        newBlock.content[h] = contenew[h]
                nextFreeBitBlock = self.__findNextFreeBlock(1)
                for h in range(len(inode.block)):
                    if inode.block[h] == -1:
                        inode.block[h] = nextFreeBitBlock[0]
                        self.__writeInDisk(pathdsk, self.superBlock.bm_block_start + nextFreeBitBlock[0], b'1')
                        self.__writeInDisk(pathdsk, self.superBlock.block_start + nextFreeBitBlock[0] * BlockFile.sizeOf(), newBlock.encode())
                        self.superBlock.first_blo = self.__findNextFreeBlock(1)[0]
                        self.superBlock.free_blocks_count -= 1
                        self.__writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        break
            inode.size = newSizeInode
            self.__writeInDisk(pathdsk, self.superBlock.inode_start + i * InodesTable.sizeOf(), inode.encode())

    def __writeFileInBlockFolder(self, i, path: List[str], pathdsk, content: str, partstart: int):
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        self.blocks.append([i, blockFolder])
        for p in range(len(blockFolder.content)):
            if not blockFolder.content[p].name.strip() in ['.', '..'] and blockFolder.content[p].inodo != -1 and blockFolder.content[p].name.strip() == path[0]:
                path.pop(0)
                self.__writeGrpFileInInodes(blockFolder.content[p].inodo, path, pathdsk, content, partstart)

    def __writeFileInBlockFile(self, i) -> Tuple[int, BlockFile]:
        self.file.seek(self.superBlock.block_start + i * BlockFile.sizeOf())
        blockFile: BlockFile = BlockFile.decode(self.file.read(BlockFile.sizeOf()))
        return i, blockFile

    def __findNextFreeInode(self, count: int):
        self.file.seek(self.superBlock.bm_block_start)
        bm_block = self.file.read(self.superBlock.blocks_count).decode('utf-8')
        freeBlocks = []
        for i in range(len(bm_block)):
            if len(freeBlocks) == count:
                break
            if bm_block[i] == '0':
                freeBlocks.append(i)
        return freeBlocks

    def __findNextFreeBlock(self, count: int):
        self.file.seek(self.superBlock.bm_block_start)
        bm_block = self.file.read(self.superBlock.blocks_count).decode('utf-8')
        freeBlocks = []
        for i in range(len(bm_block)):
            if len(freeBlocks) == count:
                break
            if bm_block[i] == '0':
                freeBlocks.append(i)
        return freeBlocks

# =========================================USERS AND GROUPS===============================================

    def getUsers(self, content) -> List[User]:
        users: list[User] = []
        registers = [[j.strip() for j in i.split(',')] for i in content.split('\n') if i.strip() != '']
        for reg in registers:
            if reg[1] == 'U' and reg[0] != '0':
                users.append(User(reg[0], reg[2], reg[3], reg[4]))
        return users

    def getGroups(self, content) -> List[Group]:
        users: list[Group] = []
        registers = [[j.strip() for j in i.split(',')] for i in content.split('\n') if i.strip() != '']
        for reg in registers:
            if reg[1] == 'G' and reg[0] != '0':
                users.append(Group(reg[0], reg[2]))
        return users

# ==========================================WRITE IN DISK=================================================

    def __writeInDisk(self, path: str, seek: int, content: bytes):
        with open(path, 'r+b') as file:
            file.seek(seek)
            file.write(content)