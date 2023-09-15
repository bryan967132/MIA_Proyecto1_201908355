from typing import List

class BlockFile:
    def __init__(self, content: List[str] = ['' for i in range(64)]):
        self.content: list[str] = content

    def encode(self):
        contetn_str = ''.join(self.content).encode('utf-8')
        result_b = contetn_str + (64 - len(contetn_str)) * b'\x00'
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
			<TR><TD BGCOLOR="#FFECA9" PORT="B{i}">Bloque {i}</TD></TR>
			<TR><TD>{content}</TD></TR>
		</TABLE>
	>];'''

    def getDotB(self, i) -> str:
        content = ''
        for r in range(len(self.content)):
            content += self.content[r].replace('\n', '\\n').replace('\"', '\\\"').replace('\'', '\\\'')
            if r % 8 == 7:
                content += '<BR/>'
        return f'''\n\tn{i}[label = <<TABLE BORDER="0">
        <TR><TD>Bloque Archivo {i}</TD></TR>
        <TR><TD><FONT FACE="Consolas">{content}</FONT></TD></TR>
    </TABLE>>];'''

    def __str__(self) -> str:
        return f'content: {self.content}\n'