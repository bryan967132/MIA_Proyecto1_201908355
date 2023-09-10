from Structures.Content import *

class BlockFolder:
    def __init__(self, content: list[Content] = [Content() for i in range(4)]):
        self.content: list[Content] = content

    def encode(self) -> bytes:
        result_b = b''
        for i in self.content:
            result_b += i.encode()
        return result_b

    def decode(data):
        content: list[Content] = []
        for i in range(4):
            content.append(Content.decode(data[i * 16:16 + i * 16]))
        return BlockFolder(content)

    def __str__(self) -> str:
        contents = ''
        for i in self.content:
            contents += i.__str__()
            if contents != '':
                contents += '\n'
        return contents