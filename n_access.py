import tinydb as tdb
from tinydb import Query
import tkinter as tk
from tkinter import ttk

db = tdb.TinyDB('mtg.json')
Card = Query()
win = tk.Tk()
win.title('MTG Card DB')
win.state('zoomed')
win['bg'] = '#3d424d'
cols = {'name': ['Name', 150], 'mc': ['Mana Cost', 100], 'col': ['Color(s)', 100], 'type': ['Type', 250],
        'rarity': ['Rarity', 80], 'pt': ['Pow/Tough', 80], 'count': ['Count', 80]}
tree = ttk.Treeview(win, columns=list(cols.keys()), show='headings', height=30, selectmode='browse')

def select_item(event, d):
    d = tree.item(d)
    out = db.search(Card["Name"].search(d['values'][0]))
    print(out[0])

def setup():
    for k, v in cols.items():
        tree.heading(k, anchor='w', text=v[0])
        tree.column(k, anchor='w', width=v[1])

    tree.grid(row=0, column=1, sticky='nsew')

    scrollbar = ttk.Scrollbar(win, orient=tk.VERTICAL, command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.grid(row=0, column=0, sticky='ns')
    tree.bind('<ButtonRelease-1>', lambda event: select_item(event, tree.focus()))

    return tree

def replace_none(t, o):
    if t != o:
        temp = t
    else:
        temp = ''
    return temp

def insert():
    tree = setup()
    list_names = []
    for item in db:
        list_names.append(item['Name'])

    for item in db:
        pt = replace_none(item['Pow/Tough'], 'None/None')
        mc = replace_none(item['Mana Cost'], None)
        if item['Color(s)']:
            col = str(item["Color(s)"])
            col = col.strip('[]')
            col = col.replace("'", "")
        else:
            col = ''
        tree.insert('', tk.END, values=(item['Name'], mc, col, item['Type'],
                                        item['Rarity'], pt, str(list_names.count(item["Name"])), item['Set']))



def main():
    insert()
    win.mainloop()


if __name__ == '__main__':
    main()