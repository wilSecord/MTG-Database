import rich.box
import tinydb as tdb
from tinydb import Query
import sys
from rich.table import Table
from rich.console import Console
import os

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
t.add_column('Rarity', no_wrap=True)
t.add_column('Text', no_wrap=False)
t.add_column('Power/Toughness', no_wrap=True)
t.add_column('Loyalty', no_wrap=True)
t.add_column('Count', no_wrap=True)



if not args:
    for i in db:
        if i["Name"] not in cs:
            col = str(i["Color(s)"])
            col = col.strip('[]')
            col = col.replace("'", "")
            t.add_row(i["Name"], str(i["Mana Cost"]), str(i["CMC"]), col, i["Type"], i["Rarity"], i["Text"],
                      i["Pow/Tough"], str(i["Loyalty"]), str(ln.count(i["Name"])))
            cs.append(i["Name"])
    c.print(t)
else:
    match args[0]:
        case '-n' | '--name':
            for i in db.search(Card['Name'] == args[1]):
                if i["Name"] not in cs:
                    col = str(i["Color(s)"])
                    col = col.strip('[]')
                    col = col.replace("'", "")
                    t.add_row(i["Name"], str(i["Mana Cost"]), str(i["CMC"]), col, i["Type"], i["Rarity"], i["Text"],
                              i["Pow/Tough"], str(i["Loyalty"]), str(ln.count(i["Name"])))
                    cs.append(i["Name"])
            c.print(t)
        case '-mc' | '--cmc':
            args[1] = float(args[1])
            for i in db.search(Card['CMC'] == args[1]):
                if i["CMC"] not in cs:
                    col = str(i["Color(s)"])
                    col = col.strip('[]')
                    col = col.replace("'", "")
                    t.add_row(i["Name"], str(i["Mana Cost"]), str(i["CMC"]), col, i["Type"], i["Rarity"], i["Text"],
                              i["Pow/Tough"], str(i["Loyalty"]), str(ln.count(i["Name"])))
                    cs.append(i["CMC"])
            c.print(t)
        case '-c' | '--colors':
            clrs = []
            if args[1].upper() == "NONE":
                print('None')
            else:
                for char in args[1]:
                    match char.upper():
                        case 'A':
                            print('Blue')
                        case 'B':
                            print('Black')
                        case 'R':
                            print('Red')
                        case 'W':
                            print('White')
                        case 'G':
                            print('Green')
                        case 'C':
                            print('Colorless')
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

