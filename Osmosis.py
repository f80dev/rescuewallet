from osmopy import Transaction, privkey_to_address
from Network import Network

# voir le détail des https://docs.figment.io/api-reference/node-api/osmosis-lcd/
class Osmosis (Network):
	def __init__(self,config:dict,network="mainnet"):
		#voir https://www.allthatnode.com/osmosis.dsrv
		super().__init__(config["osmosis"],type_network=network)

	def get_address(self,key):
		return privkey_to_address(privkey=bytes.fromhex(key))

	def exec(self,signed_tx):
		url=self.config[self.type_network]["rpc"]
		rc=self.api(url,signed_tx)
		message=rc["result"]["log"] if "result" in rc else "Pas de resultat à la requete"
		return {"transaction":rc,"message":message}

	def explorer(self,addr:str,_type="account"):
		url="https://www.mintscan.io/osmosis/"+_type+"/"+addr
		if "testnet" in self.type_network:
			url=url.replace("//www.","//testnet.").replace("/osmosis","/osmosis-testnet")
		print("Ouvrir "+url)
		return url


	def sign(self,private_key,mode="broadcast_tx_async"):
		# https://pypi.org/project/osmopy/
		addr=self.get_address(private_key)
		_account=self.api("auth/accounts/"+addr)
		signed_tx = Transaction(
			privkey=bytes.fromhex(private_key),
			account_num=int(_account["result"]["value"]["account_number"]),
			sequence=int(_account["result"]["value"]["sequence"]),
			fee=1000,
			fee_denom=self.unity,
			gas=200000,
			memo="",
			chain_id=self.config[self.type_network]["chain_id"],
			sync_mode=mode
		)
		return signed_tx
