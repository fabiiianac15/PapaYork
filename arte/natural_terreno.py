"""Arte natural de PapaYork: terreno, agua, bosque, árboles, arbustos y rocas.

Dibujo propio hecho por código; no usa ninguna imagen de otro juego. De las piezas viejas de
PapaYork solo se toma la silueta (canal alfa) para que encajen igual en los mapas.
Luz única desde arriba a la izquierda; sombras hacia el frío y luces hacia el cálido.
Salida: carpeta Natural/. Uso: python3 arte/natural_terreno.py
"""
import math, os, random
from PIL import Image

B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
OUT = os.path.join(B, "Natural")


def H(s, a=255):
    return tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (a,)


def guardar(img, ruta):
    p = os.path.join(OUT, ruta)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    img.save(p)


def ruido_periodico(ancho, alto, celdas, semilla):
    """Ruido suave que se repite sin costura."""
    r = random.Random(semilla)
    g = [[r.random() for _ in range(celdas)] for _ in range(celdas)]
    s = lambda t: t * t * (3 - 2 * t)
    sal = []
    for y in range(alto):
        fy = y / alto * celdas
        y0, ty = int(fy), s(fy - int(fy))
        fila = []
        for x in range(ancho):
            fx = x / ancho * celdas
            x0, tx = int(fx), s(fx - int(fx))
            a = g[y0 % celdas][x0 % celdas] * (1 - tx) + g[y0 % celdas][(x0 + 1) % celdas] * tx
            b = g[(y0 + 1) % celdas][x0 % celdas] * (1 - tx) + g[(y0 + 1) % celdas][(x0 + 1) % celdas] * tx
            fila.append(a * (1 - ty) + b * ty)
        sal.append(fila)
    return sal


# ---------- PASTO: manchas suaves y matas de hojas, no motas al azar ----------
P_HONDO, P_BAJO, P_MEDIO, P_ALTO, P_LUZ, P_SECO = map(H, ("#47794a", "#528749", "#5a914b", "#62994c", "#79ad54", "#a3bd62"))


def pasto():
    T = 256
    n1, n2 = ruido_periodico(T, T, 5, 11), ruido_periodico(T, T, 16, 12)
    img = Image.new("RGBA", (T, T), P_MEDIO)
    px = img.load()
    for y in range(T):
        for x in range(T):
            # Transición punteada: dos tonos vecinos se mezclan en vez de formar manchas duras
            v = n1[y][x] * .6 + n2[y][x] * .4 + (((x * 7 + y * 13) % 11) / 11 - .5) * .1
            px[x, y] = P_BAJO if v < .4 else P_MEDIO if v < .62 else P_ALTO
    r = random.Random(21)
    pon = lambda x, y, c: px.__setitem__((x % T, y % T), c)

    def mata(x, y, oscura, clara):
        for k in range(r.randint(2, 4)):
            bx, alto = x + k * 2 - 2, r.randint(2, 4)
            for j in range(alto):
                pon(bx + (j // 2) * (1 if k > 1 else -1 if k == 0 else 0), y - j, clara if j >= alto - 1 else oscura)

    for _ in range(900):
        x, y = r.randrange(T), r.randrange(T)
        v = n1[y][x]
        if v < .42:
            mata(x, y, P_HONDO, P_MEDIO)
        elif v < .6:
            mata(x, y, P_BAJO, P_ALTO)
        else:
            mata(x, y, P_MEDIO, P_LUZ)
    for _ in range(16):   # parches de trébol
        x, y = r.randrange(T), r.randrange(T)
        for _ in range(9):
            a, b = x + r.randint(-5, 5), y + r.randint(-3, 3)
            pon(a, b, P_HONDO)
            pon(a, b - 1, P_ALTO)
            pon(a + 1, b - 1, P_LUZ)
    for _ in range(9):    # hierba seca, poca
        mata(r.randrange(T), r.randrange(T), P_SECO, H("#c4c978"))
    guardar(img, "Terreno/Pasto.png")


# ---------- TIERRA: camino con la misma silueta del atlas viejo ----------
TIERRA = list(map(H, ("#7d5a41", "#96704c", "#ab8358", "#bd9666", "#cfab7b")))


def textura_tierra(sem):
    n = ruido_periodico(32, 32, 4, sem)
    return [[2 for x in range(32)] for y in range(32)]


def camino():
    viejo = Image.open(os.path.join(B, "assets/Suelo-tierra2.png")).convert("RGBA")
    W, A = viejo.size
    vp = viejo.load()
    es_tierra = [[vp[x, y][3] > 0 and vp[x, y][0] > vp[x, y][1] for x in range(W)] for y in range(A)]
    nuevo = Image.new("RGBA", (W, A), (0, 0, 0, 0))
    np_ = nuevo.load()
    tex = textura_tierra(31)
    r = random.Random(32)
    for y in range(A):
        for x in range(W):
            if not es_tierra[y][x]:
                continue
            arriba = y == 0 or y % 32 == 0 and False or (y > 0 and not es_tierra[y - 1][x] and (y - 1) // 32 == y // 32)
            izq = x > 0 and not es_tierra[y][x - 1] and (x - 1) // 32 == x // 32
            abajo = y + 1 < A and not es_tierra[y + 1][x] and (y + 1) // 32 == y // 32
            der = x + 1 < W and not es_tierra[y][x + 1] and (x + 1) // 32 == x // 32
            k = tex[y % 32][x % 32]
            if arriba or izq:
                k = 0
            elif abajo or der:
                k = 4
            c = TIERRA[0] if k == 0 else TIERRA[4] if k == 4 else TIERRA[3] if (x * 5 + y * 9) % 23 else TIERRA[2]
            np_[x, y] = c
    # Piedritas con su sombra, repartidas por casilla para que no se repitan en fila
    for ty in range(A // 32):
        for tx in range(W // 32):
            for _ in range(5):
                x, y = tx * 32 + r.randint(5, 26), ty * 32 + r.randint(5, 26)
                if es_tierra[y][x] and es_tierra[y + 1][x + 1]:
                    np_[x, y] = TIERRA[4]
                    np_[x + 1, y] = TIERRA[3]
                    np_[x, y + 1] = TIERRA[0]
                    np_[x + 1, y + 1] = TIERRA[0]
    guardar(nuevo, "Terreno/Camino.png")


# ---------- TIERRA ARADA: surcos con volumen; versiones seca, regada y abonada ----------
def tierra_arada(nombre, tonos, extra=None):
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = img.load()
    r = random.Random(41)
    for y in range(32):
        for x in range(32):
            esquina = (x in (0, 31)) and (y in (0, 31))
            borde = x in (0, 31) or y in (0, 31)
            if esquina or (borde and (x * 7 + y * 13) % 5 == 0):
                continue
            # Surco ondulado: la tierra se amontona en terrones, no en barras rectas
            fase = (y + int(1.4 * math.sin(x * .55 + y // 8))) % 8
            c = tonos[3] if fase == 1 else tonos[2] if fase in (0, 2, 3, 4) else tonos[1] if fase == 5 else tonos[0] if fase == 6 else tonos[1]
            if (x * 3 + y * 5) % 11 == 0 and fase in (2, 3):
                c = tonos[3]
            if x <= 1 and fase not in (6, 7):
                c = tonos[3] if fase < 3 else c
            if x >= 30 or y >= 30:
                c = tonos[0]
            px[x, y] = c
    for _ in range(7):
        x, y = r.randint(3, 27), r.randint(3, 27)
        if px[x, y][3]:
            px[x, y] = tonos[3]
            px[x + 1, y + 1] = tonos[0]
    if extra:
        extra(px, r)
    guardar(img, "Terreno/%s.png" % nombre)


def tierras():
    seca = list(map(H, ("#574036", "#6b4c3c", "#7a5a45", "#8c6c50")))
    mojada = list(map(H, ("#352a30", "#443339", "#503d3f", "#5f4a46")))
    tierra_arada("TierraSeca", seca)

    def brillo(px, r):
        for _ in range(6):
            x, y = r.randint(3, 25), r.randrange(1, 30, 8)
            for k in range(r.randint(2, 4)):
                if px[x + k, y][3]:
                    px[x + k, y] = H("#7f7a84")

    def abono(px, r):
        for _ in range(26):
            x, y = r.randint(2, 29), r.randint(2, 29)
            if px[x, y][3]:
                px[x, y] = r.choice((H("#a8a35c"), H("#7d8a4a"), H("#d6c98a")))

    tierra_arada("TierraRegada", mojada, brillo)
    tierra_arada("TierraAbonada", seca, abono)


# ---------- EMPEDRADO: piedras que continúan entre casillas, con la silueta vieja ----------
def empedrado():
    r = random.Random(51)
    semillas = [(x, y) for x, y in ((3, 4), (13, 2), (24, 5), (8, 13), (20, 14), (29, 16), (2, 22), (13, 24), (24, 26))]
    semillas = [(x + r.randint(-1, 1), y + r.randint(-1, 1), r.choice((0, 0, 1, 2))) for x, y in semillas]
    GRIS = [list(map(H, t)) for t in (("#77726a", "#8b8579", "#9c9586", "#ada696"),
                                      ("#78705f", "#8c826e", "#9e927b", "#afa38a"),
                                      ("#6f7372", "#828784", "#92978f", "#a3a79e"))]
    JUNTA, MUSGO = H("#5a5549"), H("#5e7046")

    def celda(x, y):
        orden = sorted(((min(abs(x - a), 32 - abs(x - a)) ** 2 + min(abs(y - b), 32 - abs(y - b)) ** 2), i)
                       for i, (a, b, _) in enumerate(semillas))
        return orden[0][1], math.sqrt(orden[1][0]) - math.sqrt(orden[0][0])

    tile = Image.new("RGBA", (32, 32))
    tp = tile.load()
    for y in range(32):
        for x in range(32):
            i, gap = celda(x, y)
            if gap < 1.1:
                tp[x, y] = MUSGO if (x * 5 + y * 3) % 17 == 0 else JUNTA
                continue
            j_ab, _ = celda((x + 1) % 32, (y + 1) % 32)
            j_ar, _ = celda((x - 1) % 32, (y - 1) % 32)
            ramp = GRIS[semillas[i][2]]
            tp[x, y] = ramp[0] if j_ab != i else ramp[3] if j_ar != i else ramp[2]
            if tp[x, y] == ramp[2] and (x * 7 + y * 11) % 13 == 0:
                tp[x, y] = ramp[1]
    viejo = Image.open(os.path.join(B, "assets/Suelo-piedra2.png")).convert("RGBA")
    W, A = viejo.size
    vp = viejo.load()
    nuevo = Image.new("RGBA", (W, A), (0, 0, 0, 0))
    np_ = nuevo.load()
    for y in range(A):
        for x in range(W):
            if vp[x, y][3]:
                np_[x, y] = tp[x % 32, y % 32]
    guardar(nuevo, "Terreno/Empedrado.png")


# ---------- AGUA: profundidad, bandas de corriente y destellos; 4 cuadros ----------
def agua():
    AZ = list(map(H, ("#23607a", "#2a7288", "#338694", "#46a0a4", "#8fd0c4", "#d8f0dc")))
    prof = ruido_periodico(32, 32, 2, 61)
    for f in range(4):
        img = Image.new("RGBA", (32, 32))
        px = img.load()
        for y in range(32):
            for x in range(32):
                ola = math.sin((x + f * 8) * 2 * math.pi / 32 + y * 2 * math.pi / 16) * .5 + \
                      math.sin(x * 4 * math.pi / 32 - (y + f * 4) * 2 * math.pi / 16) * .5
                v = prof[y][x] * .8 + ola * .22
                px[x, y] = AZ[0] if v < .22 else AZ[1] if v < .46 else AZ[2] if v < .68 else AZ[3]
        r = random.Random(70)
        for i in range(5):
            x0, y0, largo = r.randrange(32), r.randrange(32), r.randint(3, 6)
            brilla = (i + f) % 4 == 0
            for k in range(largo):
                c = AZ[5] if brilla and k in (largo // 2,) else AZ[4]
                px[(x0 + k + f * 2) % 32, y0] = c
        guardar(img, "Terreno/Agua%d.png" % (f + 1))


# ---------- ORILLAS: tierra y sombra donde el agua toca el pasto ----------
def orillas():
    LODO, TIERRA_O, CLARO, SOMBRA = H("#5c4a3c"), H("#856a4c"), H("#a88d62"), H("#1d4a60", 150)
    PA = (H("#4a7d48"), H("#6ba350"))
    r = random.Random(81)
    borde = [3 + int(1.6 * math.sin(i * 2 * math.pi / 32) + 1.1 * math.sin(i * 6 * math.pi / 32)) for i in range(32)]

    def lienzo():
        return Image.new("RGBA", (32, 32), (0, 0, 0, 0))

    # Arriba: el agua está debajo de la orilla: se ve la pared de tierra y su sombra en el agua
    n = lienzo(); p = n.load()
    for x in range(32):
        h = borde[x]
        for y in range(h + 4):
            p[x, y] = TIERRA_O if y < h else LODO
        p[x, h + 4] = SOMBRA
        p[x, h + 5] = SOMBRA if x % 3 else (0, 0, 0, 0)
        if x % 2:
            p[x, 0] = PA[1]
    guardar(n, "Terreno/OrillaN.png")
    # Abajo: playa baja y clara
    s = lienzo(); p = s.load()
    for x in range(32):
        h = borde[(x + 11) % 32]
        for y in range(h + 2):
            p[x, 31 - y] = CLARO if y > 0 else TIERRA_O
        p[x, 31 - h - 2] = H("#8fd0c4")
    guardar(s, "Terreno/OrillaS.png")
    # Lados
    o = lienzo(); p = o.load()
    for y in range(32):
        h = borde[(y + 5) % 32]
        for x in range(h + 2):
            p[x, y] = TIERRA_O if x < h else LODO
        p[h + 2, y] = SOMBRA
    guardar(o, "Terreno/OrillaO.png")
    e = lienzo(); p = e.load()
    for y in range(32):
        h = borde[(y + 19) % 32]
        for x in range(h + 2):
            p[31 - x, y] = CLARO if x < h else TIERRA_O
        p[31 - h - 2, y] = H("#8fd0c4")
    guardar(e, "Terreno/OrillaE.png")


# ---------- FOLLAJE: hojas agrupadas, más claras arriba a la izquierda ----------
HOJA = list(map(H, ("#223f3a", "#2c5540", "#3a6e45", "#4f8a49", "#6ea552", "#93bf60")))


def follaje(px, W, A, cx, cy, rx, ry, r, tonos=HOJA, densidad=1.0):
    """Pinta una copa con racimos: primero la sombra, luego luces al frente."""
    n = int(rx * ry * .55 * densidad)
    grupos = []
    for _ in range(n):
        t, d = r.random() * 2 * math.pi, math.sqrt(r.random())
        grupos.append((cx + math.cos(t) * rx * d, cy + math.sin(t) * ry * d))
    grupos.sort(key=lambda g: (g[0] - g[1]))   # de abajo a la derecha hacia arriba a la izquierda no: la luz va al final
    grupos.sort(key=lambda g: -(g[0] - cx) / rx - (g[1] - cy) / ry)
    for gx, gy in grupos:
        luz = -(gx - cx) / rx * .55 - (gy - cy) / ry * .85   # -1.4 (sombra) .. 1.4 (luz)
        i = max(1, min(4, int(2.5 + luz * 1.7 + r.uniform(-.5, .5))))
        rad = r.choice((2, 2, 3))
        for dy in range(-rad, rad + 1):
            for dx in range(-rad, rad + 1):
                if dx * dx + dy * dy <= rad * rad - (0 if rad > 2 else 1):
                    x, y = int(gx) + dx, int(gy) + dy
                    if 0 <= x < W and 0 <= y < A:
                        c = tonos[i]
                        if dy == rad or dy == rad - 1 and dx > 0:
                            c = tonos[max(0, i - 1)]
                        if dy == -rad and dx <= 0 and i >= 3:
                            c = tonos[min(5, i + 1)]
                        px[x, y] = c


def contorno(img, color):
    px = img.load()
    W, A = img.size
    marcar = []
    for y in range(A):
        for x in range(W):
            if px[x, y][3] == 0 and any(0 <= x + a < W and 0 <= y + b < A and px[x + a, y + b][3] > 0
                                        for a, b in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                marcar.append((x, y))
    for x, y in marcar:
        px[x, y] = color


def tronco(px, cx, base, alto, anc, r):
    C = list(map(H, ("#382a2e", "#51383a", "#6e4f44", "#8d6b52")))
    for y in range(base - alto, base):
        ens = 1 if y > base - 4 else 0
        for x in range(cx - anc - ens, cx + anc + ens):
            f = (x - (cx - anc - ens)) / max(1, 2 * (anc + ens) - 1)
            c = C[3] if f < .2 else C[2] if f < .55 else C[1] if f < .85 else C[0]
            if (x * 3 + y * 7) % 9 == 0 and f > .2:
                c = C[1]
            px[x, y] = c
    for x in (cx - anc - 2, cx + anc + 1):      # raíces
        px[x, base - 1] = C[1]


def arbol(nombre, semilla, tonos=HOJA, frutos=None, alto_tronco=20):
    """64 x 80. La base del tronco queda en (32, 78)."""
    img = Image.new("RGBA", (64, 80), (0, 0, 0, 0))
    px = img.load()
    r = random.Random(semilla)
    tronco(px, 32, 79, alto_tronco + 18, 4, r)
    follaje(px, 64, 80, 32, 30, 25, 25, r, tonos)
    for dx, dy, a, b in ((-13, 6, 13, 12), (13, 7, 13, 12), (0, -13, 16, 12), (0, 8, 15, 13)):
        follaje(px, 64, 80, 32 + dx, 30 + dy, a, b, r, tonos, 1.4)
    for k in range(16):   # huecos de sombra bajo la copa y ramas asomando
        x, y = 22 + r.randrange(20), 46 + r.randrange(9)
        if px[x, y][3] and r.random() < .6:
            px[x, y] = tonos[0]
    if frutos:
        for _ in range(9):
            for _ in range(20):
                x, y = r.randrange(12, 52), r.randrange(10, 50)
                if px[x, y][3] and px[x + 1, y + 1][3]:
                    px[x, y], px[x + 1, y], px[x, y + 1], px[x + 1, y + 1] = frutos[1], frutos[0], frutos[0], frutos[2]
                    break
    contorno(img, H("#1f2e30"))
    guardar(img, "Plantas/%s.png" % nombre)


def tocon():
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = img.load()
    C = list(map(H, ("#3a2c2d", "#58403b", "#7a5a48", "#a98a64", "#c7a97c")))
    for y in range(19, 30):
        for x in range(9, 24):
            px[x, y] = C[2] if x < 13 else C[1] if x < 21 else C[0]
    for a, b in ((7, 29), (8, 29), (24, 29), (25, 29), (8, 28), (24, 28)):
        px[a, b] = C[1]
    for y in range(16, 22):
        for x in range(9, 24):
            d = ((x - 16) / 7.5) ** 2 + ((y - 19) / 3) ** 2
            if d <= 1:
                px[x, y] = C[3] if d > .55 else C[4] if d > .22 else C[3]
    for x in (11, 15, 19):
        px[x, 26] = C[0]
    contorno(img, H("#231a20"))
    guardar(img, "Plantas/Tocon.png")


def arbusto(nombre, sem, frutos=None):
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = img.load()
    r = random.Random(sem)
    follaje(px, 32, 32, 16, 18, 12, 9, r, HOJA, 1.5)
    follaje(px, 32, 32, 9, 20, 6, 6, r, HOJA, 1.5)
    follaje(px, 32, 32, 23, 20, 6, 6, r, HOJA, 1.5)
    if frutos:
        for _ in range(7):
            for _ in range(20):
                x, y = r.randrange(6, 26), r.randrange(10, 25)
                if px[x, y][3]:
                    px[x, y] = frutos[0]
                    px[x - 1, y] = frutos[1]
                    break
    for x in range(5, 28):
        if px[x, 27][3]:
            px[x, 27] = HOJA[0]
    contorno(img, H("#1f2e30"))
    guardar(img, "Plantas/%s.png" % nombre)


def hierba():
    """Mata alta que se corta; 30 x 30, base abajo."""
    for n, sem in ((1, 91), (2, 92), (3, 93)):
        img = Image.new("RGBA", (30, 30), (0, 0, 0, 0))
        px = img.load()
        r = random.Random(sem)
        for k in range(15):
            bx = 5 + k * 20 // 14 + r.randint(-1, 1)
            alto = r.randint(6, 13) - abs(k - 7) // 2
            incl = r.choice((-1, 0, 0, 1))
            for j in range(alto):
                x, y = bx + incl * (j // 4), 28 - j
                px[x, y] = HOJA[2] if j < 2 else HOJA[3] if j < alto - 3 else HOJA[4] if j < alto - 1 else HOJA[5]
                if k % 2:
                    px[x + 1, y] = HOJA[1] if j < alto // 2 else HOJA[2]
        contorno(img, H("#1f2e30"))
        guardar(img, "Plantas/Hierba%d.png" % n)


# ---------- ROCAS ----------
def roca(nombre, ramp, sem, grieta=None):
    img = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    px = img.load()
    r = random.Random(sem)
    for y in range(9, 29):
        for x in range(4, 28):
            d = ((x - 16) / 11.5) ** 2 + ((y - 19) / 9.5) ** 2 + .1 * math.sin(x * .9 + sem) * math.sin(y * .8)
            if d < 1:
                luz = -(x - 16) / 11.5 * .6 - (y - 19) / 9.5 * .9
                i = 3 if luz > .55 else 2 if luz > .05 else 1 if luz > -.6 else 0
                px[x, y] = ramp[i]
    for _ in range(3):   # planos de fractura, no motas
        x, y = r.randint(8, 18), r.randint(13, 21)
        for k in range(r.randint(4, 7)):
            yy = y + k // 2
            if px[x + k, yy][3]:
                px[x + k, yy] = ramp[0]
                if px[x + k, yy - 1][3]:
                    px[x + k, yy - 1] = ramp[3]
    for x, y in ((7, 26), (10, 27), (22, 27)):   # musgo en la base húmeda
        if px[x, y][3]:
            px[x, y] = H("#56683f")
            px[x + 1, y] = H("#6e8548")
    contorno(img, H("#2a2730"))
    guardar(img, "Rocas/%s.png" % nombre)


# ---------- MURO DE BOSQUE: copas densas; las mismas 9 piezas que el atlas viejo ----------
def bosque():
    img = Image.new("RGBA", (96, 96), (0, 0, 0, 0))
    r = random.Random(101)
    # Textura de copas que se repite cada 32 píxeles
    base = Image.new("RGBA", (96, 96), HOJA[1])
    bp = base.load()
    grupos = [(r.randrange(32), r.randrange(32), r.choice((5, 6, 7))) for _ in range(9)]
    for y in range(96):
        for x in range(96):
            mejor = None
            for gx, gy, rad in grupos:
                for ox in (-32, 0, 32):
                    for oy in (-32, 0, 32):
                        a, b = ((x % 32) - gx - ox) / rad, ((y % 32) - gy - oy) / rad
                        d = a * a + b * b
                        if d < 1 and (mejor is None or gy + oy > mejor[0]):
                            mejor = (gy + oy, a, b)
            if mejor:
                _, a, b = mejor
                luz = -a * .5 - b * .9
                bp[x, y] = HOJA[4] if luz > .55 else HOJA[3] if luz > .05 else HOJA[2] if luz > -.55 else HOJA[1]
            if (x * 11 + y * 7) % 23 == 0 and bp[x, y] in (HOJA[3], HOJA[4]):
                bp[x, y] = HOJA[5] if bp[x, y] == HOJA[4] else HOJA[4]
    px = img.load()

    def borde_ond(i, f=1.0):
        return 3 + 2.4 * abs(math.sin(i * math.pi / 16 * f)) + 1.3 * abs(math.sin(i * math.pi / 8 + 1))

    for ty in range(3):
        for tx in range(3):
            for y in range(32):
                for x in range(32):
                    X, Y = tx * 32 + x, ty * 32 + y
                    if tx == 0 and x < 32 - 26 + borde_ond(y) - 3:
                        continue
                    if tx == 2 and x > 26 - borde_ond(y) + 3:
                        continue
                    if ty == 0 and y < 8 + borde_ond(x) - 3:
                        continue
                    if ty == 2 and y > 18 + borde_ond(x):
                        continue
                    px[X, Y] = bp[X, Y]
            if ty == 2:   # base oscura y troncos que asoman
                for x in range(32):
                    fondo = int(18 + borde_ond(x))
                    for y in range(max(0, fondo - 3), fondo + 1):
                        X, Y = tx * 32 + x, 64 + y
                        if px[X, Y][3]:
                            px[X, Y] = HOJA[0] if y >= fondo - 1 else HOJA[1]
                    if (x + tx * 3) % 16 in (6, 7, 8):
                        for y in range(fondo + 1, 32):
                            X, Y = tx * 32 + x, 64 + y
                            if not (tx == 0 and x < 8 or tx == 2 and x > 23):
                                px[X, Y] = {6: H("#6e4f44"), 7: H("#51383a"), 8: H("#382a2e")}[(x + tx * 3) % 16]
    contorno(img, H("#1b2a2c"))
    guardar(img, "Terreno/Bosque.png")


# ---------- DETALLES SUELTOS: flores, piedritas y briznas (atlas de 128 x 128) ----------
def flor(px, x, y, petalo, centro, tallo=HOJA[2], alto=4):
    for j in range(alto):
        px[x, y + j] = tallo
    px[x - 1, y + alto - 1] = HOJA[3]
    px[x + 1, y + alto - 2] = HOJA[2]
    for a, b in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        px[x + a, y + b - 1] = petalo
    px[x, y - 1] = centro


def detalles():
    img = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    px = img.load()
    cel = lambda i: (i % 4 * 32, i // 4 * 32)
    r = random.Random(111)
    tonos = [("#e7d27a", "#a9722f"), ("#c8b4e6", "#e9d86f"), ("#f0a8a0", "#f4e27e"), ("#fff4d2", "#e9b84c")]
    for i, (a, b) in zip((1, 2, 3, 4), tonos):
        ox, oy = cel(i)
        for k in range(3 if i != 3 else 4):
            flor(px, ox + r.randint(5, 26), oy + r.randint(5, 22), H(a), H(b), alto=r.randint(3, 4))
    for i in (5, 6, 7, 8):   # piedritas
        ox, oy = cel(i)
        for k in range(2 if i in (5, 8) else 3):
            x, y = ox + r.randint(5, 24), oy + r.randint(6, 24)
            for dy in range(3):
                for dx in range(4 + k % 2):
                    if not (dy in (0, 2) and dx in (0, 3 + k % 2)):
                        px[x + dx, y + dy] = H("#a39b8b") if dy == 0 else H("#7d7a70") if dy == 1 else H("#57584f")
            px[x + 1, y] = H("#c3bba6")
    for i in (9, 10, 11, 12):   # briznas
        ox, oy = cel(i)
        for k in range({9: 4, 10: 7, 11: 3, 12: 2}[i]):
            x, y = ox + r.randint(4, 26), oy + r.randint(8, 27)
            for b in range(3):
                alt = r.randint(2, 4)
                for j in range(alt):
                    px[x + b - 1 + (b - 1) * (j // 2), y - j] = HOJA[3] if j < alt - 1 else HOJA[5]
    guardar(img, "Terreno/Detalles.png")

    # Decoraciones: 0-2 flores grandes, 3-6 hongos, 7-9 arbustos, 10-11 y 13 arbolitos, 12 tocón
    dec = Image.new("RGBA", (128, 128), (0, 0, 0, 0))
    dp = dec.load()

    def flor_g(i, pet, pet_o, cen):
        ox, oy = cel(i)
        x, y = ox + 16, oy + 13
        for j in range(11):
            dp[x, y + j] = HOJA[2] if j % 3 else HOJA[3]
        for a, b, c in ((-3, 8, HOJA[3]), (-2, 8, HOJA[3]), (-1, 9, HOJA[2]), (3, 6, HOJA[3]), (2, 6, HOJA[4]), (1, 7, HOJA[2])):
            dp[x + a, y + b] = c
        for dy in range(-4, 4):
            for dx in range(-4, 5):
                if dx * dx + dy * dy <= 13:
                    dp[x + dx, y + dy] = H(pet) if dx + dy < 1 else H(pet_o)
        dp[x, y], dp[x - 1, y], dp[x, y - 1] = H(cen), H(cen), H(cen)

    flor_g(0, "#e88fa8", "#b75c84", "#f4d76c")
    flor_g(1, "#8fa8e0", "#5b6db0", "#f4e38c")
    flor_g(2, "#f0d268", "#c28d3c", "#a65d2c")

    def hongo(i, som, som_o, punto=None):
        ox, oy = cel(i)
        x, y = ox + 16, oy + 18
        for j in range(8):
            for a in range(-2, 3):
                dp[x + a, y + j] = H("#efe2c4") if a < 1 else H("#c0ac8e")
        for dy in range(-7, 1):
            for dx in range(-7, 8):
                if (dx / 7.5) ** 2 + (dy / 7.5) ** 2 <= 1:
                    dp[x + dx, y + dy] = H(som) if dx + dy * 1.5 < 2 else H(som_o)
        if punto:
            for a, b in ((-3, -4), (2, -5), (-1, -2), (4, -2)):
                dp[x + a, y + b] = H(punto)

    hongo(3, "#c9504f", "#8e3346", "#f3e6cf")
    hongo(4, "#a84559", "#71304b", "#f3e6cf")
    hongo(5, "#5f86b5", "#3e5a88", "#cfe4e8")
    hongo(6, "#c18a58", "#8e5f43")
    arb = [Image.open(os.path.join(OUT, "Plantas/Arbusto%d.png" % n)) for n in (1, 2, 3)]
    for i, a in zip((7, 8, 9), arb):
        dec.alpha_composite(a, cel(i))
    pequeno = Image.open(os.path.join(OUT, "Plantas/Arbol1.png")).crop((0, 0, 64, 80)).resize((32, 32), Image.NEAREST)
    fruta = Image.open(os.path.join(OUT, "Plantas/Arbol3.png")).crop((0, 0, 64, 80)).resize((32, 32), Image.NEAREST)
    dec.alpha_composite(pequeno, cel(10))
    dec.alpha_composite(pequeno, cel(11))
    dec.alpha_composite(Image.open(os.path.join(OUT, "Plantas/Tocon.png")), cel(12))
    dec.alpha_composite(fruta, cel(13))
    contorno(dec, H("#1f2e30"))
    guardar(dec, "Terreno/Decoraciones.png")



# ---------- MADERA: cercas y cajas viejas con los tonos del mundo; muelle de tablones ----------
def retocar_madera():
    RAMPA = list(map(H, ("#3f2d2c", "#5b4136", "#7a5a45", "#987857", "#b89a72", "#d0b78e")))
    for ruta, sal in [("Casas/Vaya.png", "Madera/VayaAtlas.png"), ("Decoracion/Silla.png", "Madera/Caja.png")] + \
            [(f"Decoracion/Vaya{i}.png", f"Madera/Vaya{i}.png") for i in range(1, 8)]:
        im = Image.open(os.path.join(B, ruta)).convert("RGBA")
        px = im.load()
        for y in range(im.height):
            for x in range(im.width):
                r_, g_, b_, a_ = px[x, y]
                if a_:
                    lum = (r_ * .3 + g_ * .59 + b_ * .11) / 255
                    px[x, y] = RAMPA[min(5, int(lum * 7.2))]
        guardar(im, sal)
    T = list(map(H, ("#4a3430", "#6b4c3c", "#8a6a4e", "#a68662", "#bda07a")))
    for nombre, sem in (("Muelle", 121), ("Muelle1", 122)):
        im = Image.new("RGBA", (32, 32))
        px = im.load()
        r = random.Random(sem)
        for ty in range(0, 32, 8):
            tono = r.choice((2, 2, 3))
            junta = r.randrange(6, 26)
            for y in range(ty, ty + 8):
                for x in range(32):
                    k = 0 if y == ty + 7 else 1 if y == ty + 6 else tono + 1 if y == ty else tono
                    if x == junta:
                        k = 0
                    if (x * 5 + y * 3 + ty) % 19 == 0 and k >= 2:
                        k -= 1
                    px[x, y] = T[k]
            for x in (junta - 2, junta + 2):   # clavos
                px[x % 32, ty + 2] = T[0]
                px[x % 32, ty + 4] = T[0]
        guardar(im, f"Madera/{nombre}.png")

if __name__ == "__main__":
    pasto(); camino(); tierras(); empedrado(); agua(); orillas()
    roble2 = list(map(H, ("#233f35", "#2f5a3a", "#44733f", "#5f8e43", "#83aa4b", "#a9c560")))
    arbol("Arbol1", 201)
    arbol("Arbol2", 202, roble2)
    arbol("Arbol3", 203, frutos=(H("#c84a4a"), H("#ef9a7a"), H("#7c2c3e")))
    tocon()
    arbusto("Arbusto1", 301)
    arbusto("Arbusto2", 302, (H("#c84a4a"), H("#7c2c3e")))
    arbusto("Arbusto3", 303, (H("#f0d268"), H("#c28d3c")))
    hierba()
    roca("Roca1", list(map(H, ("#55555e", "#74747a", "#96958f", "#bab6a6"))), 401)
    roca("Roca2", list(map(H, ("#2d2a38", "#433e4d", "#5e5763", "#7d7680"))), 402)
    bosque(); detalles(); retocar_madera()
    print("ok")
