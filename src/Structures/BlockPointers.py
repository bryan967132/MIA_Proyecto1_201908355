from typing import List

class BlockPointers:
    def __init__(self, pointers: List[int] = [-1 for i in range(16)]):
        self.pointers: list[int] = pointers

    def encode(self):
        result_b = b''
        for i in self.pointers:
            result_b += i.to_bytes(4, byteorder='big', signed=True)
        return result_b

    def decode(data):
        pointers: list[int] = []
        for i in range(16):
            pointers.append(int.from_bytes(data[i * 4:4 + i * 4], byteorder='big', signed=True))
        return BlockPointers(pointers)

    def sizeOf():
        return len(BlockPointers().encode())

    def getDot(self, i):
        pointers = ''
        for p in range(len(self.pointers)):
            pointers += f'''
                <TR><TD PORT="A{p}">{self.pointers[p]}</TD></TR>'''
        return f'''block{i}[label=<
        <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
            <TR><TD BGCOLOR="#FFCB97" PORT="B{i}">Bloque {i}</TD></TR>{pointers}
        </TABLE>
    >];'''

    def getDotB(self, i):
        content = ''
        for r in range(len(self.pointers)):
            content += str(self.pointers[r])
            if r % 4 == 3:
                content += '<BR/>'
        return f'''\n\tn{i}[label = <<TABLE BORDER="0">
        <TR><TD>Bloque Apuntadores {i}</TD></TR>
        <TR><TD><FONT FACE="Consolas">{content}</FONT></TD></TR>
    </TABLE>>];'''

    def __str__(self) -> str:
        return f'pointers: {self.pointers}\n'