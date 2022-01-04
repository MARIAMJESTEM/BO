from core import *

def ranking_new2(baza_dania, rezultat, lista_rankingowa_z_lodowka, lod):
    """
               Funkcja tworzy ranking najlepszych dań dla jednego posiłku
               :param baza_dania: baza dla której będzie tworzony ranking dań
               :return: zwraca posortowaną listę rankingową
               """
    #na moje nieszczescie musze dodać dwie rzeczy do listy z jednego posiłku bo inaczej nie działa dla większej liczby iteracji :(
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
            lst = ranking_random(r, metoda_iter, lod, max_value=1)

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