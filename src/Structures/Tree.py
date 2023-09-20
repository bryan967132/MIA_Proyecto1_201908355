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
                        dot += '\n\t' + self.__getDotBlockFolder(blockPointers.pointers[p])
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
                if p < 12:
                    if inode.type == '0':
                        self.__searchInBlockFolder(inode.block[p])
                    else:
                        self.__searchInBlockFile(inode.block[p])
                elif p == 12:
                    self.__searchInBlockPointers(inode.block[p], inode.type, 1)
                elif p == 13:
                    self.__searchInBlockPointers(inode.block[p], inode.type, 2)
                elif p == 14:
                    self.__searchInBlockPointers(inode.block[p], inode.type, 3)

    def __searchInBlockPointers(self, i, inodeType, simplicity):
        self.file.seek(self.superBlock.block_start + i * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        self.blocks.append([i, blockPointers])
        for p in range(len(blockPointers.pointers)):
            if blockPointers.pointers[p] != -1:
                if simplicity == 1:
                    if inodeType == '0':
                        self.__searchInBlockFolder(blockPointers.pointers[p])
                    else:
                        self.__searchInBlockFile(blockPointers.pointers[p])
                else:
                    self.__searchInBlockPointers(blockPointers.pointers[p], inodeType, simplicity - 1)

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
        try:
            dir = [i for i in path.split('/') if i != '']
            return self.__readFileInInodes(0, dir)
        except:
            return '', True

    def __readFileInInodes(self, i, path: List[str]) -> Tuple[str, bool]:
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        content = ''
        founded = False
        if inode.type == '0':
            for p in range(len(inode.block)):
                if inode.block[p] != -1:
                    if p < 12:
                        content, founded = self.__readFileInBlockFolder(inode.block[p], path)
                        if founded:
                            return content, founded
                    elif p == 12:
                        content, founded = self.__readFileInBlockPointers(inode.block[p], path, inode.type, 1)
                    elif p == 13:
                        content, founded = self.__readFileInBlockPointers(inode.block[p], path, inode.type, 2)
                    elif p == 14:
                        content, founded = self.__readFileInBlockPointers(inode.block[p], path, inode.type, 3)
        else:
            for p in range(len(inode.block)):
                if inode.block[p] != -1:
                    if p < 12:
                        cont, founded = self.__readFileInBlockFile(inode.block[p])
                        content += cont
                    elif p == 12:
                        cont, founded = self.__readFileInBlockPointers(inode.block[p], path, inode.type, 1)
                        content += cont
                    elif p == 13:
                        cont, founded = self.__readFileInBlockPointers(inode.block[p], path, inode.type, 2)
                        content += cont
                    elif p == 14:
                        cont, founded = self.__readFileInBlockPointers(inode.block[p], path, inode.type, 3)
                        content += cont
        return content, founded

    def __readFileInBlockPointers(self, i, path: List[str], inodeType, simplicity) -> Tuple[str, bool]:
        self.file.seek(self.superBlock.block_start + i * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        content = ''
        founded = False
        for p in range(len(blockPointers.pointers)):
            if blockPointers.pointers[p] != -1:
                if simplicity == 1:
                    if inodeType == '0':
                        content, founded = self.__readFileInBlockFolder(blockPointers.pointers[p], path)
                        if founded:
                            return content, founded
                    else:
                        cont, founded = self.__readFileInBlockFile(blockPointers.pointers[p])
                        content += cont
                else:
                    if inodeType == '0':
                        content, founded = self.__readFileInBlockPointers(blockPointers.pointers[p], path, inodeType, simplicity - 1)
                    else:
                        cont, founded = self.__readFileInBlockPointers(blockPointers.pointers[p], path, inodeType, simplicity - 1)
                        content += cont
        return content, founded

    def __readFileInBlockFolder(self, i, path: List[str]) -> Tuple[str, bool]:
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
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
        self.__writeFileInInodes(0, dir, diskpath, newContent, partstart)
        self.superBlock.first_blo = self.__findNextFreeBlock(1)[0]
        self.superBlock.first_ino = self.__findNextFreeInode(1)[0]

    def __writeFileInInodes(self, i: int, path: List[str], pathdsk, newContent: str, partstart: int):
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        if inode.type == '0':
            for p in range(len(inode.block)):
                if inode.block[p] != -1:
                    if p < 12:
                        writed = self.__writeFileInBlockFolder(inode.block[p], path, pathdsk, newContent, partstart)
                        if writed:
                            return
                    elif p == 12:
                        pass
                    elif p == 14:
                        pass
        else:
            blocksFile: Tuple[int, BlockFile] = -1, None
            for p in range(len(inode.block)):
                if inode.block[p] != -1:
                    if p < 12:
                        blocksFile = self.__writeFileInBlockFile(inode.block[p])
                    elif p == 12:
                        blocksFile = self.__writeFileInBlockPointers3(pathdsk, inode.block[p], 1)
                    elif p == 13:
                        blocksFile = self.__writeFileInBlockPointers3(pathdsk, inode.block[p], 2)
                    elif p == 14:
                        blocksFile = self.__writeFileInBlockPointers3(pathdsk, inode.block[p], 3)
            num, block = blocksFile
            if not block:
                block = BlockFile(['' for i in range(64)])
                num = self.__findNextFreeBlock(1)[0]
                self.__writeNewBlock(pathdsk, num, block)
                inode.block[0] = num
                self.__rewriteInode(pathdsk, i, inode)
            contents = [[r for r in block.content if r != '']]
            for z in newContent:
                if len(contents[-1]) < 64:
                    contents[-1].append(z)
                else:
                    contents.append([z])
            block.content = contents.pop(0)
            self.writeInDisk(pathdsk, self.superBlock.block_start + num * BlockFile.sizeOf(), block.encode())
            newSizeInode = (num - 1) * 64 + len(block.content)
            while len(contents) > 0:
                newBlock: BlockFile = BlockFile(['' for i in range(64)])
                contenew = contents.pop(0)
                newSizeInode = (num - 1) * 64 + len(contenew)
                if len(newBlock.content) == len(contenew):
                    newBlock.content = contenew
                else:
                    for z in range(len(contenew)):
                        newBlock.content[z] = contenew[z]
                nextFreeBitBlock = self.__findNextFreeBlock(1)
                for h in range(len(inode.block)):
                    if inode.block[h] == -1:
                        if h < 12:
                            inode.block[h] = nextFreeBitBlock[0]
                            self.writeInDisk(pathdsk, self.superBlock.bm_block_start + nextFreeBitBlock[0], b'1')
                            self.writeInDisk(pathdsk, self.superBlock.block_start + nextFreeBitBlock[0] * BlockFile.sizeOf(), newBlock.encode())
                            self.superBlock.first_blo = self.__findNextFreeBlock(1)[0]
                            self.superBlock.free_blocks_count -= 1
                            self.writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        elif h == 12:
                            inode.block[h] = nextFreeBitBlock[0]
                            self.__writeFileInBlockPointers(pathdsk, newBlock, nextFreeBitBlock[0], 1)
                            self.superBlock.free_blocks_count -= 1
                            self.writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        elif h == 13:
                            inode.block[h] = nextFreeBitBlock[0]
                            self.__writeFileInBlockPointers(pathdsk, newBlock, nextFreeBitBlock[0], 2)
                            self.superBlock.free_blocks_count -= 1
                            self.writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        elif h == 14:
                            inode.block[h] = nextFreeBitBlock[0]
                            self.__writeFileInBlockPointers(pathdsk, newBlock, nextFreeBitBlock[0], 3)
                            self.superBlock.free_blocks_count -= 1
                            self.writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        break
                    elif h == 12 and inode.block[h] != -1 and self.__validateSpacePointers(inode.block[h], 1):
                        self.__writeFileInBlockPointers(pathdsk, newBlock, inode.block[h], 1)
                        self.superBlock.free_blocks_count -= 1
                        self.writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        break
                    elif h == 13 and inode.block[h] != -1 and self.__validateSpacePointers(inode.block[h], 2):
                        posiblePointer = self.__searchPointer(inode.block[h], 2)
                        if posiblePointer[0] != -1:
                            self.__writeNewBlockInIndirect(pathdsk, posiblePointer[0], newBlock, posiblePointer[1])
                            break
                        self.__writeFileInBlockPointers(pathdsk, newBlock, inode.block[h], 2)
                        self.superBlock.free_blocks_count -= 1
                        self.writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        break
                    elif h == 14 and inode.block[h] != -1 and self.__validateSpacePointers(inode.block[h], 3):
                        posiblePointer = self.__searchPointer(inode.block[h], 3)
                        if posiblePointer[0] != -1:
                            self.__writeNewBlockInIndirect(pathdsk, posiblePointer[0], newBlock, posiblePointer[1])
                            break
                        posiblePointer = self.__searchPointer(inode.block[h], 2)
                        if posiblePointer[0] != -1:
                            self.__writeNewBlockInIndirect(pathdsk, posiblePointer[0], BlockPointers([-1 for i in range(16)]), posiblePointer[1])
                            posiblePointer = self.__searchPointer(inode.block[h], 3)
                            self.__writeNewBlockInIndirect(pathdsk, posiblePointer[0], newBlock, posiblePointer[1])
                            break
                        self.__writeFileInBlockPointers(pathdsk, newBlock, inode.block[h], 3)
                        self.superBlock.free_blocks_count -= 1
                        self.writeInDisk(pathdsk, partstart, self.superBlock.encode())
                        break
            inode.size = newSizeInode
            self.writeInDisk(pathdsk, self.superBlock.inode_start + i * InodesTable.sizeOf(), inode.encode())

    def __validateSpacePointers(self, numBlock, simplicity) -> bool:
        self.file.seek(self.superBlock.block_start + numBlock * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        resultado = False
        for i in range(len(blockPointers.pointers)):
            if simplicity == 1:
                if blockPointers.pointers[i] == -1:
                    return True
            else:
                if blockPointers.pointers[i] != -1:
                    resultado = self.__validateSpacePointers(blockPointers.pointers[i], simplicity - 1)
                else:
                    return True
        return resultado

    def __writeFileInBlockPointers(self, pathdsk, newBlockFile: BlockFile, nextFreeBitBlock: int, simplicity: int, ):
        with open(pathdsk, 'rb') as file:
            file.seek(self.superBlock.block_start + nextFreeBitBlock * BlockPointers.sizeOf())
            readed_bytes = file.read(BlockPointers.sizeOf())
            if readed_bytes != b'\x00' * BlockPointers.sizeOf():
                self.__writeFileInBlockPointers2(pathdsk, newBlockFile, nextFreeBitBlock, simplicity, )
            else:
                blockPointers: BlockPointers = BlockPointers([-1 for i in range(16)])
                self.writeInDisk(pathdsk, self.superBlock.bm_block_start + nextFreeBitBlock, b'1')
                self.writeInDisk(pathdsk, self.superBlock.block_start + nextFreeBitBlock * BlockPointers.sizeOf(), blockPointers.encode())
                self.superBlock.free_blocks_count -= 1
                self.__writeFileInBlockPointers2(pathdsk, newBlockFile, nextFreeBitBlock, simplicity, )

    def __writeFileInBlockPointers2(self, pathdsk, newBlockFile: BlockFile, nextFreeBitBlock: int, simplicity: int, ):
        with open(pathdsk, 'rb') as file:
            file.seek(self.superBlock.block_start + nextFreeBitBlock * BlockPointers.sizeOf())
            blockPointers: BlockPointers = BlockPointers.decode(file.read(BlockPointers.sizeOf()))
            newNextBit = self.__findNextFreeBlock(1)[0]
            for p in range(len(blockPointers.pointers)):
                if blockPointers.pointers[p] == -1:
                    if simplicity == 1:
                        blockPointers.pointers[p] = newNextBit
                        self.writeInDisk(pathdsk, self.superBlock.block_start + nextFreeBitBlock * BlockPointers.sizeOf(), blockPointers.encode())
                        self.writeInDisk(pathdsk, self.superBlock.block_start + newNextBit * BlockFile.sizeOf(), newBlockFile.encode())
                        self.writeInDisk(pathdsk, self.superBlock.bm_block_start + newNextBit, b'1')
                        self.superBlock.free_blocks_count -= 1
                        return
                    else:
                        blockPointers.pointers[p] = newNextBit
                        self.writeInDisk(pathdsk, self.superBlock.block_start + nextFreeBitBlock * BlockPointers.sizeOf(), blockPointers.encode())
                        self.__writeFileInBlockPointers(pathdsk, newBlockFile, self.__findNextFreeBlock(1)[0], simplicity - 1)
                        return

    def __writeNewBlockInIndirect(self, pathdsk, numBlock, newBlockFile, numPtr):
        self.file.seek(self.superBlock.block_start + numBlock * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        nextBitBlock = self.__findNextFreeBlock(1)[0]
        blockPointers.pointers[numPtr] = nextBitBlock
        self.superBlock.free_blocks_count -= 1
        self.superBlock.first_blo = nextBitBlock
        self.writeInDisk(pathdsk, self.superBlock.block_start + numBlock * BlockPointers.sizeOf(), blockPointers.encode())
        self.writeInDisk(pathdsk, self.superBlock.block_start + nextBitBlock * BlockFile.sizeOf(), newBlockFile.encode())
        self.writeInDisk(pathdsk, self.superBlock.bm_block_start + nextBitBlock, b'1')


    def __searchPointer(self, numBlock, simplicity) -> List[int]:
        self.file.seek(self.superBlock.block_start + numBlock * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        resultado = [-1, -1]
        for i in range(len(blockPointers.pointers)):
            if simplicity == 1:
                if blockPointers.pointers[i] == -1:
                    return [numBlock, i]
            else:
                if blockPointers.pointers[i] != -1:
                    resultado = self.__searchPointer(blockPointers.pointers[i], simplicity - 1)
        return resultado

    def __writeFileInBlockPointers3(self, pathdsk, i: int, simplicity: int) -> Tuple[int, BlockFile]:
        self.file.seek(self.superBlock.block_start + i * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        num: int = -1
        blockFile: BlockFile = None
        for i in range(len(blockPointers.pointers)):
            if blockPointers.pointers[i] != -1:
                if simplicity == 1:
                    num, blockFile = self.__writeFileInBlockFile(blockPointers.pointers[i])
                else:
                    num, blockFile = self.__writeFileInBlockPointers3(pathdsk, blockPointers.pointers[i], simplicity - 1)
        return num, blockFile

    def __writeFileInBlockFolder(self, i, path: List[str], pathdsk, content: str, partstart: int):
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        for p in range(len(blockFolder.content)):
            if not blockFolder.content[p].name.strip() in ['.', '..'] and blockFolder.content[p].inodo != -1 and blockFolder.content[p].name.strip() == path[0]:
                path.pop(0)
                self.__writeFileInInodes(blockFolder.content[p].inodo, path, pathdsk, content, partstart)
                return True

    def __writeFileInBlockFile(self, i) -> Tuple[int, BlockFile]:
        self.file.seek(self.superBlock.block_start + i * BlockFile.sizeOf())
        blockFile: BlockFile = BlockFile.decode(self.file.read(BlockFile.sizeOf()))
        return i, blockFile

# =========================================== MKDIR AND MKFILE =============================================

    def mkdir(self, path: str, diskpath: str):
        dir = [i for i in path.split('/') if i != '']
        self.current = 0
        self.prev = 0
        self.dir = True
        result = self.__mkdirInInode(0, dir, diskpath)
        self.superBlock.first_blo = self.__findNextFreeBlock(1)[0]
        self.superBlock.first_ino = self.__findNextFreeInode(1)[0]
        return result

    def mkfile(self, path: str, diskpath: str):
        dir = [i for i in path.split('/') if i != '']
        self.current = 0
        self.prev = 0
        self.dir = False
        result = self.__mkdirInInode(0, dir, diskpath)
        self.superBlock.first_blo = self.__findNextFreeBlock(1)[0]
        self.superBlock.first_ino = self.__findNextFreeInode(1)[0]
        return result

    def __mkdirInInode(self, i: int, path: list[str], pathdsk: str):
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        self.prev = self.current
        self.current = i
        for p in range(len(inode.block)):
            if p < 12:
                if inode.block[p] != -1:
                    mkdirBlockFolder = self.__mkdirInBlockFolder(inode.block[p], path, pathdsk)
                    if mkdirBlockFolder:
                        return mkdirBlockFolder
                else:
                    inode.block[p] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteInode(pathdsk, i, inode)
                    newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                    self.__writeNewBlock(pathdsk, inode.block[p], newBlockFolder)
                    return self.__mkdirInBlockFolder(inode.block[p], path, pathdsk)
            elif p == 12:
                if inode.block[p] != -1:
                    copyPath = [i for i in path]
                    posiblePtr = self.__searchPointerFolder(inode.block[p], 1, copyPath)
                    if posiblePtr[0] != -1:
                        match posiblePtr[2]:
                            case 'BLOCKFOLDER':
                                return self.__mkdirInBlockFolder(posiblePtr[0], path[-1:], pathdsk)
                            case 'INODE':
                                return self.__mkdirInInode(posiblePtr[0], path[-1:], pathdsk)
                            case 'BLOCKPOINTERS':
                                self.file.seek(self.superBlock.block_start + posiblePtr[0] * BlockPointers.sizeOf())
                                blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
                                blockPointers.pointers[posiblePtr[1]] = self.__findNextFreeBlock(1)[0]
                                self.__rewriteBlock(pathdsk, posiblePtr[0], blockPointers)

                                newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                                self.__writeNewBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockFolder)
                                return self.__mkdirInBlockFolder(blockPointers.pointers[posiblePtr[1]], path[-1:], pathdsk)
                    continue
                else:
                    inode.block[p] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteInode(pathdsk, i, inode)

                    newBlockPointers: BlockPointers = BlockPointers([-1 for i in range(16)])
                    self.__writeNewBlock(pathdsk, inode.block[p], newBlockPointers)
                    newBlockPointers.pointers[0] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteBlock(pathdsk, inode.block[p], newBlockPointers)

                    newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                    self.__writeNewBlock(pathdsk, newBlockPointers.pointers[0], newBlockFolder)

                    return self.__mkdirInBlockFolder(newBlockPointers.pointers[0], path, pathdsk)
            elif p == 13:
                if inode.block[p] != -1:
                    copyPath = [i for i in path]
                    posiblePtr = self.__searchPointerFolder(inode.block[p], 2, copyPath)
                    if posiblePtr[0] != -1:
                        match posiblePtr[2]:
                            case 'BLOCKFOLDER':
                                return self.__mkdirInBlockFolder(posiblePtr[0], path[-1:], pathdsk)
                            case 'INODE':
                                return self.__mkdirInInode(posiblePtr[0], path[-1:], pathdsk)
                            case 'BLOCKPOINTERS':
                                match posiblePtr[3]:
                                    case 1:
                                        self.file.seek(self.superBlock.block_start + posiblePtr[0] * BlockPointers.sizeOf())
                                        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
                                        blockPointers.pointers[posiblePtr[1]] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, posiblePtr[0], blockPointers)

                                        newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                                        self.__writeNewBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockFolder)
                                        return self.__mkdirInBlockFolder(blockPointers.pointers[posiblePtr[1]], path[-1:], pathdsk)
                                    case 2:
                                        self.file.seek(self.superBlock.block_start + posiblePtr[0] * BlockPointers.sizeOf())
                                        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
                                        blockPointers.pointers[posiblePtr[1]] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, posiblePtr[0], blockPointers)

                                        newBlockPointers: BlockPointers = BlockPointers([-1 for i in range(16)])
                                        self.__writeNewBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockPointers)
                                        newBlockPointers.pointers[0] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockPointers)

                                        newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                                        self.__writeNewBlock(pathdsk, newBlockPointers.pointers[0], newBlockFolder)
                                        return self.__mkdirInBlockFolder(newBlockPointers.pointers[0], path[-1:], pathdsk)
                    continue
                else:
                    inode.block[p] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteInode(pathdsk, i, inode)

                    newBlockPointers1: BlockPointers = BlockPointers([-1 for i in range(16)])
                    self.__writeNewBlock(pathdsk, inode.block[p], newBlockPointers1)
                    newBlockPointers1.pointers[0] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteBlock(pathdsk, inode.block[p], newBlockPointers1)

                    newBlockPointers2: BlockPointers = BlockPointers([-1 for i in range(16)])
                    self.__writeNewBlock(pathdsk, newBlockPointers1.pointers[0], newBlockPointers2)
                    newBlockPointers2.pointers[0] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteBlock(pathdsk, newBlockPointers1.pointers[0], newBlockPointers2)

                    newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                    self.__writeNewBlock(pathdsk, newBlockPointers2.pointers[0], newBlockFolder)

                    return self.__mkdirInBlockFolder(newBlockPointers2.pointers[0], path, pathdsk)
            elif p == 14:
                if inode.block[p] != -1:
                    copyPath = [i for i in path]
                    posiblePtr = self.__searchPointerFolder(inode.block[p], 3, copyPath)
                    if posiblePtr[0] != -1:
                        match posiblePtr[2]:
                            case 'BLOCKFOLDER':
                                return self.__mkdirInBlockFolder(posiblePtr[0], path[-1:], pathdsk)
                            case 'INODE':
                                return self.__mkdirInInode(posiblePtr[0], path[-1:], pathdsk)
                            case 'BLOCKPOINTERS':
                                match posiblePtr[3]:
                                    case 1:
                                        self.file.seek(self.superBlock.block_start + posiblePtr[0] * BlockPointers.sizeOf())
                                        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
                                        blockPointers.pointers[posiblePtr[1]] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, posiblePtr[0], blockPointers)

                                        newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                                        self.__writeNewBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockFolder)
                                        return self.__mkdirInBlockFolder(blockPointers.pointers[posiblePtr[1]], path[-1:], pathdsk)
                                    case 2:
                                        self.file.seek(self.superBlock.block_start + posiblePtr[0] * BlockPointers.sizeOf())
                                        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
                                        blockPointers.pointers[posiblePtr[1]] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, posiblePtr[0], blockPointers)

                                        newBlockPointers: BlockPointers = BlockPointers([-1 for i in range(16)])
                                        self.__writeNewBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockPointers)
                                        newBlockPointers.pointers[0] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockPointers)

                                        newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                                        self.__writeNewBlock(pathdsk, newBlockPointers.pointers[0], newBlockFolder)
                                        return self.__mkdirInBlockFolder(newBlockPointers.pointers[0], path[-1:], pathdsk)
                                    case 3:
                                        self.file.seek(self.superBlock.block_start + posiblePtr[0] * BlockPointers.sizeOf())
                                        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
                                        blockPointers.pointers[posiblePtr[1]] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, posiblePtr[0], blockPointers)

                                        newBlockPointers1: BlockPointers = BlockPointers([-1 for i in range(16)])
                                        self.__writeNewBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockPointers1)
                                        newBlockPointers1.pointers[0] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, blockPointers.pointers[posiblePtr[1]], newBlockPointers1)

                                        newBlockPointers2: BlockPointers = BlockPointers([-1 for i in range(16)])
                                        self.__writeNewBlock(pathdsk, newBlockPointers1.pointers[0], newBlockPointers2)
                                        newBlockPointers2.pointers[0] = self.__findNextFreeBlock(1)[0]
                                        self.__rewriteBlock(pathdsk, newBlockPointers1.pointers[0], newBlockPointers2)

                                        newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                                        self.__writeNewBlock(pathdsk, newBlockPointers2.pointers[0], newBlockFolder)
                                        return self.__mkdirInBlockFolder(newBlockPointers2.pointers[0], path[-1:], pathdsk)
                    continue
                else:
                    inode.block[p] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteInode(pathdsk, i, inode)

                    newBlockPointers1: BlockPointers = BlockPointers([-1 for i in range(16)])
                    self.__writeNewBlock(pathdsk, inode.block[p], newBlockPointers1)
                    newBlockPointers1.pointers[0] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteBlock(pathdsk, inode.block[p], newBlockPointers1)

                    newBlockPointers2: BlockPointers = BlockPointers([-1 for i in range(16)])
                    self.__writeNewBlock(pathdsk, newBlockPointers1.pointers[0], newBlockPointers2)
                    newBlockPointers2.pointers[0] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteBlock(pathdsk, newBlockPointers1.pointers[0], newBlockPointers2)

                    newBlockPointers3: BlockPointers = BlockPointers([-1 for i in range(16)])
                    self.__writeNewBlock(pathdsk, newBlockPointers2.pointers[0], newBlockPointers3)
                    newBlockPointers3.pointers[0] = self.__findNextFreeBlock(1)[0]
                    self.__rewriteBlock(pathdsk, newBlockPointers2.pointers[0], newBlockPointers3)

                    newBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                    self.__writeNewBlock(pathdsk, newBlockPointers3.pointers[0], newBlockFolder)

                    return self.__mkdirInBlockFolder(newBlockPointers3.pointers[0], path, pathdsk)

    def __mkdirInBlockFolder(self, i, path: list[str], pathdsk: str) -> bool:
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        if len(path) > 1:
            for p in range(len(blockFolder.content)):
                if blockFolder.content[p].inodo != -1 and blockFolder.content[p].name.strip() == path[0]:
                    path.pop(0)
                    return self.__mkdirInInode(blockFolder.content[p].inodo, path, pathdsk)
        else:
            for p in range(len(blockFolder.content)):
                if blockFolder.content[p].inodo == -1:
                    blockFolder.content[p].name = path[0].ljust(12)
                    blockFolder.content[p].inodo = self.__findNextFreeInode(1)[0]
                    self.__rewriteBlock(pathdsk, i, blockFolder)

                    if self.dir:
                        newInode: InodesTable = InodesTable()
                        newInode.block[0] = self.__findNextFreeBlock(1)[0]
                        self.__writeNewInode(pathdsk, blockFolder.content[p].inodo, newInode)

                        self.prev = self.current
                        self.current = blockFolder.content[p].inodo

                        firstBlockFolder: BlockFolder = BlockFolder([Content() for i in range(4)])
                        firstBlockFolder.content[0] = Content('.'.ljust(12), self.current)
                        firstBlockFolder.content[1] = Content('..'.ljust(12), self.prev)
                        self.__writeNewBlock(pathdsk, newInode.block[0], firstBlockFolder)
                    else:
                        newInode: InodesTable = InodesTable(type = '1', block = [-1 for i in range(15)])
                        self.__writeNewInode(pathdsk, blockFolder.content[p].inodo, newInode)
                    return True
        return False

    def __searchPointerInodeFolder(self, numInode, path):
        self.file.seek(self.superBlock.inode_start + numInode * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        result = [-1, -1, '', -1]
        for i in range(len(inode.block)):
            if inode.block[i] != -1:
                if i < 12:
                    result = self.__searchPointerBlockFolder(inode.block[i], path)
                    if result[0] != -1:
                        return result
                elif i == 12:
                    result = self.__searchPointerFolder(inode.block[i], 1, path)
                    if result[0] != -1:
                        return result
                elif i == 13:
                    result = self.__searchPointerFolder(inode.block[i], 2, path)
                    if result[0] != -1:
                        return result
                elif i == 14:
                    result = self.__searchPointerFolder(inode.block[i], 3, path)
                    if result[0] != -1:
                        return result
            else:
                return [numInode, i, 'INODE', -1]
        return result

    def __searchPointerFolder(self, numBlock, simplicity, path: list[str]) -> List[int]:
        self.file.seek(self.superBlock.block_start + numBlock * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        result = [-1, -1, '', -1]
        for i in range(len(blockPointers.pointers)):
            if simplicity == 1:
                if blockPointers.pointers[i] == -1:
                    return [numBlock, i, 'BLOCKPOINTERS', 1]
                else:
                    result = self.__searchPointerBlockFolder(blockPointers.pointers[i], path)
                    if result[0] != -1:
                        return result
            else:
                if blockPointers.pointers[i] == -1:
                    return [numBlock, i, 'BLOCKPOINTERS', simplicity]
                else:
                    result = self.__searchPointerFolder(blockPointers.pointers[i], simplicity - 1, path)
                    if result[0] != -1:
                        return result
        return result

    def __searchPointerBlockFolder(self, numBlock, path: list[str]) -> List[int]:
        self.file.seek(self.superBlock.block_start + numBlock * BlockFolder.sizeOf())
        blockPointers: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        resultado = [-1, -1, '', -1]
        if len(path) > 1:
            for i in range(len(blockPointers.content)):
                if blockPointers.content[i].inodo != -1 and blockPointers.content[i].name.strip() == path[0]:
                    path.pop(0)
                    return self.__searchPointerInodeFolder(blockPointers.content[i].inodo, path)
        else:
            for i in range(len(blockPointers.content)):
                if blockPointers.content[i].inodo == -1:
                    path.pop(0)
                    return [numBlock, i, 'BLOCKFOLDER', -1]
        return resultado

    def __writeNewBlock(self, pathdsk: str, numBlock: int, blockFolder: BlockFolder):
        self.writeInDisk(pathdsk, self.superBlock.block_start + numBlock * BlockFolder.sizeOf(), blockFolder.encode())
        self.writeInDisk(pathdsk, self.superBlock.bm_block_start + numBlock, b'1')
        self.superBlock.free_blocks_count -= 1

    def __writeNewInode(self, pathdsk: str, numInode: int, inode: InodesTable):
        self.writeInDisk(pathdsk, self.superBlock.inode_start + numInode * InodesTable.sizeOf(), inode.encode())
        self.writeInDisk(pathdsk, self.superBlock.bm_inode_start + numInode, b'1')
        self.superBlock.free_inodes_count -= 1

    def __rewriteBlock(self, pathdsk: str, numBlock: int, blockFolder: BlockFolder):
        self.writeInDisk(pathdsk, self.superBlock.block_start + numBlock * BlockFolder.sizeOf(), blockFolder.encode())

    def __rewriteInode(self, pathdsk: str, numInode: int, inode: InodesTable):
        self.writeInDisk(pathdsk, self.superBlock.inode_start + numInode * InodesTable.sizeOf(), inode.encode())

# =========================================== SEARCH DIRECTORY =============================================

    def searchdir(self, path: str):
        dir = [i for i in path.split('/') if i != '']
        return self.__searchdirInInode(0, dir)

    def __searchdirInInode(self, i: int, path: list[str]):
        self.file.seek(self.superBlock.inode_start + i * InodesTable.sizeOf())
        inode: InodesTable = InodesTable.decode(self.file.read(InodesTable.sizeOf()))
        result = False
        for p in range(len(inode.block)):
            if inode.block[p] != -1:
                if p < 12:
                    searchdirBlockFolder = self.__searchdirInBlockFolder(inode.block[p], path)
                    if searchdirBlockFolder:
                        return searchdirBlockFolder
                elif p == 12:
                    result = self.__searchdirInBlockPointers(inode.block[p], path, 1)
                elif p == 13:
                    result = self.__searchdirInBlockPointers(inode.block[p], path, 2)
                elif p == 14:
                    result = self.__searchdirInBlockPointers(inode.block[p], path, 3)
        return result

    def __searchdirInBlockPointers(self, i, path: list[str], simplicity: int) -> bool:
        self.file.seek(self.superBlock.block_start + i * BlockPointers.sizeOf())
        blockPointers: BlockPointers = BlockPointers.decode(self.file.read(BlockPointers.sizeOf()))
        founded = False
        for p in range(len(blockPointers.pointers)):
            if blockPointers.pointers[p] != -1:
                if simplicity == 1:
                    founded = self.__searchdirInBlockFolder(blockPointers.pointers[p], path)
                    if founded:
                        return founded
                else:
                    founded = self.__searchdirInBlockPointers(blockPointers.pointers[p], path, simplicity - 1)
        return founded

    def __searchdirInBlockFolder(self, i, path: list[str]) -> bool:
        self.file.seek(self.superBlock.block_start + i * BlockFolder.sizeOf())
        blockFolder: BlockFolder = BlockFolder.decode(self.file.read(BlockFolder.sizeOf()))
        if len(path) > 1:
            for p in range(len(blockFolder.content)):
                if blockFolder.content[p].inodo != -1 and blockFolder.content[p].name.strip() == path[0]:
                    path.pop(0)
                    return self.__searchdirInInode(blockFolder.content[p].inodo, path)
        else:
            for p in range(len(blockFolder.content)):
                if blockFolder.content[p].inodo != -1 and blockFolder.content[p].name.strip() == path[0]:
                    path.pop(0)
                    return True
        return False

# ========================================= FIND NEXT BIT =============================================

    def __findNextFreeInode(self, count: int):
        self.file.seek(self.superBlock.bm_inode_start)
        bm_inode = self.file.read(self.superBlock.inodes_count).decode('utf-8')
        freeBlocks = []
        for i in range(len(bm_inode)):
            if len(freeBlocks) == count:
                break
            if bm_inode[i] == '0':
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

# ========================================= USERS AND GROUPS ===============================================

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

# ========================================== WRITE IN DISK =================================================

    def writeInDisk(self, path: str, seek: int, content: bytes):
        with open(path, 'r+b') as file:
            file.seek(seek)
            file.write(content)