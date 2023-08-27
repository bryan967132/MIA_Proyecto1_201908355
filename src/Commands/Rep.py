from Structures.MBR import *
import os

class Rep:
    def exec(self):
        absolutePath = os.path.abspath('../Disks/Disco1.dsk')
        if not os.path.exists(absolutePath):
            print(' ->  Error rep: No existe el disco para reportar.')
            return
        with open('../Disks/Disco1.dsk', 'rb') as file:
            readed_bytes = file.read(127)
            mbr = MBR.decode(readed_bytes)
            isThereEmpty = False
            lastNoEmptyByte = 127

            dotParts = ''
            ocuppedCells = 10
            for i in range(len(mbr.partitions)):
                if mbr.partitions[i].status:
                    if isThereEmpty or mbr.partitions[i].start - lastNoEmptyByte > 1:
                        space = round(((mbr.partitions[i].start - (lastNoEmptyByte + 1)) / mbr.size) * 200, 2)
                        ocuppedCells += int(space)
                        dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                    space = round((mbr.partitions[i].size / mbr.size) * 200, 2)
                    ocuppedCells += int(space)
                    if mbr.partitions[i].type == 'P':
                        dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">{mbr.partitions[i].name.strip()}<BR/>Primaria<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                    elif mbr.partitions[i].type == 'M':
                        dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">{mbr.partitions[i].name.strip()}<BR/>Extendida<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                    lastNoEmptyByte = mbr.partitions[i].start + mbr.partitions[i].size - 1
                    isThereEmpty = False
                else:
                    isThereEmpty = True
            if lastNoEmptyByte < mbr.size:
                space = round(((mbr.size - (lastNoEmptyByte + 1)) / mbr.size) * 200, 2)
                dotParts += f'\n\t\t\t\t<TD COLSPAN="{int(space)}" ROWSPAN="6">Libre<BR/>{self.porcentaje(round(space / 2, 2))} %</TD>'
                ocuppedCells += int(space)

            dot = 'digraph Disk{\n\tnode [shape=plaintext];'
            dot += '\n\ttabla[label=<\n\t\t<TABLE BORDER="1" CELLBORDER="1" CELLSPACING="2" CELLPADDING="4">'
            dot += f'\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="{ocuppedCells}">Disk1</TD>\n\t\t\t</TR>'
            dot += '\n\t\t\t<TR>\n\t\t\t\t<TD COLSPAN="10" ROWSPAN="6">MBR</TD>'
            dot += dotParts
            dot += '\n\t\t\t</TR>'
            dot += '\n\t\t</TABLE>\n\t>];'
            dot += '\n}'
            absolutePath = os.path.abspath('../Reps/Disco1.dot')
            directory = os.path.dirname(absolutePath)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open('../Reps/Disco1.dot', 'w') as file:
                file.write(dot)
            os.system('dot -Tpdf ../Reps/Disco1.dot -o ../Reps/Disco1.pdf')
            # os.remove('../Reps/Disco1.dot')

    def porcentaje(self, number : float) -> int or float:
        num = number - int(number)
        if num > 0:
            return number
        return int(number)

    def __str__(self) -> str:
        return 'Rep'