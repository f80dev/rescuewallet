from time import sleep

import requests

from tools import transaction_to_str


class Network:
	type_network:str="testnet"
	unity:str
	config:dict

	def __init__(self,config:dict=dict(),type_network="testnet"):
		self.config=config
		self.unity=config["unity"]
		self.type_network=type_network

		# if json_chain:
		# 	#voir https://github.com/cosmos/chain-registry
		# 	cfg=requests.get(json_chain).json()
		# 	#self.ledger_client=LedgerClient(cfg)


	def get_address(self,key:str):
		pass


	def create_account(self,solde=10):
		pass
		#https://github.com/hukkin/cosmospy#generating-a-wallet


	def api(self,service:str,body=None):
		headers = {"Content-Type": "application/json"}
		if "apikey" in self.config:
			headers[self.config["apikey"]["header"]]=self.config["apikey"]["value"]

		if service.startswith("http"):
			url=service
		else:
			if not service.startswith("/"):service="/"+service
			url=self.config[self.type_network]["rest"]+service

		if body is None:
			response = requests.get(url, headers=headers)
		else:
			response = requests.post(url,data=body, headers=headers)

		if response.status_code == 200:
			return(response.json())
		else:
			raise RuntimeError(response.text)


	def balance(self,addr) -> float:
		#voir https://docs.osmosis.zone/apis/interact-rest
		rc=self.api("/cosmos/bank/v1beta1/balances/"+addr)
		for balance in rc["balances"]:
			if balance["denom"]==self.unity:
				return int(balance["amount"])/1000000
		return 0


	def explorer(self,addr,_type="account"):
		pass


	def transfer(self,_from:str,_to:str,amount:float):
		#voir https://github.com/hukkin/cosmospy#generating-a-wallet
		tx_signed=self.sign(_from)
		tx_signed.add_transfer(recipient=_to,amount=int(amount*1000000),denom=self.unity)
		result=self.exec(tx_signed.get_pushable())
		return transaction_to_str(result)


	def frac_transfer(self,key:str,_to:str,amount:float,frac=10) -> [dict]:
		rc=[]
		_from=self.get_address(key)
		solde=self.balance(_from)
		new_balance=solde

		while solde-new_balance<amount or new_balance<0.001:
			if new_balance<amount/frac:
				rc.append(self.transfer(key,_to,new_balance*0.99))
				break

			for i in range(frac):
				rc.append(self.transfer(key,_to,amount/frac))
				sleep(0.1)

			new_balance=self.balance(_from)

		return rc



	def get_transactions(self,addr):
		pass

	def sign(self,private_key:str):
		pass

	def exec(self,service:str,signed_tx:dict):
		#voir https://v1.cosmos.network/rpc/v0.45.1
		#voir le nombre de transactions sur
		#voir https://docs.figment.io/api-reference/node-api/cosmos-lcd/#/txs
		resp=self.api(service,body=signed_tx)
		return resp

	def net_infos(self):
		rc=self.api("net_info")
		return rc


	def node_infos(self):
		rc=self.api("node_info")
		return rc

	def block_latest(self):
		rc=self.api("/blocks/latest")
		return rc