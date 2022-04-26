import mtgsdk as mtg
import tinydb as tdb
from rich.console import Console

db = tdb.TinyDB('mtg.json')
run = True
ids = []
cards_n = []
failed = []
cards = []
con = Console(color_system='standard')
ln = list(set([item['Name'] for item in db]))

with open('mtg.json', 'w+') as t:
    t.truncate(0)

with open('LIST.txt') as f:
    for item in f.readlines():
        ids.append(item)
    con.print('[green]Parsing collected ids.')

    for i in range(len(ids)):
        ids[i] = ids[i].split(';')
        con.print(f'[white]{round(i * round((100/len(ids)), 3), 1)}%')

    con.print('[white]100.0%')
    for i in range(len(ids)):
        for j in range(len(ids[i])):
            ids[i][j] = ids[i][j].rstrip()

con.print('\n[green]Collecting card data')
i = 0


for item in ids:
    i += 1
    con.print(f'[white]{round(i * round((100/len(ids)), 3), 1)}%')
    try:
        if item[0] not in cards_n:
            c = list(mtg.Card.where(name=item[0], year=int(item[1]), number=int(item[2])).all())[0]
            cards.append(c)
            db.insert({'Name': c.name, 'Mana Cost': c.mana_cost, 'CMC': c.cmc, 'Color(s)': c.colors,
                       'Type': c.type, 'Subtype(s)': c.subtypes, 'Rarity': c.rarity, 'Text': c.text,
                       'Pow/Tough': f'{c.power}/{c.toughness}', 'Loyalty': c.loyalty, 'Image': c.image_url,
                       'Set': c.set})
        else:
            for jtem in cards:
                if jtem.name == item[0]:
                    c = jtem
                    db.insert({'Name': c.name, 'Mana Cost': c.mana_cost, 'CMC': c.cmc, 'Color(s)': c.colors,
                               'Type': c.type, 'Subtype(s)': c.subtypes, 'Rarity': c.rarity, 'Text': c.text,
                               'Pow/Tough': f'{c.power}/{c.toughness}', 'Loyalty': c.loyalty, 'Image': c.image_url,
                               'Set': c.set})

        cards_n.append(c.name)

    except IndexError:
        failed.append(item)
        con.print(f'[red]Card with attributes [/red]{item}[red] failed to load.[/red]')

with open('failed.txt', 'w+') as f:
    f.write(str(failed))
    con.print('[red]Check failed.txt to check for failed cards.')
