from tkinter import *
import add
#import core


root = Tk()
root.title("Menu")
x = 2
y = 25
fg = 'black'
bg = 'lightskyblue'
ab = 'blue'


def open_produkt():
    top = Toplevel()
    top.title("Dodaj produkt do sklepu")
    label1 = Label(top, text='Podaj nazwę produktu:')
    label2 = Label(top, text='Podaj cenę produktu:')
    label3 = Label(top, text='Podaj ilość kalorii:')
    label4 = Label(top, text='Podaj ilość białka:')
    label5 = Label(top, text='Podaj ilość sztuk:')
    label6 = Label(top, text='Podaj wagę produktu:')
    e1 = Entry(top, width=30)
    e2 = Entry(top, width=30)
    e3 = Entry(top, width=30)
    e4 = Entry(top, width=30)
    e5 = Entry(top, width=30)
    e6 = Entry(top, width=30)

    label1.pack()
    e1.pack()
    label2.pack()
    e2.pack()
    label3.pack()
    e3.pack()
    label4.pack()
    e4.pack()
    label5.pack()
    e5.pack()
    label6.pack()
    e6.pack()

    def dodaj_produkt(name, price, calories, protein, pieces='NaN', weight='NaN'):
        add.add_product_to_store(name, price, calories, protein, pieces, weight)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)

    enter_button = Button(top, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                          command=dodaj_produkt(e1.get(), e2.get(), e3.get(), e4.get(), e5.get(), e6.get())).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                         command=top.destroy).pack()


def open_produkt_lodowka():
    top = Toplevel()
    top.title("Dodaj produkt do lodówki")
    label1 = Label(top, text='Podaj nazwę produktu:')
    label2 = Label(top, text='Podaj datę ważności:')
    label3 = Label(top, text='Podaj ilość sztuk:')
    label4 = Label(top, text='Podaj wagę produktu:')
    e1 = Entry(top, width=30)
    e2 = Entry(top, width=30)
    e3 = Entry(top, width=30)
    e4 = Entry(top, width=30)

    label1.pack()
    e1.pack()
    label2.pack()
    e2.pack()
    label3.pack()
    e3.pack()
    label4.pack()
    e4.pack()

    def dodaj_do_lodowki(name, date, pieces='NaN', weight='NaN'):
        add.add_product_to_fridge(name, date, pieces, weight)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)

    enter_button = Button(top, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                          command=dodaj_do_lodowki(e1.get(), e2.get(), e3.get(), e4.get())).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                             command=top.destroy).pack()


def open_posilek():
    top = Toplevel()
    top.title("Dodaj posiłek")
    label1 = Label(top, text='Podaj nazwę posiłku:')
    label2 = Label(top, text='Podaj skłaniki:')
    label3 = Label(top, text='Podaj porę posiłku:')
    label4 = Label(top, text='Podaj link do przepisu:')
    e1 = Entry(top, width=30)
    e2 = Entry(top, width=30)
    e3 = Entry(top, width=30)
    e4 = Entry(top, width=30)

    label1.pack()
    e1.pack()
    label2.pack()
    e2.pack()
    label3.pack()
    e3.pack()
    label4.pack()
    e4.pack()

    def dodaj_posilek(name, produkt, pora, link):
        add.append_new_dish(name, produkt, pora, link)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)

    enter_button = Button(top, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                          command=dodaj_posilek(e1.get(), e2.get(), e3.get(), e4.get())).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                             command=top.destroy).pack()


def open_tabu():
    return

button1 = Button(root, text='Dodaj produkt', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_produkt)
button2 = Button(root, text='Dodaj produkt do lodówki', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_produkt_lodowka)
button3 = Button(root, text='Dodaj posiłek', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_posilek)
button4 = Button(root, text='Wyznacz menu', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_tabu)
button_quit = Button(root, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=root.quit)


button1.pack()
button2.pack()
button3.pack()
button4.pack()
button_quit.pack()

root.mainloop()