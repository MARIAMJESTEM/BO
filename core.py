import pandas as pd
import numpy as np
import random
import datetime

#Wczytanie baz danych do programu
sniadania = pd.read_csv("sniadania.csv", sep = ';')
sniadania2 = pd.read_csv("sniadanie2.csv", sep = ';')
obiad = pd.read_csv("obiad.csv", sep = ';')
podwieczorek = pd.read_csv("sniadanie2.csv", sep = ';')
kolacja = pd.read_csv("kolacja.csv", sep = ';')
lodowka = pd.read_csv("lodowka.csv", sep =';')
s = pd.read_csv("sklep.csv", sep =';')
sklep = s.set_index("Nazwa")

CAL = 3000
PRO = 1000

actualna_data = 28-11-2021


def find_current_date():
    """
    Funkcja wyznaczająca aktualną datę

    :return: Aktualna data
    """
    return datetime.datetime.now().date()


def calculate_product_to_fridge_points(date):
    """
    Funkcja licząca punkty dla produktów z lodówki

    :param date: Data produktu
    :return: Liczba punktów za produkt
    """
    date = datetime.date.fromisoformat(date)
    days = (date - find_current_date()).days
    if days < 0:
        return -2000                           # NA PRZYSZŁOŚĆ ZABEZPIECZENIE PRZED BŁĘDNĄ DATĄ
    elif days > 5:
        return 0
    else:
        return (6 - days) * 10


def read_sklad(idx = 0, baza = '', produkt = 0):
    """
    Funkcja odczytująca produkty z dania i przerabiająca je na listę

    :param idx: indeks dania
    :param baza: nazwa bazy z której wyjmujemy produkty
    :return: lista składu dania
    """
    if produkt == 0:
        str_list = baza['Produkty'][idx][1:-1]
    else:
        str_list = produkt[1:-1]
    l = len(str_list)
    s_list = []
    list = []
    s = 1
    element = 1
    for i in range(1,l):
        if str_list[i] == '[':
            s = i + 1
            element = 1
            list.append(s_list)
            s_list = []
        if str_list[i] == ',' and str_list[i - 1] != ']' or str_list[i] == ']':
            pro = str_list[s:i]
            s = i + 1
            if element == 2 or element == 3:
                s_list.append(int(pro))
            else:
                s_list.append(pro)
            element += 1
        if i == l - 1:
            list.append(s_list)

    return list


def calculation_points_for_dish(idx: int = 0, baza: str = '', produkt = 0):
    """
    Funkcja licząca punkty za danie

    :param idx: Indeks w bazie
    :param baza: Baza
    :param produkt: Lista produktów jeśli dodajemy nowy prosukt
    :return: Punkty za danie
    """
    sum = 0
    if produkt == 0:
        list = read_sklad(idx, baza)
    else:
        list = read_sklad(produkt = produkt)
    for j in range(len(list)):
        c = list[j][0]
        df = lodowka[lodowka["Nazwa"] == c]
        if df.empty == True:
            sum += sklep["Punkty"][c]
        else:
            sum += max(df["Punkty"])

    return sum


def roz_start(n: int):
    """
    Funkcja wyznaczająca rozwiązanie początkowe

    :param n:Wybór dań w sposób 0 - losowy 1 - najlepsze dania
    :return: Rozwiązanie początkowe w formie listy
    """
    if n == 0:
        IS = sniadania['Nazwa_dania'][random.randint(0,len(sniadania) - 1)]
        IIS = sniadania2['Nazwa_dania'][random.randint(0,len(sniadania2)- 1)]
        O = obiad['Nazwa_dania'][random.randint(0,len(obiad)- 1)]
        P = podwieczorek['Nazwa_dania'][random.randint(0,len(podwieczorek)- 1)]
        K = kolacja['Nazwa_dania'][random.randint(0,len(kolacja)- 1)]

        return [IS,IIS,O,P,K]

    if n == 1:
        n_baz = [sniadania,sniadania2,obiad,podwieczorek,kolacja]
        w_baz = [0,0,0,0,0]
        for n in range(len(n_baz)):
            max = n_baz[n]['Punkty'][0]
            idx_i = 0
            for i in range(1, len(n_baz[n])):
                if n_baz[n]['Punkty'][i] > max:
                    max = n_baz[n]['Punkty'][i]
                    idx_i = i

            w_baz[n] = n_baz[n]['Nazwa_dania'][idx_i]

        return w_baz


def standard_deviation_calories_and_protein(result):
    """
    Funkcja wyznaczająca odchylenie standardowe dla kalorii i białka

    :param result: Wynik który chcemy zbadać
    :return: Odchylenie standardowe kalori i białka
    """
    K = 0
    B = 0
    n_baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    for baz,res in zip(n_baz,result):
        df = baz[baz['Nazwa_dania'] == res]
        K += max(df['Kalorie'])
        B += max(df['Białko'])

    return np.std([K,CAL]), np.std([B,PRO])

def append_tabu(nazwa, baza, tabu):
    df = baza[baza["Nazwa_dania"] == nazwa] #zamina liczby tabu na tabu musze wyciągnąc indeks chyba
    df['Tabu'] == tabu

# append_tabu("Jabłko",sniadania2,3)
# print(sniadania2[['Nazwa_dania','Tabu']])









