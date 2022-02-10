import mtgsdk as mtg
import tinydb as tdb

db = tdb.TinyDB('mtg.json')
run = True
ids = []
inserts = {}

with open('LIST.txt') as f:
    for item in f.readlines():
        ids.append(item)
    print(ids)
    for i in range(len(ids) - 1):
        ids[i] = ids[i].rstrip()
    print(ids)
