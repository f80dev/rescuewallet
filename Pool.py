import logging

from Task import Task


class Pool:
    pool:[Task]=[]
    log: logging.Logger

    def __init__(self,poolname:str="MaPool"):
        self.log= logging.Logger(poolname,logging.INFO)

    def add(self,task:Task):
        self.pool.append(task)

    def raz(self):
        self.pool.clear()

    def run(self):
        n_exec=0
        for t in self.pool:
            if t.exec(self.log): n_exec=n_exec+1
        return n_exec