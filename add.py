import core
import pandas as pd
from copy import deepcopy


def calculate_product_to_store_points(price):
    """
    Funkcja licząca punkty produktów ze sklepu

    :param price: Cena produktu
    :return: Liczba punktów za produkt
    """
    return price * -2


def calculation_calories_and_proteins_for_dish(idx: int = 0, baza: str = '', produkt = '0'):
    """
    Funkcja obliczająca ilość kalorii i białka w daniu

    :param idx: indeks w bazie
    :param baza: baza
    :param produkt: lista produktów jeśli dodawane jest nowe danie
    :return: Kalorie i Białko
    """
    K = 0
    B = 0
    if produkt == '0':
        list = core.read_sklad(idx, baza)
    else:
        list = core.read_sklad(produkt = produkt)
    for j in range(len(list)):
        if len(list[j]) == 2:
            nazwa = list[j][0]
            waga = float(list[j][1])
            kalorie = float(core.sklep['Kalorie'][nazwa])
            bialko = float(core.sklep['Białko'][nazwa])
            K += float(waga/100 * kalorie)
            B += float(waga/100 * bialko)

        if len(list[j]) == 3:
            nazwa = list[j][0]
            sztuka = float(list[j][1])
            kalorie = float(core.sklep['Kalorie'][nazwa])
            bialko = float(core.sklep['Białko'][nazwa])
            K += float(sztuka * kalorie)
            B += float(sztuka * bialko)

    return K, B


def add_product_to_store(name, price, calories, protein, pieces='NaN', weight='NaN'):
    """
    Funkcja dodająca produkt do sklepu

    :param name: Nazwa produktu
    :param price: Cena produktu
    :param calories: Ilość kalorii na 100g lub jedną sztukę
    :param protein: Ilość białka na 100g lub 1 sztukę
    :param pieces: Ilość produktu w sztukach
    :param weight: Waga produktu
    """
    points = calculate_product_to_store_points(price)
    df = pd.DataFrame({'Nazwa': [name], 'Cena': [price], 'Sztuka': [pieces], 'Waga': [weight],
                       'Kalorie': [calories], 'Białko': [protein], 'Punkty': [points]})
    df.to_csv('bazy_danych\produkty_w_sklepie.csv', sep=';', mode='a', index=False, header=False)


def add_product_to_fridge(name, date, pieces='NaN', weight='NaN'):
    """
    Funkcja dodająca produkt do lodówki

    :param name: Nazwa produktu
    :param date: Data ważności produktu
    :param pieces: Ilość sztuk
    :param weight: Waga produktu
    """
    points = core.calculate_product_to_fridge_points(date, '2022-01-01')
    df = pd.DataFrame({'Nazwa': [name], 'Sztuka': [pieces], 'Waga': [weight], 'Punkty': [points], 'Data': [date]})
    df.to_csv('bazy_danych\lodowka.csv', sep=';', mode='a', index=False, header=False)


def append_new_dish(name: str, produkt: str, pora: str):
    """
    Funkcja dodająca nowe danie

    :param name: Nazwa
    :param produkt:Lista produktów
    :param pora: Pora dnia 1S - siadanie, 2S - sniadanie2, O - obiad, P - podwieczorek, K - Kolacja
    """
    Kal, Bia = calculation_calories_and_proteins_for_dish(0, '', produkt)
    l = deepcopy(core.lodowka)
    lod, pkt, lst = core.calculation_points_for_dish(l, 0, '', produkt)
    if pora == "1S":
        df = pd.DataFrame({'Nazwa_dania': [name], 'Produkty': [produkt], 'Kalorie': [Kal], 'Białko': [Bia], "Punkty": [pkt], 'Tabu': [0]})
        df.to_csv('bazy_danych\sniadania.csv', sep=';', mode='a', index=False, header=False)

    if pora == "2S":
        df = pd.DataFrame({'Nazwa_dania': [name], 'Produkty': [produkt], 'Kalorie': [Kal], 'Białko': [Bia], "Punkty": [pkt], 'Tabu': [0]})
        df.to_csv('bazy_danych\sniadanie2.csv', sep=';', mode='a', index=False, header=False)

    if pora == "O":
        df = pd.DataFrame({'Nazwa_dania': [name], 'Produkty': [produkt], 'Kalorie': [Kal], 'Białko': [Bia], "Punkty": [pkt], 'Tabu': [0]})
        df.to_csv('bazy_danych\obiad.csv', sep=';', mode='a', index=False, header=False)

    if pora == "P":
        df = pd.DataFrame(
            {'Nazwa_dania': [name], 'Produkty': [produkt], 'Kalorie': [Kal], 'Białko': [Bia], "Punkty": [pkt],
             'Tabu': [0]})
        df.to_csv('bazy_danych\podwieczorek.csv', sep=';', mode='a', index=False, header=False)

    if pora == "K":
        df = pd.DataFrame({'Nazwa_dania': [name], 'Produkty': [produkt], 'Kalorie': [Kal], 'Białko': [Bia], "Punkty": [pkt], 'Tabu': [0]})
        df.to_csv('bazy_danych\kolacja.csv', sep=';', mode='a', index=False, header=False)
