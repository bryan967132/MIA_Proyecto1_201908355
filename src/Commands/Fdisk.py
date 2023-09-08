from Structures.ListEBR import ListEBR
from Structures.MBR import *
from Structures.EBR import *
from io import BufferedRandom
from typing import List
import os

class Fdisk:
    def __init__(self, line: int, column: int):
        self.line = line
        self.column = column

    def setParams(self, params : dict):
        self.params = params

    def exec(self):
        if self.__isDelete():
            if self.__validateParamsDelete():
                self.__deletePartition()
            else:
                self.__printError(' -> Error fdisk: Faltan parámetros obligatorios para eliminar la partición.')
            return
        if self.__isAdd():
            if self.__validateParamsAdd():
                self.__addSpacePartition()
            else:
                self.__printError(' -> Error fdisk: Faltan parámetros obligatorios para agregar espacio a la partición.')
            return
        if self.__validateParams():
            self.__createPartition()
        else:
            self.__printError(' -> Error fdisk: Faltan parámetros obligatorios para crear la partición.')

    def __deletePartition(self):
        self.params['path'] = self.params['path'].replace('"', '')
        absolutePath = os.path.abspath(self.params['path'])
        if not os.path.exists(absolutePath):
            self.__printError(f' -> Error fdisk: No existe {os.path.basename(absolutePath).split(".")[0]} para eliminar la partición.')
            return
        with open(self.params['path'], 'rb') as file:
            readed_bytes = file.read(127)
            mbr = MBR.decode(readed_bytes)
            for i in range(len(mbr.partitions)):
                if mbr.partitions[i].status and mbr.partitions[i].name.strip() == self.params['name']:
                    listEBR = None
                    if mbr.partitions[i].type == 'E':
                        listEBR = self.__getListEBR(mbr.partitions[i].start, mbr.partitions[i].size, file).getIterable()
                    while True:
                        confirm = input(f"\033[33m -> Eliminar partición {self.params['name']} de disco {os.path.basename(absolutePath).split('.')[0]} (y/n): \033[0m")
                        if confirm.lower().strip() == 'y':
                            break
                        elif confirm.lower().strip() == 'n':
                            return
                    mbr.partitions.pop(i)
                    mbr.partitions.append(Partition())
                    with open(self.params['path'], 'r+b') as file:
                        file.seek(0)
                        file.write(mbr.encode())
                        if listEBR:
                            for ebr in listEBR:
                                file.seek(ebr.start if ebr.start else mbr.partitions[i].start)
                                file.write(b'\x00' * 30)
                    self.__printSuccessDelete(f' -> fdisk: Partición eliminada exitosamente en {os.path.basename(absolutePath).split(".")[0]}.')
                    return
            i = self.__getExtended(mbr.partitions)
            if i != -1:
                listEBR : ListEBR = self.__getListEBR(mbr.partitions[i].start, mbr.partitions[i].size, file)
                iterEBR : list[EBR] = listEBR.getIterable()
                for ebr in iterEBR:
                    if ebr.name and ebr.name.strip() == self.params["name"]:
                        while True:
                            confirm = input(f"\033[33m -> Eliminar partición {self.params['name']} de disco {os.path.basename(absolutePath).split('.')[0]} (y/n): \033[0m")
                            if confirm.lower().strip() == 'y':
                                break
                            elif confirm.lower().strip() == 'n':
                                return
                        delEBR = listEBR.delete(ebr.name)
                        with open(self.params['path'], 'r+b') as file:
                            file.seek(delEBR.start)
                            file.write(b'\x00' * 30)
                            iterEBR = listEBR.getIterable()
                            for ebr in iterEBR:
                                file.seek(ebr.start if ebr.start else mbr.partitions[i].start)
                                file.write(ebr.encode())
                        self.__printSuccessDelete(f' -> fdisk: Partición eliminada exitosamente en {os.path.basename(absolutePath).split(".")[0]}.')
                        return
            self.__printError(f' -> Error fdisk: No existe la partición que se intentó eliminar en {os.path.basename(absolutePath).split(".")[0]}.')

    def __addSpacePartition(self):
        self.params['path'] = self.params['path'].replace('"', '')
        absolutePath = os.path.abspath(self.params['path'])
        if not os.path.exists(absolutePath):
            self.__printError(f' -> Error fdisk: No existe {os.path.basename(absolutePath).split(".")[0]} para agregar espacio a la partición.')
            return
        units = 1
        if self.params['unit'] == 'M':
            units = 1024 * 1024
        elif self.params['unit'] == 'K':
            units = 1024
        elif self.params['unit'] == 'B':
            units = 1
        else:
            self.__printError(' -> Error fdisk: Unidad de Bytes Incorrecta.')
            return
        with open(self.params['path'], 'rb') as file:
            readed_bytes = file.read(127)
            mbr = MBR.decode(readed_bytes)
            for i in range(len(mbr.partitions)):
                if mbr.partitions[i].status and mbr.partitions[i].name.strip() == self.params['name']:
                    bytesAdds = self.params['add'] * units
                    msg = "sin cambios"
                    if bytesAdds < 0:
                        if abs(bytesAdds) == mbr.partitions[i].size:
                            self.__printError(' ->  Error fdisk: Intenta quitar todo el espacio del disponible en la partición.')
                            return
                        if abs(bytesAdds) > mbr.partitions[i].size:
                            self.__printError(' ->  Error fdisk: Intenta quitar más espacio del disponible en la partición.')
                            return
                        msg = "reducido"
                    elif bytesAdds > 0:
                        if i < len(mbr.partitions) - 1 and mbr.partitions[i + 1].status:
                            if bytesAdds > mbr.partitions[i + 1].start - mbr.partitions[i].size - mbr.partitions[i].start:
                                self.__printError(' -> Error fdisk: Intenta agregar más espacio del disponible después de la partición.')
                                return
                        elif bytesAdds > mbr.size - mbr.partitions[i].size - mbr.partitions[i].start:
                                self.__printError(' -> Error fdisk: Intenta agregar más espacio del disponible después de la partición.')
                                return
                        msg = "aumentado"
                    mbr.partitions[i].size += bytesAdds
                    with open(self.params['path'], 'r+b') as file:
                        file.seek(0)
                        file.write(mbr.encode())
                    self.__printSuccessAdd(f' -> fdisk: Espacio {msg} en la Partición exitosamente en {os.path.basename(absolutePath).split(".")[0]}.')
                    return
            i = self.__getExtended(mbr.partitions)
            if i != -1:
                listEBR : list[EBR] = self.__getListEBR(mbr.partitions[i].start, mbr.partitions[i].size, file).getIterable()
                for ebr in listEBR:
                    if ebr.name and ebr.name.strip() == self.params['name']:
                        bytesAdds = self.params['add'] * units
                        msg = "sin cambios"
                        if bytesAdds < 0:
                            if abs(bytesAdds) == ebr.size:
                                self.__printError(' ->  Error fdisk: Intenta quitar todo el espacio del disponible en la partición.')
                                return
                            if abs(bytesAdds) > ebr.size:
                                self.__printError(' ->  Error fdisk: Intenta quitar más espacio del disponible en la partición.')
                                return
                            msg = "reducido"
                        elif bytesAdds > 0:
                            if ebr.next != -1:
                                if bytesAdds > ebr.next - ebr.size - ebr.start:
                                    self.__printError(' -> Error fdisk: Intenta agregar más espacio del disponible después de la partición.')
                                    return
                            else:
                                if bytesAdds > mbr.partitions[i].start + mbr.partitions[i].size - ebr.size - ebr.start:
                                    self.__printError(' -> Error fdisk: Intenta agregar más espacio del disponible después de la partición.')
                                    return
                            msg = "aumentado"
                        ebr.size += bytesAdds
                        with open(self.params['path'], 'r+b') as file:
                            file.seek(ebr.start)
                            file.write(ebr.encode())
                        self.__printSuccessAdd(f' -> fdisk: Espacio {msg} en la Partición exitosamente en {os.path.basename(absolutePath).split(".")[0]}.')
                        return
            self.__printError(f' -> Error fdisk: No existe la partición en {os.path.basename(absolutePath).split(".")[0]} a la que se intentó agregar o quitar espacio.')

    def __createPartition(self):
        self.params['path'] = self.params['path'].replace('"', '')
        self.params['fit'] = self.params['fit'].upper()
        self.params['type'] = self.params['type'].upper()
        absolutePath = os.path.abspath(self.params['path'])
        if not os.path.exists(absolutePath):
            self.__printError(f' -> Error fdisk: No existe {os.path.basename(absolutePath).split(".")[0]} para particionar.')
            return
        self.params['unit'] = self.params['unit'].upper()
        if self.params['size'] < 0:
            self.__printError(' -> Error: El tamaño de la partición debe ser mayor que cero')
            return
        units = 1
        if self.params['unit'] == 'M':
            units = 1024 * 1024
        elif self.params['unit'] == 'K':
            units = 1024
        elif self.params['unit'] == 'B':
            units = 1
        else:
            self.__printError(' -> Error fdisk: Unidad de Bytes Incorrecta.')
            return
        with open(self.params['path'], 'rb') as file:
            readed_bytes = file.read(127)
            mbr = MBR.decode(readed_bytes)
            self.params['fit'] = self.params['fit'][:1]
            if self.params['type'] == 'P' or self.params['type'] == 'E':
                disponible = []
                lastNoEmptyByte = 126
                for i in range(len(mbr.partitions)):
                    if mbr.partitions[i].status:
                        if mbr.partitions[i].start - lastNoEmptyByte > 2 and mbr.partitions[i].start - lastNoEmptyByte >= self.params['size'] * units + 1:
                            disponible.append([lastNoEmptyByte + 1, mbr.partitions[i].start - lastNoEmptyByte])
                        lastNoEmptyByte = mbr.partitions[i].start + mbr.partitions[i].size - 1
                if mbr.size - lastNoEmptyByte  > 2 and mbr.size - lastNoEmptyByte >= self.params['size'] * units + 1:
                    disponible.append([lastNoEmptyByte + 1, mbr.size - lastNoEmptyByte - 1])
                if len(disponible) > 0:
                    if mbr.fit == 'B':
                        disponible = self.__sortBestFit(disponible)
                    elif mbr.fit == 'W':
                        disponible = self.__sortWorstFit(disponible)
                    if self.params['type'] == 'E' and self.__getExtended(mbr.partitions) != -1:
                        self.__printError(f' -> Error fdisk: Ya existe una partición extendida en {os.path.basename(absolutePath).split(".")[0]}.')
                        return
                    for i in range(len(mbr.partitions)):
                        if not mbr.partitions[i].status:
                            mbr.partitions[i] = Partition(
                                '0',
                                self.params['type'],
                                self.params['fit'],
                                disponible[0][0],
                                self.params['size'] * units,
                                self.params['name'][:16].ljust(16)
                            )
                            mbr.partitions = self.__sortOrder(mbr.partitions)
                            with open(self.params['path'], 'r+b') as file:
                                file.seek(0)
                                file.write(mbr.encode())
                                if self.params['type'] == 'E':
                                    file.seek(mbr.partitions[i].start)
                                    file.write(EBR().encode())
                            self.__printSuccessCreate(os.path.basename(absolutePath).split(".")[0], self.params["name"], self.params['type'], self.params["size"], self.params["unit"])
                            return
                    self.__printError(f' -> Error fdisk: No pueden crearse mas particiones en {os.path.basename(absolutePath).split(".")[0]}.')
                else:
                    self.__printError(f' -> Error fdisk: No hay espacio suficiente para la nueva partición en {os.path.basename(absolutePath).split(".")[0]}.')
            elif self.params['type'] == 'L':
                i = self.__getExtended(mbr.partitions)
                if i != -1:
                    listEBR : ListEBR = self.__getListEBR(mbr.partitions[i].start, mbr.partitions[i].size, file)
                    disponible = listEBR.searchEmptySpace(self.params['size'] * units)
                    if len(disponible) > 0:
                        if mbr.partitions[i].fit == 'B':
                            disponible = self.__sortBestFit(disponible)
                        elif mbr.partitions[i].fit == 'W':
                            disponible = self.__sortWorstFit(disponible)
                        ebr = EBR(
                            status = '0',
                            fit = self.params['fit'],
                            start = disponible[0][0],
                            size = self.params['size'] * units,
                            name = self.params['name'][:16].ljust(16)
                        )
                        listEBR.insert(ebr)
                        with open(self.params['path'], 'r+b') as file:
                            for e in listEBR.getIterable():
                                file.seek(e.start if e.start else mbr.partitions[i].start)
                                file.write(e.encode())
                        self.__printSuccessCreate(os.path.basename(absolutePath).split(".")[0], self.params["name"], self.params['type'], self.params["size"], self.params["unit"])
                        return
                    self.__printError(f' -> Error fdisk: No hay espacio suficiente para la nueva partición en {os.path.basename(absolutePath).split(".")[0]}.')
                    return
                self.__printError(f' -> Error fdisk: No existe una partición extendida en {os.path.basename(absolutePath).split(".")[0]} para crear la partición lógica.')

    def __getListEBR(self, start : int, size : int, file : BufferedRandom) -> ListEBR:
        listEBR : ListEBR = ListEBR(start, size)
        file.seek(start)
        ebr = EBR.decode(file.read(30))
        listEBR.insert(ebr)
        while ebr.next != -1:
            file.seek(ebr.next)
            ebr = EBR.decode(file.read(30))
            listEBR.insert(ebr)
        return listEBR

    def __getExtended(self, partitions : List[Partition]):
        for i in range(len(partitions)):
            if partitions[i].type == 'E':
                return i
        return -1

    def __sortBestFit(self, disponible):
        if len(disponible) > 1:
            for i in range(1, len(disponible)):
                for j in range(i, 0, -1):
                    if disponible[j][1] < disponible[j - 1][1]:
                        disponible[j], disponible[j - 1] = disponible[j - 1], disponible[j]
                        continue
                    break
        return disponible

    def __sortWorstFit(self, disponible):
        if len(disponible) > 1:
            for i in range(1, len(disponible)):
                for j in range(i, 0, -1):
                    if disponible[j][1] > disponible[j - 1][1]:
                        disponible[j], disponible[j - 1] = disponible[j - 1], disponible[j]
                        continue
                    break
        return disponible

    def __sortOrder(self, partitions):
        for i in range(1, len(partitions)):
            if partitions[i].start:
                for j in range(i, 0, -1):
                    if partitions[j].start < partitions[j - 1].start:
                        partitions[j], partitions[j - 1] = partitions[j - 1], partitions[j]
                        continue
                    break
                continue
            break
        return partitions

    def __isDelete(self):
        for k in self.params:
            if k == 'delete':
                return True
        return False

    def __validateParamsDelete(self):
        if 'path' in self.params and 'name' in self.params:
            return True
        return False

    def __isAdd(self):
        if 'add' in self.params:
            self.params['add'] = int(self.params['add'])
            return True
        return False

    def __validateParamsAdd(self):
        if 'path' in self.params and 'name' in self.params and 'unit' in self.params:
            self.params['unit'] = self.params['unit'].upper()
            return True
        return False

    def __validateParams(self):
        if 'size' in self.params and 'path' in self.params and 'name' in self.params:
            self.params['size'] = int(self.params['size'])
            return True
        return False

    def __printError(self, text):
        print(f"\033[31m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccessDelete(self, text):
        print(f"\033[32m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccessAdd(self, text):
        print(f"\033[32m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccessCreate(self, diskname, name, type, size, unit):
        type = "Primaria" if type == 'P' else ("Extendida" if type == 'E' else "Logica")
        unit = unit if unit in ['K', 'M'] else ""
        print("\033[32m -> fdisk: Partición creada exitosamente en {}. {:<9} ({}: {} {}B) [{}:{}]\033[0m".format(diskname, type.upper(), name, size, unit, self.line, self.column))

    def __str__(self) -> str:
        return 'Fdisk'    