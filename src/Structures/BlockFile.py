from typing import List

class BlockFile:
    def __init__(self, content: List[str] = ['' for i in range(64)]):
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

    def getDot(self, i) -> str:
        content = ''.join(self.content).replace('\n', '\\n').replace('\"', '\\\"').replace('\'', '\\\'')
        return f'''block{i}[label=<
		<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="4">
			<TR><TD BGCOLOR="#FFECA9" PORT="B{i}">Block {i}</TD></TR>
			<TR><TD>{content}</TD></TR>
		</TABLE>
	>];'''

    def getDotB(self, i) -> str:
        content = ''.join(self.content).replace('\n', '\\n').replace('\"', '\\\"').replace('\'', '\\\'')
        return f'''\n\tn{i}[label = <<TABLE BORDER="0">
        <TR><TD>Bloque Archivo {i}</TD></TR>
        <TR><TD ALIGN="LEFT">{content}</TD></TR>
    </TABLE>>];'''

    def __str__(self) -> str:
        return f'content: {self.content}\n'