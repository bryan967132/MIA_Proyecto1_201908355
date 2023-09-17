from Structures.SuperBlock import *
from Structures.Journal import *
from Structures.MBR import *
from Env.Env import *
import datetime

class Logout:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def exec(self):
        if currentLogged['User']:
            with open(currentLogged['PathDisk'], 'rb') as file:
                readed_bytes = file.read(127)
                mbr = MBR.decode(readed_bytes)
                for i in range(len(mbr.partitions)):
                    if mbr.partitions[i].status and mbr.partitions[i].name.strip() == currentLogged['Partition']:
                        file.seek(mbr.partitions[i].start)
                        superBlock = SuperBlock.decode(file.read(SuperBlock.sizeOf()))
                        if superBlock.filesystem_type == 3:
                            file.seek(mbr.partitions[i].start + SuperBlock.sizeOf())
                            for r in range(superBlock.inodes_count):
                                readed_bytes = file.read(Journal.sizeOf())
                                if readed_bytes == Journal.sizeOf() * b'\x00':
                                    with open(currentLogged['PathDisk'], 'r+b') as file:
                                        file.seek(mbr.partitions[i].start + SuperBlock.sizeOf() + r * Journal.sizeOf())
                                        file.write(Journal('logout', '', '', datetime.datetime.now()).encode())
                                        break
                        break
            print(f"\033[32m -> logout: Sesión finalizada exitosamente. ({currentLogged['User'].name}) [{self.line}:{self.column}]\033[0m")
            currentLogged['User'] = None
            currentLogged['Partition'] = None
            currentLogged['PathDisk'] = None
            currentLogged['IDPart'] = None
        else:
            print(f"\033[31m -> Error logout: No hay ningún usuario loggeado actualmente. [{self.line}:{self.column}]\033[0m")