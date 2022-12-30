import sys

from Pool import Pool
from tools import now, get_config

pool=Pool(
	secret=sys.argv[1],
	config=get_config(sys.argv[2] if len(sys.argv)>2 else "allthatnode")
)

print("Lancement du serveur avec "+pool.secret)
while True:
	pool.load_from_dir("./pool")
	print(pool.get_state())
	pool.run()
	pool.write_log("./log.txt")
