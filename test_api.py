from time import sleep

from Osmosis import Osmosis
from Pool import Pool
from Task import Task
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




def test_batch(to_addr=ADDRESSES["safe"]["osmosis"], private_key:str=PRIV):
	network=Osmosis("testnet")
	pool=Pool()
	pool.add(Task(private_key,to_addr,0.01,now()+3,network,occurence=3))
	solde0=network.balance(to_addr)

	for i in range(100):
		n_exec=pool.run()
		sleep(0.1)

	solde1=network.balance(to_addr)

	network.explorer(network.get_address(private_key))




def test_send(to_addr=ADDRESSES["safe"]["osmosis"], private_key:str=PRIV):
	net=Osmosis(network="testnet")
	solde0=net.balance(to_addr)
	for i in range(10):
		rc=net.transfer(private_key,to_addr,0.02)
	sleep(10)
	solde1=net.balance(to_addr)
	solde=solde1-solde0
	print("Solde "+str(solde))
	assert solde>0




def test_balance(addr=ADDRESSES["hack"]["osmosis"]):
	#rc=Cosmos("https://rpc-cosmoshub.ecostake.com").balance(addr)
	#assert rc>=0
	network=Osmosis(network="testnet")
	#latest=network.block_latest()
	#infos=network.node_infos()
	rc=network.balance(addr)
	assert rc>=0
