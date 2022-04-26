import tinydb as tdb
from tinydb import Query
import tkinter as tk
from tkinter import ttk

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
    scrollbar.pack(side='left', fill='y')
    tree.bind('<ButtonRelease-1>', lambda event: select_item(event, tree.focus()))
    tree.pack(side='left', fill='y')

    return tree

def insert_to_tv():
    tree = setup_tv()
    list_names = []
    for item in _all:
        list_names.append(item['Name'])

    def replace_none(t, o):
        if t != o:
            temp = t
        else:
            temp = ''
        return temp



    # for item in range(len(list(db))):
    #     print(type(dict(list(db)[item])))

    # for item in list_names:
    #     print(item)


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
                                        item['Rarity'], pt, str(list_names.count(item["Name"]))))


    children = tree.get_children('')
    for child in children:
        vals = tree.item(child, 'values')
        if list_names.count(vals[0]) > 1:
            tree.delete(child)
            list_names.remove(vals[0])

def create_txt(arg):
    if len(win.winfo_children()) > 2:
        win.winfo_children()[2].destroy()
    att = ['Name', 'Mana Cost', 'CMC', 'Color(s)', 'Type', 'Subtype(s)', 'Rarity', 'Text', 'Pow/Tough', 'Loyalty']
    card_prev = tk.Canvas(win, bg='#FFFFFF', height=500, width=400)
    for i in range(len(att)):
        card_prev.create_text(15, 25 + (i * 50), anchor='w', text=f'{att[i]}: {arg[att[i]]}', justify=tk.LEFT, width=350)
    card_prev.pack(side='top')


def main():
    insert_to_tv()
    # print(db.search(Card['Name'] == 'Plains'))
    win.mainloop()


if __name__ == '__main__':
    main()