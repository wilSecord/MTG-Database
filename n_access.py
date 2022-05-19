import tinydb as tdb
from tinydb import Query
import tkinter as tk
from tkinter import ttk
import re
from PIL import ImageTk, Image

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

        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

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
    search.grid(row=0, column=1, sticky='EW')
    tree.bind('<ButtonRelease-1>', lambda event: select_item(event, tree.focus()))
    tree.grid(row=1, column=1)

    search.bind('<Return>', lambda event: insert_to_tv(srch(search.get())))

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
    att = ['Name', 'Mana Cost', 'CMC', 'Color(s)', 'Type', 'Subtype(s)', 'Rarity', 'Pow/Tough', 'Loyalty']
    card_prev = tk.Canvas(win, width=700, bg='#3d424d', highlightthickness=0)
    im = Image.open(f'imgs/{arg["Name"].replace("/", "")}.ppm')
    img = ImageTk.PhotoImage(im.resize((335, 466)))
    for i in range(len(att)):
        card_prev.create_text(15, 25 + (i * 50), anchor='w', text=f'{att[i]}: {arg[att[i]]}', justify=tk.LEFT, width=200, fill="#FFFFFF")
    card_prev.create_text(15, 475, anchor='nw', text=f'Text: {arg["Text"]}', justify=tk.LEFT, width=200, fill="#FFFFFF")
    card_prev.create_image(250, 25, anchor='nw', image=img)
    card_prev.photo = img
    card_prev.grid(row=1, column=2, sticky='news')


def srch(in_str_lst):
    searches = in_str_lst.split('+')
    search_terms = [{'n': ''}, {'cmc': ''}, {'c': ''}, {'t': ''}, {'st': ''}, {'r': ''}, {'pt': ''}, {'l': ''}]

    for in_txt in searches:
        print(in_txt)
        if in_txt:
            match in_txt[0]:

                case 'c':
                    clrs = []
                    arg = in_txt[1:].replace('-', '')
                    if arg:
                        if arg.upper() == 'NONE':
                            clrs = None
                            results = db.search(Card['Color(s)'] is None)
                            # search_terms.append({'c': None})
                        else:
                            if arg[0] == '=':
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
                                # search_terms.append({'c': ['=', clrs]})
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
                                # search_terms.append({'c': [arg]})
                        return results

                case 'n':
                    arg = in_txt[1:].replace('-', '')
                    results = db.search(Card['Name'].search(str(arg), flags=re.IGNORECASE))
                    # search_terms.append({'n': str(arg)})
                    return results

                case 't':
                    arg = in_txt[1:].replace('-', '')
                    results = db.search(Card['Text'].search(str(arg), flags=re.IGNORECASE))
                    # search_terms.append({'t': str(arg)})
                    return results

                case 'm':
                    arg = in_txt[1:].replace('-', '')
                    match arg[0]:
                        case '>':
                            arg = arg.replace('>', '')
                            results = db.search(Card['CMC'] > int(arg))
                            # search_terms.append({'cmc': int(arg)})
                            return results

                        case '<':
                            arg = arg.replace('<', '')
                            results = db.search(Card['CMC'] < int(arg))
                            # search_terms.append({'cmc': int(arg)})
                            return results

                        case '=':
                            arg = arg.replace('=', '')
                            results = db.search(Card['CMC'] == int(arg))
                            # search_terms.append({'cmc': int(arg)})
                            return results
                case 's':
                    arg = in_txt[1:].replace('-', '')
                    results = db.search(Card['Subtype(s)'].any(arg.capitalize()))
                    return results

                case 'r':
                    arg = in_txt[1:].replace('-', '')
                    results = db.search(Card['Rarity'] == str(arg.capitalize()))
                    return results

        else:
            return _all

    print(search_terms)
    return search_terms

    # for item in searches:
    #     searches.search

def main():
    insert_to_tv(srch(''))
    win.mainloop()



if __name__ == '__main__':
    main()