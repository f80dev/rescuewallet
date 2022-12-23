from Network import Network

#voir https://raw.githubusercontent.com/cosmos/chain-registry/master/cosmoshub/chain.json
class Cosmos(Network):

	def __init__(self,endpoint="https://grpc-cosmoshub.blockapsis.com:429"):
		super().__init__(chain_id="cosmoshub-4",
		                 fee_denomination="uatom",
		                 endpoint=endpoint,
		                 staking_denomination="uatom")
