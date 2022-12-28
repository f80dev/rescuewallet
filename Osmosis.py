from osmopy import Transaction, privkey_to_address

from Network import Network

# voir le détail des https://docs.figment.io/api-reference/node-api/osmosis-lcd/
class Osmosis (Network):
	def __init__(self,network="mainnet"):
		api_key="vxLOEqL3dgp1ligsKnjHL9BJUbVs8hOB"
		#voir https://www.allthatnode.com/osmosis.dsrv
		url="https://osmosis-"+network+"-rpc.allthatnode.com:1317"

		super().__init__(
			endpoint=url,
			api_key=api_key,
			chain_id="osmosis-1" if network=="mainnet" else "bostrom-testnet-1",
			unity="uosmo"
		)
		# else:
		# 	#voir https://docs.allthatnode.com/protocols/osmosis
		# 	#voir https://docs.fetch.ai/CosmPy/connect-to-network/
		# 	super().__init__(
		# 		chain_id="osmosis-1",
		# 		endpoint="grpc+https://osmosis-mainnet-rpc.allthatnode.com:26657/"+api_key,
		# 		fee_minimum_gas_price=5000000000,
		# 		fee_denomination="osmo",
		# 		staking_denomination="osmo"
		# 	)

		#super().__init__(json_chain="https://raw.githubusercontent.com/cosmos/chain-registry/master/osmosis/chain.json")
		#super().__init__(endpoint="https://cosmoshub-4--lcd--archive.datahub.figment.io/")
		#super().__init__(endpoint="https://osmosis-mainnet-archive.allthatnode.com:1317")


	def get_address(self,private_key):
		return privkey_to_address(privkey=bytes.fromhex(private_key))

	def exec(self,signed_tx):
		network="mainnet" if "mainnet" in self.api_endpoint else "testnet"
		#voir https://www.allthatnode.com/osmosis.dsrv
		url="https://osmosis-"+network+"-rpc.allthatnode.com:26657"
		rc=self.api(url,signed_tx)
		message=rc["result"]["log"] if "result" in rc else "Pas de resultat à la requete"
		return {"transaction":rc,"message":message}

	def explorer(self,addr:str,_type="account"):
		url="https://www.mintscan.io/osmosis/"+_type+"/"+addr
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
			chain_id="osmo-test-4" if "testnet" in self.api_endpoint else "osmosis-1",
			sync_mode=mode
		)
		return signed_tx
