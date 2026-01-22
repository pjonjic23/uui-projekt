import tkinter as tk
from tkinter import filedialog, messagebox
import os

try:
    from maze import ucitaj_labirint_iz_datoteke
    from algorithms import a_zvijezda, pretrazivanje_u_dubinu
except Exception as e:
    raise ImportError(
        "Ne mogu importati maze/algorithms. Provjeri da su maze.py i algorithms.py u istom folderu kao gui.py.\n"
        f"Detalj: {e}"
    )

BOJA_ZID = "#b00000"
BOJA_PROLAZ = "#2b2b2b"
BOJA_GRID = "#3a3a3a"
BOJA_START = "#00c8ff"
BOJA_IZLAZ = "#b000ff"
BOJA_PUT = "#ffd000"

VEL_CELIJE = 22  # px


class Aplikacija(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Labirint – A* vs DFS (Tkinter)")
        self.geometry("1100x720")

        self.lab = None
        self.canvas = None
        self.rect_ids = {}  

        self._napravi_ui()

    def _napravi_ui(self):
        lijevo = tk.Frame(self, padx=10, pady=10)
        lijevo.pack(side=tk.LEFT, fill=tk.Y)

        desno = tk.Frame(self, padx=10, pady=10)
        desno.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        tk.Label(lijevo, text="Kontrole", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(0, 10))

        tk.Button(lijevo, text="Učitaj mapu (.txt)", command=self.ucitaj_mapu, width=24).pack(anchor="w", pady=4)
        tk.Button(lijevo, text="Pokreni A*", command=self.pokreni_astar, width=24).pack(anchor="w", pady=4)
        tk.Button(lijevo, text="Pokreni DFS", command=self.pokreni_dfs, width=24).pack(anchor="w", pady=4)
        tk.Button(lijevo, text="Pokreni oba", command=self.pokreni_oba, width=24).pack(anchor="w", pady=4)
        tk.Button(lijevo, text="Očisti put", command=self.ocisti_put, width=24).pack(anchor="w", pady=12)

        self.lbl_putanja = tk.Label(lijevo, text="Mapa: (nije učitana)", wraplength=220, justify="left")
        self.lbl_putanja.pack(anchor="w", pady=(10, 6))

        tk.Label(lijevo, text="Rezultati", font=("Segoe UI", 12, "bold")).pack(anchor="w", pady=(10, 6))
        self.txt_rez = tk.Text(lijevo, height=14, width=30)
        self.txt_rez.pack(anchor="w")

        tk.Label(desno, text="Prikaz mape", font=("Segoe UI", 14, "bold")).pack(anchor="w")

        self.canvas = tk.Canvas(desno, bg=BOJA_GRID)
        self.canvas.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        legenda = tk.Label(
            desno,
            text="Legenda: # zid (crveno), . prolaz (tamno), S start (plavo), E izlaz (ljubičasto), put (žuto)",
            fg="#dddddd",
            bg=BOJA_GRID,
            padx=6,
            pady=4
        )
        legenda.place(relx=0.0, rely=1.0, anchor="sw")

    def ucitaj_mapu(self):
        putanja = filedialog.askopenfilename(
            title="Odaberi mapu",
            filetypes=[("Text file", "*.txt"), ("All files", "*.*")]
        )
        if not putanja:
            return

        try:
            self.lab = ucitaj_labirint_iz_datoteke(putanja)
        except Exception as e:
            messagebox.showerror("Greška", f"Ne mogu učitati mapu:\n{e}")
            return

        self.lbl_putanja.config(text=f"Mapa: {os.path.basename(putanja)}")
        self.txt_rez.delete("1.0", tk.END)
        self.txt_rez.insert(tk.END, "Učitano.\n")
        self.nacrtaj_mapu()

    def nacrtaj_mapu(self):
        self.canvas.delete("all")
        self.rect_ids.clear()

        if not self.lab:
            return

        rows = len(self.lab.mreza)
        cols = len(self.lab.mreza[0]) if rows else 0

        w = cols * VEL_CELIJE
        h = rows * VEL_CELIJE
        self.canvas.config(scrollregion=(0, 0, w, h))

        for r in range(rows):
            for c in range(cols):
                ch = self.lab.mreza[r][c]
                boja = BOJA_PROLAZ
                if ch == "#":
                    boja = BOJA_ZID
                if (r, c) == self.lab.pocetak:
                    boja = BOJA_START
                if (r, c) == self.lab.izlaz:
                    boja = BOJA_IZLAZ

                x1 = c * VEL_CELIJE
                y1 = r * VEL_CELIJE
                x2 = x1 + VEL_CELIJE
                y2 = y1 + VEL_CELIJE

                rid = self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=boja,
                    outline=BOJA_GRID
                )
                self.rect_ids[(r, c)] = rid


    def ocisti_put(self):

        if not self.lab:
            return

        for (r, c), rid in self.rect_ids.items():
            ch = self.lab.mreza[r][c]
            boja = BOJA_PROLAZ
            if ch == "#":
                boja = BOJA_ZID
            if (r, c) == self.lab.pocetak:
                boja = BOJA_START
            if (r, c) == self.lab.izlaz:
                boja = BOJA_IZLAZ
            self.canvas.itemconfig(rid, fill=boja)

    def _prikazi_put(self, put):
        if not self.lab:
            return
        self.ocisti_put()
        for (r, c) in put:
            if (r, c) == self.lab.pocetak or (r, c) == self.lab.izlaz:
                continue
            rid = self.rect_ids.get((r, c))
            if rid:
                self.canvas.itemconfig(rid, fill=BOJA_PUT)

    def _upisi_rez(self, naslov, put, posjeceno, ms):
        self.txt_rez.insert(tk.END, f"{naslov}\n")
        if put:
            self.txt_rez.insert(tk.END, f"  pronađen put: DA\n")
            self.txt_rez.insert(tk.END, f"  duljina puta: {len(put)-1}\n")
        else:
            self.txt_rez.insert(tk.END, f"  pronađen put: NE\n")
        self.txt_rez.insert(tk.END, f"  posjećeno polja: {posjeceno}\n")
        self.txt_rez.insert(tk.END, f"  vrijeme (ms): {ms:.3f}\n\n")
        self.txt_rez.see(tk.END)

    def pokreni_astar(self):
        if not self.lab:
            messagebox.showinfo("Info", "Prvo učitaj mapu.")
            return
        put, posjeceno, ms = a_zvijezda(self.lab)
        self.txt_rez.delete("1.0", tk.END)
        self._upisi_rez("A*", put, posjeceno, ms)
        self._prikazi_put(put)

    def pokreni_dfs(self):
        if not self.lab:
            messagebox.showinfo("Info", "Prvo učitaj mapu.")
            return
        put, posjeceno, ms = pretrazivanje_u_dubinu(self.lab)
        self.txt_rez.delete("1.0", tk.END)
        self._upisi_rez("DFS", put, posjeceno, ms)
        self._prikazi_put(put)

    def pokreni_oba(self):
        if not self.lab:
            messagebox.showinfo("Info", "Prvo učitaj mapu.")
            return
        self.txt_rez.delete("1.0", tk.END)

        put_a, pos_a, ms_a = a_zvijezda(self.lab)
        self._upisi_rez("A*", put_a, pos_a, ms_a)

        put_d, pos_d, ms_d = pretrazivanje_u_dubinu(self.lab)
        self._upisi_rez("DFS", put_d, pos_d, ms_d)

        self._prikazi_put(put_a if put_a else put_d)


if __name__ == "__main__":
    app = Aplikacija()
    app.mainloop()
