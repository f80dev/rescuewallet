import requests



class Network:
	api_endpoint=""
	api_key=""
	ledger_client = None
	chain_id="osmosis-1"
	unity="uosmo"

	def __init__(self,endpoint="",api_key="",chain_id="",unity="uosmo",json_chain=None):
		self.api_endpoint=endpoint
		self.api_key=api_key
		self.chain_id=chain_id
		self.unity=unity
		if json_chain:
			#voir https://github.com/cosmos/chain-registry
			cfg=requests.get(json_chain).json()
			#self.ledger_client=LedgerClient(cfg)



	def create_account(self,solde=10):
		pass
		#https://github.com/hukkin/cosmospy#generating-a-wallet


	def api(self,service:str,body=None):
		headers = {"Content-Type": "application/json"}
		if self.api_key:
			headers["x-allthatnode-api-key"]=self.api_key
		if service.startswith("http"):
			url=service
		else:
			if not service.startswith("/"):service="/"+service
			url=self.api_endpoint+service

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
		if self.ledger_client is None:
			rc=self.api("/cosmos/bank/v1beta1/balances/"+addr)
			solde= int(rc["balances"][0]["amount"])/1000000
		else:
			solde=self.ledger_client.query_bank_balance(addr)
		return solde


	def explorer(self,addr,_type="account"):
		pass


	def transfer(self,_from:str,_to:str,amount:float):
		#voir https://github.com/hukkin/cosmospy#generating-a-wallet
		tx_signed=self.sign(_from.replace("4271",""))
		tx_signed.add_transfer(recipient=_to,amount=int(amount*1000000),denom=self.unity)
		result=self.exec(tx_signed.get_pushable())
		return result


	def get_transactions(self,addr):
		self.api()


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


