from os import listdir
from time import sleep

from Task import Task
from tools import now

class Pool:
    pool:[Task]=[]
    log_path=None
    logs:[str]=[]
    secret:str=""

    def log(self,line:str):
        if len(line)>0:
            content=now("str")+" - "+line
            print(content)
            self.logs.append(content)

    def __init__(self,secret,config):
        self.pool=[]
        self.secret=secret
        self.config=config

    def add(self,task:Task):
        if not task.id in [x.id for x in self.pool]:
            self.pool.append(task)

    def load_from_dir(self,dir):
        print("Chargement du répertoire "+dir)
        if not dir.endswith("/"):dir=dir+"/"
        for f in listdir(dir):
            if f.endswith("yaml"):
                self.add(Task(file=dir+f,cfg=self.config))
        return self.count()


    def write_log(self,path:str):
        print("Ecriture du journal")
        self.logs.insert(0,now("str"))
        with open(path,"a") as f:
            f.writelines("\n".join(self.logs))
            f.close()

    def raz(self):
        self.pool.clear()


    def get_state(self):
        rc=["Etat de la pool"]
        rc=rc+[str(x) for x in self.pool]
        return "\n".join(rc)

    def run(self,end_process=None):
        print("Execution de la boucle")
        if end_process is None: end_process=now()+10
        while end_process>now():
            for t in self.pool:
                rc=t.exec(secret=self.secret)
                self.log("\n".join(rc))
                sleep(0.1)

    def count(self):
        return len(self.pool)

    def clear(self):
        self.raz()

