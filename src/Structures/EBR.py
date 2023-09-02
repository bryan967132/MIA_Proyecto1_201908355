class EBR:
    def __init__(self, status = None, fit = None, start = None, size = None, next = -1, name = None):
        self.status : str = status # char      1 byte
        self.fit    : str = fit    # char      1 byte
        self.start  : int = start  # int       4 bytes
        self.size   : int = size   # int       4 bytes
        self.next   : int = next   # int       4 bytes
        self.name   : str = name   # char[16] 16 bytes

    def encode(self) -> bytes :
        result_b = self.status.encode('utf-8') if self.status else b'\x00'
        result_b += self.fit.encode('utf-8') if self.fit else b'\x00'
        result_b += self.start.to_bytes(4, byteorder='big') if self.start else b'\x00' * 4
        result_b += self.size.to_bytes(4, byteorder='big') if self.size else b'\x00' * 4
        result_b += self.next.to_bytes(4, byteorder='big', signed=True)
        result_b += self.name.encode('utf-8') if self.name else b'\x00' * 16
        return result_b
    
    def decode(data):
        status = data[:1].decode('utf-8') if data[:1] != b'\x00' else None
        fit = data[1:2].decode('utf-8') if data[1:2] != b'\x00' else None
        start = int.from_bytes(data[2:6], byteorder='big') if data[2:6] != b'\x00' * 4 else None
        size = int.from_bytes(data[6:10], byteorder='big') if data[6:10] != b'\x00' * 4 else None
        next = int.from_bytes(data[10:14], byteorder='big', signed=True)
        name = data[14:].decode('utf-8') if data[14:] != b'\x00' * 16 else None
        return EBR(status, fit, start, size, next, name)
    
    def __str__(self) -> str:
        return 'Status: {:<5} Start: {:<10} Size: {:<10} Name: {:<16} Next: {}'.format(str(self.status), str(self.start), str(self.size), str(self.name), str(self.next))