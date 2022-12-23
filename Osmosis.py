from Network import Network

class Osmosis (Network):
	def __init__(self):
		super().__init__(json_chain="https://raw.githubusercontent.com/cosmos/chain-registry/master/osmosis/chain.json")

	def balance(self,addr):
		rc=self.api("accounts/"+addr+"/balance")
		return rc["data"]
