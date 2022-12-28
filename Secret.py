from Network import Network

class Secret (Network):
	def __init__(self):
		super().__init__(json_chain="https://raw.githubusercontent.com/cosmos/chain-registry/master/secretnetwork/chain.json") #voir https://docs.scrt.network/secret-network-documentation/development/connecting-to-the-network#api-endpoints

	def balance(self,addr):
		rc=self.api("accounts/"+addr+"/balance")
		return rc["data"]
