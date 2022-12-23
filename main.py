from Osmosis import Osmosis
from Secret import Secret

def balance(network:str,addr:str):
	if "osmosis" in network: rc=Osmosis().balance(addr)
	if "osmosis" in network: rc=Secret().balance(addr)
	return rc
