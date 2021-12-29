## Spis treści
* [Informcje ogólne](#informacje-ogólne)
* [Funkcjonalności](#funkcjonalności)
* [Opcje](#opcje-obliczania-rozwiązania-końcowego)
* [Todo](#Todo)
* [Wykorzystane technologie](#technologie)
* [Pomoce naukowe](#pomoce-naukowe)

## Informacje ogólne
### Projekt powstał na labolatorium Badań Operacyjnych II. 
Jest to aplikacja, która ma zaproponować nam menu na cały tydzień **optymalizując koszty** na podstawie tego co posiadamy aktualnie w naszej lodówce, 
a także dobierać takie potrawy aby były one dla nas smaczne i posiadały zblizoną liczbę kalorii i białka. 
Dodakowo naszym zadaniem było wykorzystanie metody metaheurystycznej **Tabu Search**, która blokuje nam dania lub całe zestawy na cały dzień przez co aplikacja nie wpada w cykle.

## Funkcjonalności
* Dodanie dania do odpowiedniej bazy posiłków
* Dodanie produktu do lodówki lub bazy sklepu
* Obliczanie kalorii i białka za odpowiednie danie na podstawie informacji w sklepie
* Blokowanie powtarzania tych samych dań 
* Promowanie odpowiednich dań na dany dzień 
* Podanie listy zakupów na cały tydzień
* Zaproponowanie menu na cały tydzień 

## Opcje obliczania rozwiązania końcowego

### Metody wybierania rozwiązania startowego
* Metoda losowa
* Metoda najlepszego dania na podstawie punktów startowych

### Metody zablokowań (tabu)
* Metoda blokowania konkretnego zestawu
* Metoda blokowania konkretnego dania 

### Metody poszukiwania rozwiązania
* Metoda dokładna (sprawdza wszystkich sąsiadów) - *długi czas wykonywania*
* Metoda losowa (wybiera losowych sąsiadów)
* Metoda losowa z priorytetami (wybiera najlepszych sąsiadów z losowych baz)

## Todo
-[] Bazy danych 
-[x] Dodawanie produktów i dań 
-[x] Obliczanie punktów, kalorii i białka za konkretne danie
-[] Blokowanie powtarzania tych samych dań 
-[] Promowanie odpowiednich dań na dany dzień
-[] Naprawa błędów i bugów
-[] Gui
-[] Testy jednostkowe

## Technologie
Aplikacja powstaje w **Pythonie** wersji **3.9** (powinna działać we wczesniejszych również), zostały użyne dodatkowo biblioteki:
*pandas
*numpy
*tkinter

## Pomoce naukowe
[tkinter tutorial](https://www.youtube.com/watch?v=YXPyB4XeYLA&t=1820s)
[tkinter tutorial github](https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course)

 
 
