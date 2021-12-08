import pandas as pd
import numpy as np
import random
import datetime
from copy import deepcopy
import math

#Wczytanie baz danych do programu
sniadania = pd.read_csv("bazy_danych\sniadania.csv", sep = ';')
sniadania2 = pd.read_csv("bazy_danych\sniadanie2.csv", sep = ';')
obiad = pd.read_csv("bazy_danych\obiad.csv", sep = ';')
podwieczorek = pd.read_csv("bazy_danych\sniadanie2.csv", sep = ';')
kolacja = pd.read_csv("bazy_danych\kolacja.csv", sep = ';')
lodowka = pd.read_csv("bazy_danych\lodowka.csv", sep =';')
l_pomocnicza = pd.read_csv("bazy_danych\lodowka.csv", sep =';')
s = pd.read_csv("bazy_danych\produkty_w_sklepie.csv", sep =';')
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


# def actualization_fridge(lod, pro):
#     if len(pro) == 2:
#         l = lod[lod['Nazwa'] == pro[0]]
#         if pro[1] > l['Waga'][l.index[0]]:
#             s = sklep['Waga'][pro[0]]
#             ns = pro[1] - l['Waga'][l.index[0]]
#             p = np.ceil(ns/s)
#             ss = p*s-ns
#             sum = sklep["Punkty"][pro[0]] * p
#             lod['Waga'][l.index[0]] = ss
#             lod['Data_waznosci'][l.index[0]] = find_current_date() + datetime.timedelta(days = 14)
#         elif pro[1] == l['Waga'][l.index[0]]:
#             lod = lod.drop([l.index[0]], axis=0)
#             sum = l['Punkty'][l.index[0]]
#         else:
#             lod['Waga'][l.index[0]] = l['Waga'][l.index[0]] - pro[1]
#             sum = l['Punkty'][l.index[0]]
#
#     if len(pro) == 3:
#         l = lod[lod['Nazwa'] == pro[0]]
#         if pro[1] > l['Sztuka'][l.index[0]]:
#             s = sklep['Sztuka'][pro[0]]
#             ns = pro[1] - l['Sztuka'][l.index[0]]
#             p = np.ceil(ns / s)
#             ss = p * s - ns  # tu coś brakuje
#             sum = sklep["Punkty"][pro[0]] * p
#             lod['Sztuka'][l.index[0]] = ss
#             lod['Data_waznosci'][l.index[0]] = find_current_date() + datetime.timedelta(days=14) # dodaliśmy 14 dni ale huj wi czy to działa
#         elif pro[1] == l['Sztuka'][l.index[0]]:
#             lod = lod.drop(l.index[0], axis=0)
#             sum = l['Punkty'][l.index[0]]
#         else:
#             lod['Sztuka'][l.index[0]] = l['Sztuka'][l.index[0]] - pro[1]
#             sum = l['Punkty'][l.index[0]]
#
#     return lod, sum

def calculation_points_for_dish(lod = 0, idx: int = 0, baza: str = '',produkt = 0):
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
        nazwa = list[j][0]
        df = lodowka[lodowka["Nazwa"] == nazwa]
        if df.empty == True:
            if len(list[j]) == 2:
                s = sklep["Waga"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / s)
                ss = p * s - ns
                sum += sklep["Punkty"][nazwa] * p
                if ss != 0:
                    df = {"Nazwa": list[j][0], "Sztuka": np.nan, "Waga": ss, "Punkty": 0, "Data_waznosci": find_current_date() + datetime.timedelta(days=14)}
                    lod = lod.append(df, ignore_index=True)

            if len(list[j]) == 3:
                s = sklep["Sztuka"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / s)
                ss = p * s - ns
                sum += sklep["Punkty"][nazwa] * p
                if ss != 0:
                    df = {"Nazwa": list[j][0], "Sztuka": ss, "Waga": np.nan, "Punkty": 0, "Data_waznosci": find_current_date() + datetime.timedelta(days=14)}
                    lod = lod.append(df, ignore_index=True)
        else:
            if len(list[j]) == 2:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Waga'][l.index[0]]:
                    s = sklep['Waga'][list[j][0]]
                    ns = list[j][1] - l['Waga'][l.index[0]]
                    p = np.ceil(ns / s)
                    ss = p * s - ns
                    sum += sklep["Punkty"][list[j][0]] * p
                    lod['Waga'][l.index[0]] = ss
                    lod['Data_waznosci'][l.index[0]] = find_current_date() + datetime.timedelta(days=14)
                elif list[j][1] == l['Waga'][l.index[0]]:
                    lod = lod.drop([l.index[0]], axis=0)
                    sum += l['Punkty'][l.index[0]]
                else:
                    lod['Waga'][l.index[0]] = l['Waga'][l.index[0]] - list[j][1]
                    sum += l['Punkty'][l.index[0]]

            if len(list[j]) == 3:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Sztuka'][l.index[0]]:
                    s = sklep['Sztuka'][list[j][0]]
                    ns = list[j][1] - l['Sztuka'][l.index[0]]
                    p = np.ceil(ns / s)
                    ss = p * s - ns  # tu coś brakuje
                    sum += sklep["Punkty"][list[j][0]] * p
                    lod['Sztuka'][l.index[0]] = ss
                    lod['Data_waznosci'][l.index[0]] = find_current_date() + datetime.timedelta(days=14)
                elif list[j][1] == l['Sztuka'][l.index[0]]:
                    lod = lod.drop(l.index[0], axis=0)
                    sum += l['Punkty'][l.index[0]]
                else:
                    lod['Sztuka'][l.index[0]] = l['Sztuka'][l.index[0]] - list[j][1]
                    sum += l['Punkty'][l.index[0]]

    return lod, sum


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


def aktualization(result):
    nbaza = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    suma = 0
    lod = deepcopy(lodowka)
    for r,b in zip(result, nbaza):
        df = b[b['Nazwa_dania'] == r]
        l, s = calculation_points_for_dish(lod,df.index[0],b)
        lod = l
        suma += s
    return lod, suma



def tabu(iter, bs):
    """

    :param iter: ilośc iteracji
    :param bs: wybór sposobu znalezienia bazy startowej 0 lub 1
    :return: wynik końcowy
    """

    roz_s = roz_start(bs)
    r = roz_s
    pkt, lod = aktualization(roz_s)
    for i in range(iter):
        for s in range(len(sniadania)):
            if s == roz_s[0]:
                r[0] = sniadania['Nazwa_dania'[s]]
                pkt, lod = aktualization(r)
        for s in range(len(sniadania2)):
            if s == roz_s[1]:
                r[1] = sniadania2['Nazwa_dania'[s]]
                pkt, lod = aktualization(r)
        for s in range(len(obiad)):
            if s == roz_s[2]:
                r[2] = obiad['Nazwa_dania'[s]]
                pkt, lod = aktualization(r)
        for s in range(len(podwieczorek)):
            if s == roz_s[3]:
                r[3] = podwieczorek['Nazwa_dania'[s]]
                pkt, lod = aktualization(r)
        for s in range(len(kolacja)):
            if s == roz_s[4]:
                r[4] = kolacja['Nazwa_dania'[s]]
                pkt, lod = aktualization(r)












