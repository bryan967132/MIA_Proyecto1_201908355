from Structures.MBR import *
import os

class Fdisk:
    def setParams(self, params : dict):
        self.params = params

    def exec(self):
        if self.__isDelete():
            if self.__validateParamsDelete():
                self.__deletePartition()
            else:
                self.printError(' -> Error fdisk: Faltan parámetros obligatorios para eliminar la partición.')
            return
        if self.__isAdd():
            if self.__validateParamsAdd():
                self.__addSpacePartition()
            else:
                self.printError(' -> Error fdisk: Faltan parámetros obligatorios para agregar espacio a la partición.')
            return
        if self.__validateParams():
            self.__createPartition()
        else:
            self.printError(' -> Error fdisk: Faltan parámetros obligatorios para crear la partición.')

    def __deletePartition(self):
        self.params['path'] = self.params['path'].replace('"', '')
        absolutePath = os.path.abspath(self.params['path'])
        if not os.path.exists(absolutePath):
            self.printError(' -> Error fdisk: No existe el disco para eliminar la partición.')
            return
        with open(self.params['path'], 'rb') as file:
            readed_bytes = file.read(127)
            mbr = MBR.decode(readed_bytes)
            for i in range(len(mbr.partitions)):
                if mbr.partitions[i].name.strip() == self.params['name']:
                    while True:
                        confirm = input('Eliminar la partición (y/n): ')
                        if confirm.lower() == 'y':
                            break
                        elif confirm.lower() == 'n':
                            return
                    mbr.partitions.pop(i)
                    mbr.partitions.append(Partition())
                    with open(self.params['path'], 'r+b') as file:
                        file.seek(0)
                        file.write(mbr.encode())
                    return
            self.printError(' -> Error fdisk: No existe la partición que se intentó eliminar.')

    def __addSpacePartition(self):
        self.params['path'] = self.params['path'].replace('"', '')
        absolutePath = os.path.abspath(self.params['path'])
        if not os.path.exists(absolutePath):
            self.printError(' -> Error fdisk: No existe el disco para agregar espacio a la partición.')
            return
        units = 1
        if self.params['unit'] == 'M':
            units = 1024 * 1024
        elif self.params['unit'] == 'K':
            units = 1024
        elif self.params['unit'] == 'B':
            units = 1
        else:
            self.printError(' -> Error fdisk: Unidad de Bytes Incorrecta.')
            return
        with open(self.params['path'], 'rb') as file:
            readed_bytes = file.read(127)
            mbr = MBR.decode(readed_bytes)
            lastNoEmptyByte = 126
            indexPartition = 0
            existPartition = False
            for i in range(len(mbr.partitions)):
                if mbr.partitions[i].status and mbr.partitions[i].name.strip() == self.params['name']:
                    bytesAdds = self.params['add'] * units
                    if bytesAdds < 0:
                        if abs(bytesAdds) > mbr.partitions[i].size:
                            self.printError(' ->  Error fdisk: Intenta quitar más espacio del disponible en la partición.')
                            return
                        mbr.partitions[i].size += bytesAdds
                        with open(self.params['path'], 'r+b') as file:
                            file.seek(0)
                            file.write(mbr.encode())
                        return
                    lastNoEmptyByte = mbr.partitions[i].start + mbr.partitions[i].size - 1
                    existPartition = True
                    indexPartition = i
                    break
            if existPartition:
                nextNoEmptyByte = lastNoEmptyByte
                for i in range(indexPartition + 1, len(mbr.partitions)):
                    if mbr.partitions[i].status:
                        nextNoEmptyByte = mbr.partitions[i].start
                        break
                if nextNoEmptyByte != lastNoEmptyByte:
                    bytesAdds = self.params['add'] * units
                    if bytesAdds > nextNoEmptyByte - lastNoEmptyByte:
                        self.printError(' -> Error fdisk: Intenta agregar más espacio del disponible después de la partición.')
                        return
                    mbr.partitions[indexPartition].size += bytesAdds
                    with open(self.params['path'], 'r+b') as file:
                        file.seek(0)
                        file.write(mbr.encode())
                    return
                else:
                    bytesAdds = self.params['add'] * units
                    lastSpace = mbr.size - lastNoEmptyByte
                    if bytesAdds > lastSpace:
                        self.printError(' -> Error fdisk: Intenta agregar más espacio del disponible después de la partición.')
                        return
                    mbr.partitions[indexPartition].size += bytesAdds
                    with open(self.params['path'], 'r+b') as file:
                        file.seek(0)
                        file.write(mbr.encode())
                    return
            self.printError(' -> Error fdisk: No existe la partición a la que se intentó agregar o quitar espacio.')

    def __createPartition(self):
        self.params['path'] = self.params['path'].replace('"', '')
        self.params['fit'] = self.params['fit'].upper()
        self.params['type'] = self.params['type'].upper()
        absolutePath = os.path.abspath(self.params['path'])
        if not os.path.exists(absolutePath):
            self.printError(' -> Error fdisk: No existe el disco para particionar.')
            return
        self.params['unit'] = self.params['unit'].upper()
        if self.params['size'] < 0:
            self.printError(' -> Error: El tamaño de la partición debe ser mayor que cero')
            return
        units = 1
        if self.params['unit'] == 'M':
            units = 1024 * 1024
        elif self.params['unit'] == 'K':
            units = 1024
        elif self.params['unit'] == 'B':
            units = 1
        else:
            self.printError(' -> Error fdisk: Unidad de Bytes Incorrecta.')
            return
        with open(self.params['path'], 'rb') as file:
            readed_bytes = file.read(127)
            mbr = MBR.decode(readed_bytes)
            self.params['fit'] = self.params['fit'][:1]
            disponible = []
            lastNoEmptyByte = 126
            for i in range(len(mbr.partitions)):
                if mbr.partitions[i].status:
                    if mbr.partitions[i].start - lastNoEmptyByte > 1 and mbr.partitions[i].start - lastNoEmptyByte >= self.params['size'] * units:
                        disponible.append([lastNoEmptyByte + 1, mbr.partitions[i].start - lastNoEmptyByte])
                    lastNoEmptyByte = mbr.partitions[i].start + mbr.partitions[i].size - 1
            if mbr.size - lastNoEmptyByte  > 1 and mbr.size - lastNoEmptyByte >= self.params['size'] * units:
                disponible.append([lastNoEmptyByte + 1, mbr.size - lastNoEmptyByte - 1])
            if len(disponible) > 0:
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
                        return
            else:
                self.printError(' -> Error fdisk: No hay espacio suficiente para la nueva partición.')

    def __sortOrder(self, partitions):
        temporalPartitions = [partition for partition in partitions if partition.status]
        if len(temporalPartitions) > 1:
            for i in range(1, len(temporalPartitions)):
                for j in range(i, 0, -1):
                    if temporalPartitions[i].start < temporalPartitions[i - 1].start:
                        temporalPartitions[i], temporalPartitions[i - 1] = temporalPartitions[i - 1], temporalPartitions[i]
                        continue
                    break
            partitions = temporalPartitions
            for i in range(len(temporalPartitions), 4):
                partitions.append(Partition())
        return partitions

    def __isDelete(self):
        for k in self.params:
            if k == 'delete':
                return True
        return False

    def __validateParamsDelete(self):
        for k in self.params:
            if k == 'path':
                path = True
            elif k == 'name':
                name = True
        return path and name

    def __isAdd(self):
        for k in self.params:
            if k == 'add':
                self.params[k] = int(self.params[k])
                return True
        return False

    def __validateParamsAdd(self):
        for k in self.params:
            if k == 'path':
                path = True
            elif k == 'name':
                name = True
            elif k == 'unit':
                self.params[k] = self.params[k].upper()
                unit = True
        return path and name and unit

    def __validateParams(self):
        for k in self.params:
            if k == 'size':
                self.params[k] = int(self.params[k])
                size = True
            elif k == 'path':
                path = True
            elif k == 'name':
                name = True
        return size and path and name

    def printError(self, text):
        print(f"\033[{31}m{text}\033[0m")

    def __str__(self) -> str:
        return 'Fdisk'
    