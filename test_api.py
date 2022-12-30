import os
from os.path import exists
from time import sleep

import pytest
import yaml

from Osmosis import Osmosis
from Pool import Pool
from Task import Task
from privacy import PRIV, SECRET
from tools import now

ADDRESSES = {
	"hack":{
		"osmosis":"osmo1xrzk0rhn5nq4nlmvcps8n83360ezj0t9ludh3a",
		"secret":"secret1gcewetsfm006yzvk9r4hmt2jgeur6qc9ntrqay",
		"cosmos":"cosmos1xrzk0rhn5nq4nlmvcps8n83360ezj0t9h87880"
	},
	"safe":{
		"osmosis":"osmo1gcewetsfm006yzvk9r4hmt2jgeur6qc9e4yek2",
		"secret":"secret1gcewetsfm006yzvk9r4hmt2jgeur6qc9ntrqay",
		"cosmos":"cosmos1gcewetsfm006yzvk9r4hmt2jgeur6qc93whfqc"
	}
}


def get_config(validator_name="allthatnode"):
	rc=yaml.load(open("./config.yaml","r"),yaml.FullLoader)
	return rc["validators"][validator_name]

@pytest.fixture()
def net():
	return Osmosis(get_config()["osmosis"],network="testnet")


@pytest.fixture()
def pool():
	return Pool(SECRET,get_config("allthatnode"))


def test_add_task(net,pool,_dest=ADDRESSES["safe"]["osmosis"]):
	pool.add(Task(ADDRESSES["hack"]["osmosis"],_dest,1,"2022-12-30 19:30:44",net,id="1"))
	pool.add(Task(ADDRESSES["hack"]["osmosis"],_dest,1,"30/12/2022 19:30:44",net,id="2"))
	pool.add(Task(ADDRESSES["hack"]["osmosis"],_dest,1,now()+10,net,id="3"))
	print(pool.get_state())
	assert pool.count()==3
	pool.clear()
	assert pool.count()==0


def test_send(net,to_addr=ADDRESSES["safe"]["osmosis"], private_key:str=PRIV,amount=0.02):
	solde0=net.balance(to_addr)
	for i in range(10):
		rc=net.transfer(private_key,to_addr,amount)
		sleep(0.01)

	sleep(3)
	solde1=net.balance(to_addr)
	solde=solde1-solde0
	print("Solde "+str(solde))
	assert solde>0


def test_frac_transfer(net,to_addr=ADDRESSES["safe"]["osmosis"], private_key:str=PRIV):
	print(net.explorer(net.get_address(private_key)))
	rc=net.frac_transfer(private_key,to_addr,10,10)
	assert len(rc)>0


def test_all_process(net,pool,private_key:str=PRIV,to_addr=ADDRESSES["safe"]["osmosis"],amount=10,network="testnet"):
	solde=net.balance(net.get_address(private_key))
	pool.add(Task(private_key,to_addr,amount,now()+5,net))
	pool.run()
	assert solde-net.balance(net.get_address(private_key))>amount


def test_with_file(pool,net):
	pool.clear()
	pool.add(Task(file="./pool/test_osmo.yaml",cfg=net.config))
	pool.add(Task(file="./pool/test_osmo.yaml",cfg=net.config))
	assert pool.count()==1


def test_load_pool():
	pool=Pool()
	pool.load_from_dir("./pool")
	assert pool.count()==1


def test_log(pool):
	if exists("./log.txt"): os.remove("./log.txt")
	pool.log("line 1")
	pool.log("line 2")
	pool.log("line 3")
	pool.write_log("./log.txt")
	assert exists("./log.txt")


def test_all_process_mainnet():
	test_all_process(network="mainnet",amount=7)



def test_balance(addr=ADDRESSES["hack"]["osmosis"]):
	#rc=Cosmos("https://rpc-cosmoshub.ecostake.com").balance(addr)
	#assert rc>=0
	network=Osmosis(network="testnet")
	#latest=network.block_latest()
	#infos=network.node_infos()
	rc=network.balance(addr)
	assert rc>=0



def test_batch(net,pool,to_addr=ADDRESSES["safe"]["osmosis"], private_key:str=PRIV):
	from_addr=net.get_address(private_key)
	pool.add(Task(private_key,to_addr,0.01,now()+3,net))
	print(pool.get_state())
	solde0=net.balance(from_addr)

	pool.run(end_process=now()+20)
	print(pool.get_log())

	solde1=net.balance(from_addr)

	net.explorer(net.get_address(private_key))
