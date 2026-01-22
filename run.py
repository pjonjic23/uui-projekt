import sys
import os
from maze import ucitaj_labirint_iz_datoteke, prikazi_labirint_s_putem
from algorithms import a_zvijezda, pretrazivanje_u_dubinu

def pokreni_jednu_mapu(putanja: str):
    lab = ucitaj_labirint_iz_datoteke(putanja)

    put_a, pos_a, ms_a = a_zvijezda(lab)
    print("MAPA:", putanja)
    print("A*")
    print("pronađen put:", "DA" if put_a else "NE")
    if put_a:
        print("duljina puta:", len(put_a) - 1)
    print("posjećeno polja:", pos_a)
    print("vrijeme (ms):", round(ms_a, 3))
    print()
    if put_a:
        print(prikazi_labirint_s_putem(lab, put_a))
        print()

    put_d, pos_d, ms_d = pretrazivanje_u_dubinu(lab)
    print("DFS")
    print("pronađen put:", "DA" if put_d else "NE")
    if put_d:
        print("duljina puta:", len(put_d) - 1)
    print("posjećeno polja:", pos_d)
    print("vrijeme (ms):", round(ms_d, 3))
    print()
    if put_d:
        print(prikazi_labirint_s_putem(lab, put_d))
        print()

def pokreni_folder(folder: str):
    datoteke = sorted([f for f in os.listdir(folder) if f.lower().endswith(".txt")])
    if not datoteke:
        print("Nema .txt mapa u folderu:", folder)
        return

    print("MAPA | A*_duljina | A*_posjeceno | A*_ms | DFS_duljina | DFS_posjeceno | DFS_ms")
    print("-" * 90)

    for ime in datoteke:
        putanja = os.path.join(folder, ime)
        lab = ucitaj_labirint_iz_datoteke(putanja)

        put_a, pos_a, ms_a = a_zvijezda(lab)
        put_d, pos_d, ms_d = pretrazivanje_u_dubinu(lab)

        a_len = (len(put_a) - 1) if put_a else "-"
        d_len = (len(put_d) - 1) if put_d else "-"

        print(f"{ime} | {a_len} | {pos_a} | {ms_a:.3f} | {d_len} | {pos_d} | {ms_d:.3f}")

def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "maps"

    if os.path.isdir(target):
        pokreni_folder(target)
    else:
        pokreni_jednu_mapu(target)

if __name__ == "__main__":
    main()
