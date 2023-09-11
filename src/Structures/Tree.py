from Structures.SuperBlock import *
from Structures.SuperBlock import *
from Structures.InodesTable import *
from Structures.BlockFolder import *
from Structures.BlockFile import *
from Structures.BlockPointers import *
from Structures.Journaling import *
from io import BufferedRandom

class Tree:
    def __init__(self, superBlock: SuperBlock, file: BufferedRandom):
        self.superBlock: SuperBlock = superBlock
        self.file: BufferedRandom = file
        self.blocks = []

    def getDot(self) -> str:
        dot: str = 'digraph Tree{\n\tnode [shape=plaintext];\n\trankdir=LR;\n\t'
        dot += self.__getDotInode(0)
        dot += '\n}'
        return dot

    def __getDotInode(self, i) -> str:
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        dot = inode.getDot(i)
        for p in range(len(inode.block)):
            if inode.block[p] != -1:
                if inode.type == '0':
                    dot += '\n\t' + self.__getDotBlockFolder(inode.block[p])
                    dot += f'\n\tinode{i}:A{p} -> block{inode.block[p]}:B{inode.block[p]};'
                else:
                    dot += '\n\t' + self.__getDotBlockFile(inode.block[p])
                    dot += f'\n\tinode{i}:A{p} -> block{inode.block[p]}:B{inode.block[p]};'

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