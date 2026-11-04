"""Menú de PapaYork: papa zombie, halo verde e interfaz con el mismo estilo del inventario. Dibujo propio por código."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import natural_ui as U
A = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(A, ".."); N = os.path.join(B, "Natural/Menu"); os.makedirs(N, exist_ok=True)
H = U.H; FUENTE = os.path.join(B, "Fuentes/PixelifySans.ttf")
LINO, ROBLE, VERDE = U.LINO, U.ROBLE, U.VERDE
TINTA = H("#3f2418")
def texto(d, xc, y, t, tam, c=TINTA):
    f = ImageFont.truetype(FUENTE, tam); d.fontmode = "1"; w = d.textlength(t, font=f); d.text((xc - w / 2, y), t, fill=c, font=f)
def guardar(im, n): im.save(os.path.join(N, n + ".png"))
def brazo(d, x0, y0, x1, y1, c, luz, borde):
    N_ = 40
    for capa in (1, 0):
        for k in range(N_ + 1):
            t = k / N_; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t - math.sin(t * math.pi) * 2.5; r = 4 - 1.6 * t + capa
            d.ellipse((x - r, y - r, x + r, y + r), fill=H(borde if capa else c))
    for k in range(N_):
        t = k / N_; x = x0 + (x1 - x0) * t; y = y0 + (y1 - y0) * t - math.sin(t * math.pi) * 2.5 - (4 - 1.6 * t) + 1
        d.point((x, y), fill=H(luz))
    for s_, dy in ((-3, -1), (0, 0), (3, 1)):   # garras
        d.line((x1 - 1, y1 + s_, x1 - 4, y1 + s_ + dy), fill=H(borde), width=2)
# Papa zombie: mira a la izquierda, brazos adelante, grietas verdes y una mordida abierta
def zombie(f):
    im = Image.new("RGBA", (70, 76), (0, 0, 0, 0)); d = ImageDraw.Draw(im); p = im.load()
    bob = (0, -1, 0, 1)[f]; PA = ["#d9b184", "#b98a5e", "#8d6547", "#634535", "#3f2a26"]
    cx, cy = 38, 38 + bob
    for x, y, up in ((26, 66, f == 1), (44, 66, f == 3)):
        yy = y - (3 if up else 0)
        d.rectangle((x, yy - 7, x + 8, yy + 3), fill=H(PA[3])); d.rectangle((x - 3, yy + 3, x + 9, yy + 7), fill=H(PA[4]))
    brazo(d, 26, 33 + bob, 8, 29 + bob - (0, 1, 0, -1)[f], PA[3], PA[2], PA[4])
    for j in range(-27, 28):
        for i in range(-23, 24):
            b = (i / 23.5) ** 2 + (j / 27.5) ** 2 + .05 * math.sin(i * .7) * math.sin(j * .5)
            if b < 1:
                luz = -i / 23 * .55 - j / 27 * .85
                p[cx + i, cy + j] = H(PA[0] if luz > .55 else PA[1] if luz > 0 else PA[2] if luz > -.6 else PA[3])
    for x, y, r_ in ((50, 24, 3), (26, 52, 4), (48, 50, 3), (22, 28, 2)):   # hoyuelos
        d.ellipse((x - r_, y - r_ + bob, x + r_, y + r_ + bob), fill=H(PA[3])); d.arc((x - r_, y - r_ + bob, x + r_, y + r_ + bob), 200, 340, fill=H(PA[4]))
    # mordida con carne radiactiva
    d.polygon([(50, 40 + bob), (61, 36 + bob), (60, 54 + bob), (50, 52 + bob)], fill=H("#7cc644")); d.polygon([(52, 42 + bob), (58, 40 + bob), (57, 50 + bob), (52, 50 + bob)], fill=H("#d6f870"))
    # grietas que brillan
    for t, c in (([(30, 14), (35, 21), (33, 27), (39, 33)], "#a8ec4a"), ([(46, 18), (43, 25), (47, 31)], "#a8ec4a"), ([(36, 56), (41, 50), (46, 58)], "#7cc644")):
        d.line([(a, b + bob) for a, b in t], fill=H(c)); d.point((t[0][0], t[0][1] + bob), fill=H("#f0ffc0"))
    # brazo cercano: se afina hacia la mano y termina en tres garras
    brazo(d, 28, 51 + bob, 9, 47 + bob + (0, 1, 0, -1)[f], PA[2], PA[1], PA[4])
    # ojo saltón, ojo cosido, boca con dientes
    d.ellipse((17, 16 + bob, 31, 30 + bob), fill=H("#f4f0d0")); d.ellipse((17, 16 + bob, 31, 30 + bob), outline=H(PA[4])); d.ellipse((20, 21 + bob, 26, 27 + bob), fill=H("#7cc644")); d.rectangle((22, 23 + bob, 24, 25 + bob), fill=H("#1a1320")); d.point((21, 22 + bob), fill=H("#f0ffc0"))
    d.line((35, 19 + bob, 44, 24 + bob), fill=H(PA[4]), width=2); d.line((37, 25 + bob, 41, 18 + bob), fill=H(PA[4])); d.line((41, 27 + bob, 45, 20 + bob), fill=H(PA[4]))
    d.polygon([(17, 36 + bob), (38, 34 + bob), (35, 46 + bob), (20, 46 + bob)], fill=H("#241a20"))
    for x in (20, 26, 32): d.polygon([(x, 35 + bob), (x + 4, 35 + bob), (x + 2, 40 + bob)], fill=H("#f4f0d0"))
    for x in (23, 29): d.polygon([(x, 46 + bob), (x + 4, 46 + bob), (x + 2, 42 + bob)], fill=H("#d9d4b4"))
    d.line((26, 3 + bob, 28, 11 + bob), fill=H("#3a6e45"), width=2)
    for s, y in ((-1, 3), (1, 1)): d.polygon([(27, 5 + bob), (27 + s * 9, y + bob), (27 + s * 6, 8 + bob)], fill=H("#6ea552"))
    U_cont(im); return im
def U_cont(im):
    p = im.load(); W, Hh = im.size; m = []
    for y in range(Hh):
        for x in range(W):
            if p[x, y][3] == 0 and any(0 <= x + a < W and 0 <= y + b < Hh and p[x + a, y + b][3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): m.append((x, y))
    for x, y in m: p[x, y] = H("#1a1320")
for f in range(4): guardar(zombie(f), f"Zombie{f + 1}")
# Halo verde suave
h = Image.new("RGBA", (340, 340), (0, 0, 0, 0)); hp = h.load()
for y in range(340):
    for x in range(340):
        dd = math.hypot(x - 170, y - 170) / 170
        if dd < 1: hp[x, y] = (150, 240, 80, int(200 * (1 - dd) ** 1.8))
guardar(h, "HaloVerde")
b = Image.new("RGBA", (8, 8), (255, 255, 255, 255)); guardar(b, "Blanco")
# Icono pequeños para los botones
def ic_mochila(d, cx, cy):
    d.rectangle((cx - 9, cy - 7, cx + 9, cy + 9), fill=H("#8a6244")); d.rectangle((cx - 6, cy - 11, cx + 6, cy - 7), fill=H("#6a4634")); d.rectangle((cx - 5, cy - 2, cx + 5, cy + 5), fill=H("#c9a06a")); d.line((cx - 9, cy - 7, cx + 9, cy - 7), fill=H("#ab8259")); d.rectangle((cx - 1, cy, cx + 1, cy + 2), fill=H("#3f2d2c"))
def ic_brote(d, cx, cy):
    d.ellipse((cx - 11, cy - 2, cx + 11, cy + 11), fill=H("#c49565")); d.chord((cx - 11, cy - 2, cx + 11, cy + 11), 140, 300, fill=H("#e0b98a"))
    d.line((cx, cy - 2, cx, cy - 9), fill=H("#3a6e45"), width=2); d.polygon([(cx, cy - 8), (cx - 8, cy - 12), (cx - 6, cy - 5)], fill=H("#7cc644")); d.polygon([(cx, cy - 8), (cx + 8, cy - 12), (cx + 6, cy - 5)], fill=H("#a8ec4a"))
def ic_engr(d, cx, cy):
    for j in range(-11, 12):
        for i in range(-11, 12):
            r_ = math.hypot(i, j); a = math.atan2(j, i)
            if 3.6 < r_ < 7.5 + (3 if math.cos(a * 8) > .2 else 0): d.point((cx + i, cy + j), fill=H("#c3ccd2") if i + j < 0 else H("#7d8a96"))
# Botones principales: tablón colgado de dos cuerdas, igual que el inventario
def tablon(w, h, estado, lineas, icono):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); p = im.load()
    pw, ph = w - 4, 96; ox, oy = 2, h - ph - 4
    if estado == "Presionado": oy += 3
    for x in (24, w - 25): d.line((x, 0, x, oy + 2), fill=H("#c9b28f"), width=2); d.line((x + 1, 0, x + 1, oy + 2), fill=H("#8e7d60"))
    sub = Image.new("RGBA", (pw, ph), (0, 0, 0, 0)); sp = sub.load(); U.marco(sp, pw, ph); U.lino(sp, 8, 8, pw - 16, ph - 16)
    im.alpha_composite(sub, (ox, oy))
    if estado == "Hover":
        for i in range(ox + 3, ox + pw - 3):
            p[i, oy + 3] = VERDE[1]; p[i, oy + 4] = VERDE[2]; p[i, oy + ph - 4] = VERDE[1]
        for j in range(oy + 3, oy + ph - 3):
            p[ox + 3, j] = VERDE[1]; p[ox + pw - 4, j] = VERDE[1]; p[ox + 4, j] = VERDE[2]
    if estado == "Presionado":
        a = im.load()
        for y in range(h):
            for x in range(w):
                c = a[x, y]
                if c[3]: a[x, y] = (int(c[0] * .84), int(c[1] * .82), int(c[2] * .8), 255)
    d = ImageDraw.Draw(im); cx = w // 2
    icono(d, cx, oy + 28)
    for k, t in enumerate(lineas): texto(d, cx, oy + 44 + k * 18, t, 17)
    return im
for nom, lin, ic, tam_ in (("Cargar", ("CARGAR", "PARTIDA"), ic_mochila, (155, 126)), ("Nueva", ("NUEVA", "PARTIDA"), ic_brote, (155, 127)), ("Ajustes", ("AJUSTES",), ic_engr, (155, 128))):
    for est, suf in (("Normal", ""), ("Hover", "Hover"), ("Presionado", "Presionado")):
        guardar(tablon(tam_[0], tam_[1], est, lin, ic), f"Boton{nom}{suf}")
# Panel, ranuras y botones pequeños
im = Image.new("RGBA", (300, 240), (0, 0, 0, 0)); p = im.load(); U.marco(p, 300, 240); U.lino(p, 10, 10, 280, 220); U.emblema(p, 150, 233); guardar(im, "Panel")
def ranura(n, brillo):
    im = Image.new("RGBA", (264, 46), (0, 0, 0, 0)); d = ImageDraw.Draw(im); p = im.load()
    d.rectangle((0, 0, 263, 45), fill=ROBLE[1]); d.rectangle((2, 2, 261, 43), fill=LINO[3] if brillo else LINO[2])
    for i in range(3, 261):
        p[i, 2] = LINO[0]; p[i, 43] = LINO[3]
    for j in range(5, 42, 5):
        for i in range(4 + j % 4, 260, 9): p[i, j] = LINO[1]
    p[0, 0] = p[263, 0] = p[0, 45] = p[263, 45] = (0, 0, 0, 0)
    if brillo:
        for i in range(2, 262): p[i, 2] = VERDE[1]; p[i, 43] = VERDE[1]
        for j in range(2, 44): p[2, j] = VERDE[1]; p[261, j] = VERDE[1]
    guardar(im, n)
ranura("Ranura", False); ranura("RanuraHover", True)
def boton(n, w, h, tono, marca=None):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); p = im.load()
    d.rectangle((0, 0, w - 1, h - 1), fill=ROBLE[1]); d.rectangle((1, 1, w - 2, h - 2), fill=H(tono[0])); d.line((2, 2, w - 3, 2), fill=H(tono[1])); d.line((2, h - 3, w - 3, h - 3), fill=H(tono[2]))
    p[0, 0] = p[w - 1, 0] = p[0, h - 1] = p[w - 1, h - 1] = (0, 0, 0, 0)
    if marca: marca(d, w, h)
    guardar(im, n)
CL, HV = ("#d4bb90", "#f2e4c4", "#a5835e"), ("#e7d3ab", "#fff4d2", "#b89a72")
equis = lambda c: (lambda d, w, h: (d.line((5, 5, w - 6, h - 6), fill=H(c), width=2), d.line((w - 6, 5, 5, h - 6), fill=H(c), width=2)))
boton("BotonPeq", 84, 22, CL); boton("BotonPeqHover", 84, 22, HV); boton("BotonMini", 18, 18, CL); boton("BotonMiniHover", 18, 18, HV)
boton("BorrarNormal", 18, 18, CL, equis("#8e3c36")); boton("BorrarHover", 18, 18, ("#e88f80", "#f2b0a0", "#b85a4a"), equis("#fff4d2"))
print("ok")
