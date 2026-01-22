import heapq
import time
from typing import Dict, List, Set, Tuple
from maze import Labirint, Poz

def manhattan_udaljenost(a: Poz, b: Poz) -> int:
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def rekonstruiraj_put(roditelj: Dict[Poz, Poz], pocetak: Poz, cilj: Poz) -> List[Poz]:
    if cilj == pocetak:
        return [pocetak]
    if cilj not in roditelj:
        return []
    trenutni = cilj
    put = [trenutni]
    while trenutni != pocetak:
        trenutni = roditelj[trenutni]
        put.append(trenutni)
    put.reverse()
    return put

def a_zvijezda(lab: Labirint) -> Tuple[List[Poz], int, float]:
    t0 = time.perf_counter()

    pocetak, cilj = lab.pocetak, lab.izlaz
    otvoreni: List[Tuple[int, int, Poz]] = []
    heapq.heappush(otvoreni, (manhattan_udaljenost(pocetak, cilj), 0, pocetak))

    g_vrijednost: Dict[Poz, int] = {pocetak: 0}
    roditelj: Dict[Poz, Poz] = {}
    zatvoreni: Set[Poz] = set()

    broj_posjecenih = 0

    while otvoreni:
        f, g, trenutni = heapq.heappop(otvoreni)

        if trenutni in zatvoreni:
            continue
        zatvoreni.add(trenutni)
        broj_posjecenih += 1

        if trenutni == cilj:
            put = rekonstruiraj_put(roditelj, pocetak, cilj)
            t1 = time.perf_counter()
            return put, broj_posjecenih, (t1 - t0) * 1000.0

        for susjed in lab.susjedi_4(trenutni):
            if susjed in zatvoreni:
                continue

            novi_g = g_vrijednost[trenutni] + 1
            if novi_g < g_vrijednost.get(susjed, 10**9):
                roditelj[susjed] = trenutni
                g_vrijednost[susjed] = novi_g
                novi_f = novi_g + manhattan_udaljenost(susjed, cilj)
                heapq.heappush(otvoreni, (novi_f, novi_g, susjed))

    t1 = time.perf_counter()
    return [], broj_posjecenih, (t1 - t0) * 1000.0

def pretrazivanje_u_dubinu(lab: Labirint) -> Tuple[List[Poz], int, float]:
    t0 = time.perf_counter()

    pocetak, cilj = lab.pocetak, lab.izlaz
    stog = [pocetak]
    posjeceni: Set[Poz] = {pocetak}
    roditelj: Dict[Poz, Poz] = {}
    broj_posjecenih = 0

    while stog:
        trenutni = stog.pop()
        broj_posjecenih += 1

        if trenutni == cilj:
            put = rekonstruiraj_put(roditelj, pocetak, cilj)
            t1 = time.perf_counter()
            return put, broj_posjecenih, (t1 - t0) * 1000.0

        for susjed in lab.susjedi_4(trenutni):
            if susjed not in posjeceni:
                posjeceni.add(susjed)
                roditelj[susjed] = trenutni
                stog.append(susjed)

    t1 = time.perf_counter()
    return [], broj_posjecenih, (t1 - t0) * 1000.0
