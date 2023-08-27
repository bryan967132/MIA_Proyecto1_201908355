from Structures.Partition import *
from datetime import datetime
import random
class MBR:
    def __init__(self, size : int, date = datetime.now(), dsk = random.randint(0, 10000), fit = 'F', partitions = [
            Partition(),
            Partition(),
            Partition(),
            Partition()
        ]):
        self.size       : int = size                   #   4 bytes
        self.date       : datetime = date              #  12 bytes
        self.dsk_sig    : int = dsk                    #   2 bytes
        self.fit        : str = fit                    #   1 byte
        self.partitions : list[Partition] = partitions # 108 bytes

    def encode(self) -> bytes :
        result_b = self.size.to_bytes(4, byteorder='big')
        result_b += self.date.day.to_bytes(2, byteorder='big')
        result_b += self.date.month.to_bytes(2, byteorder='big')
        result_b += self.date.year.to_bytes(2, byteorder='big')
        result_b += self.date.hour.to_bytes(2, byteorder='big')
        result_b += self.date.minute.to_bytes(2, byteorder='big')
        result_b += self.date.second.to_bytes(2, byteorder='big')
        result_b += self.dsk_sig.to_bytes(2, byteorder='big')
        result_b += self.fit.encode('utf-8')
        for p in self.partitions:
            if p.start:
                result_b += p.encode(True)
            else:
                result_b += p.encode()
        return result_b

    def decode(data):
        size = int.from_bytes(data[:4], byteorder='big')
        dd   = int.from_bytes(data[4:6], byteorder='big')
        MM   = int.from_bytes(data[6:8], byteorder='big')
        yyyy = int.from_bytes(data[8:10], byteorder='big')
        HH   = int.from_bytes(data[10:12], byteorder='big')
        mm   = int.from_bytes(data[12:14], byteorder='big')
        ss   = int.from_bytes(data[14:16], byteorder='big')
        dsk  = int.from_bytes(data[16:18], byteorder='big')
        fit  = data[18:19].decode('utf-8')
        partitions = [
            Partition.decode(data[19:46]),
            Partition.decode(data[46:73]),
            Partition.decode(data[73:100]),
            Partition.decode(data[100:])
        ]
        return MBR(size, datetime(yyyy, MM, dd, HH, mm, ss), dsk, fit, partitions)

    def getDateTime(self) -> str:
        return f'{self.date.day}/{self.date.month}/{self.date.year} {self.date.hour}:{self.date.minute}:{self.date.second}'

    def __str__(self) -> str:
        prts = ''
        for p in self.partitions:
            prts += p.__str__()
        return 'Size: {:<10} Date: {:<20} DSK: {}'.format(self.size, self.getDateTime(), self.dsk_sig) + prts