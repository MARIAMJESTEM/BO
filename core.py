import pandas as pd
import numpy as np
import random
import datetime
from copy import deepcopy
import matplotlib.pyplot as plt
pd.set_option('mode.chained_assignment', None)


# Wczytanie baz danych do programu
sniadania = pd.read_csv("bazy_danych\sniadania.csv", sep = ';')
sniadania2 = pd.read_csv("bazy_danych\sniadanie2.csv", sep = ';')
obiad = pd.read_csv("bazy_danych\obiad.csv", sep = ';')
podwieczorek = pd.read_csv("bazy_danych\podwieczorek.csv", sep = ';')
kolacja = pd.read_csv("bazy_danych\kolacja.csv", sep = ';')
lodowka = pd.read_csv("bazy_danych\lodowka.csv", sep =';')
s = pd.read_csv("bazy_danych\produkty_w_sklepie.csv", sep =';')
sklep = s.set_index("Nazwa")

sniadania.name = "sniadania"
sniadania2.name = "sniadania2"
obiad.name = "obiad"
podwieczorek.name = "podwieczorek"
kolacja.name = "kolacja"

CAL = 3000
PRO = 1000

actual_data = datetime.date.fromisoformat('2022-01-01')

lista_priorytetow = [('2022-01-02', 'Krewetki z mango', kolacja)]


def calculate_product_to_fridge_points(date, actual):
    """
    Funkcja licząca punkty dla produktów z lodówki

    :param date: Data produktu
    :param actual: Aktualna data
    :return: Liczba punktów za produkt
    """
    actual_d = datetime.date.fromisoformat(actual)
    date = datetime.date.fromisoformat(date)
    days = (date - actual_d).days
    if days < 0:
        return -2000
    elif days > 5:
        return 0
    else:
        return (6 - days) * 10


def actual_lod(lod, actual):
    """
    Funkcja zwracająca lodówke z nową punktacją

    :param lod: lodówka aktualna
    :param actual: Aktualna data
    :return: lodówka nowa
    """
    ll = list(lod.index)
    for i in ll:
        date = lod['Data_waznosci'][i]
        pkt = calculate_product_to_fridge_points(str(date), actual)
        lod['Punkty'][i] = pkt
    return lod


def read_sklad(idx = 0, baza = '', produkt = 0):
    """
    Funkcja odczytująca produkty z dania i przerabiająca je na listę

    :param produkt:
    :param idx: indeks dania
    :param baza: nazwa bazy z której wyjmujemy produkty
    :return: lista składu dania
    """
    if produkt == 0:
        str_list = baza["Produkty"][idx][1:-1]
    else:
        str_list = produkt[1:-1]
    l = len(str_list)
    s_list = []
    list = []
    s_licz = 1
    element = 1
    for i in range(1,l):
        if str_list[i] == '[':
            s_licz = i + 1
            element = 1
            list.append(s_list)
            s_list = []
        if str_list[i] == ',' and str_list[i - 1] != ']' or str_list[i] == ']':
            pro = str_list[s_licz:i]
            s_licz = i + 1
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
    :param produkt: Lista produktów jeśli dodajemy nowy produkt
    :return: Punkty za danie
    """
     #do usuniecia bo testowe, tak btw to nie potrzebnie pisane tu jest lodowka zamiast lod
    lista = []
    sum = 0
    if produkt == 0:
        list = read_sklad(idx, baza)
    else:
        list = read_sklad(produkt = produkt)
    for j in range(len(list)):
        nazwa = list[j][0]
        df = lod[lod["Nazwa"] == nazwa]
        if df.empty == True:
            if len(list[j]) == 2:
                s = sklep["Waga"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / s)
                ss = p * s - ns
                sum += sklep["Punkty"][nazwa] * p
                cena = float(sklep["Cena"][nazwa]) * p
                if ss != 0:
                    df = {"Nazwa": list[j][0], "Sztuka": np.nan, "Waga": ss, "Punkty": 0, "Data_waznosci": actual_data + datetime.timedelta(days=14)}
                    lod = lod.append(df, ignore_index=True)
                lista.append([nazwa, np.nan, p*s, cena])

            if len(list[j]) == 3:
                s = sklep["Sztuka"][nazwa] # po ile sztuk jest sprzedawane w sklepie
                ns = list[j][1] #ilosc sztuk potrzebnych
                p = np.ceil(ns / s)
                ss = p * s - ns
                sum += sklep["Punkty"][nazwa] * p
                if ss != 0:
                    df = {"Nazwa": list[j][0], "Sztuka": ss, "Waga": np.nan, "Punkty": 0, "Data_waznosci": actual_data + datetime.timedelta(days=14)}
                    lod = lod.append(df, ignore_index=True)
                    lista.append([nazwa,ss, np.nan])
                cena = float(sklep["Cena"][nazwa]) * p
                lista.append([nazwa, p, np.nan, cena])


        else:
            if len(list[j]) == 2:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Waga'][l.index[0]]:#jeśli nie mamy wystarczającej ilości w lodówce
                    s = sklep['Waga'][list[j][0]]
                    ns = list[j][1] - l['Waga'][l.index[0]]#tyle ile nam brakuje
                    p = np.ceil(ns / s)
                    ss = p * s - ns
                    sum += sklep["Punkty"][list[j][0]] * p
                    lod['Waga'][l.index[0]] = ss
                    lod['Data_waznosci'][l.index[0]] = actual_data + datetime.timedelta(days=14)
                    lod['Data_waznosci'][l.index[0]] = '2022-01-15'
                    cena = float(sklep["Cena"][nazwa]) * p
                    lista.append([nazwa, np.nan, p*s, cena])
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
                    ss = p * s - ns
                    cena = float(sklep["Cena"][nazwa]) * p
                    lista.append([nazwa, p * s, np.nan, cena])
                    sum += sklep["Punkty"][list[j][0]] * p
                    lod['Sztuka'][l.index[0]] = ss
                    lod['Data_waznosci'][l.index[0]] = actual_data + datetime.timedelta(days=14)
                elif list[j][1] == l['Sztuka'][l.index[0]]:
                    lod = lod.drop(l.index[0], axis=0)
                    sum += l['Punkty'][l.index[0]]
                else:
                    lod['Sztuka'][l.index[0]] = l['Sztuka'][l.index[0]] - list[j][1]
                    sum += l['Punkty'][l.index[0]]

    return lod, sum, lista

def calculation_points_for_dish_only(lod = 0, idx: int = 0, baza: str = ''):
    """
    Funkcja licząca punkty za danie
    :param idx: Indeks w bazie
    :param baza: Baza
    :return: Punkty za danie
    """

    sum = 0
    list = read_sklad(idx, baza)

    for j in range(len(list)):
        nazwa = list[j][0]
        df = lod[lod["Nazwa"] == nazwa]
        if df.empty == True:
            if len(list[j]) == 2:
                s = sklep["Waga"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / s)
                ss = p * s - ns
                sum += sklep["Punkty"][nazwa] * p

            if len(list[j]) == 3:
                s = sklep["Sztuka"][nazwa] # po ile sztuk jest sprzedawane w sklepie
                ns = list[j][1] #ilosc sztuk potrzebnych
                p = np.ceil(ns / s)
                ss = p * s - ns
                sum += sklep["Punkty"][nazwa] * p
        else:
            if len(list[j]) == 2:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Waga'][l.index[0]]:#jeśli nie mamy wystarczającej ilości w lodówce
                    s = sklep['Waga'][list[j][0]]
                    ns = list[j][1] - l['Waga'][l.index[0]]#tyle ile nam brakuje
                    p = np.ceil(ns / s)
                    ss = p * s - ns
                    sum += sklep["Punkty"][list[j][0]] * p
                elif list[j][1] == l['Waga'][l.index[0]]:
                    sum += l['Punkty'][l.index[0]]
                else:
                    sum += l['Punkty'][l.index[0]]

            if len(list[j]) == 3:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Sztuka'][l.index[0]]:
                    s = sklep['Sztuka'][list[j][0]]
                    ns = list[j][1] - l['Sztuka'][l.index[0]]
                    p = np.ceil(ns / s)
                    ss = p * s - ns
                    sum += sklep["Punkty"][list[j][0]] * p
                elif list[j][1] == l['Sztuka'][l.index[0]]:
                    sum += l['Punkty'][l.index[0]]
                else:
                    sum += l['Punkty'][l.index[0]]

    return sum


def roz_start(n: int): #0 losowy sposób, 1 najlepsze danie czyli największa ilość punktów za danie w bazie
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


def standard_deviation_calories_and_protein(result): #NIEUŻYWANE
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


def aktualization(result,lod_s):
    """
        Funkcja działa jak calculation_ponits_for_dish tylko że dla całego rozwiązania a nie jednego dania

        :param result: rozwiązanie dla którego akualizowana jest lodówka i liczone są punkty
        :param lod_s: aktualizowana lodówka
        :return: lod- końcowa lodówka po zmianach, suma - ile ma punktów całe rozwiązanie, lista_zakupow- czego brakuje i trzeba dokupić
        """
    lista_zakupow = []
    nbaza = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    suma = 0
    lod = deepcopy(lod_s)
    for r,b in zip(result, nbaza):
        df = b[b['Nazwa_dania'] == r]
        l, s, lista_zak_jedno_danie = calculation_points_for_dish(lod,df.index[0],b) #zwraca punkty za danie z zatuktualizowaną lodówką i listą zakupów
        lista_zakupow = lista_zakupow + lista_zak_jedno_danie
        lod = l
        #to jakieś bonusy filipa które nie wiem jesczsze jak działają / już wiem i mądrze działają !!!!!
        bonus = df['Bonus'][df.index[0]]
        suma += s
        suma += bonus

    return lod, suma, lista_zakupow



def sort(lista_rankingowa_z_lodowka): #sortowanie bąbelkowe listy rankingowej
    """
           Funkcja sortuje listę z daniami

           :param lista_rankingowa_z_lodowka: wstępna lista rankingowa
           :return: zwraca posortowaną listę rankingową
           """
    for i in range(len(lista_rankingowa_z_lodowka) - 1):
        for j in range(0, len(lista_rankingowa_z_lodowka) - i - 1):
            if lista_rankingowa_z_lodowka[j][0][1] < lista_rankingowa_z_lodowka[j + 1][0][1]:
                lista_rankingowa_z_lodowka[j], lista_rankingowa_z_lodowka[j + 1] = lista_rankingowa_z_lodowka[j + 1], lista_rankingowa_z_lodowka[j]

    return lista_rankingowa_z_lodowka

def ranking_new(baza_dania, rezultat, lista_rankingowa_z_lodowka, lod):#pierwotna funkcja
    """
               Funkcja tworzy ranking najlepszych dań dla jednego posiłku
               :param baza_dania: baza dla której będzie tworzony ranking dań
               :return: zwraca posortowaną listę rankingową
               """
    klucz_do_nazw_posilkow = {"sniadania": 1, "sniadania2": 2, "obiad": 3, "podwieczorek": 4, "kolacja": 5}
    numer_w_liscie_rezultat = klucz_do_nazw_posilkow[baza_dania.name] - 1
    for index, row in baza_dania.iterrows():
        if baza_dania.iloc[index, 0] != rezultat[numer_w_liscie_rezultat]:
            rezultat[numer_w_liscie_rezultat] = baza_dania.iloc[index, 0]
            wynik = rezultat[:]
            lodd, sum, lista_zak = aktualization(rezultat, lod)
            lista_rankingowa_z_lodowka.append([wynik,sum,numer_w_liscie_rezultat, lodd, lista_zak])

    #sortowanie po sumie żeby utowrzyć ranking
    lista_rankingowa_z_lodowka = sort(lista_rankingowa_z_lodowka)
    return lista_rankingowa_z_lodowka

def ranking_new2(baza_dania, rezultat, lista_rankingowa_z_lodowka, lod):
    """
               Funkcja tworzy ranking najlepszych dań dla jednego posiłku
               :param baza_dania: baza dla której będzie tworzony ranking dań
               :return: zwraca posortowaną listę rankingową
               """
    klucz_do_nazw_posilkow = {"sniadania": 1, "sniadania2": 2, "obiad": 3, "podwieczorek": 4, "kolacja": 5}
    numer_w_liscie_rezultat = klucz_do_nazw_posilkow[baza_dania.name] - 1
    to_co_przyszlo = rezultat[numer_w_liscie_rezultat]

    #startowe żeby lepiej porównywać wynik
    rezultat[numer_w_liscie_rezultat] = baza_dania.iloc[0, 0]  # o tu
    lodd, sum, lista_zak = aktualization(rezultat, lod)
    for index, row in baza_dania.iterrows():
        if index > 0:
            if baza_dania.iloc[index, 0] != to_co_przyszlo: #jeżeli nazwa dania jest różna od nazwy dania z naszego rezultatu dla tego samego posiłku
                #to podmieniamy to danie na nowe
                rezultat_pomocniczy = rezultat[:]
                rezultat_pomocniczy[numer_w_liscie_rezultat] = baza_dania.iloc[index, 0]
                lodd2, sum2, lista_zak2 = aktualization(rezultat_pomocniczy, lod)

                if sum2 > sum:
                    rezultat = rezultat_pomocniczy
    lodd_koncowa, sum_koncowa, lista_zak_koncowa = aktualization(rezultat, lod)
    lista_rankingowa_z_lodowka.append([rezultat,sum,numer_w_liscie_rezultat, lodd_koncowa, lista_zak_koncowa]) # i dodajemy z tą opcją do listy

    return lista_rankingowa_z_lodowka


def ranking_random(rezultat, iter, lod, max = 0):
    rs = rezultat[:]
    rr = []
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    lista_rankingowa_z_lodowka = []
    for x in range(5):
        df = baz[x][baz[x]['Nazwa_dania'] == rezultat[x]]
        z = df.index[0]
        rr.append([x,z])
    for z in range(iter):
        r_baz = random.randint(0,4)
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
        lodd, sum , lista_zak= aktualization(rezultat, lod)
        lista_rankingowa_z_lodowka.append([wynik, sum, r_baz, lodd, lista_zak])
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


def tabu_set(iter, bs, llist, metod, lod, metoda_iter, cut_par):
    """
    Metoda funkcji tabu z listą zabronień zestawów odpowiednich dań

    :param lod: lodówka
    :param iter: ilość iteracji
    :param bs: wybór sposobu znalezienia bazy startowej 0 - losowa baza lub 1 - najlepsza baza
    :param llist: długość listy zabronień
    :param metod: wybór metody wybrania sąsiada 0 - metoda dokładna, 1 - metoda losowa (przybliżona), 2 - metoda losowa
    :param metoda_iter: ilość wyników wybranych metodą losową
    :param cut_par: wartość parametru przerwania szukania rozwiązania
    :return: Wynik końcowy
    """

    roz_s = roz_start(bs)
    # print(roz_s)
    r = roz_s[:]
    lod_str, pkt_str, lista_zak = aktualization(roz_s, lod)
    best_roz_s = roz_s[:]
    best_pkt = pkt_str
    best_lod = lod_str[:]
    tabu_list = [0]*llist
    tabu_licz = 0
    i = 0
    l = []

    for it in range(iter):
        if metod == 0:
            lst = ranking_new(sniadania, r, [], lod)
            lst = ranking_new(sniadania2, r, lst, lod)
            lst = ranking_new(obiad, r, lst, lod)
            lst = ranking_new(podwieczorek, r, lst, lod)
            lst = ranking_new(kolacja, r, lst, lod)
        if metod == 1:
            lst = ranking_random(r,metoda_iter, lod)
        if metod == 2:
            lst = ranking_random(r,metoda_iter, lod, max = 1)


        while True:
            if lst[i][0] not in tabu_list:
                tab = lst[i][0][:]
                tabu_list[tabu_licz] = tab
                break

            if len(lst) == i + 1:
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
        tabu_licz += 1
        if tabu_licz == llist:
            tabu_licz = 0

        if r1 <= cut_par:
            break

        l.append(r1)

    return l, best_pkt, best_roz_s, best_lod


def tabu_product(iter, bs, l_iter, metod, lod, metoda_iter =0, cut_par=-500):
    """
    Metoda funkcji tabu dla blokowanych dań

    :param lod: lodówka
    :param iter: ilość iteracji
    :param bs: wybór sposobu znalezienia bazy startowej 0 - losowa baza lub 1 - najlepsza baza
    :param l_iter: zablokowanie na daną liczbę iteracji
    :param metod: wybór metody wybrania sąsiada  0 - metoda dokładna, 1 - metoda losowa (przybliżona), 2 - metoda losowa
    :param metoda_iter: ilość wyników wybranych metodą losową
    :param cut_par: wartość parametru przerwania szukania rozwiązania
    :return:
    """
    roz_s = roz_start(bs)
    r = roz_s[:]
    lod_str, pkt_str, lista_zak = aktualization(roz_s, lod)
    best_roz_s = roz_s[:]
    best_pkt = pkt_str
    best_lod = lod_str[:]
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    i = 0
    l = []

    for it in range(iter):
        if metod == 0:
            lst = ranking_new(sniadania, r, [], lod)
            lst = ranking_new(sniadania2, r, lst, lod)
            lst = ranking_new(obiad, r, lst, lod)
            lst = ranking_new(podwieczorek, r, lst, lod)
            lst = ranking_new(kolacja, r, lst, lod)
        if metod == 1: #to dla mnie jest bezsensu biorąc pod uwagę rozwiązanaie losowe
            lst = ranking_random(r, metoda_iter, lod)
        if metod == 2:#i to też
            lst = ranking_random(r, metoda_iter, lod, max=1)

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

        r = lst[i][0] #rezultat który był wyliczony teraz
        r1 = lst[i][1] #ile miał punktó taki zestaw
        lst = []
        i = 0

        if r1 <= cut_par:
            break

        l.append(r1)
        tabu_list_actualization()

    return l, best_pkt, best_roz_s, best_lod

def tabu_product_wersja_2(lod, ilosc_iteracji = 5, na_ile_blokujemy_tabu = 10, wybor_sposobu_znalezienia_bazy_startowej = 0, cut_par = -500):
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    rozwiazanie_startowe = roz_start(wybor_sposobu_znalezienia_bazy_startowej)
    lod_str, pkt_str, lista_zak = aktualization(rozwiazanie_startowe, lod)
    best_pkt = pkt_str
    best_roz_s = rozwiazanie_startowe
    best_lod = lod_str
    best_lista = lista_zak#r= rozwiazanie_startowe[:] tutaj zmienia się rozwiązanie startowe pomimo tego ze go nie ruszamy
    r = deepcopy(rozwiazanie_startowe)
    for i in range(ilosc_iteracji):
        rozw_sniadania = r[:]
        rozw_sniadania2 = r[:]
        rozw_obiad = r[:]
        rozw_podwieczorek = r[:]
        rozw_kolacja = r[:]
        lst1 = ranking_new2(sniadania,rozw_sniadania , [], lod)
        lst2 = ranking_new2(sniadania2, rozw_sniadania2, [], lod)
        lst3 = ranking_new2(obiad, rozw_obiad, [], lod)
        lst4 = ranking_new2(podwieczorek, rozw_podwieczorek, [], lod)
        lst5 = ranking_new2(kolacja, rozw_kolacja, [], lod)
        #wybranie najlepszego rozwiązania na tą iteracje
        lista_do_sortowania = [lst1, lst2, lst3, lst4, lst5]
        lista_do_sortowania = sort(lista_do_sortowania)

        ktory_posilek_wymieniony_lub_nie = lista_do_sortowania[0][0][2]
        ile_ma_punktow_to_rozwiazanie = lista_do_sortowania[0][0][1]
        k = 0
        while True:
            cos = lista_do_sortowania[k][0][2]
            if i == 0:
                cc = rozwiazanie_startowe[cos]
                dff = baz[cos][baz[cos]["Nazwa_dania"] == rozwiazanie_startowe[cos]]
                dc = baz[cos].index[baz[cos]["Nazwa_dania"] == rozwiazanie_startowe[cos]]
                if dff['Tabu'][dff.index[0]] == 0:
                    # blokowanie tabu jeśli nie było to zabronione wcześniej
                    baz[cos].at[dc, 'Tabu'] = na_ile_blokujemy_tabu
                    dff['Tabu'][dff.index[0]] = na_ile_blokujemy_tabu

            nazwa_posilku = lista_do_sortowania[k][0][0][cos]
            df = baz[cos][baz[cos]["Nazwa_dania"] == nazwa_posilku]
            dl = baz[cos].index[baz[cos]["Nazwa_dania"] == nazwa_posilku]

            if df['Tabu'][df.index[0]] <5 and df['Tabu'][df.index[0]] > 0 and lista_do_sortowania[i][0][1] > best_pkt:  # kryterium aspiracji
                baz[cos].at[dl, 'Tabu'] = na_ile_blokujemy_tabu
                r = lista_do_sortowania[k][0][0]
                if lista_do_sortowania[k][0][1] > best_pkt:
                    best_pkt = lista_do_sortowania[k][0][1]
                    best_roz_s = lista_do_sortowania[k][0][0]
                    best_lod = lista_do_sortowania[k][0][3]
                    best_lista = lista_do_sortowania[k][0][4]
                break

            if df['Tabu'][df.index[0]] == 0:  # blokowanie tabu jeśli nie było to zabronione wcześniej
                baz[cos].at[dl, 'Tabu'] = na_ile_blokujemy_tabu
                r = lista_do_sortowania[k][0][0]
                if lista_do_sortowania[k][0][1] > best_pkt:
                    best_pkt = lista_do_sortowania[k][0][1]
                    best_roz_s = lista_do_sortowania[k][0][0]
                    best_lod = lista_do_sortowania[k][0][3]
                break
            tabu_list_actualization()
            k += 1
    return best_roz_s, best_pkt, best_lod, best_lista

def reload_points_for_dishes(lod):
    lista_posilkow = [sniadania, sniadania2, obiad,podwieczorek, kolacja]
    for i in lista_posilkow:
        for j in range(len(i)-1):
            suma = calculation_points_for_dish_only(lod, j, i)
            dc = i.index[i["Nazwa_dania"] == j]
            i.at[dc, "Punkty"] = suma


def calculate_when_dish_used(zestawy_wszystkie_dotychczas):
    p = 0
    lista_posilkow = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    ilosc_zestawow = len(zestawy_wszystkie_dotychczas)
    for i in zestawy_wszystkie_dotychczas:
        kara = -(150 -(ilosc_zestawow-p-1)*(-20))
        k = 0
        for j in i:
            dl = lista_posilkow[k].index[lista_posilkow[k]["Nazwa_dania"] == j]
            ile_jest_dotychczas = lista_posilkow[k][lista_posilkow[k]["Nazwa_dania"] == j] #zabezpieczenie jakbyśmy w innym miejscu dodawali inny bonus

            lista_posilkow[k].at[dl, "Bonus"] = kara + ile_jest_dotychczas["Bonus"]
            k += 1
        p += 1

def week_set_tabu_product(lodowka):
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    zestawy = []
    lista_wszytskich_zakupow_na_caly_tydzien = []
    actual = '2022-01-01'
    for dni in range(7):
        actual = '2022-01-0' + str(dni + 1)
        for lsti in lista_priorytetow:
            if lsti[0] == actual:
                ktory_posilek = lsti[2]
                df = ktory_posilek[ktory_posilek['Nazwa_dania'] == lsti[1]]
                dl = ktory_posilek.index[ktory_posilek['Nazwa_dania'] == lsti[1]]
                ktory_posilek.at[dl, "Bonus"] = 1000 + df["Bonus"]
        best_roz_s, best_pkt, best_lod, best_lista = tabu_product_wersja_2(lodowka)
        zestawy.append(best_roz_s)
        lista_wszytskich_zakupow_na_caly_tydzien.append(best_lista)
        calculate_when_dish_used(zestawy) #kary dodajemy jako bonus
        reload_points_for_dishes(best_lod)
        lodowka = best_lod
        for lsti in lista_priorytetow:
            if lsti[0] == actual:
                ktory_posilek = lsti[2]
                df = ktory_posilek[ktory_posilek['Nazwa_dania'] == lsti[1]]
                dl = ktory_posilek.index[ktory_posilek['Nazwa_dania'] == lsti[1]]
                ktory_posilek.at[dl, "Bonus"] =  df["Bonus"] -1000

        print(actual)
        print(best_roz_s)
        print(best_pkt)

week_set_tabu_product(lodowka)

def week_set(iter, bs, llist, metod, metoda_iter = 4, cut_par = -500):
    wynik = []
    baz = [sniadania,sniadania2,obiad,podwieczorek,kolacja]
    lod = deepcopy(lodowka)
    actual = '2022-01-01'
    lod = actual_lod(lod,actual)
    for iteracja in range(7):

        w, bp, br, bl = tabu_set(iter, bs, llist, metod, lod, metoda_iter, cut_par)

        plt.plot(w)
        plt.title(str(bp))
        plt.show()

        print(actual,'\n',br)
        print(bp)
        wynik.append(br)

        actual = '2022-01-0' + str(iteracja + 2)
        lod = bl[:]
        lod = actual_lod(lod, actual)

        for lsti in lista_priorytetow:
            if lsti[0] == actual:
                bb = lsti[2]
                df = bb[bb['Nazwa_dania'] == lsti[1]]
                bb['Bonus'][df.index[0]] = 1000
            if lsti[0] == '2022-01-0' + str(iteracja):
                bb = lsti[2]
                df = bb[bb['Nazwa_dania'] == lsti[1]]
                bb['Bonus'][df.index[0]] = 0


        for i in range(len(wynik)):  # funkcja kary
            for j, b in zip(wynik[i], baz):
                df = b[b['Nazwa_dania'] == j]
                b['Bonus'][df.index[0]] = ((len(wynik) - i - 1) * 5) - 65

        reload_points_for_dishes(lod)




#week_set(10,1,10,0,metoda_iter = 5)

#
#
# week_set(30,1,10,2,metoda_iter = 5)


# wyświetlanie wykresu i wyniku

#sprawdzenie czy nie ma błędów

# dodanie pozycji do baz
# przeładowanie podwieczorków
