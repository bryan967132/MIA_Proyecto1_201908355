from Structures.Content import *
from typing import List

class BlockFolder:
    def __init__(self, content: List[Content] = [Content() for i in range(4)]):
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

    def sizeOf():
        return len(BlockFolder().encode())

    def getDot(self, i) -> str:
        pointers = ''
        for p in range(len(self.content)):
            pointers += f'''
                <TR><TD>{self.content[p].name.strip()}</TD><TD PORT="A{p}">{self.content[p].inodo}</TD></TR>'''
        return f'''block{i}[label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD COLSPAN="2" BGCOLOR="#D1BCD2" PORT="B{i}">Bloque {i}</TD></TR>{pointers}
        </TABLE>
    >];'''

    def getDotB(self, i) -> str:
        pointers = ''
        for p in range(len(self.content)):
            pointers += f'\n\t\t<TR><TD ALIGN="LEFT">{self.content[p].name.strip()}</TD><TD ALIGN="LEFT">{self.content[p].inodo}</TD></TR>'
        return f'''\n\tn{i}[label = <<TABLE BORDER="0">
        <TR><TD COLSPAN="2">Bloque Carpeta {i}</TD></TR>{pointers}
    </TABLE>>];'''

    def __str__(self) -> str:
        contents = ''
        for i in self.content:
            contents += i.__str__()
            if contents != '':
                contents += '\n'
        return contents