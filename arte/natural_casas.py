"""Casas de PapaYork por dentro y por fuera: exteriores distintos, salas y muebles. Dibujo propio por código.
Salida: Natural/Casas/, Natural/Salas/, Natural/Muebles/. Uso: python3 arte/natural_casas.py"""
import math, os, random
from PIL import Image, ImageDraw
A = os.path.dirname(os.path.abspath(__file__)); N = os.path.join(A, "..", "Natural")
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
K = H("#2a1d2b")
MAD = list(map(H, ("#3f2d2c", "#5b4136", "#7a5a45", "#987857", "#b89a72")))
OSC = list(map(H, ("#241a20", "#3a2a2a", "#54392f", "#6f4f3b", "#8d6a4c")))
PIE = list(map(H, ("#55555e", "#74747a", "#96958f", "#b6b2a4")))
def guardar(im, r):
    p = os.path.join(N, r + ".png"); os.makedirs(os.path.dirname(p), exist_ok=True); im.save(p)
def lz(w, h): im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); return im, ImageDraw.Draw(im), im.load()
def rc(d, x, y, w, h, c): d.rectangle((x, y, x + w - 1, y + h - 1), fill=c)
def contorno(im):
    p = im.load(); W, Hh = im.size; m = []
    for y in range(Hh):
        for x in range(W):
            if p[x, y][3] == 0 and any(0 <= x + a < W and 0 <= y + b < Hh and p[x + a, y + b][3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): m.append((x, y))
    for x, y in m: p[x, y] = K
def tablas_v(d, x, y, w, h, r, paso=7):
    rc(d, x, y, w, h, r[2])
    for i in range(x, x + w, paso):
        rc(d, i, y, 1, h, r[0]); rc(d, i + 1, y, 1, h, r[3])
    rc(d, x + w - 6, y, 6, h, r[1])
def tablas_h(d, x, y, w, h, r, paso=6):
    rc(d, x, y, w, h, r[2])
    for j in range(y, y + h, paso):
        rc(d, x, j, w, 1, r[0]); rc(d, x, j + 1, w, 1, r[3])
def piedra(d, x, y, w, h, r=PIE, sem=1):
    rn = random.Random(sem); rc(d, x, y, w, h, r[0])
    for f, j in enumerate(range(y, y + h, 7)):
        i = x - (f % 2) * 6
        while i < x + w:
            a = rn.randint(9, 14); x0, x1 = max(x, i), min(x + w - 2, i + a - 2); y1 = min(y + h - 1, j + 5)
            if x1 >= x0:
                d.rectangle((x0, j, x1, y1), fill=r[rn.choice((1, 2, 2))]); d.line((x0, j, x1, j), fill=r[3])
            i += a
def puerta(d, x, y, w, h, c="#7a4a34", marco=OSC):
    rc(d, x - 2, y - 2, w + 4, h + 2, marco[1]); rc(d, x, y, w, h, H(c))
    d.line((x, y, x, y + h), fill=H("#a06a48"))
    for i in (x + w // 2, x + w - 1): d.line((i, y, i, y + h), fill=H("#4a2c22"))
    d.line((x, y + h // 3, x + w, y + h // 3), fill=H("#4a2c22")); rc(d, x + w - 4, y + h // 2, 2, 3, H("#e8c76f"))
def ventana(d, x, y, w, h, marco=OSC[1], flores=False):
    rc(d, x - 2, y - 2, w + 4, h + 4, marco); rc(d, x, y, w, h, H("#6fa8b0"))
    d.polygon([(x, y), (x + w // 2, y), (x, y + h // 2)], fill=H("#a8d3cf"))
    d.line((x + w // 2, y, x + w // 2, y + h), fill=marco); d.line((x, y + h // 2, x + w, y + h // 2), fill=marco)
    if flores:
        rc(d, x - 3, y + h + 2, w + 6, 4, MAD[1])
        for i in range(x - 2, x + w + 2, 3):
            d.point((i, y + h + 1), fill=H(random.Random(i).choice(("#e88fa8", "#f0d268", "#fff4d2")))); d.point((i + 1, y + h + 1), fill=H("#4f8a49"))
def techo(d, x, y, w, h, r, fila=6, ancho=8):
    for j in range(h):
        f = j // fila; o = (f % 2) * ancho // 2
        for i in range(w):
            q = (i + o) % ancho; s = j % fila
            k = 3 if s == fila - 1 else 2 if q == ancho - 1 or s == fila - 2 else 0 if s == 0 else 1
            if i / w > .72 and k < 3: k += 1
            d.point((x + i, y + j), fill=r[k])
TEJA_ROJA = list(map(H, ("#d9775a", "#b85a4a", "#93433f", "#6e3236")))
TEJA_AZUL = list(map(H, ("#7a97b8", "#5a7696", "#425a78", "#2e405a")))
TEJA_VERDE = list(map(H, ("#7fa86a", "#5f8a58", "#466a48", "#324e3a")))
PIZARRA = list(map(H, ("#6a6a78", "#4f4f60", "#3a3a4c", "#2a2a3a")))
PAJA = list(map(H, ("#e3c478", "#c9a65e", "#a5834a", "#7c5f3a")))

# ---------- Exteriores. Cada función devuelve su imagen y la x de la puerta ----------
def nordica():
    """Mercado de Rosa: madera oscura, techo de césped muy inclinado, gablete tallado."""
    im, d, p = lz(160, 140); W = 160
    tablas_v(d, 22, 74, 116, 52, OSC, 6)
    rc(d, 22, 120, 116, 7, PIE[1]); d.line((22, 120, 137, 120), fill=PIE[3])
    # techo a dos aguas con césped
    d.polygon([(4, 78), (80, 8), (156, 78)], fill=OSC[1]); d.polygon([(14, 78), (80, 18), (146, 78)], fill=OSC[2])
    rn = random.Random(3)
    for y in range(16, 78):
        m = (y - 8) * 76 // 70
        for x in range(80 - m, 80 + m):
            if (x + y * 2) % 3 != 0 or y < 30:
                v = rn.random()
                d.point((x, y), fill=H("#3a6e45" if v < .3 else "#4f8a49" if v < .7 else "#6ea552") if x < 80 else H("#2c5540" if v < .4 else "#3a6e45"))
    for m_ in range(0, 70, 3):      # flores en el césped
        d.point((rn.randint(50, 120), rn.randint(40, 74)), fill=H(rn.choice(("#f0d268", "#e88fa8", "#fff4d2"))))
    d.line((4, 78, 80, 8), fill=OSC[0], width=3); d.line((80, 8, 156, 78), fill=OSC[0], width=3)
    # cabezas talladas en las puntas del gablete
    for a, b, s in ((80, 6, 1), (80, 6, -1)):
        d.line((a, b, a + s * 8, b - 6), fill=OSC[4], width=2); d.point((a + s * 9, b - 7), fill=OSC[3])
    tablas_v(d, 52, 58, 56, 22, OSC, 5)
    d.polygon([(52, 58), (80, 30), (108, 58)], fill=OSC[3]); d.polygon([(58, 58), (80, 36), (102, 58)], fill=OSC[2])
    for i in range(62, 100, 8): d.line((i, 56, i, 46 + abs(i - 80) // 2), fill=OSC[1])
    rc(d, 75, 44, 10, 10, H("#ffd777")); d.line((80, 44, 80, 54), fill=OSC[0])
    # letrero y toldo de mercado
    rc(d, 46, 82, 68, 10, MAD[3]); d.line((46, 82, 113, 82), fill=MAD[4]); d.text((54, 81), "MERCADO", fill=H("#3f2d2c"))
    puerta(d, 70, 96, 22, 30, "#8a5a38"); ventana(d, 32, 96, 18, 14, OSC[0], True); ventana(d, 110, 96, 18, 14, OSC[0], True)
    for x, y in ((14, 118), (136, 118)):   # cajas con verdura
        rc(d, x, y, 14, 9, MAD[2]); d.line((x, y, x + 13, y), fill=MAD[3])
        for i in range(x + 1, x + 13, 3): d.point((i, y - 1), fill=H("#f09a3f"))
    contorno(im); return im, 81
def minera():
    """Herrería de Fermín: piedra, vigas, castillete de mina y vagoneta con mineral."""
    im, d, p = lz(170, 140)
    # castillete
    for x in (124, 158): d.line((x, 20, x + (8 if x < 140 else -8), 110), fill=OSC[2], width=3)
    for y in (34, 58, 82): d.line((126 + (y - 20) // 12, y, 156 - (y - 20) // 12, y), fill=OSC[3], width=2)
    d.line((120, 20, 162, 20), fill=OSC[1], width=4); d.ellipse((134, 10, 148, 24), outline=PIE[1], width=2)
    d.line((141, 18, 141, 100), fill=PIE[0])
    piedra(d, 10, 62, 118, 64, sem=4)
    rc(d, 10, 62, 118, 3, OSC[1])
    for x in (10, 66, 124): rc(d, x, 62, 5, 64, OSC[2]); d.line((x, 62, x, 125), fill=OSC[4])
    rc(d, 10, 92, 118, 4, OSC[2])
    techo(d, 2, 28, 134, 36, PIZARRA, 5, 8); d.line((2, 28, 135, 28), fill=PIZARRA[0]); d.line((2, 63, 135, 63), fill=K)
    # chimenea de fragua con humo y resplandor
    piedra(d, 20, 6, 20, 26, sem=9); rc(d, 18, 4, 24, 4, PIE[0])
    puerta(d, 56, 96, 24, 30, "#5c4436"); ventana(d, 24, 98, 18, 14, OSC[0]); rc(d, 92, 100, 22, 22, H("#3a2228"))
    rc(d, 95, 110, 16, 10, H("#f09a3f")); rc(d, 99, 113, 8, 6, H("#ffd777"))
    rc(d, 44, 72, 50, 12, MAD[2]); d.line((44, 72, 93, 72), fill=MAD[4]); d.text((54, 71), "HERRERIA", fill=H("#241a20"))
    # raíl y vagoneta
    d.line((130, 134, 168, 134), fill=PIE[0], width=2); d.line((130, 128, 168, 128), fill=PIE[1])
    rc(d, 138, 112, 26, 16, PIE[0]); d.line((138, 112, 163, 112), fill=PIE[3])
    for x in range(140, 162, 4): d.ellipse((x, 106, x + 4, 112), fill=H("#8a6a4a")); d.point((x + 1, 107), fill=H("#e8c76f"))
    for x in (143, 158): d.ellipse((x - 3, 126, x + 3, 132), fill=K)
    contorno(im); return im, 68
def alcaldia():
    """Alcaldía: piedra clara, columnas, torre del reloj y bandera."""
    im, d, p = lz(180, 170); CL = list(map(H, ("#8a8676", "#b0ac98", "#cfcab4", "#e6e0ca")))
    piedra(d, 12, 96, 156, 60, CL, 2); rc(d, 12, 96, 156, 4, CL[3])
    techo(d, 4, 74, 172, 24, TEJA_AZUL, 5, 9); d.line((4, 98, 175, 98), fill=K)
    piedra(d, 72, 30, 36, 50, CL, 5)
    d.polygon([(66, 32), (90, 6), (114, 32)], fill=TEJA_AZUL[1]); d.polygon([(90, 6), (114, 32), (90, 32)], fill=TEJA_AZUL[2])
    d.ellipse((79, 40, 101, 62), fill=H("#fbf5ea"), outline=K); d.line((90, 51, 90, 44), fill=K); d.line((90, 51, 96, 51), fill=K)
    d.line((90, 6, 90, 0), fill=K); d.polygon([(91, 0), (102, 3), (91, 6)], fill=H("#c04a4a"))
    for x in (54, 72, 102, 120): rc(d, x, 104, 7, 52, CL[3]); rc(d, x + 5, 104, 2, 52, CL[0]); rc(d, x - 1, 102, 9, 3, CL[1]); rc(d, x - 1, 153, 9, 3, CL[1])
    rc(d, 50, 98, 80, 7, CL[2]); d.text((68, 97), "ALCALDIA", fill=H("#3f3f50"))
    puerta(d, 80, 120, 20, 36, "#6a4230", CL); ventana(d, 22, 112, 18, 22, CL[0]); ventana(d, 140, 112, 18, 22, CL[0])
    rc(d, 44, 154, 92, 4, CL[1]); rc(d, 36, 158, 108, 4, CL[0])
    contorno(im); return im, 90
def cottage():
    """Casa de Lupita: pequeña y alegre, muro amarillo y techo azul."""
    im, d, p = lz(120, 110); Y = list(map(H, ("#c9a040", "#e6c25e", "#f4d98a")))
    rc(d, 14, 52, 92, 46, Y[1]); rc(d, 14, 52, 4, 46, Y[2]); rc(d, 94, 52, 12, 46, Y[0])
    techo(d, 4, 14, 112, 40, TEJA_AZUL); d.line((4, 54, 115, 54), fill=K)
    puerta(d, 48, 68, 20, 30, "#d0605e"); ventana(d, 22, 66, 16, 14, OSC[1], True); ventana(d, 80, 66, 16, 14, OSC[1], True)
    d.ellipse((52, 28, 64, 40), fill=H("#fff4d2"), outline=OSC[1])
    piedra(d, 14, 94, 92, 8, sem=2)
    rc(d, 84, 2, 10, 16, MAD[2])
    contorno(im); return im, 58
def pescador():
    """Cabaña de Tomás: tablas azules gastadas, redes y flotadores."""
    im, d, p = lz(130, 110); AZ = list(map(H, ("#2f4f60", "#47708a", "#6a94a8", "#8db4c0")))
    tablas_h(d, 14, 50, 102, 50, AZ, 6)
    d.polygon([(2, 54), (65, 10), (128, 54)], fill=PAJA[1]); d.polygon([(65, 10), (128, 54), (65, 54)], fill=PAJA[2])
    for y in range(16, 54, 5):
        m = (y - 10) * 63 // 44; d.line((65 - m, y, 65 + m, y), fill=PAJA[3])
    puerta(d, 54, 68, 20, 32, "#6f5240"); ventana(d, 24, 66, 16, 12, OSC[0])
    for x in range(84, 112, 4):      # red colgada
        d.line((x, 60, x + 3, 86), fill=H("#d8d0b8")); d.line((x + 3, 60, x, 86), fill=H("#d8d0b8"))
    for x, c in ((86, "#d84f5f"), (98, "#f4d36a"), (108, "#d84f5f")): d.ellipse((x, 84, x + 5, 89), fill=H(c))
    rc(d, 8, 96, 114, 8, MAD[1])
    contorno(im); return im, 64
def taberna():
    """La Papa Contenta: dos plantas con vigas a la vista y letrero colgante."""
    im, d, p = lz(170, 160); CR = list(map(H, ("#b8a688", "#d9c8a4", "#efe2c4")))
    rc(d, 14, 60, 142, 86, CR[1]); rc(d, 14, 60, 4, 86, CR[2]); rc(d, 140, 60, 16, 86, CR[0])
    for x in (14, 58, 106, 152): rc(d, x, 60, 5, 86, OSC[2]); d.line((x, 60, x, 145), fill=OSC[4])
    rc(d, 14, 100, 142, 5, OSC[2])
    for a, b in ((19, 58), (106, 152)):
        d.line((a, 100, b, 62), fill=OSC[2], width=3); d.line((a, 62, b, 100), fill=OSC[2], width=3)
    techo(d, 4, 18, 162, 44, TEJA_ROJA); d.line((4, 62, 165, 62), fill=K)
    piedra(d, 14, 132, 142, 14, sem=6); rc(d, 128, 2, 16, 20, PIE[1])
    puerta(d, 72, 108, 24, 38, "#6a4230")
    ventana(d, 24, 112, 26, 16, OSC[0]); ventana(d, 116, 112, 26, 16, OSC[0]); ventana(d, 72, 68, 24, 20, OSC[0], True)
    for x in (25, 117): rc(d, x, 113, 24, 14, H("#ffd777")); d.line((x + 12, 113, x + 12, 126), fill=OSC[0])
    rc(d, 4, 96, 34, 3, OSC[1]); d.line((10, 99, 10, 104), fill=K); d.line((30, 99, 30, 104), fill=K)
    rc(d, 5, 104, 32, 16, MAD[3]); d.ellipse((13, 106, 29, 118), fill=H("#c49565"), outline=K); d.point((18, 110), fill=K); d.point((24, 110), fill=K); d.line((18, 114, 24, 114), fill=K)
    contorno(im); return im, 84
def biblioteca():
    """Biblioteca: ladrillo, techo verde de cobre y ventanal redondo."""
    im, d, p = lz(170, 150); LD = list(map(H, ("#6a3a34", "#8a4f42", "#a56a54", "#bf8a70")))
    piedra(d, 14, 62, 142, 76, LD, 3); techo(d, 4, 22, 162, 42, TEJA_VERDE); d.line((4, 64, 165, 64), fill=K)
    d.polygon([(60, 24), (85, 2), (110, 24)], fill=TEJA_VERDE[1]); d.polygon([(85, 2), (110, 24), (85, 24)], fill=TEJA_VERDE[2])
    d.ellipse((69, 66, 101, 96), fill=OSC[1]); d.ellipse((72, 69, 98, 93), fill=H("#a8d3cf")); d.line((85, 69, 85, 93), fill=OSC[1]); d.line((72, 81, 98, 81), fill=OSC[1])
    rc(d, 44, 98, 82, 8, MAD[3]); d.text((52, 97), "BIBLIOTECA", fill=H("#241a20"))
    puerta(d, 74, 108, 22, 30, "#5c3f2f"); ventana(d, 28, 92, 20, 26, OSC[1]); ventana(d, 122, 92, 20, 26, OSC[1])
    rc(d, 66, 138, 38, 3, PIE[2]); rc(d, 60, 141, 50, 3, PIE[1])
    contorno(im); return im, 85
def capilla():
    """Capilla vieja, cerrada desde la evacuación."""
    im, d, p = lz(110, 140); CL = list(map(H, ("#8a8a80", "#a8a89c", "#c4c4b6", "#dcdccc")))
    piedra(d, 14, 60, 82, 68, CL, 7); d.polygon([(4, 64), (55, 26), (106, 64)], fill=PIZARRA[1]); d.polygon([(55, 26), (106, 64), (55, 64)], fill=PIZARRA[2])
    piedra(d, 42, 10, 26, 30, CL, 8); d.polygon([(38, 12), (55, 0), (72, 12)], fill=PIZARRA[2]); rc(d, 50, 18, 10, 14, K)
    d.ellipse((46, 66, 64, 84), fill=H("#c8716a"), outline=K); d.line((55, 66, 55, 84), fill=K); d.line((46, 75, 64, 75), fill=K)
    puerta(d, 44, 98, 22, 30, "#4a3028")
    d.line((44, 102, 66, 124), fill=MAD[0], width=2); d.line((66, 102, 44, 124), fill=MAD[0], width=2)
    for x, y in ((18, 110), (88, 92), (24, 74)): d.point((x, y), fill=H("#6ea552")); d.point((x + 1, y), fill=H("#4f8a49")); d.point((x, y + 1), fill=H("#3a6e45"))
    contorno(im); return im, 55
def casa_sencilla(nombre, techo_r, muro):
    im, d, p = lz(116, 106); M = list(map(H, muro))
    rc(d, 14, 52, 88, 44, M[1]); rc(d, 14, 52, 4, 44, M[2]); rc(d, 90, 52, 12, 44, M[0])
    techo(d, 4, 16, 108, 38, techo_r); d.line((4, 54, 111, 54), fill=K)
    puerta(d, 46, 66, 20, 30); ventana(d, 22, 66, 14, 14, OSC[1], True); ventana(d, 76, 66, 14, 14, OSC[1])
    piedra(d, 14, 92, 88, 8, sem=5); contorno(im); return im, 56
EXT = {"Nordica": nordica, "Minera": minera, "Alcaldia": alcaldia, "Cottage": cottage, "Pescador": pescador, "Taberna": taberna, "Biblioteca": biblioteca, "Capilla": capilla,
       "Rosada": lambda: casa_sencilla("Rosada", TEJA_ROJA, ("#c08a8a", "#e0b0a8", "#f2d0c4")), "Verde": lambda: casa_sencilla("Verde", PIZARRA, ("#7f9a78", "#a0b890", "#c0d0a8"))}
PUERTAS = {}
for n, f in EXT.items():
    im, x = f(); guardar(im, "Casas/" + n); PUERTAS[n] = (x, im.size)
import json; json.dump(PUERTAS, open(os.path.join(N, "Casas/puertas.json"), "w"))

# ---------- Muebles: la parte de abajo es lo que estorba al caminar ----------
def mueble(n, w, h, fn):
    im, d, p = lz(w, h); fn(d, w, h); contorno(im); guardar(im, "Muebles/" + n)
def lomos(d, x, y, w, h):
    r = random.Random(x + y); i = x
    while i < x + w - 1:
        a = r.randint(2, 4); c = r.choice(("#c04a4a", "#4f7ec9", "#5f8a58", "#e0c060", "#8a5fa8", "#d9c8a4"))
        al = r.randint(h - 3, h); rc(d, i, y + h - al, a, al, H(c)); d.line((i, y + h - al, i, y + h), fill=H("#2a1d2b")); i += a
def estante(d, w, h):
    rc(d, 0, 0, w, h, MAD[1]); rc(d, 2, 2, w - 4, h - 4, MAD[0])
    for y in range(3, h - 8, 13): lomos(d, 3, y, w - 6, 10); rc(d, 2, y + 10, w - 4, 2, MAD[2])
    d.line((0, 0, w, 0), fill=MAD[3]); rc(d, 0, h - 3, w, 3, MAD[1])
def cama(d, w, h):
    rc(d, 0, 0, w, h, MAD[1]); rc(d, 2, 2, w - 4, 10, MAD[3]); rc(d, 3, 10, w - 6, 13, H("#f2e9d6")); rc(d, 3, 22, w - 6, h - 26, H("#c05a4a"))
    for i in range(3, w - 3, 6):
        for j in range(22, h - 4, 6): rc(d, i, j, 3, 3, H("#d67a60"))
    rc(d, 3, h - 7, w - 6, 3, H("#8e3c36"))
def estufa(d, w, h):
    rc(d, 0, 8, w, h - 8, H("#3a3a48")); rc(d, 2, 10, w - 4, 3, H("#5c5c6c")); rc(d, 5, 18, w - 10, h - 24, K); rc(d, 8, 22, w - 16, h - 30, H("#f09a3f")); rc(d, 12, 26, w - 24, h - 36, H("#ffd777"))
    rc(d, w - 11, 0, 7, 10, H("#3a3a48"))
    d.ellipse((3, 5, 13, 11), fill=H("#6a6a7a"))
def mesa(d, w, h):
    rc(d, 0, 0, w, h - 10, MAD[3]); d.line((0, 0, w, 0), fill=MAD[4]); rc(d, 0, h - 12, w, 3, MAD[1])
    for x in (2, w - 6): rc(d, x, h - 10, 4, 10, MAD[1])
    for x in range(5, w - 5, 8): d.line((x, 2, x, h - 13), fill=MAD[2])
def mostrador(d, w, h):
    tablas_v(d, 0, 8, w, h - 8, MAD, 8); rc(d, 0, 0, w, 10, MAD[4]); d.line((0, 9, w, 9), fill=MAD[0])
    for x in range(8, w - 6, 26): d.ellipse((x, 1, x + 8, 7), fill=H("#c49565"), outline=MAD[1])
def armario(d, w, h):
    tablas_v(d, 0, 0, w, h, MAD, w // 2); rc(d, w // 2 - 3, h // 2, 2, 4, H("#e8c76f")); rc(d, w // 2 + 1, h // 2, 2, 4, H("#e8c76f")); d.line((0, 0, w, 0), fill=MAD[4])
def barril(d, w, h):
    d.ellipse((0, 0, w - 1, 8), fill=MAD[1]); rc(d, 0, 4, w, h - 8, MAD[2]); d.ellipse((0, h - 9, w - 1, h - 1), fill=MAD[1]); d.ellipse((2, 1, w - 3, 7), fill=MAD[0]); rc(d, 0, 10, w, 2, PIE[0]); rc(d, 0, h - 11, w, 2, PIE[0]); rc(d, 2, 5, 3, h - 10, MAD[3])
def yunque(d, w, h):
    rc(d, 6, h - 8, w - 12, 8, MAD[1]); rc(d, w // 2 - 4, 10, 8, h - 18, PIE[0]); d.polygon([(0, 2), (w, 2), (w - 4, 11), (6, 11)], fill=PIE[1]); d.line((0, 2, w, 2), fill=PIE[3])
def fragua(d, w, h):
    piedra(d, 0, 12, w, h - 12, sem=3); rc(d, 8, 24, w - 16, h - 34, K); rc(d, 11, h - 22, w - 22, 9, H("#f09a3f")); rc(d, 16, h - 19, w - 32, 5, H("#ffe39a")); rc(d, w // 2 - 7, 0, 14, 14, PIE[0])
def escritorio(d, w, h):
    rc(d, 0, 0, w, h - 6, MAD[2]); d.line((0, 0, w, 0), fill=MAD[4]); rc(d, 3, 13, w // 3, h - 20, MAD[1]); rc(d, w - w // 3 - 3, 13, w // 3, h - 20, MAD[1])
    rc(d, 8, 2, 12, 8, H("#f2e9d6")); rc(d, w - 18, 2, 4, 8, H("#3f3f74")); d.line((10, 4, 18, 4), fill=K); d.line((10, 7, 16, 7), fill=K)
def cuadro(d, w, h):
    rc(d, 0, 0, w, h, H("#a8783c")); d.line((0, 0, w, 0), fill=H("#e0b860")); rc(d, 3, 3, w - 6, h - 6, H("#c8b48a"))
    cx = w // 2; d.ellipse((cx - 7, 8, cx + 7, 22), fill=H("#d6a180")); d.ellipse((cx - 13, 5, cx + 13, 11), fill=H("#e3c478")); rc(d, cx - 6, 2, 12, 6, H("#e3c478")); rc(d, cx - 5, 7, 10, 2, H("#2e6e7c")); d.line((cx - 3, 18, cx + 3, 18), fill=H("#a8a49c"), width=2); rc(d, cx - 11, 23, 22, h - 26, H("#5f7c52"))
def mapa(d, w, h):
    rc(d, 0, 0, w, h, H("#d9c8a4")); d.line((0, 0, w, 0), fill=H("#efe2c4")); d.polygon([(6, 6), (20, 8), (24, 18), (10, 22)], fill=H("#6ea552")); d.polygon([(w - 18, 8), (w - 6, 10), (w - 10, 24)], fill=H("#47708a"))
    d.line((14, 14, w - 12, 16), fill=H("#c04a4a"), width=1); d.line((w // 2 - 3, h - 11, w // 2 + 3, h - 5), fill=H("#c04a4a"), width=2); d.line((w // 2 + 3, h - 11, w // 2 - 3, h - 5), fill=H("#c04a4a"), width=2)
def planta(d, w, h):
    d.polygon([(6, h - 12), (w - 6, h - 12), (w - 8, h), (8, h)], fill=H("#b85a4a"))
    r = random.Random(w)
    for _ in range(24):
        x, y = r.randint(2, w - 3), r.randint(0, h - 13); rc(d, x, y, 3, 2, H(r.choice(("#3a6e45", "#4f8a49", "#6ea552"))))
def chimenea(d, w, h):
    piedra(d, 0, 0, w, h, sem=2); rc(d, 8, h - 28, w - 16, 26, K); rc(d, 12, h - 12, w - 24, 8, H("#f09a3f")); rc(d, 18, h - 10, w - 36, 5, H("#ffd777")); rc(d, 0, h - 34, w, 5, MAD[2]); d.line((0, h - 34, w, h - 34), fill=MAD[4])
def piano(d, w, h):
    rc(d, 0, 0, w, h - 6, MAD[0]); d.line((0, 0, w, 0), fill=MAD[2]); rc(d, 3, 20, w - 6, 6, H("#f2e9d6"))
    for x in range(5, w - 4, 4): d.line((x, 20, x, 25), fill=K)
    for x in (2, w - 6): rc(d, x, h - 6, 4, 6, MAD[0])
def vitrina(d, w, h):
    rc(d, 0, h - 16, w, 16, MAD[2]); d.line((0, h - 16, w, h - 16), fill=MAD[4]); rc(d, 2, 0, w - 4, h - 15, H("#a8d3cf")); d.line((2, 0, w - 3, 0), fill=H("#e6f6f0")); d.line((5, 3, 12, 10), fill=H("#e6f6f0")); rc(d, w // 2 - 7, h - 25, 14, 9, H("#efe2c4")); d.line((w // 2 - 5, h - 22, w // 2 + 5, h - 22), fill=K)
def juguetes(d, w, h):
    rc(d, 0, 10, w, h - 10, H("#d0605e")); d.line((0, 10, w, 10), fill=H("#e88fa8")); d.ellipse((4, 2, 14, 12), fill=H("#4f7ec9")); rc(d, 16, 2, 8, 8, H("#f4d36a")); d.ellipse((18, 0, 22, 4), fill=H("#c49565"))
def red(d, w, h):
    rc(d, 0, 0, w, 3, MAD[2])
    for x in range(0, w, 6): d.line((x, 3, x + 8, h - 2), fill=H("#d8d0b8")); d.line((x + 8, 3, x, h - 2), fill=H("#d8d0b8"))
    for x in (4, w // 2, w - 8): d.ellipse((x, h - 7, x + 5, h - 2), fill=H("#d84f5f"))
def cana_pared(d, w, h):
    d.line((1, h - 2, w - 2, 2), fill=H("#b58a55"), width=2); d.line((w - 2, 2, w - 2, h - 6), fill=H("#f7f7ee")); rc(d, w - 4, h - 6, 3, 4, H("#d84f5f"))
def fuente(d, w, h):
    d.ellipse((0, h - 26, w - 1, h - 1), fill=PIE[1]); d.ellipse((4, h - 24, w - 5, h - 5), fill=H("#338694")); d.ellipse((12, h - 20, w - 13, h - 9), fill=H("#46a0a4"))
    rc(d, w // 2 - 3, 14, 6, h - 28, PIE[2]); d.ellipse((w // 2 - 11, 8, w // 2 + 11, 18), fill=PIE[2]); d.ellipse((w // 2 - 7, 2, w // 2 + 7, 13), fill=H("#c49565"))
    for x, y in ((-8, 22), (8, 20), (-14, 30), (14, 28)): d.point((w // 2 + x, y), fill=H("#d8f0dc"))
def tumba(d, w, h):
    d.rounded_rectangle((4, 0, w - 5, h - 8), 6, fill=PIE[2]); d.line((7, 3, w - 8, 3), fill=PIE[3]); rc(d, 0, h - 9, w, 9, H("#6ea552"))
    for x in range(2, w - 2, 3): d.point((x, h - 10), fill=H("#3a6e45"))
    d.line((w // 2, 8, w // 2, 22), fill=PIE[0], width=2); d.line((w // 2 - 5, 13, w // 2 + 5, 13), fill=PIE[0], width=2)
    d.ellipse((w - 12, h - 15, w - 5, h - 8), fill=H("#e3c478"))
def reja(d, w, h):
    for x in range(0, w, 7): rc(d, x, 0, 2, h, H("#5c6470")); d.point((x, 0), fill=H("#c9d2d8"))
    rc(d, 0, 10, w, 3, H("#3c424e")); rc(d, 0, h - 14, w, 3, H("#3c424e")); rc(d, w // 2 - 15, 18, 30, 26, H("#f4d36a")); d.polygon([(w // 2, 22), (w // 2 - 10, 40), (w // 2 + 10, 40)], fill=K); d.point((w // 2, 34), fill=H("#f4d36a"))
    for x, y in ((6, 58), (w - 12, 48), (20, 66)): rc(d, x, y, 4, 2, H("#7cc644"))
def banco(d, w, h):
    rc(d, 0, 6, w, 5, MAD[3]); d.line((0, 6, w, 6), fill=MAD[4]); rc(d, 0, 0, w, 4, MAD[2]); rc(d, 3, 11, 3, h - 11, MAD[1]); rc(d, w - 6, 11, 3, h - 11, MAD[1])
def farol(d, w, h):
    rc(d, w // 2 - 1, 12, 3, h - 12, H("#3c424e")); rc(d, w // 2 - 4, h - 3, 9, 3, H("#3c424e")); rc(d, w // 2 - 4, 2, 9, 10, H("#ffd777")); d.line((w // 2 - 5, 1, w // 2 + 5, 1), fill=H("#3c424e")); d.line((w // 2 - 5, 12, w // 2 + 5, 12), fill=H("#3c424e"))
def pagina(d, w, h):
    d.polygon([(1, 2), (w - 3, 0), (w - 1, h - 3), (3, h - 1)], fill=H("#efe2c4")); d.line((4, 5, w - 5, 4), fill=H("#7a5a45")); d.line((4, 8, w - 6, 7), fill=H("#7a5a45")); d.line((4, 11, w - 8, 10), fill=H("#7a5a45"))
for n, w, h, f in (("Estante", 60, 62, estante), ("EstanteBajo", 44, 38, estante), ("Cama", 44, 62, cama), ("Estufa", 36, 44, estufa), ("Mesa", 56, 30, mesa), ("MesaChica", 32, 28, mesa), ("Mostrador", 170, 30, mostrador), ("Armario", 38, 58, armario),
    ("Barril", 22, 30, barril), ("Yunque", 34, 28, yunque), ("Fragua", 60, 60, fragua), ("Escritorio", 72, 32, escritorio), ("Cuadro", 34, 40, cuadro), ("Mapa", 58, 36, mapa), ("Planta", 24, 34, planta), ("Chimenea", 70, 64, chimenea),
    ("Piano", 60, 40, piano), ("Vitrina", 44, 50, vitrina), ("Juguetes", 30, 24, juguetes), ("Red", 50, 36, red), ("CanaPared", 34, 28, cana_pared), ("Fuente", 76, 66, fuente), ("Tumba", 30, 42, tumba), ("Reja", 90, 74, reja), ("Banco", 40, 20, banco), ("Farol", 11, 46, farol), ("Pagina", 15, 15, pagina)):
    mueble(n, w, h, f)

# ---------- Salas ----------
def sala(nombre, suelo, pared, zocalo, sem=1, alfombra=None, ventanas=(90, 366)):
    im, d, p = lz(480, 288); r = random.Random(sem)
    if suelo == "madera":
        for j in range(56, 288, 14):
            desf = (j // 14 % 3) * 30
            for i in range(0, 480):
                c = MAD[3] if (j + 2) % 14 > 1 else MAD[1]
                if (i + desf) % 90 == 0: c = MAD[1]
                d.point((i, j), fill=c) if False else None
            rc(d, 0, j, 480, 13, H(r.choice(("#a5805a", "#9a7652", "#ac875f")))); rc(d, 0, j + 13, 480, 1, MAD[1])
            for i in range(desf, 480, 90): rc(d, i, j, 1, 13, MAD[1])
            for _ in range(10):
                x = r.randrange(470); d.line((x, j + r.randint(2, 11), x + r.randint(4, 14), j + r.randint(2, 11)), fill=H("#8a6848"))
    elif suelo == "piedra":
        piedra(d, 0, 56, 480, 232, list(map(H, ("#3f3b40", "#5e5a5c", "#6f6a68", "#827c78"))), sem)
    else:
        for j in range(56, 288, 24):
            for i in range(0, 480, 24):
                rc(d, i, j, 24, 24, H("#c2a878") if (i + j) // 24 % 2 else H("#8a6f58"))
    # pared con friso y luz de ventana
    rc(d, 0, 0, 480, 56, H(pared[1])); rc(d, 0, 0, 480, 4, H(pared[0]))
    for y in range(8, 42, 8):
        for x in range((y // 8 % 2) * 12, 480, 24): rc(d, x, y, 1, 8, H(pared[0]))
    rc(d, 0, 40, 480, 16, H(zocalo[1])); rc(d, 0, 40, 480, 2, H(zocalo[0])); rc(d, 0, 54, 480, 2, H(zocalo[2]))
    for vx in ventanas:
        rc(d, vx - 2, 8, 28, 28, MAD[1]); rc(d, vx, 10, 24, 24, H("#a8d3e4")); d.polygon([(vx, 10), (vx + 14, 10), (vx, 24)], fill=H("#dff2f4")); d.line((vx + 12, 10, vx + 12, 34), fill=MAD[1]); d.line((vx, 22, vx + 24, 22), fill=MAD[1])
        for j in range(58, 118):      # luz que entra por la ventana
            for i in range(vx - 2 + (j - 58) // 3, vx + 26 + (j - 58) // 3):
                if (i + j) % 3 == 0:
                    c = p[i, j]; p[i, j] = (min(255, c[0] + 24), min(255, c[1] + 20), min(255, c[2] + 8), 255)
    if alfombra:
        ax, ay, aw, ah, c1, c2 = alfombra
        rc(d, ax, ay, aw, ah, H(c1)); rc(d, ax + 4, ay + 4, aw - 8, ah - 8, H(c2)); rc(d, ax + 8, ay + 8, aw - 16, ah - 16, H(c1))
    # marco inferior con la salida
    rc(d, 0, 276, 480, 12, K); rc(d, 208, 262, 64, 14, H("#5a7a4a")); rc(d, 210, 264, 60, 10, H("#74935a"))
    for i in range(212, 268, 6): rc(d, i, 266, 3, 6, H("#8fae68"))
    rc(d, 216, 276, 48, 12, H("#d9c8a4"))
    rc(d, 0, 0, 8, 288, K); rc(d, 472, 0, 8, 288, K)
    guardar(im, "Salas/" + nombre)
BEIGE = ("#c8b490", "#e2d0ac"); ZM = ("#8d6a4c", "#6f4f3b", "#3f2d2c")
sala("Pedro", "madera", BEIGE, ZM, 1, (150, 120, 150, 90, "#b85a4a", "#d9a06a"))
sala("Mercado", "madera", ("#5f4638", "#7a5a45"), ("#3f2d2c", "#2f2226", "#241a20"), 2, (160, 170, 160, 70, "#5f8a58", "#a8c07a"))
sala("Herreria", "piedra", ("#4a4650", "#62606a"), ("#5b4136", "#3f2d2c", "#241a20"), 3)
sala("Alcaldia", "ajedrez", ("#a0a8b8", "#bcc4d0"), ("#5a6494", "#3f4775", "#2d3358"), 4, (170, 110, 140, 150, "#8e3c36", "#c05a4a"))
sala("Lupita", "madera", ("#e6c25e", "#f4d98a"), ("#c9a040", "#a07a30", "#6f5228"), 5, (170, 130, 140, 90, "#e88fa8", "#f4c0c8"))
sala("Tomas", "madera", ("#47708a", "#6a94a8"), ("#6f5240", "#533d32", "#3c2c28"), 6, ventanas=(226,))
sala("Taberna", "madera", ("#7a5a45", "#987857"), ("#3f2d2c", "#2f2226", "#241a20"), 7, ventanas=(60, 200))
sala("Biblioteca", "ajedrez", ("#6a3a34", "#8a4f42"), ("#3f2d2c", "#2f2226", "#241a20"), 8, (180, 140, 120, 110, "#3f5a78", "#6f8aa8"), ventanas=(226,))
# Comida de la taberna
def contorna(im): contorno(im); return im
im, d, p = lz(32, 32); d.ellipse((6, 13, 26, 27), fill=H("#8a6244")); d.ellipse((6, 11, 26, 21), fill=H("#ab8259")); d.ellipse((9, 13, 23, 19), fill=H("#e8c98a")); rc(d, 12, 15, 3, 2, H("#f09a3f")); rc(d, 18, 14, 3, 2, H("#fff4d2"))
for x in (12, 18): d.line((x, 9, x + 1, 5), fill=H("#f2f2ea"))
guardar(contorna(im), "Objetos/SopaPapa")
im, d, p = lz(32, 32); d.ellipse((5, 11, 27, 25), fill=H("#c8934f")); d.ellipse((7, 11, 24, 20), fill=H("#e0b070"))
for x in (11, 16, 21): d.line((x, 13, x - 2, 19), fill=H("#8a5a30"))
for x, y in ((9, 21), (17, 22), (23, 19)): d.point((x, y), fill=H("#f09a3f"))
guardar(contorna(im), "Objetos/PanZanahoria")
print("ok")
