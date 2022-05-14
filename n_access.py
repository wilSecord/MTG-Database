import tinydb as tdb
from tinydb import Query
import tkinter as tk
from tkinter import ttk
import re

db = tdb.TinyDB('mtg.json')
_all = db.all()
Card = Query()
win = tk.Tk()
win.title('MTG Card DB')
win.state('zoomed')
win['bg'] = '#3d424d'



def setup_tv():
    cols = {'name': ['Name', 150], 'mc': ['Mana Cost', 100], 'col': ['Color(s)', 100], 'type': ['Type', 250],
            'rarity': ['Rarity', 80], 'pt': ['Pow/Tough', 80], 'count': ['Count', 80]}
    tree = ttk.Treeview(win, columns=list(cols.keys()), show='headings', height=38, selectmode='browse')

    def select_item(event, d):
        d = tree.item(d)
        out = db.search(Card["Name"].search(d['values'][0]))
        create_txt(out[0])

    for k, v in cols.items():
        tree.heading(k, anchor='w', text=v[0])
        tree.column(k, anchor='w', width=v[1])


    scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    search = tk.Entry(win)
    scrollbar.grid(row=1, column=0, sticky='WNS')
    # scrollbar.pack(side='left', fill='y')
    search.grid(row=0, column=1, sticky='EW')
    tree.bind('<ButtonRelease-1>', lambda event: select_item(event, tree.focus()))
    # tree.pack(side='left', fill='y')
    tree.grid(row=1, column=1)

    search.bind('<Return>', lambda event: insert_to_tv(srch(search.get())))

    return tree


tree = setup_tv()


def insert_to_tv(cards):
    children = tree.get_children('')

    for child in children:
        tree.delete(child)

    list_names = []
    for item in cards:
        list_names.append(item['Name'])

    def replace_none(t, o):
        if t != o:
            temp = t
        else:
            temp = ''
        return temp

    for item in cards:
        pt = replace_none(item['Pow/Tough'], 'None/None')
        mc = replace_none(item['Mana Cost'], None)
        if item['Color(s)']:
            col = str(item["Color(s)"])
            col = col.strip('[]')
            col = col.replace("'", "")
        else:
            col = ''
        tree.insert('', tk.END, values=(item['Name'], mc, col, item['Type'],
                                        item['Rarity'], pt, str(list_names.count(item["Name"]))))

    children = tree.get_children('')

    for child in children:
        vals = tree.item(child, 'values')
        if list_names.count(vals[0]) > 1:
            tree.delete(child)
            list_names.remove(vals[0])

def create_txt(arg):
    if len(win.winfo_children()) > 3:
        win.winfo_children()[3].destroy()
    att = ['Name', 'Mana Cost', 'CMC', 'Color(s)', 'Type', 'Subtype(s)', 'Rarity', 'Pow/Tough', 'Loyalty']
    card_prev = tk.Canvas(win, bg='#3d424d', height=500, width=400, highlightthickness=0)
    for i in range(len(att)):
        card_prev.create_text(15, 25 + (i * 50), anchor='w', text=f'{att[i]}: {arg[att[i]]}', justify=tk.LEFT, width=350, fill="#FFFFFF")
    card_prev.create_text(15, 475, anchor='nw', text=f'Text: {arg["Text"]}', justify=tk.LEFT, width=350, fill="#FFFFFF")
    # card_prev.pack(side='top')
    card_prev.grid(row=1, column=2, sticky='NS')


def srch(in_txt):
    if in_txt:
        match in_txt[0]:
            case 't':
                arg = in_txt.replace('t', '').replace('()', '')
                results = db.search(Card['Text'].search(str(arg), flags=re.IGNORECASE))
                return results
    else:
        return _all

def main():
    insert_to_tv(srch(''))
    # insert_to_tv(_all)
    # search()
    # print(db.search(Card['Name'] == 'Plains'))
    win.mainloop()



if __name__ == '__main__':
    main()