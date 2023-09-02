from Structures.EBR import *

class Node:
    def __init__(self, ebr : EBR):
        self.ebr : EBR = ebr
        self.next : Node = None
        self.prev : Node = None

    def __str__(self) -> str:
        return self.ebr.__str__()

class ListEBR:
    def __init__(self, startPartition : int, size : int):
        self.startPartition : int = startPartition
        self.lastStart : int = 1024
        self.size : int = size
        self.first : Node = None
        self.last : Node = None

    def insert(self, newEBR : EBR):
        if self.first:
            if not self.first.ebr.status and newEBR.start == self.startPartition:
                newNode = Node(newEBR)
                if self.first.next:
                    newEBR.next = self.first.next.ebr.start
                    self.first.next.prev = newNode
                    newNode.next = self.first.next
                self.first = newNode
                self.lastStart = newEBR.start
                return
            if newEBR.start > self.lastStart:
                self.last.next = Node(newEBR)
                self.last.ebr.next = self.last.next.ebr.start
                self.last.next.prev = self.last
                self.last = self.last.next
                self.lastStart = newEBR.start
                return
            current : Node = self.first.next
            newNode : Node = Node(newEBR)
            while current:
                if newEBR.start > current.ebr.start and newEBR.start < current.next.ebr.start:
                    current.ebr.next = newNode.ebr.start
                    newNode.ebr.next = current.next.ebr.start
                    newNode.prev = current
                    newNode.next = current.next
                    current.next.prev = newNode
                    current.next = newNode
                    self.lastStart = newEBR.start
                    return
                current = current.next
            return
        self.first = Node(newEBR)
        self.last = self.first

    def delete(self, name : str) -> EBR:
        if self.first.ebr.name == name:
            deleted = self.first.ebr
            newFirst = Node(EBR(next = self.first.ebr.next))
            newFirst.next = self.first.next
            self.first = newFirst
            return deleted
        current = self.first
        while current.next:
            if current.next.ebr.name == name:
                deleted = current.next.ebr
                current.ebr.next = current.next.ebr.next
                if current.next:
                    current.next = current.next.next
                if current.next.next:
                    current.next.next.prev = current
                return deleted
            current = current.next
        return None

    def searchEmptySpace(self, newSize : int) -> list:
        emptySpaces = []
        lastNoEmptyByte = self.startPartition - 1
        if self.first.ebr.status:
            lastNoEmptyByte += self.first.ebr.size
        current = self.first.next
        while current:
            if current.ebr.start - lastNoEmptyByte > 2 and current.ebr.start - lastNoEmptyByte >= newSize + 1:
                emptySpaces.append([lastNoEmptyByte + 1, current.ebr.start - lastNoEmptyByte - 1])
            lastNoEmptyByte = current.ebr.start + current.ebr.size - 1
            current = current.next
        if self.startPartition + self.size - lastNoEmptyByte > 2 and self.startPartition + self.size - lastNoEmptyByte >= newSize + 1:
            emptySpaces.append([lastNoEmptyByte + 1, self.startPartition + self.size - lastNoEmptyByte - 1])
        return emptySpaces

    def print(self):
        current = self.first
        while current:
            print(current.ebr)
            current = current.next

    def getIterable(self) -> list[EBR]:
        ebrs = []
        current = self.first
        while current:
            ebrs.append(current.ebr)
            current = current.next
        return ebrs