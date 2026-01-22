# Pronalaženje rute u labirintu (A\* i DFS)

Projekt iz kolegija **Uvod u umjetnu inteligenciju**. Aplikacija učitava tekstualne mape labirinta i uspoređuje algoritme **A\*** i **DFS** kroz:
- konzolni način rada (CLI) za brzu obradu jedne ili više mapa
- grafičko sučelje (Tkinter) za učitavanje mape i vizualizaciju pronađene rute

## Pokretanje (CLI)

1) Pokretanje nad svim mapama u direktoriju maps/ (zadano):
python run.py

Alternativno (eksplicitno zadavanje direktorija):
python run.py maps/

2) Pokretanje nad određenom mapom:
python run.py maps/map1.txt

## Pokretanje (GUI)

python gui.py

U sučelju:
- učitaj mapu (.txt)
- pokreni A\* / DFS / oba
- pogledaj metrike i vizualizaciju pronađenog puta na mreži

## Format mape

Svaki znak predstavlja jedno polje mreže:
- \# zid (neprohodno)
- . prolaz (prohodno)
- S početak
- E cilj
  
