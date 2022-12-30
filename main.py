import sys

import yaml

from Pool import Pool
from tools import now


pool=Pool(
	secret=sys.argv[1],
	config=yaml.load(open("./config.yaml","r"),yaml.FullLoader)
)
print("Lancement du serveur avec "+pool.secret)

while True:
	pool.load_from_dir("./pool")
	pool.run(end_process=now()+10*60)
	pool.write_log("./log.txt")
