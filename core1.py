import pandas as pd
import numpy as np
import random
import datetime
from copy import deepcopy

#Wczytanie baz danych do programu
sniadania = pd.read_csv("bazy_danych\sniadania.csv", sep = ';')
sniadania2 = pd.read_csv("bazy_danych\sniadanie2.csv", sep = ';')
obiad = pd.read_csv("bazy_danych\obiad.csv", sep = ';')
podwieczorek = pd.read_csv("bazy_danych\sniadanie2.csv", sep = ';')
kolacja = pd.read_csv("bazy_danych\kolacja.csv", sep = ';')
lodowka = pd.read_csv("bazy_danych\lodowka2.csv", sep =';')

sniadania.name = "sniadania"
sniadania2.name = "sniadania2"
obiad.name = "obiad"
podwieczorek.name = "podwieczorek"
kolacja.name = "kolacja"

l_pomocnicza = pd.read_csv("bazy_danych\lodowka2.csv", sep =';')
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
    :param produkt: Lista produktów jeśli dodajemy nowy produkt
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


def aktualization(result):
    nbaza = [sniadania, sniadania2, obiad, podwieczorek, kolacja]
    suma = 0
    lod = deepcopy(lodowka)
    for r,b in zip(reversed(result), reversed(nbaza)):
        df = b[b['Nazwa_dania'] == r]
        l, s = calculation_points_for_dish(lod,df.index[0],b)
        lod = l
        suma += s
    return lod, suma


def ranking_new(baza_dania, rezultat, lista_rankingowa_z_lodowka = []):
    klucz_do_nazw_posilkow = {"sniadania": 1, "sniadania2": 2, "obiad": 3, "podwieczorek": 4, "kolacja": 5}
    numer_w_liscie_rezultat = klucz_do_nazw_posilkow[baza_dania.name] - 1
    for index, row in baza_dania.iterrows():
        if baza_dania.iloc[index, 0] != rezultat[numer_w_liscie_rezultat]:
            rezultat[numer_w_liscie_rezultat] = baza_dania.iloc[index, 0]
            wynik = rezultat[:]
            lod, sum = aktualization(rezultat)
            lista_rankingowa_z_lodowka.append([wynik,sum,numer_w_liscie_rezultat])

    #sortowanie po sumie żeby utowrzyć ranking
    for i in range(len(lista_rankingowa_z_lodowka) - 1):
        for j in range(0, len(lista_rankingowa_z_lodowka) - i - 1):
            if lista_rankingowa_z_lodowka[j][1] < lista_rankingowa_z_lodowka[j + 1][1]:
                lista_rankingowa_z_lodowka[j], lista_rankingowa_z_lodowka[j + 1] = lista_rankingowa_z_lodowka[j + 1], lista_rankingowa_z_lodowka[j]

    return lista_rankingowa_z_lodowka

def tabu_list_actualization(tabu_list: list):
    """
    Funkcja aktualizuje ilość iteracji na które elementy zostały umieszczone w liście tabu
        :param tabu_list: lista tabu postaci [[nazwa_dania1, ilosc iteracji1], [nazwa_dania2, ilosc_iteracji2]]
        """
    for i in tabu_list:
        if i[1] > 1:
            i[1] -=1
        else:
            tabu_list.remove(i)
    return tabu_list


def tabu(iter, bs, t_idx, t_iter = 7):
    """

    :param iter: ilośc iteracji
    :param bs: wybór sposobu znalezienia bazy startowej 0 lub 1
    :param t_idx: 0 stała lista tabu zestawu na stałe, 1 zablokowanie dania na tabu_iter rund
    :return: wynik końcowy
    """
    roz_s = roz_start(bs)
    r = roz_s[:]
    lod_str, pkt_str = aktualization(roz_s)
    best_roz_s = roz_s[:]
    best_pkt = pkt_str
    best_lod = lod_str[:]
    tabu_list = []
    i = 0
    baz = [sniadania, sniadania2, obiad, podwieczorek, kolacja]

    for it in range(iter):
        lst = ranking_new(sniadania, r, [])
        lst = ranking_new(sniadania2, r, lst)
        lst = ranking_new(obiad, r, lst)
        lst = ranking_new(podwieczorek, r, lst)
        lst = ranking_new(kolacja, r, lst)

        if t_idx == 0:    #nie dodałem jeszcze kryterium aspiracji,  czy napewno tu trzeba ją tu dawac ?
            while True:
                if lst[i][0] not in tabu_list:
                    tab = lst[i][0][:]
                    tabu_list.append(tab)
                    break

                i += 1

            if lst[i][1] > best_pkt:
                best_pkt = lst[i][1]
                best_roz_s = lst[i][0]
                # best_lod = lst[i][3] # dla lodówki jeszcze nie dodane

        if t_idx == 1:
            while True:
                numer = lst[i][2]
                k = baz[numer]
                df = k[k["Nazwa_dania"] == lst[i][0][numer]]
                if k['Tabu'][df.index[0]] != 0 and lst[i][1] > best_pkt:  #kryterium aspiracji
                    k['Tabu'][df.index[0]] = t_iter
                    break

                if k['Tabu'][df.index[0]] == 0: #blokowanie tabu jeśli nie było to zabronione wcześniej
                    k['Tabu'][df.index[0]] = t_iter
                    break

                i += 1

            if lst[i][1] > best_pkt:
                best_pkt = lst[i][1]
                best_roz_s = lst[i][0]
                # best_lod = lst[i][3] # dla lodówki jeszcze nie dodane


        r = lst[i][0]
        r1 = lst[i][1]

        lst = []
        i = 0
        print(r,r1)
        # print(tabu_list)

    print(best_lod,"\n", best_pkt, "\n", best_roz_s)



tabu(20, 1, 1)














