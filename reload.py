import core
import add
from core import sniadania, sniadania2, obiad, kolacja

baza = [sniadania, sniadania2]
pora = ['1S','2S']
# pora = '0'
# baza = [obiad]

p = 0
for b in baza:
    for j in range(len(b)):
        nazwa = b['Nazwa_dania'][j]
        produkty = b['Produkty'][j]
        link = b['Link'][j]
        add.append_new_dish(nazwa,produkty,pora[p],link)
    p += 1


