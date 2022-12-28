from cosmospy import Transaction

from Network import Network

#voir https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/chain.json
#voir le détail des api : https://docs.figment.io/api-reference/node-api/cosmos-lcd/#/txs

class Cosmos(Network):

	def __init__(self,network="mainnet"):
		#voir https://www.allthatnode.com/project.dsrv?seq=fe6339fdc0faac2b63f7a7d8fb16a47151c3989d
		api_key="CWgWXZRlcVfqfr8tKQdGXekcArhOdu4H"
		if network=="mainnet":
			super().__init__(chain_id="cosmoshub-4",unity="uatom",endpoint="https://cosmos-mainnet-rpc.allthatnode.com:1317",api_key=api_key)
		else:
			super().__init__(chain_id="cosmoshub-4",unity="uatom",endpoint="https://cosmos-testnet-rpc.allthatnode.com:1317",api_key=api_key)

	def sign(self,private_key):
		# https://v1.cosmos.network/rpc/v0.45.1
		signed_tx = Transaction(
			privkey=bytes.fromhex(private_key),
			account_num=11335,
			sequence=0,
			fee=1000,
			fee_denom=self.unity,
			gas=37000,
			memo="",
			chain_id=self.ledger_client.network_config.chain_id if self.ledger_client else self.chain_id,
			sync_mode="sync"
		)

		#signed_tx=self.api("txs/sign",body={"tx":payload,"priv_key":private_key})
		return signed_tx
