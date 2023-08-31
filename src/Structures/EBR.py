class EBR:
    def __init__(self, status = None, fit = None, start = None, size = None, next = None, name = None):
        self.status : str = status # char      1 byte
        self.fit    : str = fit    # char      1 byte
        self.start  : int = start  # int       4 bytes
        self.size   : int = size   # int       4 bytes
        self.next   : int = next   # int       4 bytes
        self.name   : str = name   # char[16] 16 bytes

    def encode(self, flag = False) -> bytes :
        if flag:
            result_b = self.status.encode('utf-8')
            result_b += self.fit.encode('utf-8')
            result_b += self.start.to_bytes(4, byteorder='big')
            result_b += self.size.to_bytes(4, byteorder='big')
            result_b += self.next.to_bytes(4, byteorder='big', signed=True)
            result_b += self.name.encode('utf-8')
            return result_b
        next = -1
        result_b = next.to_bytes(4, byteorder='big', signed=True)
        return b'\x00' * 10 + result_b + b'\x00' * 16
    
    def decode(data):
        status = data[:1].decode('utf-8') if data[:1] != b'\x00' else None
        fit = data[1:2].decode('utf-8') if data[1:2] != b'\x00' else None
        start = int.from_bytes(data[2:6], byteorder='big')
        size = int.from_bytes(data[6:10], byteorder='big')
        next = int.from_bytes(data[10:14], byteorder='big', signed=True)
        name = data[14:].decode('utf-8') if data[14:] != b'\x00' * 16 else None
        return EBR(status, fit, start, size, next, name)
    
    def __str__(self) -> str:
        return '\tStart: {:<10} Size: {:<10} Name: {:<16} Next: {}'.format(self.start, self.size, str(self.name), self.next)