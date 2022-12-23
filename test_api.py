from Cosmos import Cosmos
from Osmosis import Osmosis
from Secret import Secret


OSMOSIS_ACCOUNT="osmo1gcewetsfm006yzvk9r4hmt2jgeur6qc9e4yek2"
SECRET_ACCOUNT="secret1gcewetsfm006yzvk9r4hmt2jgeur6qc9ntrqay"
COSMOS_ACCOUNT="cosmos1gcewetsfm006yzvk9r4hmt2jgeur6qc93whfqc"

def test_balance(addr=COSMOS_ACCOUNT):
	rc=Cosmos("https://rpc-cosmoshub.ecostake.com").balance(addr)
	assert rc>=0