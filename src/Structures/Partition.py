class Partition:
    def __init__(self, status = None, type = None, fit = None, start = None, size = None, name = None):
        self.status : str = status # char      1 byte
        self.type   : str = type   # char      1 byte
        self.fit    : str = fit    # char      1 byte
        self.start  : int = start  # int       4 bytes
        self.size   : int = size   # int       4 bytes
        self.name   : str = name   # char[16] 16 bytes

    def encode(self, flag = False) -> bytes :
        if flag:
            result_b = self.status.encode('utf-8')
            result_b += self.type.encode('utf-8')
            result_b += self.fit.encode('utf-8')
            result_b += self.start.to_bytes(4, byteorder='big')
            result_b += self.size.to_bytes(4, byteorder='big')
            result_b += self.name.encode('utf-8')
            return result_b
        return b'\x00' * 27
    
    def decode(data):
        status = data[:1].decode('utf-8') if data[:1] != b'\x00' else None
        type = data[1:2].decode('utf-8') if data[1:2] != b'\x00' else None
        fit = data[2:3].decode('utf-8') if data[2:3] != b'\x00' else None
        start = int.from_bytes(data[3:7], byteorder='big')
        size = int.from_bytes(data[7:11], byteorder='big')
        name = data[11:].decode('utf-8') if data[11:] != b'\x00' * 16 else None
        return Partition(status, type, fit, start, size, name)
    
    def __str__(self) -> str:
        return '\n\tStart: {:<10} Fit: {} Size: {:<10} Name: {}'.format(self.start, self.fit, self.size, self.name)