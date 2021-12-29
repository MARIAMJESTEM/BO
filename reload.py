import add
from core import sniadania, sniadania2, obiad, kolacja, podwieczorek

# baza = [sniadania, sniadania2]
# pora = ['1S','2S']
pora = 'P'
baza = [podwieczorek]

p = 0
for b in baza:
    for j in range(len(b)):
        nazwa = b['Nazwa_dania'][j]
        produkty = b['Produkty'][j]
        add.append_new_dish(nazwa,produkty,pora)
    p += 1


