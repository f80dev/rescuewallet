import datetime
import logging

from Network import Network
from tools import now

DEFAULT_OCCURENCE=5

class Task:
    start_time:float
    end_time:float
    amount:float
    network:Network

    def __init__(self,hach_addr,safe_addr,amount,start_time,network:Network,occurence=DEFAULT_OCCURENCE):
        self.hack_addr=hach_addr
        self.safe_addr=safe_addr
        self.amount=amount
        if type(start_time)==datetime: start_time=start_time.timestamp()
        self.start_time=start_time
        self.end_time=start_time+10
        self.network=network
        self.occurence=occurence

    def exec(self,log:logging.Logger=None):
        rc=False
        if self.start_time<now() and self.end_time>now():
            rc=True
            for i in range(self.occurence):
                if log: log.info("Transfert de "+self.hack_addr+" vers "+self.safe_addr+" pour "+str(self.amount))
                rc=self.network.transfer(self.hack_addr,self.safe_addr,self.amount/self.occurence)
                if log: log.info(rc["message"])

        return rc


