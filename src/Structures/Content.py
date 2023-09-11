class Content:
    def __init__(self, name: str = None, inodo:int = -1):
        self.name: str = name
        self.inodo: int = inodo

    def encode(self) -> bytes:
        result_b = self.name.encode('utf-8') if self.name else b'\x20' * 12
        result_b += self.inodo.to_bytes(4, byteorder='big', signed=True)
        return result_b

    def decode(data):
        name: str = data[:12].decode('utf-8') if data[:16] != b'\x20' * 12 else None
        inodo: int = int.from_bytes(data[12:], byteorder='big', signed=True)
        return Content(name, inodo)

    def __str__(self) -> str:
        return f'''name: {self.name} inodo: {self.inodo}'''