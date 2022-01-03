import unittest
import pandas as pd
import numpy as np

from core import calculation_points_for_dish
from core import aktualization
from core import roz_start


#Wczytanie baz danych do programu
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



lod1 = pd.read_csv("bazy_danych\lodowki_do_testow\lod1.csv", sep = ';')
lod2 = pd.read_csv("bazy_danych\lodowki_do_testow\lod2.csv", sep = ';')
lod3 = pd.read_csv("bazy_danych\lodowki_do_testow\lod3.csv", sep = ';')

class TestListaZakupow(unittest.TestCase):
    def test_1(self): #gdy nie ma dwóch rzeczy w ogóle w lodówce
        #lod1
        lodowka, suma, lista_produktow_do_dokupienia =calculation_points_for_dish(lod1, 2, podwieczorek)
        self.assertEqual(lista_produktow_do_dokupienia, [ ["Bułka", 2, np.nan, 0.6],["Masło", np.nan, 200.0, 6.89]])

    def test_2(self): #gdy jest za mało danej rzczy w lodówce w przypadku wagi
        #lod2
        lodowka, suma, lista_produktow_do_dokupienia = calculation_points_for_dish(lod2, 2, podwieczorek)
        self.assertEqual(lista_produktow_do_dokupienia, [["Masło", np.nan, 200.0, 6.89]])

    def test_3(self): #gdy jest za mało danej rzczy w lodówce w przypadku sztuki
        #lod3
        lodowka, suma, lista_produktow_do_dokupienia = calculation_points_for_dish(lod3, 2, podwieczorek)
        self.assertEqual(lista_produktow_do_dokupienia, [["Bułka", 1.0, np.nan, 0.3]])

    def test_4(self):#sprawdzenie działania listy zakupów dla całego jednego rozwiązania
        rozwiazanie_startowe = [sniadania['Nazwa_dania'][9], sniadania2['Nazwa_dania'][4], obiad['Nazwa_dania'][4],podwieczorek['Nazwa_dania'][4], kolacja['Nazwa_dania'][10]]
        lod, sum, lista = aktualization(rozwiazanie_startowe)
        self.assertEqual([['Mleko', np.nan, 1000.0, 2.89], ['Drożdżówka z serem', 1.0, np.nan, 3.0], ['Boczek', np.nan, 150.0, 3.49], ['Bulion', np.nan, 1000.0, 0.6], ['Mango', 1.0, np.nan, 5.5], ['Mozarella', 1.0, np.nan, 3.2], ['Bułka', 2.0, np.nan, 0.6]], lista)




if __name__ == '__main__':
    unittest.main()