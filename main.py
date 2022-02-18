import mtgsdk as mtg
import tinydb as tdb

db = tdb.TinyDB('mtg.json')
run = True
ids = []
cards_n = []
failed = []
cards = {}

with open('LIST.txt') as f:
    for item in f.readlines():
        ids.append(item)
        print(f'Reading Line: {item}')
    print()
    print()
    print('Parsing collected ids.')
    for i in range(len(ids)):
        ids[i] = ids[i].split(',')
        print(f'{i * round((100/len(ids)), 3)}%')
    print('100% Done!')
    print()
    print()
    for i in range(len(ids)):
        for j in range(len(ids[i])):
            ids[i][j] = ids[i][j].rstrip()

print('Collecting card data')
i = 0
for item in ids:
    i += 1
    print(f'{i * round((100/len(ids)), 3)}%')
    try:
        c = list(mtg.Card.where(name=item[0], year=int(item[1]), number=int(item[2])).all())[0]
        cards_n.append(c.name)
        cards[c.name] = {'Name': c.name, 'Mana Cost': c.mana_cost, 'CMC': c.cmc, 'Color(s)': c.colors,
                         'Type': c.type, 'Subtype(s)': c.subtypes, 'Rarity': c.rarity, 'Text': c.text,
                         'Pow/Tough': f'{c.power}/{c.toughness}', 'Loyalty': c.loyalty, 'Image': c.image_url}
    except IndexError:
        failed.append(item)
        print(f'Card with attributes {item} failed to load.')

for item in cards.keys():
    cards[item]['Count'] = cards_n.count(item)

with open('failed.txt', 'w+') as f:
    f.write(str(failed))
    print('Check failed.txt to view failed cards.')

print()
print()
db.insert(cards)
print(cards)
print('Inserted to mtg.json')
