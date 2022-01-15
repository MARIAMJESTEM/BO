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

actual_data = datetime.date.fromisoformat('2022-01-01')

# lista_priorytetów = [['2022-01-01', 'Pieczona owsianka brownie', sniadania], ['2022-01-02', 'Bułki z pomidorem i mozarella', kolacja],['2022-01-03', 'Kurczak w sosie curry',obiad]]
lista_priorytetów = []


def change_pkt(lst_pkt):
    dl = len(lst_pkt)
    w_up = 0
    w_down = 0
    w_stay = 0
    for i in range(dl - 1):
        if lst_pkt[i + 1] > lst_pkt[i]:
            w_up += 1
        elif lst_pkt[i + 1] == lst_pkt[i]:
            w_stay += 1
        else:
            w_down += 1

    p_up = (w_up / dl) * 100
    p_stay = (w_stay / dl) * 100
    p_down = (w_down / dl) * 100

    return round(p_up, 1), round(p_stay, 1), round(p_down, 1)

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
        lod.at[i, "Punkty"] = pkt
    return lod


def read_sklad(idx=0, baza='', produkt = 0):
    """
    Funkcja odczytująca produkty z dania i przerabiająca je na listę

    :param produkt:
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
    Funkcja licząca punkty za danie i aktualizująca lodówkę jeśli dodajemy nowy zakupiony produkt lub usuwamy cały, który złużyjemy

    :param lod: Lodówka
    :param idx: Indeks w bazie
    :param baza: Baza
    :param produkt: Lista produktów jeśli dodajemy nowy produkt
    :return: Punkty za danie
    """
    lista = []
    sum_dish = 0
    if produkt == 0:
        list = read_sklad(idx, baza)
    else:
        list = read_sklad(produkt = produkt)
    for j in range(len(list)):
        nazwa = list[j][0]
        df = lod[lod["Nazwa"] == nazwa]
        if df.empty:
            if len(list[j]) == 2:
                shop_s = sklep["Waga"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / shop_s)
                ss = p * shop_s - ns
                sum_dish += sklep["Punkty"][nazwa] * p
                cena = float(sklep["Cena"][nazwa]) * p
                if ss != 0:
                    df = {"Nazwa": list[j][0], "Sztuka": np.nan, "Waga": ss, "Punkty": 0, "Data_waznosci": actual_data + datetime.timedelta(days=14)}
                    lod = lod.append(df, ignore_index=True)
                lista.append([nazwa, np.nan, p * shop_s, cena])

            if len(list[j]) == 3:
                shop_s = sklep["Sztuka"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / shop_s)
                ss = p * shop_s - ns
                sum_dish += sklep["Punkty"][nazwa] * p
                if ss != 0:
                    df = {"Nazwa": list[j][0], "Sztuka": ss, "Waga": np.nan, "Punkty": 0, "Data_waznosci": actual_data + datetime.timedelta(days=14)}
                    lod = lod.append(df, ignore_index=True)
                    #lista.append([nazwa,ss, np.nan])
                cena = float(sklep["Cena"][nazwa]) * p
                lista.append([nazwa, p, np.nan, cena])

        else:
            if len(list[j]) == 2:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Waga'][l.index[0]]:
                    shop_s = sklep['Waga'][list[j][0]]
                    ns = list[j][1] - l['Waga'][l.index[0]]
                    p = np.ceil(ns / shop_s)
                    ss = p * shop_s - ns
                    sum_dish += sklep["Punkty"][list[j][0]] * p
                    lod['Waga'][l.index[0]] = ss
                    lod['Data_waznosci'][l.index[0]] = actual_data + datetime.timedelta(days=14)
                    lod['Data_waznosci'][l.index[0]] = '2022-01-15'
                    cena = float(sklep["Cena"][nazwa]) * p
                    lista.append([nazwa, np.nan, p * shop_s, cena])
                elif list[j][1] == l['Waga'][l.index[0]]:
                    lod = lod.drop([l.index[0]], axis=0)
                    sum_dish += l['Punkty'][l.index[0]]
                else:
                    lod['Waga'][l.index[0]] = l['Waga'][l.index[0]] - list[j][1]
                    sum_dish += l['Punkty'][l.index[0]]

            if len(list[j]) == 3:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Sztuka'][l.index[0]]:
                    shop_s = sklep['Sztuka'][list[j][0]]
                    ns = list[j][1] - l['Sztuka'][l.index[0]]
                    p = np.ceil(ns / shop_s)
                    ss = p * shop_s - ns
                    cena = float(sklep["Cena"][nazwa]) * p
                    lista.append([nazwa, p * shop_s, np.nan, cena])
                    sum_dish += sklep["Punkty"][list[j][0]] * p
                    lod['Sztuka'][l.index[0]] = ss
                    lod['Data_waznosci'][l.index[0]] = actual_data + datetime.timedelta(days=14)
                elif list[j][1] == l['Sztuka'][l.index[0]]:
                    lod = lod.drop(l.index[0], axis=0)
                    sum_dish += l['Punkty'][l.index[0]]
                else:
                    lod['Sztuka'][l.index[0]] = l['Sztuka'][l.index[0]] - list[j][1]
                    sum_dish += l['Punkty'][l.index[0]]

    return lod, sum_dish, lista


def calculation_points_for_dish_only(lod = 0, idx: int = 0, baza: str = ''):
    """
    Funkcja tylko licząca punkty za danie i nie ingerująca w lodówkę

    :param lod: Lodówka
    :param idx: Indeks w bazie
    :param baza: Baza
    :return: Punkty za danie
    """

    sum_dish = 0
    list = read_sklad(idx, baza)
    for j in range(len(list)):
        nazwa = list[j][0]
        df = lod[lod["Nazwa"] == nazwa]
        if df.empty:
            if len(list[j]) == 2:
                shop_s_ = sklep["Waga"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / shop_s_)
                sum_dish += sklep["Punkty"][nazwa] * p

            if len(list[j]) == 3:
                shop_s_ = sklep["Sztuka"][nazwa]
                ns = list[j][1]
                p = np.ceil(ns / shop_s_)
                sum_dish += sklep["Punkty"][nazwa] * p
        else:
            if len(list[j]) == 2:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Waga'][l.index[0]]:
                    shop_s_ = sklep['Waga'][list[j][0]]
                    ns = list[j][1] - l['Waga'][l.index[0]]
                    p = np.ceil(ns / shop_s_)
                    sum_dish += sklep["Punkty"][list[j][0]] * p
                elif list[j][1] == l['Waga'][l.index[0]]:
                    sum_dish += l['Punkty'][l.index[0]]
                else:
                    sum_dish += l['Punkty'][l.index[0]]

            if len(list[j]) == 3:
                l = lod[lod['Nazwa'] == list[j][0]]
                if list[j][1] > l['Sztuka'][l.index[0]]:
                    shop_s_ = sklep['Sztuka'][list[j][0]]
                    ns = list[j][1] - l['Sztuka'][l.index[0]]
                    p = np.ceil(ns / shop_s_)
                    sum_dish += sklep["Punkty"][list[j][0]] * p
                elif list[j][1] == l['Sztuka'][l.index[0]]:
                    sum_dish += l['Punkty'][l.index[0]]
                else:
                    sum_dish += l['Punkty'][l.index[0]]

    return sum_dish


def roz_start(n: int):
    """
    Funkcja wyznaczająca rozwiązanie początkowe

    :param n:Wybór dań w sposób 0 - losowy 1 - najlepsze dania
    :return: Rozwiązanie początkowe w formie listy
    """
    if n == 0:
        IS = sniadania['Nazwa_dania'][random.randint(0,len(sniadania) - 1)]
        IIS = sniadania2['Nazwa_dania'][random.randint(0,len(sniadania2) - 1)]
        O = obiad['Nazwa_dania'][random.randint(0,len(obiad) - 1)]
        P = podwieczorek['Nazwa_dania'][random.randint(0,len(podwieczorek) - 1)]
        K = kolacja['Nazwa_dania'][random.randint(0,len(kolacja) - 1)]

        return [IS,IIS,O,P,K]

    if n == 1:
        n_baz = [sniadania,sniadania2,obiad,podwieczorek,kolacja]
        w_baz = [0,0,0,0,0]
        for n in range(len(n_baz)):
            max_pkt = n_baz[n]['Punkty'][0]
            idx_i = 0
            for i in range(1, len(n_baz[n])):
                if n_baz[n]['Punkty'][i] > max_pkt:
                    max_pkt = n_baz[n]['Punkty'][i]
                    idx_i = i

            w_baz[n] = n_baz[n]['Nazwa_dania'][idx_i]

        return w_baz


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
        l, sum_dish, lista_zak_jedno_danie = calculation_points_for_dish(lod, df.index[0], b)
        lista_zakupow = lista_zakupow + lista_zak_jedno_danie
        lod = l
        bonus = df['Bonus'][df.index[0]]
        suma += sum_dish
        suma += bonus
    suma_kalorii, punkty_ujemne = counting_calories_per_set(result, CAL)
    suma -= punkty_ujemne
    return lod, suma, lista_zakupow, suma_kalorii

kara_cal_global = 5
def counting_calories_per_set(set_n, calories_per_day):
    """Funkcja liczy sume kalorii za poszczególne dania w podanym zestawie i wylicza punkty ujemne za kalorie które
    się różnią od docelowych

    :param set_n: zestaw dań
    :param calories_per_day: docelowa ilość kalorii na jeden dzień"""
    bazy = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    kara_cal = kara_cal_global
    p = 0
    suma = 0
    for i in set_n:
        df = bazy[p][bazy[p]["Nazwa_dania"] == i]
        suma += df.iloc[0]["Kalorie"]
        p += 1
    difference_with_calories = np.abs(calories_per_day - suma)
    punkty_ujemne = int(difference_with_calories/kara_cal)

    return suma, punkty_ujemne


def sort(lista_rankingowa_z_lodowka):
    """
    Funkcja sortuje listę z daniami

    :param lista_rankingowa_z_lodowka: wstępna lista rankingowa
    :return: zwraca posortowaną listę rankingową
    """
    for i in range(len(lista_rankingowa_z_lodowka) - 1):
        for j in range(0, len(lista_rankingowa_z_lodowka) - i - 1):
            if lista_rankingowa_z_lodowka[j][1] < lista_rankingowa_z_lodowka[j + 1][1]:
                lista_rankingowa_z_lodowka[j], lista_rankingowa_z_lodowka[j + 1] = lista_rankingowa_z_lodowka[j + 1], lista_rankingowa_z_lodowka[j]

    return lista_rankingowa_z_lodowka


def ranking_new(baza_dania, rezultat, lista_rankingowa_z_lodowka, lod):
    """
    Funkcja sprawdzająca sąsiadów danego rezultatu i tworząca listę

    :param baza_dania: Pora dnia która sprawdzamy
    :param rezultat: Badany wynik
    :param lista_rankingowa_z_lodowka: Lista wynikowa
    :param lod: Aktualna lodówka
    :return: lista rankingowa
    """
    klucz_do_nazw_posilkow = {"sniadania": 1, "sniadania2": 2, "obiad": 3, "podwieczorek": 4, "kolacja": 5}
    numer_w_liscie_rezultat = klucz_do_nazw_posilkow[baza_dania.name] - 1
    for index, row in baza_dania.iterrows():
        if baza_dania.iloc[index, 0] != rezultat[numer_w_liscie_rezultat]:
            rezultat[numer_w_liscie_rezultat] = baza_dania.iloc[index, 0]
            wynik = rezultat[:]
            lod_set, sum_set, lista_zak, suma_kalorii = aktualization(rezultat, lod)
            lista_rankingowa_z_lodowka.append([wynik, sum_set, numer_w_liscie_rezultat, lod_set, lista_zak, suma_kalorii])

    lista_rankingowa_z_lodowka = sort(lista_rankingowa_z_lodowka)
    return lista_rankingowa_z_lodowka


def ranking_random(rezultat, iter, lod, actual, max_value = 0):
    rs = rezultat[:]
    rr = []
    blad = 1000
    baz_a = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    for lsti in lista_priorytetów:
        if lsti[0] == actual:
            if lsti[2].name == 'sniadania':
                baz = [0,sniadania2, obiad, podwieczorek, kolacja]
                blad = 0
            elif lsti[2].name == 'sniadania2':
                baz = [sniadania, 0, obiad, podwieczorek, kolacja]
                blad = 1
            elif lsti[2].name == 'obiad':
                baz = [sniadania, sniadania2, 0, podwieczorek, kolacja]
                blad = 2
            elif lsti[2].name == 'podwieczorek':
                baz = [sniadania, sniadania2, obiad, 0, kolacja]
                blad = 3
            elif lsti[2].name == 'kolacja':
                baz = [sniadania, sniadania2, obiad, podwieczorek, 0]
                blad = 4
            else:
                print("BŁĄD")

    lista_rankingowa_z_lodowka = []
    for x in range(5):
        df = baz_a[x][baz_a[x]['Nazwa_dania'] == rezultat[x]]
        z = df.index[0]
        rr.append([x,z])
    for z in range(iter):
        r_baz = random.randint(0,4)
        baz_w = baz[r_baz]
        while blad == r_baz:
            r_baz = random.randint(0, 4)
            baz_w = baz[r_baz]

        if max_value == 0:
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
        lod_set, sum_set, lista_zak, suma_kalorii = aktualization(rezultat, lod)
        lista_rankingowa_z_lodowka.append([wynik, sum_set, r_baz, lod_set, lista_zak, suma_kalorii])
        rezultat = rs[:]

    lista_rankingowa_z_lodowka = sort(lista_rankingowa_z_lodowka)
    return lista_rankingowa_z_lodowka


def tabu_list_actualization():
    """
    Funkcja aktualizuje ilość iteracji na które elementy zostały umieszczone w liście tabu. Ilość iteracji jest zmieniana
    w bazie danych
        """
    lista_posilkow = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    for i in lista_posilkow:
        znalezione_tabu = i.loc[i['Tabu'] > 0]
        if len(znalezione_tabu) > 0:
            for j in range(len(znalezione_tabu)):
                i.loc[znalezione_tabu.index[j],"Tabu"] -= 1
    return lista_posilkow


def tabu_set(iter, bs, llist, metod, lod, actual, metoda_iter):
    """
    Metoda funkcji tabu z listą zabronień zestawów odpowiednich dań

    :param lod: lodówka
    :param iter: ilość iteracji
    :param bs: wybór sposobu znalezienia bazy startowej 0 - losowa baza lub 1 - najlepsza baza
    :param llist: długość listy zabronień
    :param metod: wybór metody wybrania sąsiada 0 - metoda dokładna, 1 - metoda losowa (przybliżona), 2 - metoda losowa
    :param metoda_iter: ilość wyników wybranych metodą losową
    :param actual: Aktualna data
    :return: Wynik końcowy
    """
    iteration = 0
    roz_s = roz_start(bs)
    r = roz_s[:]
    lod_str, pkt_str, lista_zak, kalorie_sum = aktualization(roz_s, lod)
    klucz_do_nazw_posilkow = {"sniadania": 1, "sniadania2": 2, "obiad": 3, "podwieczorek": 4, "kolacja": 5}

    best_roz_s = roz_s[:]
    best_pkt = pkt_str
    best_lod = lod_str[:]
    best_list = lista_zak[:]
    best_cal = kalorie_sum

    tabu_list = [0]*llist
    tabu_licz = 0
    i = 0
    print_result = [pkt_str]
    lista_do_sortowania = []

    for it in range(iter):
        iteration += 1
        if metod == 0:
            rozw_sniadania = r[:]
            rozw_sniadania2 = r[:]
            rozw_obiad = r[:]
            rozw_podwieczorek = r[:]
            rozw_kolacja = r[:]
            lst1 = ranking_new(sniadania, rozw_sniadania, [], lod)
            lst2 = ranking_new(sniadania2, rozw_sniadania2, [], lod)
            lst3 = ranking_new(obiad, rozw_obiad, [], lod)
            lst4 = ranking_new(podwieczorek, rozw_podwieczorek, [], lod)
            lst5 = ranking_new(kolacja, rozw_kolacja, [], lod)
            lista_do_sortowania = lst1 + lst2 + lst3 + lst4 + lst5
            lista_do_sortowania = sort(lista_do_sortowania)
        if metod == 1:
            for lsti in lista_priorytetów:
                if lsti[0] == actual:
                    k = klucz_do_nazw_posilkow[lsti[2].name]
                    r[k - 1] = lsti[1]
            lista_do_sortowania = ranking_random(r,metoda_iter, lod, actual)
        if metod == 2:
            for lsti in lista_priorytetów:
                if lsti[0] == actual:
                    k = klucz_do_nazw_posilkow[lsti[2].name]
                    r[k - 1] = lsti[1]
            lista_do_sortowania = ranking_random(r, metoda_iter, lod, actual, max_value= 1)

        while True:
            if lista_do_sortowania[i][0] not in tabu_list:
                tab = lista_do_sortowania[i][0]
                tabu_list[tabu_licz] = tab
                break

            if len(lista_do_sortowania) == i + 1:
                break

            i += 1

        if lista_do_sortowania[i][1] > best_pkt:
            best_roz_s = lista_do_sortowania[i][0]
            best_pkt = lista_do_sortowania[i][1]
            best_lod = lista_do_sortowania[i][3]
            best_list = lista_do_sortowania[i][4]
            best_cal = lista_do_sortowania[i][5]

        r = lista_do_sortowania[i][0]
        r1 = lista_do_sortowania[i][1]
        lista_do_sortowania = []
        i = 0
        tabu_licz += 1
        print_result.append(r1)
        if tabu_licz == llist:
            tabu_licz = 0

    return best_roz_s, best_pkt, best_lod, best_list, best_cal, print_result, iteration


def counting_cash_to_spend_on_groceries(lista_zakupow):
    """Funkcja liczy ile trzeba wydać pieniędzy na zobienie zakupów na podstawie podanej listy zakupów"""
    if len(lista_zakupow) > 0:
        suma = 0
        for i in lista_zakupow:
            if len(i) >= 4:
                suma += i[3]
        return suma
    else:
        return 0


def tabu_product(lod, ilosc_iteracji, na_ile_blokujemy_tabu, wybor_sposobu_znalezienia_bazy_startowej, metod, metoda_iter, actual):
    """
    Funckja wyszukuje najlepszy posiłek który na podstawie jego punktów
    :param lod: aktualna lodówka
    :param ilosc_iteracji: ilość iteracji
    :param  na_ile_blokujemy_tabu: ilość iteracji na które danie jest zablokowane
    :param wybor_sposobu_znalezienia_bazy_startowej: możemy podać 0 dla rozwiązania startowego losowego i 1 dla najlepszego
    :param metod: wybór metody wybrania sąsiada  0 - metoda dokładna, 1 - metoda losowa (przybliżona), 2 - metoda losowa
    :param metoda_iter: ilość wyników wybranych metodą losową
    :param actual: Aktualna data
    :returm wynik dnia tabu produktu
    """
    iteration = 0
    klucz_do_nazw_posilkow = {"sniadania": 1, "sniadania2": 2, "obiad": 3, "podwieczorek": 4, "kolacja": 5}
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    rozwiazanie_startowe = roz_start(wybor_sposobu_znalezienia_bazy_startowej)
    best_lod, best_pkt, best_lista, best_suma_kalorii = aktualization(rozwiazanie_startowe, lod)
    best_roz_s = rozwiazanie_startowe
    r = deepcopy(rozwiazanie_startowe)
    lista_do_sortowania = []
    punkty = []
    for i in range(ilosc_iteracji):
        iteration += 1
        if metod == 0:
            rozw_sniadania = r[:]
            rozw_sniadania2 = r[:]
            rozw_obiad = r[:]
            rozw_podwieczorek = r[:]
            rozw_kolacja = r[:]
            lst1 = ranking_new(sniadania,rozw_sniadania, [], lod)
            lst2 = ranking_new(sniadania2, rozw_sniadania2, [], lod)
            lst3 = ranking_new(obiad, rozw_obiad, [], lod)
            lst4 = ranking_new(podwieczorek, rozw_podwieczorek, [], lod)
            lst5 = ranking_new(kolacja, rozw_kolacja, [], lod)
            lista_do_sortowania = lst1 + lst2 + lst3 + lst4 + lst5
            lista_do_sortowania = sort(lista_do_sortowania)
        if metod == 1:
            for lsti in lista_priorytetów:
                if lsti[0] == actual:
                    k = klucz_do_nazw_posilkow[lsti[2].name]
                    r[k - 1] = lsti[1]
            lista_do_sortowania = ranking_random(r, metoda_iter, lod, actual)
        if metod == 2:
            for lsti in lista_priorytetów:
                if lsti[0] == actual:
                    k = klucz_do_nazw_posilkow[lsti[2].name]
                    r[k - 1] = lsti[1]
            lista_do_sortowania = ranking_random(r, metoda_iter, lod, actual, max_value=1)
        k = 0
        while True:
            numer_posilku = lista_do_sortowania[k][2]
            if i == 0:
                dff = baz[numer_posilku][baz[numer_posilku]["Nazwa_dania"] == rozwiazanie_startowe[numer_posilku]]
                dc = baz[numer_posilku].index[baz[numer_posilku]["Nazwa_dania"] == rozwiazanie_startowe[numer_posilku]]
                if dff['Tabu'][dff.index[0]] == 0:
                    # blokowanie tabu jeśli nie było to zabronione wcześniej
                    baz[numer_posilku].at[dc, 'Tabu'] = na_ile_blokujemy_tabu

            nazwa_posilku = lista_do_sortowania[k][0][numer_posilku]
            df = baz[numer_posilku][baz[numer_posilku]["Nazwa_dania"] == nazwa_posilku]
            dl = baz[numer_posilku].index[baz[numer_posilku]["Nazwa_dania"] == nazwa_posilku]

            # kryterium aspiracji
            if 5 > df['Tabu'][df.index[0]] > 0 and lista_do_sortowania[k][1] > best_pkt:
                baz[numer_posilku].at[dl, 'Tabu'] = na_ile_blokujemy_tabu
                r = lista_do_sortowania[k][0]
                if lista_do_sortowania[k][1] > best_pkt:
                    best_pkt = lista_do_sortowania[k][1]
                    best_roz_s = lista_do_sortowania[k][0]
                    best_lod = lista_do_sortowania[k][3]
                    best_lista = lista_do_sortowania[k][4]
                    best_suma_kalorii = lista_do_sortowania[k][5]
                break

            # blokowanie tabu jeśli nie było to zabronione wcześniej
            if df['Tabu'][df.index[0]] == 0:
                baz[numer_posilku].at[dl, 'Tabu'] = na_ile_blokujemy_tabu
                r = lista_do_sortowania[k][0]
                if lista_do_sortowania[k][1] > best_pkt:
                    best_pkt = lista_do_sortowania[k][1]
                    best_roz_s = lista_do_sortowania[k][0]
                    best_lod = lista_do_sortowania[k][3]
                    best_lista = lista_do_sortowania[k][4]
                    best_suma_kalorii = lista_do_sortowania[k][5]
                break

            k += 1

        tabu_list_actualization()
        punkty.append(lista_do_sortowania[k][1])
    return best_roz_s, best_pkt, best_lod, best_lista, best_suma_kalorii, punkty, iteration


def reload_points_for_dishes(lod):
    """Funkcja aktualizuje punkty za każde danie, jest używana ponieważ w każdej iteracji zmienia się zawartość lodówki i tym samym punkty za danie
    "param lod: lodówka
    """
    lista_posilkow = [sniadania, sniadania2, obiad,podwieczorek, kolacja]
    for i in lista_posilkow:
        for j in range(len(i)-1):
            suma = calculation_points_for_dish_only(lod, j, i)
            i.at[j, "Punkty"] = suma

kara_global = -150
def calculate_when_dish_used(zestawy_wszystkie_dotychczas):
    """Funkcja dodaje kary za posiłki które zostały już użyte w wyliczonych zestawach
    Im bliżej aktualnego dnia tym kary są mniejsze
    :param zestawy_wszystkie_dotychczas: lista z zestawami dań już użytymi"""
    p = 0
    kara = kara_global
    w_kara = int(kara/5)
    lista_posilkow = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    ilosc_zestawow = len(zestawy_wszystkie_dotychczas)
    for i in zestawy_wszystkie_dotychczas:
        kara = -(kara + (ilosc_zestawow-p-1)*w_kara)
        k = 0
        for j in i:
            if kara > 0:
                dl = lista_posilkow[k].index[lista_posilkow[k]["Nazwa_dania"] == j]
                lista_posilkow[k].at[dl, "Bonus"] = 0
                k += 1
            else:
                dl = lista_posilkow[k].index[lista_posilkow[k]["Nazwa_dania"] == j]
                lista_posilkow[k].at[dl, "Bonus"] = kara
                k += 1

        p += 1

def update_list(lista_zakupow):
    nowa_lista = []
    lista_nazw = []

    iter = 0
    for i in lista_zakupow:
        if i[0] not in lista_nazw:
            nowa_lista.append(i)
            lista_nazw.append(i[0])
            lista_nazw.append(iter)
            iter += 1
        else:
            index = lista_nazw.index(i[0])
            index_w_liscie_docelowej = lista_nazw[index+1]
            stare = nowa_lista[index_w_liscie_docelowej]
            if stare[1] != np.nan:
                stare[1] += i[1]
            if stare[2] != np.nan:
                stare[2] += i[2]
            stare[3] += i[3]
            nowa_lista[index_w_liscie_docelowej] = stare
    return nowa_lista

def week_set_tabu_product(lodowka, ilosc_iteracji, na_ile_blokujemy_tabu, wybor_sposobu_znalezienia_bazy_startowej,  metod, metoda_iter):
    """Funkcja wylicza zestawy dań dla całego tygodnia na podstawie zestawu zwracanego przez funkcję tabu_product_wersja_2
    :param lodowka: lodówka
    :param ilosc_iteracji: ilość iteracji algorytmu tabu
    :param na_ile_blokujemy_tabu: ilość iteracji kiedy tabu jest zablokowane
    :param metod: wybór metody
    :param metoda_iter: długość metody losowej
    :param wybor_sposobu_znalezienia_bazy_startowej: 0 losowy, 1 najlepsza baza"""
    zestawy_najlepsze_punkty = []
    wykresy = []
    kalorie = []
    iteracje = []
    iter_all = 0
    zestawy = []
    cena_d = []
    lista_wszytskich_zakupow_na_caly_tydzien = []
    for dni in range(7):
        actual = '2022-01-0' + str(dni + 1)
        lodowka = actual_lod(lodowka, actual)
        for lsti in lista_priorytetów:
            if lsti[0] == actual:
                ktory_posilek = lsti[2]
                dl = ktory_posilek.index[ktory_posilek['Nazwa_dania'] == lsti[1]]
                ktory_posilek.at[dl, "Bonus"] = 1000
        best_roz_s, best_pkt, best_lod, best_lista, best_suma_kalorii, punkty, iteration = tabu_product(lodowka, ilosc_iteracji, na_ile_blokujemy_tabu, wybor_sposobu_znalezienia_bazy_startowej,  metod, metoda_iter, actual)
        zestawy.append(best_roz_s)
        for d in best_lista:
            lista_wszytskich_zakupow_na_caly_tydzien.append(d)
        calculate_when_dish_used(zestawy)
        reload_points_for_dishes(best_lod)
        lodowka = best_lod
        iter_all += iteration
        wykresy.append(punkty)
        zestawy_najlepsze_punkty.append(best_pkt)
        kalorie.append(best_suma_kalorii)
        iteracje.append(ilosc_iteracji)
        cena_d.append(counting_cash_to_spend_on_groceries(best_lista))

    lista_wszytskich_zakupow_na_caly_tydzien = update_list(lista_wszytskich_zakupow_na_caly_tydzien)
    return wykresy, zestawy_najlepsze_punkty, zestawy, lista_wszytskich_zakupow_na_caly_tydzien, kalorie, iteracje, cena_d

def week_set(lodowka, ilosc_iteracji, na_ile_blokujemy_liste, wybor_sposobu_znalezienia_bazy_startowej,  metod, metoda_iter):
    """Funkcja wylicza zestawy dań dla całego tygodnia na podstawie zestawu zwracanego przez funkcję tabu_product_wersja_2
    :param lodowka: lodówka
    :param ilosc_iteracji: ilość iteracji algorytmu tabu
    :param na_ile_blokujemy_liste: Jak długa jest lista tabu
    :param metod: wybór metody
    :param metoda_iter: wybór ilości dla metody iteracyjnej
    :cut_par: moment przerwania iteracji
    :param wybor_sposobu_znalezienia_bazy_startowej: 0 losowy, 1 najlepsza baza"""
    zestawy_najlepsze_punkty = []
    wykresy = []
    kalorie = []
    iteracje = []
    iter_all = 0
    zestawy = []
    lista_wszytskich_zakupow_na_caly_tydzien = []
    cena_d = []
    for dni in range(7):
        actual = '2022-01-0' + str(dni + 1)
        lodowka = actual_lod(lodowka, actual)
        for lsti in lista_priorytetów:
            if lsti[0] == actual:
                ktory_posilek = lsti[2]
                dl = ktory_posilek.index[ktory_posilek['Nazwa_dania'] == lsti[1]]
                ktory_posilek.at[dl, "Bonus"] = 1000
        best_roz_s, best_pkt, best_lod, best_lista, best_suma_kalorii, punkty, iteration = tabu_set(ilosc_iteracji,wybor_sposobu_znalezienia_bazy_startowej,na_ile_blokujemy_liste,metod,lodowka,actual,metoda_iter)
        kalorie.append(best_suma_kalorii)
        iteracje.append(iteration)
        zestawy.append(best_roz_s)
        zestawy_najlepsze_punkty.append(best_pkt)
        for d in best_lista:
            lista_wszytskich_zakupow_na_caly_tydzien.append(d)
        calculate_when_dish_used(zestawy)
        reload_points_for_dishes(best_lod)
        lodowka = best_lod
        iter_all += iteration
        wykresy.append(punkty)
        cena_d.append(counting_cash_to_spend_on_groceries(best_lista))

    lista_wszytskich_zakupow_na_caly_tydzien = update_list(lista_wszytskich_zakupow_na_caly_tydzien)
    return wykresy, zestawy_najlepsze_punkty, zestawy, lista_wszytskich_zakupow_na_caly_tydzien, kalorie, iteracje, cena_d


####################################################################

"""Testy poprawności działania funkcji"""

#week_set_tabu_product(lodowka)

