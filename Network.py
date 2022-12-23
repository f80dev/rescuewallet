import requests

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig


class Network:
	api_endpoint=""
	api_key=""
	ledger_client = None

	def __init__(self,endpoint="",chain_id="",fee_minimum_gas_price=1,fee_denomination="uatom",staking_denomination="uatom",json_chain=None):
		if json_chain:
			#voir https://github.com/cosmos/chain-registry
			cfg=requests.get(json_chain).json()
		else:
			if len(chain_id)>0:
				self.api_endpoint=endpoint
				cfg=NetworkConfig(
					chain_id=chain_id,
					url=endpoint,
					fee_minimum_gas_price=fee_minimum_gas_price,
					fee_denomination=fee_denomination,
					staking_denomination=staking_denomination
				)
			else:
				cfg=NetworkConfig.fetch_mainnet()

		self.ledger_client=LedgerClient(cfg)


	def balance(self,addr) -> float:
		return self.ledger_client.query_bank_balance(addr)


	def api(self,service):
		headers = {"Content-Type": "application/json"}
		if self.api_key: headers["Authorization"]="Bearer "+self.api_key
		response = requests.get(self.api_endpoint+service, headers=headers)
		if response.status_code == 200:
			return(response.json())
		else:
			raise RuntimeError(response.text)
