from typing import List
import datetime

class Journal:
    def __init__(self, operation: str = None, path: str = None, content: str = None, date: datetime = None):
        self.operation: str = operation         #   8 bytes
        self.path: str = path         #  40 bytes
        self.content: str = content   # 100 bytes
        self.date: datetime = date    #   4 bytes

    def encode(self):
        result_b = self.operation.encode('utf-8') + (8 - len(self.operation)) * b'\x00' if self.operation else b'\x00' * 8
        result_b += self.path.encode('utf-8') + (40 - len(self.path)) * b'\x00' if self.path else b'\x00' * 40
        result_b += self.content.encode('utf-8') + (100 - len(self.content)) * b'\x00' if self.content else b'\x00' * 100
        result_b += int(self.date.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.date else b'\x00' * 4
        return result_b

    def decode(data: bytes):
        type = ''
        for i in data[:8]:
            if i != 0:
                type += chr(i)
        name = ''
        for i in data[8:48]:
            if i != 0:
                name += chr(i)
        content = ''
        for i in data[48:148]:
            if i != 0:
                content += chr(i)
        date = datetime.datetime.fromtimestamp(int.from_bytes(data[148:], byteorder='big', signed=True)) if data[148:] != b'\x00' * 4 else None
        return Journal(type, name, content, date)

    def getSize(self):
        return len(self.encode())

    def sizeOf():
        return len(Journal().encode())

    def getDot(self) -> str:
        content = ''.join(self.content).replace('\n', '\\n').replace('\"', '\\\"').replace('\'', '\\\'')
        return f'\n\t\t<TR><TD>{self.operation.strip()}</TD><TD>{self.path}</TD><TD>{content}</TD><TD>{self.date.date()}</TD></TR>'

    def __str__(self) -> str:
        return f'{self.operation} - {self.path} - {self.content} - {self.date}'