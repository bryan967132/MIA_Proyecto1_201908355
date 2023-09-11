from typing import List
import datetime

class Journal:
    def __init__(self, type: str = None, name: str = None, content: str = None, date: datetime = None):
        self.type: str = type         #   8 bytes
        self.name: str = name         #  40 bytes
        self.content: str = content   # 100 bytes
        self.date: datetime = date    #   4 bytes

    def encode(self):
        result_b = self.type.encode('utf-8') if self.type else b'\x00' * 8
        result_b += self.name.encode('utf-8') if self.name else b'\x00' * 40
        result_b += self.content.encode('utf-8') + (100 - len(self.content)) * b'\x00' if self.content else b'\x00' * 100
        result_b += int(self.date.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.date else b'\x00' * 4
        return result_b

    def decode(data):
        type = data[:8].decode('utf-8')
        name = data[8:48].decode('utf-8')
        content = data[48:148].decode('utf-8')
        date = datetime.datetime.fromtimestamp(int.from_bytes(data[148:], byteorder='big', signed=True)) if data[148:] != b'\x00' * 4 else None
        return Journal(type, name, content, date)

    def sizeOf():
        return len(Journal().encode())