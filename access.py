import tinydb as tdb
from tinydb import Query
import sys
from rich.table import Table
from rich.console import Console

db = tdb.TinyDB('mtg.json')
Card = Query()
t = Table(width=200)
c = Console(color_system='standard')

args = sys.argv[1:]

t.add_column('Name', no_wrap=True)
t.add_column('Mana Cost', no_wrap=True)
t.add_column('CMC', no_wrap=True)
t.add_column('Color(s)', no_wrap=True)
t.add_column('Type', no_wrap=True)
t.add_column('Rarity', no_wrap=True)
t.add_column('Text', no_wrap=False)
t.add_column('Power/Toughness', no_wrap=True)
t.add_column('Loyalty', no_wrap=True)
t.add_column('Set', no_wrap=True)
t.add_column('Count', no_wrap=True)


for i in db:
    col = str(i["Color(s)"])
    col = col.strip('[]')
    col = col.replace("'", "")
    t.add_row(i["Name"], str(i["Mana Cost"]), str(i["CMC"]), col, i["Type"], i["Rarity"], i["Text"], i["Pow/Tough"], str(i["Loyalty"]), i["Set"])

c.print(t)

if args:
    match args[0]:
        case '-n' | '--name':
            for item in db.search(Card['Name'] == args[1]):
                print(item)
    #     case '-mc' | '--cmc':
    #         print('CMC')
    #     case '-c' | '--colors':
    #         print('Color(s)')
    #     case '-t' | '--type':
    #         print('Type')
    #     case '-st' | '--subtypes':
    #         print('Subtype(s)')
    #     case '-r' | '--rarity':
    #         print('Rarity')
    #     case '-it' | '--intext':
    #         print('Searching texts...')
    #     case '-pt' | '--powtough':
    #         print('power/toughness')
    #     case '-s' | '--sort':
    #         print('sorted')
