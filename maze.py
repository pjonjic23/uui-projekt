from dataclasses import dataclass
from typing import List, Tuple

Poz = Tuple[int, int]

@dataclass
class Labirint:
    mreza: List[List[str]]
    pocetak: Poz
    izlaz: Poz

    @property
    def redovi(self) -> int:
        return len(self.mreza)

    @property
    def stupci(self) -> int:
        return len(self.mreza[0]) if self.mreza else 0

    def je_u_granicama(self, r: int, s: int) -> bool:
        return 0 <= r < self.redovi and 0 <= s < self.stupci

    def je_prohodno(self, r: int, s: int) -> bool:
        return self.mreza[r][s] != '#'

    def susjedi_4(self, p: Poz) -> List[Poz]:
        r, s = p
        kandidati = [(r - 1, s), (r + 1, s), (r, s - 1), (r, s + 1)]
        out: List[Poz] = []
        for rr, ss in kandidati:
            if self.je_u_granicama(rr, ss) and self.je_prohodno(rr, ss):
                out.append((rr, ss))
        return out

def ucitaj_labirint_iz_teksta(tekst: str) -> Labirint:
    linije = [ln.rstrip("\n") for ln in tekst.splitlines() if ln.strip() != ""]
    if not linije:
        raise ValueError("Prazan ulaz labirinta.")

    sirina = max(len(ln) for ln in linije)
    mreza: List[List[str]] = []
    pocetak = izlaz = None

    for r, ln in enumerate(linije):
        ln = ln.ljust(sirina, '#')
        red = list(ln)
        for s, znak in enumerate(red):
            if znak == 'S':
                pocetak = (r, s)
            elif znak == 'E':
                izlaz = (r, s)
        mreza.append(red)

    if pocetak is None or izlaz is None:
        raise ValueError("Labirint mora sadržavati 'S' (početak) i 'E' (izlaz).")

    return Labirint(mreza=mreza, pocetak=pocetak, izlaz=izlaz)

def ucitaj_labirint_iz_datoteke(putanja: str) -> Labirint:
    
    with open(putanja, "r", encoding="utf-8") as f:
        tekst = f.read()
        
    return ucitaj_labirint_iz_teksta(tekst)

def prikazi_labirint_s_putem(lab: Labirint, put: List[Poz]) -> str:
    g = [red[:] for red in lab.mreza]
    for (r, s) in put:
        if g[r][s] in ('.', ' '):
            g[r][s] = '*'
    pr, ps = lab.pocetak
    ir, is_ = lab.izlaz
    g[pr][ps] = 'S'
    g[ir][is_] = 'E'
    return "\n".join("".join(red) for red in g)
