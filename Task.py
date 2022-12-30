import datetime
import logging

import yaml

from Cosmos import Cosmos
from Network import Network
from Osmosis import Osmosis
from Secret import Secret
from tools import now, log, convert_date, toDate, open_html_file, send_mail

DEFAULT_OCCURENCE=5
OFFSET=10





class Task:
    start_time:float
    end_time:float
    amount:float
    network:Network=None
    id:str="id_"+now("hex")
    frac=10
    contact=""
    status="waiting"

    def __init__(self,hack_addr="",safe_addr="",amount=0,
                 start_time=0,network:Network=None,duration=600,
                 file="",id=None,frac=10,cfg=dict(),contact=""):
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
            id=file.replace("./pool/","").replace(".yaml","") if not "id" in _d else _d["id"]
            contact=_d["contact"] if "contact" in _d else ""

        self.hack_addr=hack_addr
        self.safe_addr=safe_addr
        self.amount=amount
        self.frac=frac
        if id: self.id=id
        self.contact=contact

        self.start_time=convert_date(start_time)
        self.end_time=self.start_time+duration
        if type(network)==str:
            type_network="testnet" if "testnet" in network else "mainnet"
            if "osmosis" in network: self.network=Osmosis(network=type_network,config=cfg)
            if "secret" in network: self.network=Secret(network=type_network,config=cfg)
            if "cosmos" in network: self.network=Cosmos(network=type_network,config=cfg)
        else:
            self.network=network

    def send_contact(self,text:str):
        send_mail(open_html_file("mail_info",{"body":text}),self.contact,subject="Info Rescue Wallet")

    def exec(self,secret=None):
        rc=[]
        if self.status!="ending" and self.end_time<now(): self.status="ending"
        if self.start_time-OFFSET<now() and self.end_time>now():

            if self.status=="waiting":
                self.status="running"
                self.send_contact(self.__str__()+"<br><br>Process enclenché")

            log(self.__str__())
            self.hack_addr=self.hack_addr.replace(secret,"")
            rc=self.network.frac_transfer(self.hack_addr,self.safe_addr,self.amount,frac=self.frac)

        return rc

    def __str__(self):
        rc=self.hack_addr[:10]+".. -> "\
               +self.safe_addr[:10]+".. pour "+str(self.amount)\
               +" "+self.network.unity+" de "+str(toDate(self.start_time))+" à "+str(toDate(self.end_time))
        rc=self.id+" ("+self.status+") "+rc
        return rc
