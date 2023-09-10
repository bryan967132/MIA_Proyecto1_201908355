import datetime
from typing import List

class InodesTable:
    def __init__(self,
        uid: int = 1,
        gid: int = 1,
        size: int = 0,
        atime: datetime = None,
        ctime: datetime = datetime.datetime.now(),
        mtime: datetime = None,
        block: List[int] = [-1 for i in range(15)],
        type: str = '0',
        perm: int = 664
    ):
        self.uid: int = uid
        self.gid: int = gid
        self.size: int = size
        self.atime: datetime = atime
        self.ctime: datetime = ctime
        self.mtime: datetime = mtime
        self.block: list[int] = block
        self.type: str = type
        self.perm: int = perm

    def encode(self) -> bytes:
        result_b = self.uid.to_bytes(4, byteorder='big', signed=True)
        result_b += self.gid.to_bytes(4, byteorder='big', signed=True)
        result_b += self.size.to_bytes(4, byteorder='big', signed=True)
        result_b += int(self.atime.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.atime else b'\x00' * 4
        result_b += int(self.ctime.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.ctime else b'\x00' * 4
        result_b += int(self.mtime.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.mtime else b'\x00' * 4
        for i in self.block:
            result_b += i.to_bytes(4, byteorder='big', signed=True)
        result_b += self.type.encode('utf-8')
        result_b += self.perm.to_bytes(4, byteorder='big', signed=True)
        return result_b

    def decode(data):
        uid: int = int.from_bytes(data[:4], byteorder='big', signed=True)
        gid: int = int.from_bytes(data[4:8], byteorder='big', signed=True)
        size: int = int.from_bytes(data[8:12], byteorder='big', signed=True)
        atime: datetime = datetime.datetime.fromtimestamp(int.from_bytes(data[12:16], byteorder='big', signed=True)) if data[12:16] != b'\x00' * 4 else None
        ctime: datetime = datetime.datetime.fromtimestamp(int.from_bytes(data[16:20], byteorder='big', signed=True)) if data[16:20] != b'\x00' * 4 else None
        mtime: datetime = datetime.datetime.fromtimestamp(int.from_bytes(data[20:24], byteorder='big', signed=True)) if data[20:24] != b'\x00' * 4 else None
        block: list[int] = []
        for i in range(15):
            block.append(int.from_bytes(data[24 + i * 4:28 + i * 4], byteorder='big', signed=True))
        type: str = data[84:85].decode('utf-8')
        perm: int = int.from_bytes(data[85:], byteorder='big', signed=True)
        return InodesTable(
            uid,
            gid,
            size,
            atime,
            ctime,
            mtime,
            block,
            type,
            perm
        )

    def sizeOf():
        return len(InodesTable().encode())

    def __str__(self) -> str:
        return f'''uid: {self.uid}
gid: {self.gid}
size: {self.size}
atime: {self.atime}
ctime: {self.ctime}
mtime: {self.mtime}
block: {self.block}
bype: {self.type}
perm: {self.perm}
'''