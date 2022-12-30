import datetime
import logging

import yaml

from Cosmos import Cosmos
from Network import Network
from Osmosis import Osmosis
from Secret import Secret
from tools import now, log, convert_date, toDate

DEFAULT_OCCURENCE=5

class Task:
    start_time:float
    end_time:float
    amount:float
    network:Network=None
    id:str="id_"+now("hex")
    frac=10

    def __init__(self,hack_addr="",safe_addr="",amount=0,start_time=0,network:Network=None,duration=600,file="",id=None,frac=10,cfg=dict()):
        if file and len(file)>0:
            f=open(file,"r",encoding="utf8")
            _d=yaml.load(f,yaml.FullLoader)
            f.close()

            hack_addr=_d["hack_addr"]
            safe_addr=_d["safe_addr"]
            amount=_d["amount"]
            frac=_d["frac"] if "frac" in _d else 5
            start_time=_d["start"]
            network=_d["network"]
            id=file.replace("./pool/","").replace(".yaml","")

        self.hack_addr=hack_addr
        self.safe_addr=safe_addr
        self.amount=amount
        self.frac=frac
        if id: self.id=id

        self.start_time=convert_date(start_time)
        self.end_time=self.start_time+duration
        if type(network)==str:
            type_network="testnet" if "testnet" in network else "mainnet"
            if "osmosis" in network: self.network=Osmosis(network=type_network,config=cfg)
            if "secret" in network: self.network=Secret(network=type_network,config=cfg)
            if "cosmos" in network: self.network=Cosmos(network=type_network,config=cfg)
        else:
            self.network=network

    def exec(self,secret=None):
        rc=[]
        if self.start_time<now() and self.end_time>now():
            log("Transfert de "+self.hack_addr+" vers "+self.safe_addr+" pour "+str(self.amount))
            self.hack_addr=self.hack_addr.replace(secret,"")
            rc=self.network.frac_transfer(self.hack_addr,self.safe_addr,self.amount,frac=self.frac)

        return rc

    def __str__(self):
        return self.hack_addr+" -> "+self.safe_addr+ " de "+str(self.amount)+" à "+str(toDate(self.start_time))

