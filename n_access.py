import tinydb as tdb
from tinydb import Query
import tkinter as tk
from tkinter import ttk
import re
from PIL import ImageTk, Image
import io

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
        if d:
            d = tree.item(d)
            out = db.search(Card["Name"].search(d['values'][0]))
            create_txt(out[0])


    def sort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        for k, v in cols.items():
            tv.heading(k, text=v[0], command=lambda _col=k: \
                sort_column(tv, _col, not reverse))

    for k, v in cols.items():
        tree.heading(k, anchor='w', text=v[0], command=lambda _col=k: sort_column(tree, _col, False))
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
    # tree.bind('a', lambda event: sort_column(tree, 'name', True))

    return tree


tree = setup_tv()


def insert_to_tv(cards):
    children = tree.get_children('')

    for child in children:
        tree.delete(child)

    def replace_none(t, o):
        if t != o:
            temp = t
        else:
            temp = ''
        return temp

    list_names = []
    if cards:
        for item in cards:
            list_names.append(item['Name'])



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
    # if len(win.winfo_children()) > 4:
    #     win.winfo_children()[4].destroy()
    att = ['Name', 'Mana Cost', 'CMC', 'Color(s)', 'Type', 'Subtype(s)', 'Rarity', 'Pow/Tough', 'Loyalty']
    card_prev = tk.Canvas(win, width=500, bg='#3d424d', highlightthickness=1)
    im = Image.open(f'imgs/{arg["Name"].replace("/", "")}.ppm')
    img = ImageTk.PhotoImage(im)
    for i in range(len(att)):
        card_prev.create_text(15, 25 + (i * 50), anchor='w', text=f'{att[i]}: {arg[att[i]]}', justify=tk.LEFT, width=200, fill="#FFFFFF")
    card_prev.create_text(15, 475, anchor='nw', text=f'Text: {arg["Text"]}', justify=tk.LEFT, width=200, fill="#FFFFFF")
    card_prev.create_image(200, 25, anchor='nw', image=img)
    # lbl = tk.Label(win, image=img)
    card_prev.photo = img
    # lbl.grid(row=1, column=3)
    card_prev.grid(row=1, column=2, sticky='news')
    for item in card_prev.find_all():
        print(card_prev.coords(item))


def srch(in_txt):
    if in_txt:
        match in_txt[0]:

            case 'c':
                clrs = []
                arg = in_txt.replace('c', '').replace('(', '').replace(')', '')
                if arg:
                    if arg.upper() == 'NONE':
                        clrs = None
                        # noinspection PyTypeChecker
                        results = db.search(Card['Color(s)'] is None)
                    else:
                        if arg[0] == '=':
                            print('startswith =')
                            arg = arg.replace('=', '')
                            for char in arg:
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
                            results = db.search(Card['Color(s)'] == clrs)
                        else:
                            for char in arg:
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

                            results = db.search(Card['Color(s)'].any(clrs))
                    return results

            case 'n':
                arg = in_txt.replace('n', '').replace('(', '').replace(')', '')
                results = db.search(Card['Name'].search(str(arg), flags=re.IGNORECASE))
                return results

            case 't':
                arg = in_txt.replace('t', '').replace('(', '').replace(')', '')
                results = db.search(Card['Text'].search(str(arg), flags=re.IGNORECASE))
                return results

            case 'm':
                arg = in_txt.replace('m', '').replace('(', '').replace(')', '')
                match arg[0]:
                    case '>':
                        arg = arg.replace('>', '')
                        results = db.search(Card['CMC'] > int(arg))
                        return results

                    case '<':
                        arg = arg.replace('<', '')
                        results = db.search(Card['CMC'] < int(arg))
                        return results

                    case '=':
                        arg = arg.replace('=', '')
                        results = db.search(Card['CMC'] == int(arg))
                        return results

    else:
        return _all

def main():
    insert_to_tv(srch(''))
    # card_prev = tk.Canvas(win, bg='#3d424d', highlightthickness=1)
    # card_prev.create_text(15, 400, anchor='w', text='test')
    # img = tk.PhotoImage(file='imgs/Steppe Glider.ppm')
    # card_prev.create_image(0, 0, anchor='nw', image=img)
    # card_prev.grid(row=1, column=2, sticky='news')
    win.mainloop()



if __name__ == '__main__':
    main()