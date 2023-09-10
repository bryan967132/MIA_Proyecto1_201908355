from typing import List

class BlockPointers:
    def __init__(self, pointers: List[int] = [-1 for i in range(16)]):
        self.pointers: list[int] = pointers

    def encode(self):
        result_b = b''
        for i in self.pointers:
            result_b += i.to_bytes(4, byteorder='big', signed=True)
        return result_b

    def decode(data):
        pointers: list[int] = []
        for i in range(16):
            pointers.append(int.from_bytes(data[i * 4:4 + i * 4], byteorder='big', signed=True))
        return BlockPointers(pointers)

    def sizeOf():
        return len(BlockPointers().encode())

    def __str__(self) -> str:
        return f'pointers: {self.pointers}\n'