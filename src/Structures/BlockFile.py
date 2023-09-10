class BlockFile:
    def __init__(self, content: list[str] = ['' for i in range(64)]):
        self.content: list[str] = content

    def encode(self):
        result_b = b''
        for i in self.content:
            result_b += i.encode('utf-8') if i != '' else b'\x00'
        return result_b

    def decode(data):
        content: list[str] = []
        for i in range(64):
            content.append(data[i:i + 1].decode('utf-8') if data[i:i + 1] != b'\x00' else '')
        return BlockFile(content)

    def sizeOf():
        return len(BlockFile().encode())

    def __str__(self) -> str:
        return f'content: {self.content}\n'