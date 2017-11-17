import multiprocessing as mp

import threading as th

from math import e
from math import tanh
from math import pi

import enum

class ProcessThreadManager:

    class ChildType(enum.Enum):

        noChilds = -1
        thread = 0
        process = 1

    class Type(enum.Enum):

        thread = 0
        process = 1

    def __init__(self):

        self.cores = mp.cpu_count()
        self.processes = {}
        self.threads = {}
        self.transition = {}
        self.processChildren = {}
        self.threadChildren = {}
        self.processType = {}
        self.takenNumbers = []
        self.processLocks = {}
        self.threadLocks = {}
        self.unlinkedChildren = {}
        self.childOut = {}
        self.IDMethods = []

    def _hasChildren(self,ID):

        try:
            tmp = self.processChildren[ID]
            return True
        except:
            try:
                tmp = self.threadChildren[ID]
                return True
            except:
                return False

    def _childType(self,ID):

        try:
            return self.processType[ID]
        except:
            return self.ChildType.noChilds

    def _exists(self,ID):
        try:
            self.takenNumbers.index(ID)
            return True
        except:
            return False

    def _sort(self):
        self.takenNumbers = sorted(self.takenNumbers)

    def _killChildren(self,ID):

        if self._hasChildren(ID) != self.ChildType.noChilds:
            if(self.processType[ID]):
                Children = self.processChildren[ID]

            elif(not self.processType[ID]):
                Children = self.threadChildren[ID]

            for ChildID in Children:
                if self._hasChildren(ChildID):
                    self._killChildren(ChildID)
                if self._childType(ChildID):
                    self._killProcess(ID)
                elif self._childType(ChildID)+1:
                    self._killThread(ID)
                else:
                    raise TypeError("Child is neither a thread nor a process")
                self._sort()


    def _killDead(self):
        for p in self.processes:
            if not p.is_alive():
                self._freeNumber(self.processes[p])
                self._killProcess(self.processes[p])

        for t in self.threads:
            if not t.is_alive():
                self._freeNumber(self.threads[t])
                self._killThread(self.threads[t])
        self._sort()

    def _freeID(self):
        number = -1
        try:
            for i in range(0,2000):
                number = self.takenNumbers[i]
        except:
            return number + 1


    def _clearProcess(self):
        return len(self.processes) < self.cores * 10

    def createChild(self,Method,prefrence,parameters):
        ID = self._freeId()



    def _killProcess(self,ID):
        if self._exists(ID):
            if self._hasChildren(ID):
                self._killChildren(ID)
            if self._childType(ID) == self.ChildType.process:
                self.processes[ID].terminate()
            elif self._childType(ID) == self.ChildType.thread:
                self._killThread(ID)

    def createChildUnlinked(self,Prefrence,Method):
        if(Prefrence):
            ID = self._createProcess(Method)
        else:
            ID = self._createThread(Method)

    def createParent(self,prefrence,Method,children):
        if(prefrence):
            parent = self._createProcess(Method)
            childID = []
            for child in children:


    def linkOrphan(self,ParentID):
