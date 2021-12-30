import add
from core import sniadania, sniadania2, obiad, kolacja, podwieczorek


pora = 'O'
baza = [obiad]

p = 0
for b in baza:
    for j in range(len(b)):
        nazwa = b['Nazwa_dania'][j]
        produkty = b['Produkty'][j]
        add.append_new_dish(nazwa,produkty,pora)
    p += 1


