"""Interfaz propia de PapaYork: madera de roble con lino cosido y detalles radiactivos.
También dibuja los peces, la caña, los corazones y el minijuego de pesca. Dibujo original por código.
Uso: python3 arte/natural_ui.py"""
import math, os, random
from PIL import Image
A = os.path.dirname(os.path.abspath(__file__)); N = os.path.join(A, "..", "Natural")
H = lambda s, a=255: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (a,)
ROBLE = list(map(H, ("#2f1f22", "#4a3029", "#6a4634", "#8a6244", "#ab8259")))
LINO = list(map(H, ("#b89a72", "#d4bb90", "#e7d3ab", "#f2e4c4")))
HUECO = list(map(H, ("#5a4338", "#6e5444", "#826550")))
VERDE = list(map(H, ("#3c7a3a", "#7cc644", "#c9f06a", "#f0ffc0")))
def guardar(im, ruta):
    p = os.path.join(N, ruta); os.makedirs(os.path.dirname(p), exist_ok=True); im.save(p)
def lienzo(w, h): return Image.new("RGBA", (w, h), (0, 0, 0, 0))
def caja(px, x, y, w, h, c):
    for j in range(y, y + h):
        for i in range(x, x + w): px[i, j] = c
def madera(px, x, y, w, h, sem=1, sobrio=False):
    r = random.Random(sem)
    for j in range(y, y + h):
        for i in range(x, x + w):
            v = math.sin((j + 2.5 * math.sin(i * .06 + sem)) * .9)
            px[i, j] = ROBLE[3] if v > .75 else ROBLE[2] if v > -.6 else ROBLE[1]
    for _ in range((w * h) // 260):                         # nudos y vetas cortas
        i, j = r.randrange(x, x + w), r.randrange(y, y + h)
        for k in range(r.randint(3, 8)):
            if x <= i + k < x + w: px[i + k, j] = ROBLE[1]
def marco(px, w, h, grosor=10):
    """Marco de roble con esquinas redondeadas, luz arriba a la izquierda y remaches de hierro."""
    madera(px, 0, 0, w, h, 3)
    for i in range(w):
        px[i, 0] = ROBLE[0]; px[i, 1] = ROBLE[4]; px[i, h - 1] = ROBLE[0]; px[i, h - 2] = ROBLE[1]
    for j in range(h):
        px[0, j] = ROBLE[0]; px[1, j] = ROBLE[4]; px[w - 1, j] = ROBLE[0]; px[w - 2, j] = ROBLE[1]
    for a, b in ((0, 0), (1, 0), (0, 1), (w - 1, 0), (w - 2, 0), (w - 1, 1), (0, h - 1), (1, h - 1), (0, h - 2), (w - 1, h - 1), (w - 2, h - 1), (w - 1, h - 2)):
        px[a, b] = (0, 0, 0, 0)
    for a, b in ((5, 5), (w - 6, 5), (5, h - 6), (w - 6, h - 6)):    # remaches
        for dx, dy, c in ((0, 0, "#8d97a0"), (1, 0, "#5c6470"), (0, 1, "#5c6470"), (1, 1, "#3c424e"), (-1, 0, "#c9d2d8"), (0, -1, "#c9d2d8")):
            px[a + dx, b + dy] = H(c)
def lino(px, x, y, w, h):
    """Tela de lino: trama fina y costura alrededor."""
    for j in range(y, y + h):
        for i in range(x, x + w):
            t = (i + j * 2) % 7 == 0 or (i * 2 - j) % 11 == 0
            px[i, j] = LINO[1] if t else LINO[2]
    for i in range(x, x + w):
        px[i, y] = ROBLE[1]; px[i, y + 1] = LINO[0]; px[i, y + h - 1] = LINO[3]
    for j in range(y, y + h):
        px[x, j] = ROBLE[1]; px[x + 1, j] = LINO[0]; px[x + w - 1, j] = LINO[3]
    for i in range(x + 5, x + w - 5, 6):                     # puntada
        for k in range(3):
            px[i + k, y + 4] = H("#9a7a55"); px[i + k, y + h - 5] = H("#9a7a55")
    for j in range(y + 5, y + h - 5, 6):
        for k in range(3):
            px[x + 4, j + k] = H("#9a7a55"); px[x + w - 5, j + k] = H("#9a7a55")
def emblema(px, cx, cy):
    """Papa con brote radiactivo: el sello de PapaYork."""
    for j in range(-5, 6):
        for i in range(-6, 7):
            if (i / 6.5) ** 2 + (j / 5.5) ** 2 < 1:
                px[cx + i, cy + j] = H("#e0b98a") if i + j < -3 else H("#c49565") if i + j < 4 else H("#99704e")
    for a, b in ((-2, -1), (2, 1), (-1, 3)): px[cx + a, cy + b] = H("#6e4d3e")
    for k, c in ((-6, VERDE[0]), (-7, VERDE[1]), (-8, VERDE[2])): px[cx, cy + k] = c
    px[cx + 1, cy - 8] = VERDE[1]; px[cx - 1, cy - 7] = VERDE[1]
def panel(w, h, nombre, separa=None):
    im = lienzo(w, h); px = im.load()
    marco(px, w, h); lino(px, 10, 10, w - 20, h - 20)
    if separa:
        for i in range(14, w - 14):
            px[i, separa] = H("#9a7a55") if i % 4 < 2 else LINO[2]; px[i, separa + 1] = LINO[3]
    emblema(px, w // 2, h - 7)
    guardar(im, f"UI/{nombre}.png")
panel(380, 200, "PanelMochila", 145); panel(380, 200, "PanelPausa"); panel(380, 246, "PanelTienda", 112)
# Casillas: hueco oscuro de madera; la elegida brilla en verde radiactivo
def casilla(nombre, borde, brillo, fondo=HUECO):
    im = lienzo(34, 34); px = im.load()
    for j in range(34):
        for i in range(34):
            if (i in (0, 33)) and (j in (0, 33)): continue
            b = i in (0, 33) or j in (0, 33)
            px[i, j] = borde[1] if b else fondo[1]
    for i in range(1, 33):
        px[i, 1] = fondo[0]; px[1, i] = fondo[0]; px[i, 32] = fondo[2]; px[32, i] = fondo[2]
    for j in range(4, 30, 5):
        for i in range(3 + j % 3, 31, 7): px[i, j] = fondo[2]
    if brillo:
        for i in range(1, 33):
            for a, b in ((i, 1), (1, i), (i, 32), (32, i)): px[a, b] = brillo[1]
        for a, b in ((1, 1), (32, 1), (1, 32), (32, 32), (2, 2), (31, 2), (2, 31), (31, 31)): px[a, b] = brillo[2]
    guardar(im, f"UI/{nombre}.png")
casilla("Casilla", ROBLE, None); casilla("CasillaHover", (ROBLE[0], H("#c9a06a")), None, [H("#6e5444"), H("#826550"), H("#9a7a5e")]); casilla("CasillaSeleccionada", ROBLE, VERDE)
# Barra rápida
im = lienzo(352, 42); px = im.load(); marco(px, 352, 42); guardar(im, "UI/BarraRapida.png")
# Etiqueta del nombre del objeto
vieja = Image.open(os.path.join(A, "..", "Inventario/EtiquetaItem.png")); im = lienzo(*vieja.size); px = im.load()
W, Al = vieja.size; caja(px, 1, 1, W - 2, Al - 2, LINO[2])
for i in range(W): px[i, 0] = ROBLE[1]; px[i, Al - 1] = ROBLE[1]
for j in range(Al): px[0, j] = ROBLE[1]; px[W - 1, j] = ROBLE[1]
guardar(im, "UI/EtiquetaItem.png")
# Pestañas con ícono
def pestana(nombre, dibujo):
    for activa in (False, True):
        im = lienzo(28, 24); px = im.load()
        madera(px, 0, 0, 28, 24, 5)
        fondo = LINO[2] if activa else ROBLE[2]
        for j in range(3, 24):
            for i in range(3, 25): px[i, j] = fondo
        for i in range(28): px[i, 0] = ROBLE[0]; px[i, 1] = ROBLE[4]
        for j in range(24): px[0, j] = ROBLE[0]; px[27, j] = ROBLE[0]; px[1, j] = ROBLE[4] if activa else ROBLE[3]
        px[0, 0] = px[27, 0] = (0, 0, 0, 0)
        if activa:
            for i in range(3, 25): px[i, 3] = VERDE[1]
        dibujo(px, activa)
        guardar(im, f"UI/Pestana{nombre}{'Activa' if activa else ''}.png")
def d_mochila(px, ac):
    c, o, l = H("#8a6244"), H("#4a3029"), H("#c9a06a")
    caja(px, 8, 10, 12, 10, c); caja(px, 10, 7, 8, 3, c)
    for i in range(8, 20): px[i, 20] = o; px[i, 9] = l
    caja(px, 11, 13, 6, 4, l); px[13, 15] = px[14, 15] = o
def d_corazon(px, ac): corazon_en(px, 14, 15, H("#d84f5f"), H("#f08a8a"), H("#8e2f45"))
def corazon_en(px, cx, cy, c, l, o, e=1):
    for j in range(-5, 6):
        for i in range(-6, 7):
            x, y = i / 6, -j / 5 + .15
            if (x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0:
                px[cx + i, cy + j] = l if i + j < -4 else o if i + j > 4 else c
def d_engranaje(px, ac):
    for j in range(-7, 8):
        for i in range(-7, 8):
            d = math.hypot(i, j); a = math.atan2(j, i)
            if 2.6 < d < 4.7 + (2.2 if math.cos(a * 8) > .2 else 0): px[14 + i, 14 + j] = H("#c3ccd2") if i + j < 0 else H("#7d8a96")
def d_puerta(px, ac):
    caja(px, 9, 7, 10, 14, H("#6a4634"))
    for j in range(7, 21): px[9, j] = H("#ab8259"); px[18, j] = H("#2f1f22"); px[13, j] = H("#4a3029")
    for i in range(9, 19): px[i, 7] = H("#ab8259")
    px[16, 14] = px[16, 15] = H("#e8c76f")
for n, f in (("Mochila", d_mochila), ("Vecinos", d_corazon), ("Opciones", d_engranaje), ("Salir", d_puerta)): pestana(n, f)
# Corazones de amistad
for n, cols in (("Lleno", ("#d84f5f", "#f08a8a", "#8e2f45")), ("Vacio", ("#b39a78", "#c9b28f", "#957d60"))):
    im = lienzo(15, 13); corazon_en(im.load(), 7, 6, *map(H, cols)); guardar(im, f"UI/Corazon{n}.png")
# Corazón que sube al hablar o regalar
# Minijuego de pesca: pista de agua de 200 de alto
im = lienzo(62, 222); px = im.load(); marco(px, 62, 222)
for j in range(11, 211):
    for i in range(10, 40):
        v = j / 222 + .05 * math.sin(j * .3 + i * .4)
        px[i, j] = H("#46a0a4") if v < .35 else H("#338694") if v < .7 else H("#2a7288")
for j in range(11, 211):
    for i in range(46, 54): px[i, j] = H("#2f1f22")
emblema(px, 50, 215 - 11) if False else None
guardar(im, "Pesca/Pista.png")
im = lienzo(30, 50); px = im.load()
for j in range(50):
    for i in range(30):
        b = j in (0, 49) or i in (0, 29)
        px[i, j] = H("#e7ff9c", 255) if b else H("#a8ec4a", 120)
guardar(im, "Pesca/Barra.png")
im = lienzo(8, 200); px = im.load(); caja(px, 0, 0, 8, 200, H("#ffffff")); guardar(im, "Pesca/Medidor.png")
im = lienzo(2, 2); caja(im.load(), 0, 0, 2, 2, H("#f7f7ee", 230)); guardar(im, "Pesca/Linea.png")
for f in range(2):       # Boya roja y blanca sobre una onda
    im = lienzo(14, 14); px = im.load(); o = f
    for i in range(-5, 6):
        if abs(i) > 1 + f: px[7 + i, 11] = H("#d8f0dc")
    for j in range(4):
        for i in range(-2, 3):
            if not (abs(i) == 2 and j in (0, 3)): px[7 + i, 4 + j + o] = H("#d84f5f") if j < 2 else H("#fbf5ea")
    px[6, 4 + o] = H("#f08a8a"); px[7, 3 + o] = H("#2f1f22"); px[7, 2 + o] = H("#2f1f22")
    guardar(im, f"Pesca/Boya{f + 1}.png")
im = lienzo(14, 22); px = im.load()             # Signo de que picó
caja(px, 4, 1, 6, 13, H("#2f1f22")); caja(px, 5, 2, 4, 11, H("#f4d36a")); caja(px, 4, 16, 6, 5, H("#2f1f22")); caja(px, 5, 17, 4, 3, H("#f4d36a"))
guardar(im, "Pesca/Aviso.png")
# Icono de la caña
im = lienzo(32, 32); px = im.load()
for k in range(24):
    x, y = 4 + k, 28 - k
    px[x, y] = H("#6f4b35") if k < 8 else H("#b58a55") if k < 17 else H("#e3c478"); px[x, y + 1] = H("#3f2d2c")
for j in range(5, 21): px[28, j] = H("#f7f7ee")
caja(px, 27, 21, 3, 4, H("#d84f5f")); caja(px, 8, 20, 4, 4, H("#a9bcc8")); px[8, 20] = H("#e6edf0")
guardar(im, "Pesca/Cana.png")
# ---------- Peces originales de PapaYork ----------
def pez(nombre, cuerpo, largo, alto, panza, lomo, aleta, ojo="#1a1320", extra=None, cola=5):
    im = lienzo(32, 32); px = im.load(); cx, cy = 15, 16
    for j in range(-alto - 3, alto + 4):
        for i in range(-largo - cola - 2, largo + 3):
            x, y = i / largo, j / alto
            if x * x + y * y < 1:
                c = lomo if j < -alto * .25 else panza if j > alto * .4 else cuerpo
                if (i + j * 2) % 5 == 0 and abs(j) < alto * .6: c = lomo
                px[cx + i, cy + j] = H(c)
    for k in range(cola + 1):                              # cola
        for j in range(-k - 1, k + 2):
            px[cx + largo + k - 1, cy + j] = H(aleta if abs(j) > k * .3 else cuerpo)
    for k in range(-largo // 2, largo // 2):               # aletas
        px[cx + k, cy - alto - 1 - (1 if (k % 3 == 0) else 0)] = H(aleta)
    px[cx - 1, cy + alto] = H(aleta); px[cx, cy + alto + 1] = H(aleta); px[cx + 1, cy + alto] = H(aleta)
    ox = cx - int(largo * .6); px[ox, cy - 1] = H("#fbf5ea"); px[ox + 1, cy - 1] = H(ojo); px[ox + 1, cy - 2] = H("#fbf5ea")
    if extra: extra(px, cx, cy)
    # contorno oscuro
    M = []; 
    for j in range(32):
        for i in range(32):
            if px[i, j][3] == 0 and any(0 <= i + a < 32 and 0 <= j + b < 32 and px[i + a, j + b][3] for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))): M.append((i, j))
    for i, j in M: px[i, j] = H("#2a1d2b")
    guardar(im, f"Peces/{nombre}.png")
def grietas(px, cx, cy):
    for a, b in ((-3, -1), (-2, 0), (-1, 0), (0, 1), (2, 1), (3, 0)): px[cx + a, cy + b] = VERDE[1]
    px[cx - 1, cy] = VERDE[3]
def manchas(c):
    return lambda px, cx, cy: [px.__setitem__((cx + a, cy + b), H(c)) for a, b in ((-2, -2), (1, -1), (3, -3), (0, 2), (4, 1))]
pez("Carpita", "#d9894a", 8, 5, "#f2cf96", "#b6622f", "#c1503c")
pez("PezPapa", "#c49565", 7, 6, "#e0b98a", "#99704e", "#7d5a41", extra=manchas("#6e4d3e"), cola=3)
pez("Bagre", "#6f6a60", 10, 4, "#b8b09c", "#4f4a45", "#3f3b38", extra=lambda px, cx, cy: [px.__setitem__((cx - 11 - k, cy + 1 + k), H("#2a1d2b")) for k in range(3)])
pez("Trucha", "#a9bcc8", 10, 4, "#e6edf0", "#6f8c9a", "#7c8fa2", extra=manchas("#d84f5f"))
pez("Anguila", "#5f7a4f", 13, 2, "#a9b878", "#3f5a3a", "#2c4030", cola=2)
pez("Mojarra", "#7cc644", 7, 5, "#c9f06a", "#3c7a3a", "#a8ec4a", extra=grietas)
pez("Lucio", "#4f7a68", 12, 4, "#b0c8a8", "#2f5548", "#d84f5f", extra=grietas)
pez("ReyTuberculo", "#a87a4e", 11, 8, "#d9b888", "#6e4d3e", "#a8ec4a", ojo="#a8ec4a", extra=lambda px, cx, cy: (grietas(px, cx, cy), [px.__setitem__((cx - 5 + k * 3, cy - 10 - (k % 2)), H("#f4d36a")) for k in range(4)]), cola=4)
print("ok")
