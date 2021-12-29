import pandas as pd
import numpy as np
import random
import datetime
from copy import deepcopy
import matplotlib.pyplot as plt
import math

#Wczytanie baz danych do programu
sniadania = pd.read_csv("bazy_danych\sniadania.csv", sep = ';')
sniadania2 = pd.read_csv("bazy_danych\sniadanie2.csv", sep = ';')
obiad = pd.read_csv("bazy_danych\obiad.csv", sep = ';')
podwieczorek = pd.read_csv("bazy_danych\sniadanie2.csv", sep = ';')
kolacja = pd.read_csv("bazy_danych\kolacja.csv", sep = ';')
lodowka = pd.read_csv("bazy_danych\lodowka2.csv", sep =';')
l_pomocnicza = pd.read_csv("bazy_danych\lodowka2.csv", sep =';')
s = pd.read_csv("bazy_danych\produkty_w_sklepie.csv", sep =';')
sklep = s.set_index("Nazwa")

sniadania.name = "sniadania"
sniadania2.name = "sniadania2"
obiad.name = "obiad"
podwieczorek.name = "podwieczorek"
kolacja.name = "kolacja"


CAL = 3000
PRO = 1000



def find_current_date(z):
    """
    Funkcja wyznaczająca aktualną datę

    :return: Aktualna data
    """
    return '2022-01-' + str(z)


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
                    df = {"Nazwa": list[j][0], "Sztuka": np.nan, "Waga": ss, "Punkty": 0, "Data_waznosci": '2022-01-15'}
                    lod = lod.append(df, ignore_index=True)

            if len(list[j]) == 3:
                s = sklep["Sztuka"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / s)
                ss = p * s - ns
                sum += sklep["Punkty"][nazwa] * p
                if ss != 0:
                    df = {"Nazwa": list[j][0], "Sztuka": ss, "Waga": np.nan, "Punkty": 0, "Data_waznosci": '2022-01-15'}
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
                    lod['Data_waznosci'][l.index[0]] = '2022-01-15'
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
                    lod['Data_waznosci'][l.index[0]] = '2022-01-15'
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

def sort(lista_rankingowa_z_lodowka):
    for i in range(len(lista_rankingowa_z_lodowka) - 1):
        for j in range(0, len(lista_rankingowa_z_lodowka) - i - 1):
            if lista_rankingowa_z_lodowka[j][1] < lista_rankingowa_z_lodowka[j + 1][1]:
                lista_rankingowa_z_lodowka[j], lista_rankingowa_z_lodowka[j + 1] = lista_rankingowa_z_lodowka[j + 1], lista_rankingowa_z_lodowka[j]

    return lista_rankingowa_z_lodowka

def ranking_new(baza_dania, rezultat, lista_rankingowa_z_lodowka = []):
    klucz_do_nazw_posilkow = {"sniadania": 1, "sniadania2": 2, "obiad": 3, "podwieczorek": 4, "kolacja": 5}
    numer_w_liscie_rezultat = klucz_do_nazw_posilkow[baza_dania.name] - 1
    for index, row in baza_dania.iterrows():
        if baza_dania.iloc[index, 0] != rezultat[numer_w_liscie_rezultat]:
            rezultat[numer_w_liscie_rezultat] = baza_dania.iloc[index, 0]
            wynik = rezultat[:]
            lod, sum = aktualization(rezultat)
            lista_rankingowa_z_lodowka.append([wynik,sum,numer_w_liscie_rezultat, lod])

    #sortowanie po sumie żeby utowrzyć ranking
    lista_rankingowa_z_lodowka = sort(lista_rankingowa_z_lodowka)
    return lista_rankingowa_z_lodowka


def ranking_random(rezultat, iter, max = 0):
    rs = rezultat[:]
    rr = []
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    lista_rankingowa_z_lodowka = []
    for x in range(5):
        df = baz[x][baz[x]['Nazwa_dania'] == rezultat[x]]
        z = df.index[0]
        rr.append([x,z])
    for z in range(iter):
        r_baz = random.randint(0,4) #odpowiednią bazę oraz indeks w wyniku rezulatatu
        baz_w = baz[r_baz]

        if max == 0:
            l_baz = random.randint(0, len(baz_w) - 1)
            while [r_baz,l_baz] in rr:
                l_baz = random.randint(0, len(baz_w) - 1)

        else:
            df = baz_w.sort_values('Punkty', ascending=False)
            l_baz = df.index[0]
            i = 1
            while [r_baz,l_baz] in rr:
                l_baz = df.index[i]
                i += 1

        rr.append([r_baz,l_baz])
        rezultat[r_baz] = baz_w['Nazwa_dania'][l_baz]
        wynik = rezultat[:]
        lod, sum = aktualization(rezultat)
        lista_rankingowa_z_lodowka.append([wynik, sum, r_baz, lod])
        rezultat = rs[:]

    lista_rankingowa_z_lodowka = sort(lista_rankingowa_z_lodowka)
    return lista_rankingowa_z_lodowka

def tabu_list_actualization():
    """
    Funkcja aktualizuje ilość iteracji na które elementy zostały umieszczone w liście tabu. Ilość iteracji jest zmieniana
    w bazie danych
        """
    lista_posilkow= [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    for i in lista_posilkow:
        znalezione_tabu = i.loc[i['Tabu'] > 0]
        if len(znalezione_tabu) > 0:
            for j in range(len(znalezione_tabu)):
                i.loc[znalezione_tabu.index[j],"Tabu"] -= 1
    return lista_posilkow


def tabu_set(iter, bs, llist, metod, metoda_iter = 4, cut_par = -200):
    """
    Metoda funkcji tabu z listą zabronień zestawów odopwiednich dań

    :param iter: ilość iteracji
    :param bs: wybór sposobu znalezienia bazy startowej 0 - losowa baza lub 1 - najlepsza baza
    :param llist: długość listy zabronień
    :param metod: wybór metody wybrania sąsiada  0 - metoda dokładna, 1 - metoda losowa (przybliżona), 2 - metoda losowa
    :param metod_iter: ilość wyników wybranych metodą losową
    :param cut_par: wartość parametru przerwania szukania rozwiązania
    :return: Wynik końcowy
    """

    roz_s = roz_start(bs)
    r = roz_s[:]
    lod_str, pkt_str = aktualization(roz_s)
    best_roz_s = roz_s[:]
    best_pkt = pkt_str
    best_lod = lod_str[:]
    tabu_list = [0]*llist
    tabu_licz = 0
    i = 0
    l = []

    for it in range(iter):
        if metod == 0:
            lst = ranking_new(sniadania, r, [])
            lst = ranking_new(sniadania2, r, lst)
            lst = ranking_new(obiad, r, lst)
            lst = ranking_new(podwieczorek, r, lst)
            lst = ranking_new(kolacja, r, lst)
        if metod == 1:
            lst = ranking_random(r,metoda_iter)
        if metod == 2:
            lst = ranking_random(r,metoda_iter, max = 1)

        while True:
            if lst[i][0] not in tabu_list:
                tab = lst[i][0][:]
                tabu_list[tabu_licz] = tab
                break #co w momencie jak nic z nowej listy nie możemy zniszczyć bo wszystko już tam jest

            i += 1

        if lst[i][1] > best_pkt:
            best_pkt = lst[i][1]
            best_roz_s = lst[i][0]
            best_lod = lst[i][3]

        r = lst[i][0]
        r1 = lst[i][1]
        lst = []
        i = 0
        tabu_licz += 1
        if tabu_licz == llist:
            tabu_licz = 0

        if r1 <= cut_par:
            break

        l.append(r1)

    print(best_pkt, best_roz_s, best_lod)
    return l


def tabu_product(iter, bs, l_iter, metod, metoda_iter = 4, cut_par = -200):
    roz_s = roz_start(bs)
    r = roz_s[:]
    lod_str, pkt_str = aktualization(roz_s)
    best_roz_s = roz_s[:]
    best_pkt = pkt_str
    best_lod = lod_str[:]
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    i = 0
    l = []

    for it in range(iter):
        if metod == 0:
            lst = ranking_new(sniadania, r, [])
            lst = ranking_new(sniadania2, r, lst)
            lst = ranking_new(obiad, r, lst)
            lst = ranking_new(podwieczorek, r, lst)
            lst = ranking_new(kolacja, r, lst)
        if metod == 1:
            lst = ranking_random(r, metoda_iter)
        if metod == 2:
            lst = ranking_random(r, metoda_iter, max=1)

        while True:
            numer = lst[i][2]
            k = baz[numer]
            df = k[k["Nazwa_dania"] == lst[i][0][numer]]
            if k['Tabu'][df.index[0]] != 0 and lst[i][1] > best_pkt:  # kryterium aspiracji
                k['Tabu'][df.index[0]] = l_iter
                break

            if k['Tabu'][df.index[0]] == 0:  # blokowanie tabu jeśli nie było to zabronione wcześniej
                k['Tabu'][df.index[0]] = l_iter
                break

            if len(lst) == i + 1: #głupie zabezpieczenie XD ale niech narazie będzie XD
                break
            i += 1

        if lst[i][1] > best_pkt:
            best_pkt = lst[i][1]
            best_roz_s = lst[i][0]
            best_lod = lst[i][3]

        r = lst[i][0]
        r1 = lst[i][1]
        lst = []
        i = 0

        if r1 <= cut_par:
            break

        l.append(r1)
        tabu_list_actualization()

    return l, best_pkt, best_roz_s, best_lod


l = tabu_set(500,1,20,2)
plt.plot(l)
plt.show()

# def week_set(iter, bs, llist, metod, metoda_iter = 4, cut_par = -200):
#     for i in range(7):
#         # preferencje()
#         w, bp, br, bl = tabu_set(iter, bs, llist, metod, metoda_iter, cut_par)
#         plt.plot(w)
#         plt.show()
#         lodowka = deepcopy(bl)
        # append_kara() # dodanie funkcji kary dla poszczególnych dań w zależności od kiedty zostało to dodane

        # policz_koszt() # w liczeniu punktów za set, zwróć listę Marysia

        # to razem: Piotrek
        #     dodaj dzień()
        #     funkcja przeładowania lodówki()

        # return wyniki



# wyświetlanie wykresu i wyniku

#sprawdzenie czy nie ma błędów

# dodanie pozycji do baz
# przeładowanie podwieczorków


#dodać pieduły sprawdzające poprawności
#zrobić dokumentacje
#przyspieszyć procesy
