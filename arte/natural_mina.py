"""Mina de PapaYork: tres zonas, entrada, escaleras y enemigos propios. Dibujo original por código.
Atlas: 20 columnas por zona. 0-15 techo según vecinos, 16 pared frontal, 17-19 suelo. Uso: python3 arte/natural_mina.py"""
import math, os, random
from PIL import Image, ImageDraw
A = os.path.dirname(os.path.abspath(__file__)); N = os.path.join(A, "..", "Natural/Mina"); os.makedirs(N, exist_ok=True)
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
K = H("#1c1420")
ZONAS = [  # techo, sombra techo, luz; pared 3 tonos; suelo 3 tonos; detalle
 dict(t=("#3a2c2a", "#2a1f22", "#54403a"), p=("#5e4638", "#7a5c48", "#94745a"), s=("#6b5444", "#7a6250", "#88705c"), d="#b8925e"),
 dict(t=("#26364a", "#1a2636", "#3c5470"), p=("#3f5c78", "#567a98", "#7fa4bc"), s=("#4a6072", "#566e80", "#647c8e"), d="#a8e4f0"),
 dict(t=("#1f2e22", "#141f18", "#3a5238"), p=("#34503a", "#47704a", "#64944f"), s=("#3c4a38", "#475844", "#546650"), d="#c9f06a"),
]
def tile_techo(d, ox, oy, z, m, r):
    t = [H(c) for c in z["t"]]
    d.rectangle((ox, oy, ox + 31, oy + 31), fill=t[0])
    for _ in range(9):
        x, y = ox + r.randint(1, 28), oy + r.randint(1, 28); d.line((x, y, x + r.randint(1, 3), y), fill=t[1])
    for _ in range(4):
        x, y = ox + r.randint(1, 28), oy + r.randint(1, 28); d.point((x, y), fill=t[2])
    n, e, s, o = m & 1, m & 2, m & 4, m & 8
    if not n: d.rectangle((ox, oy, ox + 31, oy + 2), fill=t[2])
    if not o: d.rectangle((ox, oy, ox + 2, oy + 31), fill=t[2])
    if not e: d.rectangle((ox + 29, oy, ox + 31, oy + 31), fill=t[1])
def tile_pared(d, ox, oy, z, r):
    p = [H(c) for c in z["p"]]
    d.rectangle((ox, oy, ox + 31, oy + 31), fill=p[1])
    for f, j in enumerate(range(oy + 2, oy + 30, 8)):
        i = ox - (f % 2) * 7
        while i < ox + 32:
            a = r.randint(10, 15)
            d.rectangle((max(ox, i), j, min(ox + 31, i + a - 2), j + 6), fill=p[r.choice((1, 1, 2))]); d.line((max(ox, i), j + 6, min(ox + 31, i + a - 2), j + 6), fill=p[0]); i += a
    d.rectangle((ox, oy, ox + 31, oy + 2), fill=p[0]); d.rectangle((ox, oy + 29, ox + 31, oy + 31), fill=p[0])
    for _ in range(2):
        x, y = ox + r.randint(3, 27), oy + r.randint(5, 25); d.point((x, y), fill=H(z["d"])); d.point((x + 1, y + 1), fill=H(z["d"]))
def tile_suelo(d, ox, oy, z, r, v):
    s = [H(c) for c in z["s"]]
    d.rectangle((ox, oy, ox + 31, oy + 31), fill=s[1])
    for _ in range(14 + v * 8):
        x, y = ox + r.randint(0, 29), oy + r.randint(0, 30); c = s[r.choice((0, 2))]; d.line((x, y, x + r.randint(1, 2), y), fill=c)
    if v == 1:
        for _ in range(3):
            x, y = ox + r.randint(3, 26), oy + r.randint(3, 26); d.rectangle((x, y, x + 2, y + 1), fill=s[2]); d.line((x, y + 2, x + 2, y + 2), fill=s[0])
    if v == 2:
        x, y = ox + 6, oy + 8
        for k in range(14): x += r.choice((0, 1, 1)); y += r.choice((0, 1)); d.point((x, y), fill=s[0])
        d.point((ox + 22, oy + 22), fill=H(z["d"]))
im = Image.new("RGBA", (20 * 32, 3 * 32)); d = ImageDraw.Draw(im)
for f, z in enumerate(ZONAS):
    r = random.Random(40 + f)
    for m in range(16): tile_techo(d, m * 32, f * 32, z, m, r)
    tile_pared(d, 16 * 32, f * 32, z, r)
    for v in range(3): tile_suelo(d, (17 + v) * 32, f * 32, z, r, v)
im.save(os.path.join(N, "Atlas.png"))

def lz(w, h): i = Image.new("RGBA", (w, h), (0, 0, 0, 0)); return i, ImageDraw.Draw(i), i.load()
def contorno(im, c=K):
    p = im.load(); W, Hh = im.size; m = []
    for y in range(Hh):
        for x in range(W):
            if p[x, y][3] == 0 and any(0 <= x + a < W and 0 <= y + b < Hh and p[x + a, y + b][3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): m.append((x, y))
    for x, y in m: p[x, y] = c
def guardar(im, n): contorno(im); im.save(os.path.join(N, n + ".png"))
# Entrada: boca de mina con vigas, vagoneta y farol
im, d, p = lz(110, 84)
d.polygon([(0, 84), (10, 30), (30, 6), (80, 4), (100, 30), (110, 84)], fill=H("#74747a"))
d.polygon([(0, 84), (10, 30), (30, 6), (55, 5), (55, 84)], fill=H("#96958f"))
r = random.Random(3)
for _ in range(40):
    x, y = r.randint(8, 100), r.randint(10, 80); d.line((x, y, x + r.randint(3, 8), y + r.randint(0, 2)), fill=H("#55555e"))
d.rectangle((30, 28, 80, 84), fill=H("#140e16"))
for a, b in ((26, 24), (80, 24)): d.rectangle((a, b, a + 5, 84), fill=H("#7a5a45")); d.line((a, b, a, 84), fill=H("#b89a72")); d.line((a + 5, b, a + 5, 84), fill=H("#3f2d2c"))
d.rectangle((22, 20, 88, 27), fill=H("#987857")); d.line((22, 20, 88, 20), fill=H("#b89a72")); d.line((22, 27, 88, 27), fill=H("#3f2d2c"))
d.rectangle((38, 8, 72, 18), fill=H("#7a5a45")); d.text((42, 7), "MINA", fill=H("#f4d36a"))
for y in range(44, 84, 8): d.line((36, y, 74, y), fill=H("#5b4136"))
d.line((44, 34, 40, 84), fill=H("#8d97a0")); d.line((66, 34, 70, 84), fill=H("#8d97a0"))
d.rectangle((96, 44, 102, 54), fill=H("#ffd777")); d.line((95, 43, 103, 43), fill=K)
guardar(im, "Entrada")
# Escaleras
for n, abajo in (("Bajar", True), ("Subir", False)):
    im, d, p = lz(30, 32)
    if abajo:
        d.ellipse((1, 4, 28, 30), fill=H("#140e16")); d.ellipse((1, 4, 28, 30), outline=H("#54403a"))
    for x in (9, 20): d.line((x, 2 if not abajo else 7, x, 30 if not abajo else 28), fill=H("#987857"), width=2)
    for y in range(5 if not abajo else 10, 29, 5): d.line((9, y, 21, y), fill=H("#b89a72"))
    if not abajo:
        d.rectangle((6, 0, 24, 2), fill=H("#3f2d2c"))
    guardar(im, "Escalera" + n)
# Enemigos, mirando a la izquierda
PAP = ("#e0b98a", "#c49565", "#99704e", "#6e4d3e")
GLOW = ("#e7ff9c", "#a8ec4a", "#5aa83c")
def ojos(d, x, y, sep=7, c="#fff8d0"):
    for a in (x, x + sep): d.rectangle((a, y, a + 2, y + 2), fill=H(c)); d.point((a, y + 1), fill=H("#1a1320")); d.point((a + 1, y + 1), fill=H("#1a1320"))
def cuerpo(d, cx, cy, rx, ry, cols):
    d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=H(cols[1]))
    d.chord((cx - rx, cy - ry, cx + rx, cy + ry), 130, 300, fill=H(cols[0]))
    d.chord((cx - rx, cy - ry, cx + rx, cy + ry), -50, 100, fill=H(cols[2]))
def brotecito(f):
    im, d, p = lz(26, 26); b = (0, -2, -3, -1)[f]
    cuerpo(d, 13, 18 + b, 8, 6 - (f == 0), PAP)
    d.line((13, 12 + b, 13, 6 + b), fill=H("#3a6e45"), width=2)
    for s in (-1, 1): d.polygon([(13, 7 + b), (13 + s * 7, 2 + b + (f % 2)), (13 + s * 5, 8 + b)], fill=H("#6ea552"))
    ojos(d, 7, 16 + b, 6); d.line((8, 21 + b, 12, 21 + b), fill=H("#3f2d2c"))
    if b == 0:
        for x in (8, 16): d.line((x, 23, x + 2, 23), fill=H("#6e4d3e"))
    return im
def murcipapa(f):
    im, d, p = lz(38, 26); al = (-7, -2, 4, -2)[f]
    for s in (-1, 1):
        d.polygon([(19 + s * 5, 12), (19 + s * 18, 11 + al), (19 + s * 13, 15 + al // 2), (19 + s * 9, 13 + al // 2), (19 + s * 6, 18)], fill=H("#54405c"))
        d.line((19 + s * 5, 12, 19 + s * 18, 11 + al), fill=H("#8a6a94"))
    cuerpo(d, 19, 14, 7, 7, ("#c49565", "#99704e", "#6e4d3e", ""))
    for x in (14, 24): d.polygon([(x, 8), (x + 2, 2), (x + 4, 8)], fill=H("#6e4d3e"))
    ojos(d, 14, 12, 7, "#e7ff9c"); d.point((16, 18), fill=H("#fff8d0")); d.point((21, 18), fill=H("#fff8d0"))
    return im
def topapa(f):
    im, d, p = lz(32, 26)
    cuerpo(d, 18, 15, 11, 8, ("#8a6a54", "#6e5040", "#4a362c", ""))
    d.ellipse((2, 11, 14, 21), fill=H("#c49565")); d.ellipse((1, 13, 6, 18), fill=H("#e88fa8"))
    ojos(d, 7, 12, 4); 
    s = f % 2 * 2
    for x, y in ((12, 22 - s), (24, 22 + s - 2)):
        d.ellipse((x - 3, y - 2, x + 3, y + 2), fill=H("#4a362c"))
        for k in (-2, 0, 2): d.point((x + k, y + 3), fill=H("#efe2c4"))
    for x in range(20, 28, 3): d.line((x, 8, x + 1, 5), fill=H("#3a2820"))
    return im
def escarabajo(f):
    im, d, p = lz(34, 24); s = f % 2
    for i, x in enumerate((9, 16, 24)):
        y = 18 if (i + s) % 2 else 20
        d.line((x, 16, x - 3, y + 2), fill=H("#1f2e22"), width=2)
    d.ellipse((8, 5, 30, 19), fill=H("#2c5540")); d.chord((8, 5, 30, 19), 170, 320, fill=H("#4f8a49")); d.line((19, 5, 21, 18), fill=H("#1f2e22"))
    d.ellipse((1, 8, 12, 18), fill=H("#1f2e22")); ojos(d, 3, 11, 4, "#e7ff9c")
    d.line((3, 9, 0, 3), fill=H("#1f2e22")); d.line((7, 8, 6, 2), fill=H("#1f2e22"))
    for x, y in ((14, 9), (23, 8), (18, 13), (26, 13)): d.point((x, y), fill=H(GLOW[0] if (f + x) % 2 else GLOW[1]))
    return im
def golem(f):
    im, d, p = lz(52, 54); ST = ("#b6b2a4", "#96958f", "#74747a", "#55555e"); b = (0, -1, 0, 1)[f]; s = f % 2 * 2
    for x, y in ((15, 44 - s), (34, 44 - 2 + s)): d.rectangle((x, y, x + 10, 52), fill=H(ST[2])); d.line((x, y, x + 10, y), fill=H(ST[1]))
    d.polygon([(8, 24 + b), (14, 12 + b), (40, 10 + b), (46, 24 + b), (42, 44 + b), (12, 44 + b)], fill=H(ST[1]))
    d.polygon([(8, 24 + b), (14, 12 + b), (28, 11 + b), (24, 30 + b), (12, 44 + b)], fill=H(ST[0]))
    d.polygon([(40, 10 + b), (46, 24 + b), (42, 44 + b), (32, 40 + b)], fill=H(ST[2]))
    for x, y, a in ((1, 22 + s, 10), (43, 24 - s, 9)): d.rectangle((x, y + b, x + a - 2, y + 16 + b), fill=H(ST[2])); d.line((x, y + b, x + a - 2, y + b), fill=H(ST[1]))
    d.ellipse((14, 2 + b, 36, 20 + b), fill=H(PAP[1])); d.chord((14, 2 + b, 36, 20 + b), 150, 300, fill=H(PAP[0]))
    ojos(d, 17, 9 + b, 9, "#e7ff9c"); d.line((20, 16 + b, 29, 16 + b), fill=H("#3f2d2c"))
    for a, c in ((24, 28), (30, 34), (20, 36)): d.line((a, c + b, a + 4, c + 3 + b), fill=H(GLOW[1]))
    return im
def espora(f):
    im, d, p = lz(30, 30); rad = (9, 10, 11, 10)[f]; cy = 14 + (0, -1, 0, 1)[f]
    for k in range(10):
        a = k * math.pi / 5 + f * .2; x, y = 15 + math.cos(a) * (rad + 2), cy + math.sin(a) * (rad + 2); d.point((int(x), int(y)), fill=H(GLOW[1]))
    d.ellipse((15 - rad, cy - rad, 15 + rad, cy + rad), fill=H("#7a5a8c")); d.chord((15 - rad, cy - rad, 15 + rad, cy + rad), 150, 320, fill=H("#9a7aac"))
    d.ellipse((10, cy - 5, 20, cy + 5), fill=H(GLOW[2])); d.ellipse((12, cy - 3, 18, cy + 3), fill=H(GLOW[f % 2]))
    ojos(d, 9, cy - 2, 8, "#fff8d0")
    return im
for n, fn in (("Brotecito", brotecito), ("Murcipapa", murcipapa), ("Topapa", topapa), ("Escarabajo", escarabajo), ("Golem", golem), ("Espora", espora)):
    for f in range(4): guardar(fn(f), f"{n}{f + 1}")
print("ok")
