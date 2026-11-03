"""Fondos pintados de la introducción y del desmayo. Dibujo propio hecho por código, por capas para dar profundidad.
Cielo, Montes, Valle y Frente se mueven a distinta velocidad. Salida: Natural/IntroN/. Uso: python3 arte/natural_intro.py"""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFont
A = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(A, ".."); N = os.path.join(B, "Natural"); OUT = os.path.join(N, "IntroN")
os.makedirs(OUT, exist_ok=True)
W, H = 540, 270
BAYER = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) / 16
hx = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5))
def cargar(r): return Image.open(os.path.join(N, r)).convert("RGBA")
def vacio(w=W, h=H): return Image.new("RGBA", (w, h), (0, 0, 0, 0))

def degradado(cols, w=W, h=H, bandas=14):
    """Cielo por bandas con transición punteada."""
    cols = [np.array(hx(c), float) for c in cols]
    a = np.zeros((h, w, 4), np.uint8); a[..., 3] = 255
    for y in range(h):
        t = y / (h - 1) * (len(cols) - 1); i = min(int(t), len(cols) - 2); f = t - i
        for x in range(w):
            g = f * bandas; g0 = math.floor(g) + (1 if (g - math.floor(g)) > BAYER[y % 4, x % 4] else 0)
            c = cols[i] + (cols[i + 1] - cols[i]) * (g0 / bandas)
            a[y, x, :3] = c
    return Image.fromarray(a, "RGBA").copy()

def nubes(im, sem, n, luz, medio, sombra, y0=8, y1=70):
    r = random.Random(sem); px = im.load()
    for _ in range(n):
        cx, cy, ancho = r.randrange(-20, W), r.randint(y0, y1), r.randint(26, 70)
        bolas = [(cx + r.randint(-ancho // 2, ancho // 2), cy + r.randint(-3, 2), r.randint(4, max(5, ancho // 5))) for _ in range(ancho // 4)]
        for bx, by, br in bolas:
            for y in range(by - br, by + br):
                if y > cy + 4: continue
                for x in range(bx - br, bx + br + 1):
                    if 0 <= x < W and 0 <= y < H and (x - bx) ** 2 + (y - by) ** 2 <= br * br:
                        d = (y - by) / br
                        c = luz if d < -.25 else medio if d < .35 else sombra
                        if (x - bx) / br > .6: c = medio if c == luz else sombra
                        px[x, y] = hx(c) + (255,)

def cresta(x, sem, escala=1.0):
    r = random.Random(sem); fs = [(r.uniform(.006, .012), r.uniform(0, 6), 1), (r.uniform(.02, .03), r.uniform(0, 6), .45), (r.uniform(.05, .08), r.uniform(0, 6), .18), (r.uniform(.13, .2), r.uniform(0, 6), .06)]
    return sum(a * math.sin(f * x + p) for f, p, a in fs) * escala

def montes(im, base, alto, sem, luz, som, nieve=None, pico=.72):
    """Picos con cara iluminada a la izquierda y en sombra a la derecha; la nieve baja en dientes irregulares."""
    px = im.load(); r = random.Random(sem)
    picos = []; x = -40
    while x < W + 60:
        picos.append((x, alto * r.uniform(.55, 1.0), r.uniform(46, 84))); x += r.randint(58, 104)
    for x in range(W):
        mejor, cual = -1e9, None
        for p in picos:
            h = p[1] * (1 - abs(x - p[0]) / p[2])
            if h > mejor: mejor, cual = h, p
        if mejor < 2: mejor = 2
        h = mejor + 1.6 * math.sin(x * .31 + sem) + .9 * math.sin(x * .73)
        top = int(base - h)
        for y in range(top, base + 1):
            if not (0 <= y < H): continue
            ruido = 2.5 * math.sin(y * .5 + cual[0]) + 1.5 * math.sin(y * 1.3 + x * .1)
            c = luz if x < cual[0] + ruido else som
            if nieve and cual[1] > alto * .62:
                bajada = cual[1] * .3 + 3 * math.sin(x * .9 + sem) + 2 * math.sin(x * .37)
                if y - (base - cual[1]) < bajada and y - top < bajada:
                    c = nieve if x < cual[0] + ruido else som_nieve(nieve, som)
            px[x, y] = hx(c) + (255,)

def som_nieve(n, s):
    a, b = hx(n), hx(s)
    return "#%02x%02x%02x" % tuple((p * 3 + q) // 4 for p, q in zip(a, b))

def colina(im, y0, amp, sem, tile, tono=None, arb=0, arb_c=("#355a3f", "#2a4a38")):
    px = im.load(); t = tile.load(); r = random.Random(sem)
    for x in range(W):
        top = int(y0 + amp * cresta(x, sem, .9))
        for y in range(top, H):
            c = t[x % tile.width, y % tile.height]
            px[x, y] = c
        px[x, top] = tuple(min(255, v + 18) for v in t[x % tile.width, top % tile.height][:3]) + (255,)
    for _ in range(arb):    # arboledas lejanas
        x, rad = r.randrange(W), r.randint(4, 9); top = int(y0 + amp * cresta(x, sem, .9))
        for yy in range(top - rad * 2, top + 2):
            for xx in range(x - rad - 2, x + rad + 3):
                if 0 <= xx < W and 0 <= yy < H and ((xx - x) / (rad + 2)) ** 2 + ((yy - (top - rad)) / (rad + 1)) ** 2 < 1:
                    px[xx, yy] = hx(arb_c[0] if xx - x + yy - (top - rad) < 1 else arb_c[1]) + (255,)

def pegar(im, spr, x, y, flip=False, esc=1):
    s = spr
    if esc != 1: s = s.resize((int(s.width * esc), int(s.height * esc)), Image.NEAREST)
    if flip: s = s.transpose(Image.FLIP_LEFT_RIGHT)
    im.alpha_composite(s, (int(x), int(y))) if x >= 0 and y >= 0 else im.paste(s, (int(x), int(y)), s)

def camino_horizontal(im, y0, y1):
    px = im.load(); r = random.Random(5)
    bor = [(int(1.6 * math.sin(i * .17)), int(1.6 * math.sin(i * .11 + 2))) for i in range(W)]
    for x in range(W):
        for y in range(y0 + bor[x][0], y1 + bor[x][1]):
            c = "#bd9666" if (x * 5 + y * 9) % 23 else "#ab8358"
            if y <= y0 + bor[x][0] + 1: c = "#7d5a41"
            elif y >= y1 + bor[x][1] - 1: c = "#cfab7b"
            px[x, y] = hx(c) + (255,)
    for _ in range(90):
        x, y = r.randrange(W - 2), r.randint(y0 + 3, y1 - 3)
        px[x, y] = hx("#cfab7b"); px[x + 1, y + 1] = hx("#7d5a41")

def mata(px, x, y, r, tono):
    """Mata de papa pequeña: hojas agrupadas con luz arriba a la izquierda."""
    H_ = {"papas": ("#2c5540", "#3a6e45", "#4f8a49", "#6ea552", "#93bf60"), "brotes": ("#2c5540", "#3a6e45", "#4f8a49", "#6ea552", "#93bf60")}[tono]
    tam = 5 if tono == "papas" else 3
    for _ in range(9 if tono == "papas" else 5):
        hx_, hy_ = x + r.randint(-tam, tam), y + r.randint(-tam, 1)
        luz = -(hx_ - x) * .4 - (hy_ - y) * .7
        k = max(1, min(4, int(2.3 + luz + r.uniform(-.5, .5))))
        for a_, b_, c_ in ((0, 0, k), (1, 0, k), (0, 1, max(0, k - 1)), (1, 1, max(0, k - 2)), (-1, 0, k)):
            if 0 <= hx_ + a_ < W and 0 <= hy_ + b_ < H: px[hx_ + a_, hy_ + b_] = hx(H_[c_]) + (255,)

def surcos(im, x0, x1, y0, y1, planta, sem=3, dy=11, salto=13):
    r = random.Random(sem); px = im.load()
    for fy in range(y0, y1, dy):
        for x in range(x0, x1):
            for y in range(fy, fy + 6):
                c = "#6b4c3c" if y < fy + 2 else "#7a5a45" if y < fy + 4 else "#574036"
                if (x * 3 + y) % 13 == 0: c = "#8c6c50"
                px[x, y] = hx(c) + (255,)
        if planta:
            for x in range(x0 + 5 + (fy % 2) * 6, x1 - 4, salto):
                mata(px, x + r.randint(-1, 1), fy + 1, r, planta)

def cerca(im, x0, x1, y):
    px = im.load()
    for x in range(x0, x1):
        for dy in (6, 11):
            px[x, y + dy] = hx("#987857"); px[x, y + dy + 1] = hx("#5b4136")
    for x in range(x0, x1, 15):
        for yy in range(y + 2, y + 18):
            px[x, yy] = hx("#b89a72"); px[x + 1, yy] = hx("#7a5a45"); px[x + 2, yy] = hx("#3f2d2c")

def grada(im, mul, suma=(0, 0, 0), satura=1.0):
    a = np.array(im, float); rgb = a[..., :3]
    g = rgb.mean(axis=2, keepdims=True); rgb = g + (rgb - g) * satura
    rgb = rgb * np.array(mul) + np.array(suma)
    a[..., :3] = np.clip(rgb, 0, 255)
    return Image.fromarray(a.astype(np.uint8), "RGBA").copy()

def ventanas(im, casa_x, casa_y, color="#ffd777"):
    px = im.load()
    for x0, y0, w, h in ((78, 65, 18, 12), (18, 69, 10, 10)):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                X, Y = casa_x + x, casa_y + y
                if px[X, Y][3]: px[X, Y] = hx(color) + (255,)

def letrero(im, x, y, texto):
    fuente = ImageFont.truetype(os.path.join(B, "Fuentes/PixelifySans.ttf"), 10); d = ImageDraw.Draw(im); d.fontmode = "1"
    w = int(d.textlength(texto, font=fuente)) + 10
    d.rectangle((x + w // 2 - 2, y + 12, x + w // 2 + 1, y + 28), fill=hx("#6e4f44"))
    d.rectangle((x, y, x + w, y + 14), fill=hx("#987857"), outline=hx("#3f2d2c")); d.line((x + 1, y + 1, x + w - 1, y + 1), fill=hx("#b89a72"))
    d.text((x + 5, y + 1), texto, fill=hx("#3f2d2c"), font=fuente)

def reactor(im, x, base):
    px = im.load()
    def torre(cx, h, ancho):
        for y in range(base - h, base):
            t = (y - (base - h)) / h; w = ancho * (.72 + .28 * abs(t - .62) * 2.2)
            for xx in range(int(cx - w), int(cx + w)):
                f = (xx - (cx - w)) / (2 * w)
                c = "#c3c0b4" if f < .25 else "#9d9a92" if f < .6 else "#716f70"
                if (y % 7 == 0) and f < .9: c = "#85837e"
                px[xx, y] = hx(c) + (255,)
    torre(x, 54, 15); torre(x + 38, 46, 13)
    for y in range(base - 22, base):
        for xx in range(x + 58, x + 92):
            px[xx, y] = hx("#8a8780") if xx < x + 66 else hx("#6d6b6c")
    for xx in range(x + 58, x + 92):
        px[xx, base - 23] = hx("#b9b6aa")
    for yy in range(base - 40, base - 22):
        for xx in range(x + 74, x + 79): px[xx, yy] = hx("#6d6b6c") if xx > x + 76 else hx("#8a8780")
    for xx, yy in ((x + 66, base - 12), (x + 76, base - 12), (x + 84, base - 12)):
        for a in range(3):
            for b in range(3): px[xx + a, yy + b] = hx("#ffdf8a")

CASA = lambda: cargar("Objetos/Casa.png"); GRANERO = lambda: cargar("Objetos/Granero.png")
ARB = lambda n: cargar(f"Plantas/Arbol{n}.png")
PAPA2, PAPA3 = (lambda: cargar("Cultivos/Papa_2.png")), (lambda: cargar("Cultivos/Papa_3.png"))
TILE = lambda: cargar("Terreno/Pasto.png")

def primer_plano(sem, flores=True):
    im = vacio(); px = im.load(); r = random.Random(sem); t = TILE().load()
    for x in range(W):
        top = 250 + int(5 * cresta(x, sem))
        for y in range(top, H):
            c = t[x % 256, y % 256]; px[x, y] = tuple(int(v * .78) for v in c[:3]) + (255,)
    for k in range(240):
        x = r.randrange(W); top = 250 + int(5 * cresta(x, sem)); alto = r.randint(4, 12)
        inc = r.choice((-1, 0, 1))
        for j in range(alto):
            X, Y = x + inc * (j // 4), top + 2 - j
            if 0 <= X < W and 0 <= Y < H:
                px[X, Y] = hx("#2c5540") if j < alto // 2 else hx("#3a6e45") if j < alto - 1 else hx("#6ea552")
    if flores:
        for _ in range(16):
            x, y = r.randrange(4, W - 4), r.randint(250, 262); c = r.choice(("#e88fa8", "#f0d268", "#c8b4e6", "#fff4d2"))
            for a, b in ((-1, 0), (1, 0), (0, -1), (0, 1)): px[x + a, y + b] = hx(c)
            px[x, y] = hx("#e9b84c")
            for j in range(1, 6): px[x, y + j] = hx("#2c5540")
    return im

def base_valle(casa=True, campo="papas", granero=False, estado="nueva", letr=None, arboles=True, flores_cam=True):
    im = vacio(); colina(im, 140, 8, 21, TILE()); t = im.load()
    if arboles:
        for n, x, y in ((1, -12, 78), (2, 34, 84), (2, 416, 82), (1, 470, 74), (3, 372, 90)):
            pegar(im, ARB(n), x, y)
    if casa:
        c = CASA()
        if estado == "ruina":
            c = cargar_ruina()
        pegar(im, c, 96, 72)
    if granero:
        pegar(im, GRANERO(), 262, 58)
    cerca(im, 0, 96, 152); cerca(im, 232 if not granero else 396, 372 if not granero else 540, 152)
    if campo:
        surcos(im, 0, W, 200, 244, campo, 3)
    camino_horizontal(im, 175, 195)
    if letr: letrero(im, 26, 148, letr)
    return im

def cargar_ruina():
    """Casa abandonada: el mismo edificio, gastado, con el techo roto y hiedra."""
    c = np.array(grada(CASA(), (.72, .68, .62), (6, 6, 4), .55)).copy(); r = random.Random(4)
    for x0, y0, w, h in ((58, 14, 26, 18), (28, 26, 16, 10), (84, 30, 12, 8)):
        for y in range(y0, y0 + h):
            for x in range(x0, x0 + w):
                if (x - x0 - w / 2) ** 2 / (w / 2) ** 2 + (y - y0 - h / 2) ** 2 / (h / 2) ** 2 < 1:
                    c[y, x] = (*hx("#2a1f24"), 255)
    for _ in range(170):   # hiedra
        x, y = r.randrange(4, 110), r.randrange(34, 100)
        if c[y, x, 3]: c[y, x] = (*hx(r.choice(("#3a6e45", "#4f8a49", "#6ea552"))), 255)
    for x0, y0 in ((74, 70), (18, 68)):
        for y in range(y0, y0 + 12):
            for x in range(x0, x0 + 18 if x0 == 74 else x0 + 12):
                c[y, x] = (*hx("#241b22"), 255)
    return Image.fromarray(c, "RGBA").copy()

def maleza(im, sem=9, n=420):
    r = random.Random(sem); px = im.load()
    for _ in range(n):
        x, y = r.randrange(W), r.randint(148, 236); alto = r.randint(3, 11)
        for j in range(alto):
            Y = y - j
            if 0 <= Y < H and px[x, y][3]:
                px[x, Y] = hx(r.choice(("#3a6e45", "#4f8a49", "#6ea552", "#a3bd62")))

def escena(nombre, cielo, montes_cfg, nube_cols, nube_n, valle, gr, frente=True, gr_frente=None, extra_montes=None):
    c = degradado(cielo); nubes(c, 11, nube_n, *nube_cols); c.convert("RGB").save(os.path.join(OUT, nombre + "_Cielo.png"))
    m = vacio()
    montes(m, 128, 66, 31, *montes_cfg[0], nieve=montes_cfg[1]); montes(m, 136, 42, 41, *montes_cfg[2])
    colina(m, 128, 9, 13, grada(TILE(), *montes_cfg[3]), arb=28, arb_c=montes_cfg[4])
    if extra_montes: extra_montes(m)
    m.save(os.path.join(OUT, nombre + "_Montes.png"))
    grada(valle, *gr).save(os.path.join(OUT, nombre + "_Valle.png"))
    f = primer_plano(77)
    grada(f, *(gr_frente or gr)).save(os.path.join(OUT, nombre + "_Frente.png")) if frente else None

MDIA = (("#7f94b8", "#5f7196"), "#f2f4f6", ("#6f8f8a", "#587a78"), ((.82, .9, .86), (4, 8, 12), .9), ("#4f7a5a", "#3f6a50"))
NUBE_DIA = ("#ffffff", "#e8eff5", "#c5d3e4")
NUBE_ORO = ("#fff0cf", "#f6c98f", "#d1906f")
NUBE_NOCHE = ("#3a4166", "#2c3254", "#212744")
SOL = (1.03, .98, .88)
# 1847: la tierra dorada
escena("Valle", ["#5fa9dc", "#8cc6e6", "#c2e2ec", "#f6e9c4"], MDIA, NUBE_DIA, 7,
       base_valle(granero=False, letr="PAPAYORK"), (SOL, (8, 6, 0), 1.08))
# La familia, atardecer de cosecha
escena("Cosecha", ["#4f6fa8", "#c87f8e", "#f2a765", "#ffd98f"], (("#a0719b", "#6f5a8c"), "#ffd9b0", ("#8a6a88", "#6d5a7d"), ((.9, .72, .6), (10, 0, 0), .85), ("#6a5a4a", "#524a44")), NUBE_ORO, 6,
       base_valle(), ((1.06, .84, .66), (14, 4, 0), 1.0))
# El otro lado del valle: el reactor
def con_reactor(m): reactor(m, 300, 128)
MGRIS = (("#7c8498", "#5e6580"), "#c9ccd2", ("#68747a", "#515d68"), ((.72, .76, .72), (2, 4, 8), .55), ("#46604e", "#384e44"))
escena("Reactor", ["#6d7f96", "#a4a89e", "#d0bc90", "#e8c98c"], MGRIS, ("#d8d4c8", "#b4b0a6", "#8a8780"), 6,
       base_valle(casa=False, campo="brotes", arboles=True), ((.9, .84, .72), (6, 4, 0), .75), extra_montes=con_reactor)
# Sigue igual pero con el cielo verde
MVERDE = (("#50704a", "#38503c"), "#a8d078", ("#3f6240", "#2c4a34"), ((.5, .72, .4), (0, 8, 0), .5), ("#2c4a30", "#223c28"))
escena("Verde", ["#1c3322", "#3f7a38", "#a8d850", "#f0ff9c"], MVERDE, ("#d8f090", "#90c050", "#507a38"), 8,
       base_valle(casa=False, campo="brotes"), ((.56, .78, .42), (0, 8, 0), .5), extra_montes=con_reactor)
# Huida por el camino
escena("Huida", ["#16261f", "#2f5a34", "#7aa83f", "#c6d866"], MVERDE, ("#a8c870", "#6f9a4a", "#3f6a38"), 8,
       base_valle(casa=True, campo=None), ((.42, .6, .34), (0, 6, 0), .45))
# Generaciones después: la casa abandonada, mañana con neblina
v = base_valle(estado="ruina", campo=None); maleza(v)
escena("Ruina", ["#8ea8ba", "#b7c8cc", "#dcdcc8", "#f0e7c8"], (("#9aa4b4", "#808ca0"), "#e4e8ea", ("#8e9c9c", "#7a8a8c"), ((.78, .82, .78), (20, 20, 20), .6), ("#7a9080", "#6a8272")), ("#f0f0ea", "#d8dcd8", "#b8c0c0"), 4,
       v, ((.88, .92, .84), (10, 12, 10), .78))
# Cuatro estaciones de la granja recuperada
for nom, cie, cfg, gr_v, camp in (
    ("Primavera", ["#6cb4e0", "#a2d4ea", "#d8ecec", "#fdf2d6"], MDIA, (SOL, (8, 8, 2), 1.1), "brotes"),
    ("Verano", ["#3f9edc", "#70bce8", "#b2dcec", "#f6efc0"], MDIA, ((1.05, 1.0, .82), (10, 8, 0), 1.14), "papas"),
    ("Otono", ["#7f9fc0", "#cdb38c", "#efc282", "#fbe0a4"], (("#a07f7c", "#7f6a78"), "#f6e8d0", ("#8f8068", "#786c5c"), ((1.05, .78, .5), (10, 4, 0), .9), ("#a8682f", "#8a4f2c")), ((1.12, .86, .55), (12, 6, 0), .92), "papas")):
    escena(nom, cie, cfg, NUBE_DIA, 5, base_valle(granero=True, campo=camp), gr_v)
def nevar(im):
    a = np.array(im).astype(float); r_, g_, b_, al = a[..., 0], a[..., 1], a[..., 2], a[..., 3]
    verde = (g_ > r_ * 1.02) & (g_ > b_) & (al > 0)
    lum = (r_ * .3 + g_ * .59 + b_ * .11) / 255
    nieve = np.stack([200 + lum * 70, 212 + lum * 60, 226 + lum * 40], axis=-1)
    a[..., :3][verde] = np.clip(nieve[verde], 0, 255)
    h_, w_ = a.shape[:2]
    for x in range(w_):        # nieve sobre lo que tenga cielo encima
        vis = np.nonzero(al[:, x] > 0)[0]
        if len(vis):
            for y in vis[:1]:
                a[y:y + 3, x, :3] = (240, 244, 250)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), "RGBA").copy()

v_inv = base_valle(granero=True, campo=None)
casa_y = 72
pv = v_inv.load()
for yy in range(72, 124):       # tejados nevados
    for xx in list(range(96, 216)) + list(range(262, 392)):
        c = pv[xx, yy]
        if c[3] and ((c[0] > c[1] * 1.25 and yy < 118) or (abs(c[0] - c[2]) < 14 and c[0] < 110 and xx > 262 and yy < 100)):
            if (yy + (xx // 9)) % 6 < 4: pv[xx, yy] = (232 + (xx % 3) * 6, 238, 246, 255)
v_inv = nevar(v_inv)
escena("Invierno", ["#7f98b8", "#a8bccc", "#d0dce4", "#eef2f4"], (("#b6c0d0", "#8c98ae"), "#ffffff", ("#aab8c4", "#8896a6"), ((1.2, 1.26, 1.34), (46, 50, 58), .3), ("#8a9ca8", "#74868f")), NUBE_DIA, 5, v_inv, ((.96, .98, 1.04), (0, 0, 4), 1.0))
nf = nevar(primer_plano(77)); grada(nf, (.96, .98, 1.04), (0, 0, 4), 1.0).save(os.path.join(OUT, "Invierno_Frente.png"))

# Atardecer: Chuchini le deja la granja a Pedro
escena("Herencia", ["#3f5288", "#b8688a", "#f09858", "#ffcf7a"], (("#8a5f90", "#5f4f80"), "#ffc8a4", ("#785878", "#5f4e70"), ((.86, .64, .56), (10, 0, 0), .8), ("#5a4a44", "#46403e")), NUBE_ORO, 5,
       base_valle(granero=True, campo="papas"), ((1.04, .78, .6), (12, 2, 0), .98))
# Primera noche con un brillo verde en el surco
def noche(nombre, verde=True):
    v = base_valle(granero=True, campo="brotes")
    v = grada(v, (.26, .32, .55), (6, 8, 22), .55); ventanas(v, 96, 72)
    if verde:
        p = v.load(); r = random.Random(8)
        for _ in range(7):
            cx, cy = r.randrange(60, 480), r.randrange(202, 238)
            for y in range(cy - 7, cy + 8):
                for x in range(cx - 13, cx + 14):
                    if 0 <= x < W:
                        d = (x - cx) ** 2 / 169 + (y - cy) ** 2 / 49
                        if d < 1:
                            k = 1 - d; c = p[x, y]   # brillo suave que sube desde la tierra
                            p[x, y] = (min(255, int(c[0] + 26 * k)), min(255, int(c[1] + 96 * k)), min(255, int(c[2] + 16 * k)), 255)
    c = degradado(["#0a0f28", "#141b40", "#232d5c", "#3f4778"]); nubes(c, 11, 4, *NUBE_NOCHE); px = c.load(); r = random.Random(12)
    for _ in range(170):
        x, y = r.randrange(W), r.randrange(0, 100); px[x, y] = hx(r.choice(("#ffffff", "#c8d4f0", "#ffeec8")))
    for j in range(-13, 14):       # luna
        for i in range(-13, 14):
            if i * i + j * j < 170:
                px[70 + i, 34 + j] = hx("#eef0d8") if i + j < 2 else hx("#c8ccb4")
                if (i + 4) ** 2 + (j + 3) ** 2 < 10 or (i - 5) ** 2 + (j - 4) ** 2 < 7: px[70 + i, 34 + j] = hx("#aeb29c")
    c.convert("RGB").save(os.path.join(OUT, nombre + "_Cielo.png"))
    m = vacio(); montes(m, 128, 66, 31, "#232a52", "#191f40", nieve="#5a6288"); montes(m, 136, 42, 41, "#1d2645", "#151c38")
    colina(m, 128, 9, 13, grada(TILE(), (.2, .26, .42), (2, 4, 14), .5), arb=28, arb_c=("#141c34", "#101728"))
    m.save(os.path.join(OUT, nombre + "_Montes.png")); v.save(os.path.join(OUT, nombre + "_Valle.png"))
    grada(primer_plano(77), (.2, .26, .44), (2, 4, 14), .5).save(os.path.join(OUT, nombre + "_Frente.png"))
noche("Noche"); noche("Desmayo")
# Objetos sueltos que se animan encima
def humo():
    for f in range(4):
        im = vacio(40, 44); p = im.load(); r = random.Random(30 + f)
        for k in range(9):
            cx, cy, rad = 20 + int(5 * math.sin(k * .7 + f)), 40 - k * 4, 3 + k // 2
            for y in range(cy - rad, cy + rad):
                for x in range(cx - rad, cx + rad):
                    if 0 <= x < 40 and 0 <= y < 44 and (x - cx) ** 2 + (y - cy) ** 2 < rad * rad:
                        p[x, y] = hx("#d8d4c8" if x - cx + y - cy < -1 else "#a4a098") + (235 - k * 16,)
        im.save(os.path.join(OUT, f"Humo{f + 1}.png"))
humo()
def ave():
    for f, alas in enumerate(((-2, -1), (0, 0), (2, 1))):
        im = vacio(11, 7); p = im.load(); y0, y1 = alas
        for a, b in ((-4, y0), (-3, y1 if y1 else 0), (-2, 0), (-1, 0), (0, 1), (1, 0), (2, 0), (3, y1), (4, y0)):
            p[5 + a, 3 + b] = hx("#2f2a3a")
        im.save(os.path.join(OUT, f"Ave{f + 1}.png"))
ave()
def explosion():
    """Hongo radiactivo: cabeza ancha y achatada con centro incandescente, anillo de humo y tallo fino."""
    COL = ("#fbfff0", "#e4f79c", "#a8d850", "#5a8f3c", "#2f5a34")
    for f, rad in enumerate((10, 24, 40, 54)):
        im = vacio(170, 170); p = im.load(); r = random.Random(50 + f)
        cx, cy = 85, 146 - int(rad * 1.7)
        def bola(bx, by, ra, tonos=COL):
            for y in range(int(by - ra), int(by + ra) + 1):
                for x in range(int(bx - ra), int(bx + ra) + 1):
                    if 0 <= x < 170 and 0 <= y < 170 and (x - bx) ** 2 + (y - by) ** 2 <= ra * ra:
                        d = ((y - by) * .8 + (x - bx) * .4) / ra
                        p[x, y] = hx(tonos[1] if d < -.5 else tonos[2] if d < .15 else tonos[3] if d < .65 else tonos[4]) + (255,)
        ancho = 2 + f
        for y in range(cy, 170):               # tallo fino con base de polvo
            w = ancho + max(0, (y - 150) // 2)
            for x in range(cx - w, cx + w + 1):
                if 0 <= x < 170: p[x, y] = hx(COL[1] if x < cx - w // 2 else COL[2] if x < cx + w // 3 else COL[3]) + (255,)
        if f >= 2:                             # polvo levantado en la base
            for k in range(11): bola(cx + (k - 5) * (5 + f), 160 + r.randint(-2, 3), 5 + f, ("", COL[2], COL[3], COL[3], COL[4]))
        if f >= 1:                             # anillo de humo alrededor del tallo
            for k in range(12):
                t_ = k / 12 * 2 * math.pi
                bola(cx + math.cos(t_) * rad * .42, cy + rad * .72 + math.sin(t_) * 3, 2 + f * 1.6, ("", COL[2], COL[3], COL[4], COL[4]))
        puntos = [(cx + rad * .86 * math.cos(a * 2 * math.pi / 11), cy + rad * .3 * math.sin(a * 2 * math.pi / 11), rad * .34) for a in range(11)]
        puntos += [(cx + r.uniform(-.45, .45) * rad, cy - rad * r.uniform(.12, .34), rad * .36) for _ in range(5)]
        puntos.sort(key=lambda b: b[1])
        for b_ in puntos: bola(*b_)
        for y in range(int(cy - rad * .22), int(cy + rad * .22)):      # centro incandescente
            for x in range(int(cx - rad * .36), int(cx + rad * .36)):
                d = ((x - cx) / (rad * .36)) ** 2 + ((y - cy) / (rad * .22)) ** 2
                if d < 1 and 0 <= x < 170 and 0 <= y < 170: p[x, y] = hx(COL[0] if d < .45 else COL[1]) + (255,)
        im.save(os.path.join(OUT, f"Explosion{f + 1}.png"))
explosion()
def carreta():
    for f in range(2):
        im = vacio(84, 54); p = im.load(); d = ImageDraw.Draw(im)
        d.rectangle((14, 20, 64, 38), fill=hx("#7a5a45"), outline=hx("#3f2d2c"))
        for x in range(22, 64, 8): d.line((x, 21, x, 37), fill=hx("#5b4136"))
        d.line((15, 21, 63, 21), fill=hx("#987857"))
        d.pieslice((16, 0, 62, 42), 180, 360, fill=hx("#e8dcc0"), outline=hx("#8a7a60"))
        for x in (26, 38, 50): d.arc((x - 10, 2, x + 10, 42), 200, 340, fill=hx("#c8b89a"))
        for s in (22, 56):
            d.ellipse((s - 9, 32, s + 9, 50), fill=hx("#5b4136"), outline=hx("#2f1f22")); d.ellipse((s - 2, 39, s + 2, 43), fill=hx("#b89a72"))
            a = f * math.pi / 4
            for k in range(4):
                q = a + k * math.pi / 2; d.line((s, 41, s + 8 * math.cos(q), 41 + 8 * math.sin(q)), fill=hx("#2f1f22"))
        d.line((14, 34, 0, 40), fill=hx("#3f2d2c"), width=2)
        im.save(os.path.join(OUT, f"Carreta{f + 1}.png"))
carreta()
def papa_brote():
    for f, h in enumerate((0, 4, 9, 14)):
        im = vacio(28, 26); p = im.load()
        for j in range(-h // 2, h // 2 + 1):
            for i in range(-9, 10):
                if h and (i / 9.5) ** 2 + (j / (h / 2 + .5)) ** 2 < 1: p[14 + i, 22 - h // 2 + j] = hx("#c49565" if i + j < 0 else "#99704e")
        for i in range(-11, 12):
            for dy in (22, 23, 24): p[14 + i, dy] = hx("#574036")
        if h >= 9:
            p[10, 22 - h + 3] = p[11, 22 - h + 3] = hx("#e7ff9c"); p[17, 22 - h + 3] = p[18, 22 - h + 3] = hx("#e7ff9c"); p[11, 22 - h + 4] = p[18, 22 - h + 4] = hx("#1a1320")
        if h >= 4:
            p[14, 22 - h] = hx("#a8ec4a"); p[14, 21 - h] = hx("#7cc644"); p[13, 21 - h] = hx("#a8ec4a")
        im.save(os.path.join(OUT, f"PapaBrota{f + 1}.png"))
papa_brote()
# Menú: mismo valle dorado en un lienzo alto para el paneo
print("ok")
