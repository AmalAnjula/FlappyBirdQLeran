import json
from itertools import chain
 
qval = {}
 
for x in chain(list(range(-40, 140, 10)), list(range(140, 421, 70))):
    for y in chain(list(range(-300, 180, 10)), list(range(180, 421, 60))):
        for v in range(-10, 11):
            qval[str(x) + "_" + str(y) + "_" + str(v)] = [0, 0]


fd = open("data/qval.json", "w")
json.dump(qval, fd)
fd.close()
