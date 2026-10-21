"""Crea los NPC del pueblo a partir del sprite de frente de Pedro (assets/NewSprite13.png), para que tengan
exactamente sus proporciones, contorno y piel. Cada NPC tiene 2 cuadros: quieto (1) y parpadeando (2).
Uso: python3 arte/npcs.py"""
from PIL import Image
import os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
base = Image.open(os.path.join(B, "assets/NewSprite13.png")).convert("RGBA")
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
PELO, PELO_OSC, PIEL = H("#46200a"), H("#311200"), H("#e3bc9a")
CAM_OSC, CAM, OVER_OSC, OVER, CONT = H("#560505"), H("#ad0a0a"), H("#048288"), H("#07d4de"), H("#3a3434")

def recolor(img, mapa):
    img = img.copy(); px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y] in mapa: px[x, y] = mapa[px[x, y]]
    return img
def parpadeo(img):
    img = img.copy(); px = img.load()
    for x in (12, 13, 19, 20):
        px[x, 12] = PIEL; px[x, 14] = PIEL if px[x, 14] == CONT else px[x, 14]
    for x in (11, 12, 13, 19, 20, 21): px[x, 13] = CONT
    return img
def guardar(nombre, img):
    img.save(os.path.join(B, "Pueblo/%s1.png" % nombre)); parpadeo(img).save(os.path.join(B, "Pueblo/%s2.png" % nombre))

# Dona Rosa: canosa con monio, blusa morada y delantal verde
rosa = recolor(base, {PELO: H("#c2c3c7"), PELO_OSC: H("#8b8d96"), CAM_OSC: H("#45283c"), CAM: H("#76428a"),
                      OVER_OSC: H("#4b692f"), OVER: H("#6abe30")})
px = rosa.load()
GRIS, GRIS2, BLANCO = H("#c2c3c7"), H("#8b8d96"), H("#ffffff")
for y in range(0, 3):          # monio redondo encima de la cabeza
    for x in range(12, 21): px[x, y] = (0, 0, 0, 0)
MONIO = [".aaaaa.", "agGggga", "aggggGa"]
for y, fila in enumerate(MONIO):
    for i, ch in enumerate(fila):
        if ch != ".": px[13 + i, y] = {"a": CONT, "g": GRIS, "G": GRIS2}[ch]
px[15, 1] = BLANCO
guardar("Rosa", rosa)

# Don Fermin: calvo, patillas cafes, barba gris, camisa gris y delantal de cuero, martillo en la mano
fermin = recolor(base, {CAM_OSC: H("#595652"), CAM: H("#847e87"), OVER_OSC: H("#663931"), OVER: H("#8f563b")})
px = fermin.load()
for y in range(3, 9):          # coronilla calva
    for x in range(8, 25):
        if px[x, y] in (PELO, PELO_OSC): px[x, y] = PIEL if y > 3 else px[x, y]
for x in range(11, 22): px[x, 4] = PIEL
px[14, 5] = H("#fff0d8"); px[15, 5] = H("#fff0d8")                      # brillo de la calva
for y in range(9, 12):
    for x in range(8, 25):
        if px[x, y] == PELO: px[x, y] = H("#46200a")
for y in range(14, 19):        # barba
    for x in range(9, 24):
        c = px[x, y]
        if c in (PIEL, H("#e3775a")) or (y >= 16 and c[3] > 0 and c != CONT):
            px[x, y] = H("#9badb7") if (x + y) % 3 else H("#696a6a")
for x in range(13, 20): px[x, 15] = H("#663931")                         # boca
# martillo
for y in range(17, 25): px[25, y] = H("#8f563b")
for x in range(23, 29):
    for y in range(15, 18): px[x, y] = H("#696a6a")
px[23, 15] = CONT; px[28, 17] = CONT; px[24, 15] = H("#9badb7")
guardar("Fermin", fermin)
print("ok")
