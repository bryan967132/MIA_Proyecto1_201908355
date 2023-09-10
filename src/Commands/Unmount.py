from Structures.ListEBR import ListEBR
from Structures.MBR import *
from Structures.EBR import *
from io import BufferedRandom
from typing import List
from Env.Env import *
import os
import re

class Unmount:
    def __init__(self, line: int, column:int):
        self.line = line
        self.column = column

    def setParams(self, params : dict):
        self.params = params

    def exec(self):
        if self.__validateParams():
            self.__unmount()
            return
        else:
            self.__printError(' -> Error unmount: Faltan parámetros obligatorios para desmontar la partición')
            return

    def __unmount(self):
        match = re.match(r'(\d+)([a-zA-Z]+\d+)', self.params['id'])
        if match.group(2) in disks:
            if self.params['id'] in disks[match.group(2)]['ids']:
                absolutePath = disks[match.group(2)]['path']
                namePartition = disks[match.group(2)]['ids'][self.params['id']]
                with open(absolutePath, 'rb') as file:
                    readed_bytes = file.read(127)
                    mbr = MBR.decode(readed_bytes)
                    for i in range(len(mbr.partitions)):
                        if mbr.partitions[i].status and mbr.partitions[i].name.strip() == namePartition:
                            with open(absolutePath, 'r+b') as file:
                                file.seek(19 + i * 27)
                                file.write('0'.encode('utf-8'))
                            thisDisk = disks[os.path.basename(absolutePath).split('.')[0]]
                            del thisDisk['ids'][self.params['id']]
                            self.__printSuccess(os.path.basename(absolutePath).split('.')[0], self.params['id'], namePartition, mbr.partitions[i].type)
                            return
                    i = self.__getExtended(mbr.partitions)
                    if i != -1:
                        listEBR: list[EBR] = self.__getListEBR(mbr.partitions[i].start, mbr.partitions[i].size, file).getIterable()
                        for ebr in listEBR:
                            if ebr.name and ebr.name.strip() == namePartition:
                                with open(absolutePath, 'r+b') as file:
                                    file.seek(ebr.start)
                                    file.write('0'.encode('utf-8'))
                                thisDisk = disks[os.path.basename(absolutePath).split('.')[0]]
                                del thisDisk['ids'][self.params['id']]
                                self.__printSuccess(os.path.basename(absolutePath).split('.')[0], self.params['id'], namePartition, 'L')
                                return
                    self.__printError(f' -> Error unmount: Intenta desmontar una partición inexistente en {match.group(2)}.')
                    return
            self.__printError(f' -> Error unmount: No existe el código de partición {self.params["id"]} para desmontar en el disco {match.group(2)}.')
            return
        self.__printError(f' -> Error unmount: No existe el disco {match.group(2)} para desmontar la partición.')

    def __getListEBR(self, start: int, size: int, file: BufferedRandom) -> ListEBR:
        listEBR: ListEBR = ListEBR(start, size)
        file.seek(start)
        ebr = EBR.decode(file.read(30))
        listEBR.insert(ebr)
        while ebr.next != -1:
            file.seek(ebr.next)
            ebr = EBR.decode(file.read(30))
            listEBR.insert(ebr)
        return listEBR

    def __getExtended(self, partitions: List[Partition]):
        for i in range(len(partitions)):
            if partitions[i].type == 'E':
                return i
        return -1

    def __validateParams(self):
        if 'id' in self.params:
            return True
        return False

    def __printError(self, text):
        print(f"\033[31m{text} [{self.line}:{self.column}]\033[0m")

    def __printSuccess(self, diskname, codePart, name, type):
        type = "PRIMARIA " if type == 'P' else ("EXTENDIDA" if type == 'E' else "LOGICA   ")
        print(f"\033[32m -> unmount: Partición desmontada exitosamente en {diskname}. {type} ({codePart}: {name}) [{self.line}:{self.column}]\033[0m")