import mtgsdk as mtg
import tinydb as tdb

db = tdb.TinyDB('mtg.json')
run = True
ids = []
cards_n = []
failed = []

with open('LIST.txt') as f:
    for item in f.readlines():
        ids.append(item)
    print(ids)
    for i in range(len(ids)):
        ids[i] = ids[i].split(',')
    for i in range(len(ids)):
        for j in range(len(ids[i])):
            ids[i][j] = ids[i][j].rstrip()
    print(ids)

for item in ids:
    try:
        c = list(mtg.Card.where(name=item[0], year=int(item[1]), number=int(item[2])).all())[0]
        cards_n.append(c.name)
    except IndexError:
        failed.append(item)
        print(f'Card with attributes {item} failed to load.')
print(failed)
print(cards_n)