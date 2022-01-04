from tkinter import *
import add
import core
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

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

    def dodaj_produkt():
        sztuki = e5.get()
        if sztuki != '':
            sztuki = float(sztuki)
        else:
            sztuki = 'NaN'

        waga = e6.get()
        if waga != '':
            waga = float(waga)
        else:
            waga = 'NaN'
        add.add_product_to_store(str(e1.get()), float(e2.get()), float(e3.get()), float(e4.get()), sztuki, waga)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)
        e5.delete(0, END)
        e6.delete(0, END)

    e_button = Button(top, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=dodaj_produkt).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=top.destroy).pack()


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

    def dodaj_do_lodowki():
        sztuki = e3.get()
        if sztuki != '':
            sztuki = float(sztuki)
        else:
            sztuki = 'NaN'

        waga = e4.get()
        if waga != '':
            waga = float(waga)
        else:
            waga = 'NaN'
        add.add_product_to_fridge(str(e1.get()), str(e2.get()), sztuki, waga)
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)
        e4.delete(0, END)

    enter_button = Button(top, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                          command=dodaj_do_lodowki).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                             command=top.destroy).pack()


def open_posilek():
    top = Toplevel()
    top.title("Dodaj posiłek")
    label1 = Label(top, text='Podaj nazwę posiłku:')
    label2 = Label(top, text='Podaj skłaniki:')
    label3 = Label(top, text='Podaj porę posiłku:')
    e1 = Entry(top, width=30)
    e2 = Entry(top, width=30)
    e3 = Entry(top, width=30)

    label1.pack()
    e1.pack()
    label2.pack()
    e2.pack()
    label3.pack()
    e3.pack()
    def dodaj_posilek():
        add.append_new_dish(str(e1.get()), str(e2.get()), str(e3.get()))
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)

    enter_button = Button(top, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                          command=dodaj_posilek).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                             command=top.destroy).pack()


def open_tabu():
    top = Toplevel()
    top.title("Wyznacz menu")
    lista_priorytetow = []
    parametry = [10, 1, 10, 0, 5, -500]
    def open_preferencje():
        top2 = Toplevel()
        top2.title("Dodaj preferencje")
        label1 = Label(top2, text='Podaj nazwę posiłku:')
        label2 = Label(top2, text='Podaj datę:')
        label3 = Label(top2, text='Podaj porę posiłku:')
        e1 = Entry(top2, width=30)
        e2 = Entry(top2, width=30)
        e3 = Entry(top2, width=30)
        label1.pack()
        e1.pack()
        label2.pack()
        e2.pack()
        label3.pack()
        e3.pack()
        def dodaj_preferencje():
            lista_priorytetow.append((str(e1.get()), str(e2.get()), str(e3.get())))
            e1.delete(0, END)
            e2.delete(0, END)
            e3.delete(0, END)
        enter_button = Button(top2, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                              command=dodaj_preferencje).pack()
        button_quit_top = Button(top2, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                                 command=top2.destroy).pack()
    def open_parametry():
        top2 = Toplevel()
        top2.title("Dobierz parametry")

        label1 = Label(top2, text='Podaj ilość iteracji:')
        e1 = Entry(top2, width=30)
        label2 = Label(top2, text='Wybierz sposób znalezienia bazy początkowej:')
        clicked = StringVar()
        clicked.set('baza losowa')
        drop2 = OptionMenu(top2, clicked, 'baza losowa', 'najlepsza baza')
        label3 = Label(top2, text='Podaj przez ile iteracji ma obowiązywać blokada:')
        e3 = Entry(top2, width=30)
        label4 = Label(top2, text='Wybierz metodę wyboru sąsiada:')
        clicked2 = StringVar()
        clicked2.set('metoda dokładna')
        drop4 = OptionMenu(top2, clicked2, 'metoda dokładna', 'metoda losowa (przybliżona)', 'metoda losowa')
        label5 = Label(top2, text='Podaj ilość wyników wybranych metodą losową:')
        e5 = Entry(top2, width=30)
        label6 = Label(top2, text='Podaj wartość parametru przerwania szukania rozwiązania:')
        e6 = Entry(top2, width=30)

        label1.pack()
        e1.pack()
        label2.pack()
        drop2.pack()
        label3.pack()
        e3.pack()
        label4.pack()
        drop4.pack()
        label5.pack()
        e5.pack()
        label6.pack()
        e6.pack()
        def dodaj_parametry():
            parametry[0] = e1.get()
            if str(clicked.get()) == 'baza losowa':
                parametry[1] = 0
            else:
                parametry[1] = 1

            parametry[2] = e3.get()

            if str(clicked2.get()) == 'metoda dokładna':
                parametry[3] = 0
            elif str(clicked2.get()) == 'metoda losowa (przybliżona)':
                parametry[3] = 1
            else:
                parametry[3] = 2
            parametry[4] = e5.get()
            parametry[5] = e6.get()

            e1.delete(0, END)
            clicked.set('baza losowa')
            e3.delete(0, END)
            clicked2.set('metoda dokładna')
            e5.delete(0, END)
            e6.delete(0, END)

        enter_button = Button(top2, text="Akceptuj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                              command=dodaj_parametry).pack()
        button_quit_top = Button(top2, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                                 command=top2.destroy).pack()

    def open_wynik():
        top2 = Toplevel()
        top2.title("Zobacz wynik")
        w, bp, wynik = core.week_set(parametry[0], parametry[1], parametry[2], parametry[3], parametry[4], parametry[5])
        label6 = Label(top2, text='Menu', bg=bg)
        label6.grid(row=0, column=0, columnspan=7)
        for i in range(7):
            label = Label(top2, text='Dzień {}'.format(i+1), bg=bg)
            label.grid(row=1, column=i)

        for i in range(len(wynik)):
            for j in range(len(wynik[i])):
                label = Label(top2, text=str(wynik[i][j]))
                label.grid(row=j+2, column=i)



        def statystyki():
            for i in range(7):
                label = Label(top2, text='Najlepszy wynik: {}'.format(bp[i]))
                label.grid(row=10, column=i)


        enter_button = Button(top2, text="Statystyki dla nerdów", fg=fg, bg=bg, activebackground=ab,
                              command=statystyki).grid(row=7, column=6)
        button_quit_top = Button(top2, text='Wyjdź', fg=fg, bg=bg, activebackground=ab,
                                 command=top2.destroy).grid(row=8, column=6)

    button1 = Button(top, text='Dodaj preferencje', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                     command=open_preferencje).pack()
    button2 = Button(top, text='Dobierz parametry', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                     command=open_parametry).pack()
    button3 = Button(top, text='Zobacz wynik', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                     command=open_wynik).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                             command=top.destroy).pack()





button1 = Button(root, text='Dodaj produkt', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_produkt).pack()
button2 = Button(root, text='Dodaj produkt do lodówki', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_produkt_lodowka).pack()
button3 = Button(root, text='Dodaj posiłek', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_posilek).pack()
button4 = Button(root, text='Wyznacz menu', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_tabu).pack()
button_quit = Button(root, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=root.quit).pack()


root.mainloop()