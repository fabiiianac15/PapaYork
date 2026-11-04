"""Panel de vida de Pedro: madera como el reloj, retrato con gestos y barra con marcas. Dibujo propio por código."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import natural_ui as U
A = os.path.dirname(os.path.abspath(__file__)); B = os.path.join(A, ".."); N = os.path.join(B, "Natural/Vida"); os.makedirs(N, exist_ok=True)
H = U.H; FUENTE = os.path.join(B, "Fuentes/PixelifySans.ttf"); HOYO = (42, 26, 16, 255); W, Alto = 236, 70
def guardar(im, n): im.save(os.path.join(N, n + ".png"))
# ---------- Números propios: en la fuente del juego el 5 se confunde con una S ----------
DIG = {"0": "01110 10001 10011 10101 11001 10001 01110", "1": "00100 01100 00100 00100 00100 00100 01110", "2": "01110 10001 00001 00110 01000 10000 11111", "3": "11110 00001 00001 01110 00001 00001 11110", "4": "00010 00110 01010 10010 11111 00010 00010",
       "5": "11111 10000 11110 00001 00001 10001 01110", "6": "00110 01000 10000 11110 10001 10001 01110", "7": "11111 00001 00010 00100 01000 01000 01000", "8": "01110 10001 10001 01110 10001 10001 01110", "9": "01110 10001 10001 01111 00001 00010 01100", "/": "00001 00010 00010 00100 01000 01000 10000"}
CLARO, OSC = H("#f2e4c4"), H("#a98d68")
def digito(p, x0, y0, c):
    for j, fila in enumerate(DIG[c].split()):
        for i, v in enumerate(fila):
            if v == "1":
                for a in (0, 1):
                    p[x0 + i * 2 + a, y0 + j * 2] = CLARO; p[x0 + i * 2 + a, y0 + j * 2 + 1] = OSC if (j == 6 or DIG[c].split()[j + 1][i] == "0") else CLARO
# ---------- Panel ----------
im = Image.new("RGBA", (W, Alto), (0, 0, 0, 0)); p = im.load(); U.marco(p, W, 62)
d = ImageDraw.Draw(im)
d.ellipse((6, 4, 62, 58), fill=HOYO); d.ellipse((6, 4, 62, 58), outline=U.ROBLE[4]); d.ellipse((9, 7, 59, 55), fill=H("#79a892")); d.ellipse((9, 7, 59, 55), outline=U.ROBLE[0])
d.rectangle((68, 7, 228, 25), fill=HOYO); d.line((68, 26, 228, 26), fill=U.ROBLE[4])
d.rectangle((68, 31, 228, 54), fill=HOYO); d.line((68, 55, 228, 55), fill=U.ROBLE[4]); d.rectangle((72, 35, 224, 50), fill=H("#1c110d"))
U.corazon_en(p, 79, 16, H("#d84f5f"), H("#f08a8a"), H("#8e2f45"))
f = ImageFont.truetype(FUENTE, 15); d.fontmode = "1"; d.text((90, 7), "Pedro", fill=H("#f2e4c4"), font=f)
for k, c in enumerate("/50"): digito(p, 191 + k * 12, 9, c)
for x, h_ in ((26, 7), (75, 5), (132, 8), (190, 5), (216, 6)):   # brotes que cuelgan, como en el reloj
    d.line((x, 62, x, 62 + h_), fill=H("#3c7a3a"), width=2); d.point((x, 62 + h_), fill=H("#c9f06a")); d.line((x - 2, 63, x + 3, 63), fill=H("#7cc644"))
guardar(im, "Panel")
for c in "0123456789":
    t = Image.new("RGBA", (10, 14), (0, 0, 0, 0)); digito(t.load(), 0, 0, c); guardar(t, "Num" + c)
# ---------- Relleno ----------
def relleno(n, cs):
    im = Image.new("RGBA", (150, 14), (0, 0, 0, 255)); p = im.load()
    for y in range(14):
        c = H(cs[0] if y < 2 else cs[1] if y < 6 else cs[2] if y < 11 else cs[3])
        for x in range(150): p[x, y] = c
    guardar(im, n)
relleno("Verde", ("#d3f58a", "#8fd451", "#5fae3f", "#37752f")); relleno("Amarillo", ("#fff0a0", "#f4cf52", "#dca035", "#a06a24")); relleno("Rojo", ("#ffb0a0", "#ec5f53", "#c43a40", "#80232f")); relleno("Rastro", ("#fff6dc", "#f6e3b6", "#e6c98c", "#b2925f"))
# Marcas cada 10 de vida y brillo de vidrio, encima del relleno
m = Image.new("RGBA", (150, 14), (0, 0, 0, 0)); d = ImageDraw.Draw(m)
for x in (30, 60, 90, 120): d.line((x, 0, x, 13), fill=(28, 17, 13, 165)); d.line((x + 1, 0, x + 1, 13), fill=(255, 255, 255, 34))
d.line((1, 1, 148, 1), fill=(255, 255, 255, 70)); guardar(m, "Marcas")
# ---------- Retratos: parten del retrato del diálogo y se reducen a la mitad ----------
base = Image.open(os.path.join(B, "Natural/Retratos/Pedro.png")).convert("RGBA")
fon = base.getpixel((4, 4))
px = base.load()
# El fondo del retrato se vuelve transparente para que el sombrero salga del círculo
pila = [(0, 0), (127, 0), (0, 80), (127, 80)]; vis = set()
while pila:
    x, y = pila.pop()
    if (x, y) in vis or not (0 <= x < 128 and 0 <= y < 128): continue
    c = px[x, y]
    if c[1] < c[0] or c[1] < c[2] or c[0] > 170: continue     # solo tonos del fondo verde
    vis.add((x, y)); px[x, y] = (0, 0, 0, 0); pila += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
PIEL = base.getpixel((64, 70)); TINTA = (46, 28, 26, 255); SOMBRA = base.getpixel((52, 70))
def cara(tipo):
    im = base.copy(); d = ImageDraw.Draw(im)
    if tipo in ("Parpadeo", "Herido", "Critico"):
        # cada ojo se tapa con la piel de su propio lado (la cara tiene luz y sombra)
        for x0, x1 in ((48, 61), (68, 83)):
            piel = base.getpixel(((x0 + x1) // 2, 69))
            d.rectangle((x0, 50, x1, 66), fill=piel)
    if tipo == "Parpadeo":
        for x0, x1 in ((48, 61), (68, 83)): d.rectangle((x0, 58, x1, 60), fill=TINTA)
    if tipo == "Herido":
        for x0, x1, s in ((48, 61, 1), (68, 83, -1)):   # ojos apretados
            d.line((x0, 54 if s > 0 else 62, x1, 58, ), fill=TINTA, width=3); d.line((x0, 62 if s > 0 else 54, x1, 58), fill=TINTA, width=3)
        d.rectangle((54, 72, 76, 83), fill=PIEL); d.rectangle((56, 74, 74, 82), fill=H("#5a2028")); d.rectangle((58, 74, 72, 76), fill=H("#f4f0d0"))
    if tipo == "Critico":
        for x0, x1 in ((48, 61), (68, 83)):
            d.rectangle((x0 + 2, 56, x1 - 2, 64), fill=H("#f4f0d0")); d.rectangle((x0 + 5, 58, x1 - 4, 64), fill=TINTA)
        d.line((48, 54, 60, 50), fill=TINTA, width=3); d.line((70, 50, 83, 54), fill=TINTA, width=3)   # cejas caídas
        d.rectangle((54, 72, 76, 82), fill=PIEL); d.line((56, 80, 62, 76), fill=TINTA, width=2); d.line((62, 76, 68, 79), fill=TINTA, width=2); d.line((68, 79, 74, 76), fill=TINTA, width=2)
        a = im.load()      # palidez verdosa
        for y in range(44, 94):
            for x in range(30, 100):
                c = a[x, y]
                if c[3] and c[0] > c[2] + 30 and c[0] > 170: a[x, y] = (int(c[0] * .86), int(c[1] * .95), int(c[2] * .86), 255)
        d.polygon([(90, 44), (86, 54), (94, 54)], fill=H("#a8dcf0")); d.ellipse((85, 51, 95, 60), fill=H("#a8dcf0")); d.point((88, 53), fill=H("#ffffff"))
    r = im.crop((6, 0, 122, 118)).resize((58, 59), Image.NEAREST)
    return r
for t in ("Normal", "Parpadeo", "Herido", "Critico"): guardar(cara(t), "Pedro" + t)
