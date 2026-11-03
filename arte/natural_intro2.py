"""Piezas sueltas de la introducción, del desmayo y del menú. Requiere haber ejecutado natural_intro.py."""
import os, random
from PIL import Image, ImageDraw, ImageFont
import importlib.util, sys
A = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(A, ".."); O = os.path.join(B, "Natural/IntroN")
hx = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))
def nube(nombre, sem, ancho):
    r = random.Random(sem); im = Image.new("RGBA", (ancho + 12, 30), (0, 0, 0, 0)); p = im.load(); b = 22
    for _ in range(ancho // 5):
        cx, cy, ra = r.randint(8, ancho), r.randint(11, 18), r.randint(5, 10)
        for y in range(cy - ra, cy + ra):
            if y > b: continue
            for x in range(cx - ra, cx + ra + 1):
                if 0 <= x < im.width and 0 <= y < 30 and (x - cx) ** 2 + (y - cy) ** 2 <= ra * ra:
                    d = (y - cy) / ra
                    c = "#ffffff" if d < -.2 else "#e4edf4" if d < .35 else "#bccce0"
                    if (x - cx) / ra > .6 and c == "#ffffff": c = "#e4edf4"
                    p[x, y] = hx(c) + (255,)
    im.save(os.path.join(O, nombre + ".png"))
nube("Nube1", 3, 70); nube("Nube2", 7, 44); nube("Nube3", 9, 96)
c = Image.new("RGBA", (3, 3), (0, 0, 0, 0)); cp = c.load(); cp[1, 0] = cp[0, 1] = cp[1, 1] = cp[2, 1] = cp[1, 2] = (255, 255, 255, 235); c.save(os.path.join(O, "Copo.png"))
# Fondo del desmayo en una sola imagen
f = Image.open(os.path.join(O, "Desmayo_Cielo.png")).convert("RGBA")
for l in ("Montes", "Valle", "Frente"):
    f.alpha_composite(Image.open(os.path.join(O, f"Desmayo_{l}.png")))
f.crop((0, 0, 480, 270)).save(os.path.join(O, "DesmayoFondo.png"))
# Título: letras crema con sombra cálida, sin goteos
tam = Image.open(os.path.join(B, "GameOver/TituloGameOver.png")).size
t = Image.new("RGBA", tam, (0, 0, 0, 0)); fuente = ImageFont.truetype(os.path.join(B, "Fuentes/PixelifySans.ttf"), 28)
m = Image.new("L", tam, 0); d = ImageDraw.Draw(m); d.fontmode = "1"
w = d.textlength("Te desmayaste", font=fuente); d.text(((tam[0] - w) / 2, (tam[1] - 34) / 2), "Te desmayaste", fill=255, font=fuente)
mp, tp = m.load(), t.load()
for y in range(tam[1]):
    for x in range(tam[0]):
        if mp[x, y]:
            alto = y / tam[1]
            tp[x, y] = hx("#fff4d2" if alto < .5 else "#f0c98a") + (255,)
borde = []
for y in range(tam[1]):
    for x in range(tam[0]):
        if not mp[x, y] and any(0 <= x + a < tam[0] and 0 <= y + b < tam[1] and mp[x + a, y + b] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (0, 2))):
            borde.append((x, y))
for x, y in borde: tp[x, y] = hx("#2a1d2b") + (255,)
t.save(os.path.join(O, "TituloDesmayo.png"))
# Halo suave del farol
h = Image.new("RGBA", (64, 64), (0, 0, 0, 0)); hp = h.load()
for y in range(64):
    for x in range(64):
        d = ((x - 31.5) ** 2 + (y - 31.5) ** 2) ** .5 / 32
        if d < 1: hp[x, y] = (255, 222, 140, int(110 * (1 - d) ** 1.5))
h.save(os.path.join(O, "Halo.png"))
print("ok")
