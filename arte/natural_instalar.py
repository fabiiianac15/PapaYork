"""Copia los dibujos de arte/out/sprites a Natural/ con el formato que usa el juego."""
import os, shutil
from PIL import Image
A = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(A, ".."); O = os.path.join(A, "out/sprites"); N = os.path.join(B, "Natural")
def cp(src, dst):
    p = os.path.join(N, dst); os.makedirs(os.path.dirname(p), exist_ok=True); shutil.copyfile(os.path.join(O, src + ".png"), p)
for d in ("Abajo", "Arriba", "Izquierda", "Derecha"):
    for f in range(1, 5):
        cp(f"Pedro_{d}{f}", f"Pedro/{d}{f}.png"); cp(f"Papa_{d}{f}", f"Papa/{d}{f}.png")
    for f in range(1, 4):
        cp(f"Pedro_Ataque{d}{f}", f"Pedro/Ataque{d}{f}.png")
for n in ("Rosa", "Fermin", "Ramiro", "Lupita", "Tomas", "Ines", "Beto"):
    cp(n + "1", f"Vecinos/{n}1.png"); cp(n + "2", f"Vecinos/{n}2.png")
for n in ("Pedro", "PedroSin", "Hetol", "Chuchini", "ChuchiniViejo", "Rosa", "Fermin", "Ramiro", "Lupita", "Tomas", "Ines", "Beto"):
    im = Image.open(os.path.join(O, f"Retrato{n}.png")).convert("RGBA").resize((128, 128), Image.NEAREST)
    p = os.path.join(N, f"Retratos/{n}.png"); os.makedirs(os.path.dirname(p), exist_ok=True); im.save(p)
for t in ("Zanahoria", "Papa", "PapaMutante"):
    for i in range(4): cp(f"{t}_{i}", f"Cultivos/{t}_{i}.png")
for n in ("Regadera", "EnergiaMarco", "EnergiaRelleno", "Granero"): cp(n, f"Objetos/{n}.png")
# Pedro con sombrero: caminar, correr, reposo y golpes
for d in ("Abajo", "Arriba", "Izquierda", "Derecha"):
    for f in range(1, 9):
        cp(f"PedroN_{d}{f}", f"Pedro2/{d}{f}.png"); cp(f"PedroN_Correr{d}{f}", f"Pedro2/Correr{d}{f}.png")
    for f in range(1, 4):
        cp(f"PedroN_Quieto{d}{f}", f"Pedro2/Quieto{d}{f}.png"); cp(f"PedroN_Ataque{d}{f}", f"Pedro2/Ataque{d}{f}.png")
cp("PolvoPaso", "Pedro2/PolvoPaso.png")
for d in ("Abajo", "Arriba", "Izquierda", "Derecha"):
    for f in range(1, 4): cp(f"PedroN_Espada{d}{f}", f"Pedro2/Espada{d}{f}.png")
for d in ("Abajo", "Arriba", "Izquierda", "Derecha"):
    for h in ("Hacha", "Pico", "Azadon"):
        for f in range(1, 6): cp(f"PedroN_{h}{d}{f}", f"Pedro2/{h}{d}{f}.png")
    for f in range(1, 5): cp(f"PedroN_Regar{d}{f}", f"Pedro2/Regar{d}{f}.png")
    for n, t in (("Lanzar", 3), ("Esperar", 2), ("Tirar", 2)):
        for f in range(1, t + 1): cp(f"PedroN_Pesca{n}{d}{f}", f"Pedro2/Pesca{n}{d}{f}.png")
# Carita de la barra de vida con el sombrero de Pedro
marco = Image.open(os.path.join(B, "assets/Marco-Barra-de-Vida2.png")).convert("RGBA"); mp = marco.load()
HEX = lambda t: tuple(int(t[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
Q = [HEX(c) for c in ("#f7e3a4", "#e3c478", "#bd9a58", "#8d7044", "#2e6e7c", "#2a1d2b")]
for x in range(0, 21):
    mp[x, 11] = Q[5]; mp[x, 14] = Q[5]
for x in range(1, 20):
    mp[x, 12] = Q[0] if x < 9 else Q[1]; mp[x, 13] = Q[2] if x < 16 else Q[3]
for x in range(6, 15):
    mp[x, 6] = Q[5]; mp[x, 10] = Q[4]
for y in range(8, 10):
    for x in range(5, 16):
        mp[x, y] = Q[0] if x < 8 else Q[2] if x > 13 else Q[1]
for x in range(6, 15):
    mp[x, 7] = Q[0] if x < 9 else Q[1]
for x, y in ((5, 7), (15, 7), (4, 8), (16, 8), (4, 9), (16, 9), (4, 10), (16, 10)):
    mp[x, y] = Q[5]
for x, y in ((5, 10), (15, 10)):
    mp[x, y] = Q[4]
marco.save(os.path.join(N, "Objetos/MarcoVida.png"))
# Elenco de la introducción y del desmayo
for n in ("Hija", "Hijo", "PedroNino"):
    for f in (1, 2): cp(f"Actor_{n}_Frente{f}", f"Actores/{n}_Frente{f}.png")
for n in ("Hetol", "Chuchini", "ChuchiniSombrero", "ChuchiniViejo", "ChuchiniViejoSin", "PedroSin", "Tomas"):
    for f in range(1, 9): cp(f"Actor_{n}_Camina{f}", f"Actores/{n}_Camina{f}.png")
    for f in (1, 2):
        cp(f"Actor_{n}_Lado{f}", f"Actores/{n}_Lado{f}.png"); cp(f"Actor_{n}_Frente{f}", f"Actores/{n}_Frente{f}.png")
for n in ("PedroCae1", "PedroCae2", "PedroCae3", "SombreroSuelo", "Sombrero", "Farol", "Halo"): cp("Actor_" + n, f"Actores/{n}.png")
cp("Zanahoria_Icono", "Objetos/Zanahoria.png")
for n in ("Rosa", "Fermin", "Ramiro", "Lupita", "Tomas", "Ines", "Beto"):
    for d in ("Abajo", "Arriba", "Izquierda", "Derecha"):
        for f in range(1, 5): cp(f"Vecino_{n}_{d}{f}", f"Vecinos/{n}_{d}{f}.png")
# La casa vieja ocupaba (12,8)-(110,100) con la puerta cerca de x=46: se encaja igual
casa = Image.open(os.path.join(O, "Casa.png")).convert("RGBA")
lienzo = Image.new("RGBA", (128, 128), (0, 0, 0, 0)); lienzo.alpha_composite(casa.crop((7, 7, 128, 128)), (0, 0))
lienzo.save(os.path.join(N, "Objetos/Casa.png"))
print("ok")
