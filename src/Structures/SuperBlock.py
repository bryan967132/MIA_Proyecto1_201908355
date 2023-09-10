import datetime

class SuperBlock:
    def __init__(self,
        filesystem_type: int = -1,
        inodes_count: int = -1,
        blocks_count: int = -1,
        free_blocks_count: int = -1,
        free_inodes_count: int = -1,
        mtime: datetime = None,
        umtime: datetime = None,
        mnt_count: int = -1,
        magic: int = 0xEF53,
        inode_s: int = -1,
        block_s: int = -1,
        first_ino: int = -1,
        first_blo: int = -1,
        bm_inode_start: int = -1,
        bm_block_start: int = -1,
        inode_start: int = -1,
        block_start: int = -1
    ):
        self.filesystem_type: int = filesystem_type
        self.inodes_count: int = inodes_count
        self.blocks_count: int = blocks_count
        self.free_blocks_count: int = free_blocks_count
        self.free_inodes_count: int = free_inodes_count
        self.mtime: datetime = mtime
        self.umtime: datetime = umtime
        self.mnt_count: int = mnt_count
        self.magic: int = magic
        self.inode_s: int = inode_s
        self.block_s: int = block_s
        self.first_ino: int = first_ino
        self.first_blo: int = first_blo
        self.bm_inode_start: int = bm_inode_start
        self.bm_block_start: int = bm_block_start
        self.inode_start: int = inode_start
        self.block_start: int = block_start

    def encode(self) -> bytes:
        result_b = self.filesystem_type.to_bytes(4, byteorder='big', signed=True)
        result_b += self.inodes_count.to_bytes(4, byteorder='big', signed=True)
        result_b += self.blocks_count.to_bytes(4, byteorder='big', signed=True)
        result_b += self.free_blocks_count.to_bytes(4, byteorder='big', signed=True)
        result_b += self.free_inodes_count.to_bytes(4, byteorder='big', signed=True)
        result_b += int(self.mtime.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.mtime else b'\x00' * 4
        result_b += int(self.umtime.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.umtime else b'\x00' * 4
        result_b += self.mnt_count.to_bytes(4, byteorder='big', signed=True)
        result_b += self.magic.to_bytes(4, byteorder='big', signed=True)
        result_b += self.inode_s.to_bytes(4, byteorder='big', signed=True)
        result_b += self.block_s.to_bytes(4, byteorder='big', signed=True)
        result_b += self.first_ino.to_bytes(4, byteorder='big', signed=True)
        result_b += self.first_blo.to_bytes(4, byteorder='big', signed=True)
        result_b += self.bm_inode_start.to_bytes(4, byteorder='big', signed=True)
        result_b += self.bm_block_start.to_bytes(4, byteorder='big', signed=True)
        result_b += self.inode_start.to_bytes(4, byteorder='big', signed=True)
        result_b += self.block_start.to_bytes(4, byteorder='big', signed=True)
        return result_b

    def decode(data):
        filesystem_type: int = int.from_bytes(data[:4], byteorder='big', signed=True)
        inodes_count: int = int.from_bytes(data[4:8], byteorder='big', signed=True)
        blocks_count: int = int.from_bytes(data[8:12], byteorder='big', signed=True)
        free_blocks_count: int = int.from_bytes(data[12:16], byteorder='big', signed=True)
        free_inodes_count: int = int.from_bytes(data[16:20], byteorder='big', signed=True)
        mtime: datetime = datetime.datetime.fromtimestamp(int.from_bytes(data[20:24], byteorder='big', signed=True)) if data[20:24] != b'\x00' * 4 else None
        umtime: datetime = datetime.datetime.fromtimestamp(int.from_bytes(data[24:28], byteorder='big', signed=True)) if data[24:28] != b'\x00' * 4 else None
        mnt_count: int = int.from_bytes(data[28:32], byteorder='big', signed=True)
        magic: int = int.from_bytes(data[32:36], byteorder='big', signed=True)
        inode_s: int = int.from_bytes(data[36:40], byteorder='big', signed=True)
        block_s: int = int.from_bytes(data[40:44], byteorder='big', signed=True)
        first_ino: int = int.from_bytes(data[44:48], byteorder='big', signed=True)
        first_blo: int = int.from_bytes(data[48:52], byteorder='big', signed=True)
        bm_inode_start: int = int.from_bytes(data[52:56], byteorder='big', signed=True)
        bm_block_start: int = int.from_bytes(data[56:60], byteorder='big', signed=True)
        inode_start: int = int.from_bytes(data[60:64], byteorder='big', signed=True)
        block_start: int = int.from_bytes(data[64:], byteorder='big', signed=True)
        return SuperBlock(
            filesystem_type,
            inodes_count,
            blocks_count,
            free_blocks_count,
            free_inodes_count,
            mtime,
            umtime,
            mnt_count,
            magic,
            inode_s,
            block_s,
            first_ino,
            first_blo,
            bm_inode_start,
            bm_block_start,
            inode_start,
            block_start
        )

    def sizeOf():
        return len(SuperBlock().encode())

    def __str__(self) -> str:
        return f'''filsystem_type: {self.filesystem_type}
inodes_count: {self.inodes_count}
blocks_count: {self.blocks_count}
free_blocks_count: {self.free_blocks_count}
free_inodes_count: {self.free_inodes_count}
mtime: {self.mtime}
umtime: {self.umtime}
mnt_count: {self.mnt_count}
magic: {self.magic}
inode_s: {self.inode_s}
block_s: {self.block_s}
first_ino: {self.first_ino}
first_blo: {self.first_blo}
bm_inode_start: {self.bm_inode_start}
bm_block_start: {self.bm_block_start}
inode_start: {self.inode_start}
block_start: {self.block_start}
'''