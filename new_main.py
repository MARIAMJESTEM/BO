from tkinter import *
import pandas as pd
import add
import core
import datetime
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import matplotlib
import matplotlib.pyplot as plt

root = Tk()
root.title("Menu")
x = 2
y = 25
fg = 'black'
bg = 'lightskyblue'
ab = 'blue'
#---------------------------------------------------------------------------------------------------
def open_preferencje():
    top = Toplevel()
    top.title("Dodaj preferencje")
    label1 = Label(top, text='Podaj nazwę posiłku:')
    label2 = Label(top, text='Podaj datę:')
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

    def dodaj_preferencje():
        core.lista_priorytetów.append((str(e2.get()), str(e1.get()), str(e3.get())))
        e1.delete(0, END)
        e2.delete(0, END)
        e3.delete(0, END)

    enter_button = Button(top, text="Dodaj", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                          command=dodaj_preferencje).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                             command=top.destroy).pack()


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

def usun_preferencje():
    top = Toplevel()
    top.title("Usuń preferencję")
    label1 = Label(top, text='Podaj nazwę posiłku:')
    e1 = Entry(top, width=30)

    label1.pack()
    e1.pack()

    def usun_ja():
        preferencja = str(e1.get())
        for i in core.lista_priorytetów:
            if i[1] == preferencja:
                core.lista_priorytetów.remove(i)
        print(core.lista_priorytetów)

    enter_button = Button(top, text="Usuń", height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                          command=usun_ja).pack()
    button_quit_top = Button(top, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                             command=top.destroy).pack()



def open_wynik():
    core.CAL = int(e1.get())

    if str(clicked3.get()) == 'lodówka 1':
        lodowka = pd.read_csv("bazy_danych\lodowki_do_testow\lod1.csv", sep=';')
    elif str(clicked3.get()) == 'lodówka 2':
        lodowka = pd.read_csv("bazy_danych\lodowki_do_testow\lod2.csv", sep=';')
    else:
        lodowka = pd.read_csv("bazy_danych\lodowki_do_testow\lod3.csv", sep=';')

    core.lodowka = lodowka
    liczba_iteracji = int(e4.get())
    blokada = int(slider5.get())

    if str(clicked6.get()) == 'losowe':
        rozwiazanie_startowe = 0
    else:
        rozwiazanie_startowe = 1

    if str(clicked7.get()) == 'dokładna':
        sasiedzi = 0
    elif str(clicked7.get()) == 'losowa':
        sasiedzi = 1
    else:
        sasiedzi = 2

    metoda_iter = int(slider12.get())
    kara = int(slider13.get())
    core.kara_global = kara
    kara_kalorie = int(slider14.get())
    core.kara_cal_global = kara_kalorie
#-----------------------Wywołanie funkcji dających wynik----------------------------------------
    if str(clicked11.get()) == 'set':
        wykresy, najlepsze_punkty, menu, lista_zakupow, kalorie, iteracje = core.week_set(lodowka,
                                        liczba_iteracji, blokada, rozwiazanie_startowe, sasiedzi, metoda_iter)
    else:
        wykresy, najlepsze_punkty, menu, lista_zakupow, kalorie, iteracje= core.week_set_tabu_product(lodowka,
                                        liczba_iteracji, blokada, rozwiazanie_startowe, sasiedzi,metoda_iter)

    top2 = Toplevel()
    top2.title("Zobacz wynik")
    label6 = Label(top2, text='Menu')
    label6.grid(row=0, column=3)
    for i in range(7):
        label = Label(top2, text='Dzień {}'.format(i + 1), bg=bg)
        label2 = Label(top2, text='Kalorie: {}'.format(round(kalorie[i])), bg='green')
        label.grid(row=1, column=i)
        label2.grid(row=8, column=i)

    for i in range(len(menu)):
        for j in range(len(menu[i])):
            label = Label(top2, text=str(menu[i][j]))
            label.grid(row=j + 2, column=i)
    def wykres1():
        plt.plot(wykresy[0])
        plt.title('Najlepszy wynik: {}'.format(round(najlepsze_punkty[0])))
        plt.show()
    def wykres2():
        plt.plot(wykresy[1])
        plt.title('Najlepszy wynik: {}'.format(round(najlepsze_punkty[1])))
        plt.show()
    def wykres3():
        plt.plot(wykresy[2])
        plt.title('Najlepszy wynik: {}'.format(round(najlepsze_punkty[2])))
        plt.show()
    def wykres4():
        plt.plot(wykresy[3])
        plt.title('Najlepszy wynik: {}'.format(round(najlepsze_punkty[3])))
        plt.show()
    def wykres5():
        plt.plot(wykresy[4])
        plt.title('Najlepszy wynik: {}'.format(round(najlepsze_punkty[4])))
        plt.show()
    def wykres6():
        plt.plot(wykresy[5])
        plt.title('Najlepszy wynik: {}'.format(round(najlepsze_punkty[5])))
        plt.show()
    def wykres7():
        plt.plot(wykresy[6])
        plt.title('Najlepszy wynik: {}'.format(round(najlepsze_punkty[6])))
        plt.show()
    def zakupy():
        top3 = Toplevel()
        top3.title("Lista zakupów")
        label1 = Label(top3, text='Nazwa produktu', bg=bg)
        label1.grid(row=0, column=0)
        label2 = Label(top3, text='Liczba sztuk', bg=bg)
        label2.grid(row=0, column=1)
        label3 = Label(top3, text='Waga', bg=bg)
        label3.grid(row=0, column=2)
        label4 = Label(top3, text='Cena', bg=bg)
        label4.grid(row=0, column=3)
        for i in range(len(lista_zakupow)):
            for j in range(4):
                if j == 3:
                    label5 = Label(top3, text=str(round(lista_zakupow[i][j], 2)))
                    label5.grid(row=i + 1, column=j)
                else:
                    label5 = Label(top3, text=str(lista_zakupow[i][j]))
                    label5.grid(row=i + 1, column=j)

    def statystyki():
        for i in range(7):
            label = Label(top2, text='Najlepszy wynik: {}'.format(round(najlepsze_punkty[i])))
            label.grid(row=14, column=i)
            label = Label(top2, text='Liczba iteracji: {}'.format(round(iteracje[i])))
            label.grid(row=15, column=i)

            p_up, p_stay, p_down = core.change_pkt(wykresy[i])
            label = Label(top2, text='Procent popraw: {}%'.format(p_up))
            label.grid(row=17, column=i)
            label = Label(top2, text='Procent bez zmian: {}%'.format(p_stay))
            label.grid(row=18, column=i)
            label = Label(top2, text='Procent pogorszeń: {}%'.format(p_down))
            label.grid(row=19, column=i)
        button = Button(top2, text='Pokaż wykres', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                        command=wykres1).grid(row=16, column=0)
        button = Button(top2, text='Pokaż wykres', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                        command=wykres2).grid(row=16, column=1)
        button = Button(top2, text='Pokaż wykres', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                        command=wykres3).grid(row=16, column=2)
        button = Button(top2, text='Pokaż wykres', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                        command=wykres4).grid(row=16, column=3)
        button = Button(top2, text='Pokaż wykres', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                        command=wykres5).grid(row=16, column=4)
        button = Button(top2, text='Pokaż wykres', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                        command=wykres6).grid(row=16, column=5)
        button = Button(top2, text='Pokaż wykres', height=x, width=y, fg=fg, bg=bg, activebackground=ab,
                        command=wykres7).grid(row=16, column=6)

    glupia_biblioteka = Label(top2, text='')
    glupia_biblioteka.grid(row=9, column=6)
    glupia_biblioteka2 = Label(top2, text='')
    glupia_biblioteka2.grid(row=13, column=6)
    button_zakupy = Button(top2, text="Wyświetl listę zakupów", fg=fg, bg=bg, activebackground=ab,
                          command=zakupy).grid(row=10, column=6)
    enter_button = Button(top2, text="Statystyki dla nerdów", fg=fg, bg=bg, activebackground=ab,
                          command=statystyki).grid(row=11, column=6)
    button_quit_top = Button(top2, text='Wyjdź', fg=fg, bg=bg, activebackground=ab,
                             command=top2.destroy).grid(row=12, column=6)



#----------------------------PANEL GŁÓWNY----------------------------------------------------------
label1 = Label(root, text="Ustaw liczbę kalorii: ").grid(row=1, column=2)
e1 = Entry(root, width=30)
e1.grid(row=2, column=2)

button2 = Button(root, text='Dodaj preferencje', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_preferencje).grid(row=7, column=0)

label3 = Label(root, text='Wybierz lodówkę').grid(row=1, column=4)
clicked3 = StringVar()
clicked3.set('lodówka 1')
drop3 = OptionMenu(root, clicked3, 'lodówka 1', 'lodówka 2', 'lodówka 3').grid(row=2, column=4)

label4 = Label(root, text="Ustaw liczbę iteracji: ").grid(row=3, column=2)
e4 = Entry(root, width=30)
e4.grid(row=4, column=2)

label5 = Label(root, text="Jak długo blokujemy produkt/listę: ").grid(row=5, column=2)
slider5 = Scale(root, from_=1, to=15, orient=HORIZONTAL)
slider5.set(8)
slider5.grid(row=6, column=2)

label6 = Label(root, text='Wybierz rozwiązanie startowe: ').grid(row=3, column=4)
clicked6 = StringVar()
clicked6.set('losowe')
drop6 = OptionMenu(root, clicked6, 'losowe', 'najlepsze').grid(row=4, column=4)

label7 = Label(root, text='Wybierz metodę szukania sąsiadów: ').grid(row=5, column=4)
clicked7 = StringVar()
clicked7.set('dokładna')
drop7 = OptionMenu(root, clicked7, 'dokładna', 'losowa', 'losowa z priorytetami').grid(row=6, column=4)

button8 = Button(root, text='Dodaj produkt', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_produkt).grid(row=1, column=0)

button9 = Button(root, text='Dodaj produkt do lodówki', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_produkt_lodowka).grid(row=3, column=0)

button10 = Button(root, text='Dodaj posiłek', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_posilek).grid(row=5, column=0)

label11 = Label(root, text='Wybierz metodę tabu: ').grid(row=7, column=4)
clicked11 = StringVar()
clicked11.set('set')
drop11 = OptionMenu(root, clicked11, 'set', 'produkt').grid(row=8, column=4)

label12 = Label(root, text="Ilość sąsiadów").grid(row=7, column=2)
slider12 = Scale(root, from_=1, to=10, orient=HORIZONTAL)
slider12.set(4)
slider12.grid(row=8, column=2)

label13 = Label(root, text="Wartość kary").grid(row=1, column=6)
slider13 = Scale(root, from_=-300, to=-50, orient=HORIZONTAL)
slider13.set(-150)
slider13.grid(row=2, column=6)

label14 = Label(root, text="Wartość kary za kalorie").grid(row=3, column=6)
slider14 = Scale(root, from_=2, to=20, orient=HORIZONTAL)
slider14.set(5)
slider14.grid(row=4, column=6)

Button15 = Button(root, text='Usuń preferencję', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=usun_preferencje).grid(row=9, column=0)

Label16 = Label(root, text='Preferencje').grid(row=0, column=8, columnspan=3)
Label17 = Label(root, text='Data').grid(row=1, column=8)
Label18 = Label(root, text='Nazwa posiłku').grid(row=1, column=9)
Label19 = Label(root, text='Pora posiłku').grid(row=1, column=10)
licznik_p = 0
for i in core.lista_priorytetów:
    label3000 = Label(root, text=''.format(i[0])).grid(row=2 + licznik_p, column=8)
    label3001 = Label(root, text=''.format(i[1])).grid(row=2 + licznik_p, column=9)
    label3002 = Label(root, text=''.format(i[2])).grid(row=2 + licznik_p, column=10)

button12 = Button(root, text='Pokaż wynik', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=open_wynik).grid(row=7, column=6)
button_quit = Button(root, text='Wyjdź', height=x, width=y, fg=fg, bg=bg, activebackground=ab, command=root.quit).grid(row=9, column=6)








root.mainloop()





#-------------------------------------------------------------------------------------------------------------
