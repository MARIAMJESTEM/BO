import add
from core import sniadania, sniadania2, obiad, kolacja, podwieczorek


pora = ['1S','2S','O','K','P']
baza = [sniadania, sniadania2, obiad, kolacja, podwieczorek]

p = 0
for b in baza:
    for j in range(len(b)):
        nazwa = b['Nazwa_dania'][j]
        produkty = b['Produkty'][j]
        add.append_new_dish(nazwa,produkty,pora[p])
    p += 1


