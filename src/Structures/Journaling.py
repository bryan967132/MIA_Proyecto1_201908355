from typing import List
import datetime

class Record:
    def __init__(self, type: str = None, name: str = None, content: str = None, date: datetime = None):
        self.type: str = type         #  8 bytes
        self.name: str = name         # 12 bytes
        self.content: str = content   #  8 bytes
        self.date: datetime = date    #  4 bytes

    def encode(self):
        result_b = self.type.encode('utf-8') if self.type else b'\x00' * 8
        result_b += self.name.encode('utf-8') if self.name else b'\x00' * 12
        result_b += self.content.encode('utf-8') if self.content else b'\x00' * 8
        result_b += int(self.date.timestamp()).to_bytes(4, byteorder='big', signed=True) if self.date else b'\x00' * 4
        return result_b

    def decode(data):
        type = data[:8].decode('utf-8')
        name = data[8:20].decode('utf-8')
        content = data[20:28].decode('utf-8')
        date = datetime.datetime.fromtimestamp(int.from_bytes(data[28:], byteorder='big', signed=True)) if data[28:] != b'\x00' * 4 else None
        return Record(type, name, content, date)

class Journaling:
    def __init__(self, records: List[Record] = [Record() for i in range(16)]):
        self.records: list[Record] = records # Capacidad Para

    def encode(self):
        result_b = b''
        for i in self.records:
            result_b += i.encode()
        return result_b

    def decode(data):
        records: list[Record] = []
        for i in range(16):
            records.append(data[i * 32:32 + i * 32])
        return Journaling(records)

    def sizeOf():
        return len(Journaling().encode())