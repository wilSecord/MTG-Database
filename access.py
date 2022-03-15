import rich.box
import tinydb as tdb
from tinydb import Query
import sys
from rich.table import Table
from rich.console import Console
import os
import re

db = tdb.TinyDB('mtg.json')
Card = Query()
c = Console(color_system='windows')
t = Table(width=200, box=rich.box.ROUNDED, show_lines=True, header_style="bold")

args = sys.argv[1:]

cs = []
ln = []

for item in db:
    ln.append(item['Name'])

os.system('cls')


t.add_column('Name', no_wrap=True)
t.add_column('Mana Cost', no_wrap=True)
t.add_column('CMC', no_wrap=True)
t.add_column('Color(s)', no_wrap=True)
t.add_column('Type', no_wrap=True)
t.add_column('Subtype(s)', no_wrap=True)
t.add_column('Rarity', no_wrap=True)
t.add_column('Text', no_wrap=False)
t.add_column('Power/Toughness', no_wrap=True)
t.add_column('Loyalty', no_wrap=True)
t.add_column('Count', no_wrap=True)


def search(arg):
    for i in arg:
        if i["Name"] not in cs:
            col = str(i["Color(s)"])
            col = col.strip('[]')
            col = col.replace("'", "")
            st = str(i["Subtype(s)"])
            st = st.strip('[]')
            st = st.replace("'", "")
            t.add_row(i["Name"], str(i["Mana Cost"]), str(i["CMC"]), col, i["Type"], st, i["Rarity"], i["Text"],
                      i["Pow/Tough"], str(i["Loyalty"]), str(ln.count(i["Name"])))
            cs.append(i["Name"])
    c.print(t)


if not args:
    search(db)

else:
    match args[0]:

        case '-n' | '--name':
            search(db.search(Card.Name.matches(f'([A-z]*){args[1]}([A-z]*)', flags=re.IGNORECASE)))

        case '-mc' | '--cmc':
            args[1] = float(args[1])
            search(db.search(Card['CMC'] == args[1]))

        case '-c' | '--colors':
            clrs = []
            if args[1].upper() == "NONE":
                clrs = None
            else:
                for char in args[1]:
                    match char.upper():
                        case 'U':
                            clrs.append("Blue")
                        case 'B':
                            clrs.append("Black")
                        case 'R':
                            clrs.append("Red")
                        case 'W':
                            clrs.append("White")
                        case 'G':
                            clrs.append("Green")

            search(db.search(Card['Color(s)'] == clrs))

        case '-t' | '--type':
            search(db.search(Card['Type'] == args[1]))

        case '-st' | '--subtypes':
            search(db.search(Card['Subtype(s)'] == args[1]))

        case '-r' | '--rarity':
            search(db.search(Card['Rarity'] == args[1]))

    #     case '-it' | '--intext':
    #         print('Searching texts...')
    #     case '-pt' | '--powtough':
    #         print('power/toughness')
    #     case '-s' | '--sort':
    #         print('sorted')

