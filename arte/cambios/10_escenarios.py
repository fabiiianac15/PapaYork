"""Rediseno de escenarios: granja y bosque nuevos (mas grandes y con sentido), pueblo con mas vecinos.

Los mapas se arman con una cuadricula de 32px y funciones (bloques de bosque, caminos, estanque, rio...), y de ahi
salen: los mapas de teselas (bosque de borde con 9 piezas, caminos de tierra con esquinas y extremos, plazas de piedra,
flores y hierbitas), las colisiones (rectangulos unidos) y todos los objetos.

Granja (48x32 casillas): casa, mesa de trabajo, granero, buzon, campo cercado con hierbajos y piedras para limpiar,
estanque, jardin con la estatua de HetolMimiao, zona contaminada (charcos que hacen dano y barriles) y salida al bosque.
Bosque (56x40): rio con puente hacia el pueblo, cantera con vetas, cabana en ruinas, claro de hongos y la cueva
bloqueada con una papa gigante.
Pueblo: el alcalde Ramiro, Lupita, el abuelo Tomas y un tablon de anuncios.
Tambien: interactuar (clic) con estatua, carteles, buzon..., dormir en la casa (pasa la noche y guarda la partida),
papa brillante y papa gigante, hongos silvestres para recolectar.
"""
import json, sys, os, random
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
T = 32
def cmp(a, op, b): return C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def ext(n): return next(e for e in d["externalEvents"] if e["name"] == n)
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])

# =====================================================================================
# Mapa en cuadricula
# =====================================================================================
class Mapa:
    def __init__(s, w, h, semilla):
        s.w, s.h = w, h
        s.g = [["." for _ in range(w)] for _ in range(h)]
        s.ocupado = set()       # casillas con algo encima (no poner mas cosas)
        s.inst = []
        s.colisiones = []       # rectangulos extra (bases de edificios) en pixeles
        s.r = random.Random(semilla)
    def rect(s, x0, y0, x1, y1, ch):
        for y in range(max(0, y0), min(s.h, y1 + 1)):
            for x in range(max(0, x0), min(s.w, x1 + 1)): s.g[y][x] = ch
    def get(s, x, y): return s.g[y][x] if 0 <= x < s.w and 0 <= y < s.h else "T"
    def borde(s, grosor=2, irregular=True):
        for y in range(s.h):
            for x in range(s.w):
                if x < grosor or y < grosor or x >= s.w - grosor or y >= s.h - grosor: s.g[y][x] = "T"
        if irregular:
            for x in range(s.w):
                for (y, dy) in ((grosor, 1), (s.h - grosor - 1, -1)):
                    if s.r.random() < 0.45: s.g[y][x] = "T"
            for y in range(s.h):
                for (x, dx) in ((grosor, 1), (s.w - grosor - 1, -1)):
                    if s.r.random() < 0.45: s.g[y][x] = "T"
    def camino(s, puntos):
        for (x0, y0), (x1, y1) in zip(puntos, puntos[1:]):
            for x in range(min(x0, x1), max(x0, x1) + 1): s.g[y0][x] = "="
            for y in range(min(y0, y1), max(y0, y1) + 1): s.g[y][x1] = "="
    def libre(s, x, y, w=1, h=1, margen=0):
        for yy in range(y - margen, y + h + margen):
            for xx in range(x - margen, x + w + margen):
                if s.get(xx, yy) != "." or (xx, yy) in s.ocupado: return False
        return True
    def ocupar(s, x, y, w=1, h=1):
        for yy in range(y, y + h):
            for xx in range(x, x + w): s.ocupado.add((xx, yy))
    def poner(s, nombre, px, py, z=None, anim=None, variables=(), w=None, h=None, capa=""):
        i = inst(nombre, px, py, capa, py if z is None else z, w, h, variables=list(variables))
        if anim is not None: i["numberProperties"] = [{"name": "animation", "value": anim}]
        s.inst.append(i); return i
    def esparcir(s, n, zona, fn, margen=1, intentos=4000):
        x0, y0, x1, y1 = zona; hechos = 0
        while hechos < n and intentos > 0:
            intentos -= 1
            x, y = s.r.randint(x0, x1), s.r.randint(y0, y1)
            if s.libre(x, y, margen=margen):
                fn(x, y); s.ocupar(x, y); hechos += 1

def tilemap(nombre, mapa, celdas, z, capa=""):
    """celdas: dict (x,y) -> indice de tesela. Crea una instancia de mapa de teselas del tamano del mapa."""
    tiles = [[celdas.get((x, y), -1) for x in range(mapa.w)] for y in range(mapa.h)]
    i = inst(nombre, 0, 0, capa, z)
    i["stringProperties"] = [{"name": "tilemap", "value": json.dumps({"tileWidth": T, "tileHeight": T, "dimX": mapa.w, "dimY": mapa.h,
                                                                      "layers": [{"id": 0, "alpha": 1, "tiles": tiles}]}, separators=(",", ":"))}]
    return i

def autotile_bosque(m):
    c = {}
    for y in range(m.h):
        for x in range(m.w):
            if m.g[y][x] != "T": continue
            n, s_, w, e = m.get(x, y - 1) == "T", m.get(x, y + 1) == "T", m.get(x - 1, y) == "T", m.get(x + 1, y) == "T"
            fila = 0 if not n else (2 if not s_ else 1)
            col = 0 if not w else (2 if not e else 1)
            c[(x, y)] = fila * 3 + col
    return c
def autotile_camino(m):
    """Teselas de Suelo-tierra: 1 TB, 4 LR, 0/2/8/10 esquinas, 6/7/9/11 extremos, 3 suelto."""
    c = {}
    for y in range(m.h):
        for x in range(m.w):
            if m.g[y][x] != "=": continue
            n, s_, w, e = m.get(x, y - 1) == "=", m.get(x, y + 1) == "=", m.get(x - 1, y) == "=", m.get(x + 1, y) == "="
            k = (n, s_, w, e)
            tabla = {(True, True, False, False): 4, (False, False, True, True): 1, (False, True, False, True): 0, (False, True, True, False): 2,
                     (True, False, False, True): 8, (True, False, True, False): 10, (False, True, False, False): 6, (True, False, False, False): 7,
                     (False, False, False, True): 11, (False, False, True, False): 9, (False, False, False, False): 3}
            c[(x, y)] = tabla.get(k, 4 if (n or s_) else 1)
    return c
def colisiones(m, chars="T~", saltar=()):
    """Une las casillas solidas en rectangulos y devuelve instancias de Colision."""
    solido = [[m.g[y][x] in chars and (x, y) not in saltar for x in range(m.w)] for y in range(m.h)]
    usados = [[False] * m.w for _ in range(m.h)]; out = []
    for y in range(m.h):
        for x in range(m.w):
            if not solido[y][x] or usados[y][x]: continue
            x1 = x
            while x1 + 1 < m.w and solido[y][x1 + 1] and not usados[y][x1 + 1]: x1 += 1
            y1 = y
            while y1 + 1 < m.h and all(solido[y1 + 1][k] and not usados[y1 + 1][k] for k in range(x, x1 + 1)): y1 += 1
            for yy in range(y, y1 + 1):
                for xx in range(x, x1 + 1): usados[yy][xx] = True
            out.append(inst("Colision", x * T, y * T, "", 0, (x1 - x + 1) * T, (y1 - y + 1) * T))
    for (px, py, pw, ph) in m.colisiones: out.append(inst("Colision", px, py, "", 0, pw, ph))
    return out

# helpers de objetos
ARBOLES = ["Arbol", "Arbol", "Arbol_2", "Arbol_3", "Arbol_4"]
def arbol(m, x, y):
    n = m.r.choice(ARBOLES)
    if n == "Arbol_4": m.poner(n, x * T, y * T)
    else: m.poner(n, x * T + 16, y * T + 32)
def arbusto(m, x, y): m.poner("Arbusto", x * T + 15, y * T + 26, anim=m.r.randint(0, 2))
def roca(m, x, y): m.poner(m.r.choice(["Roca_1", "Roca_2"]), x * T + 16, y * T + 25)
def hierba(m, x, y): m.poner("Hierba", x * T + 1, y * T + 2, anim=m.r.randint(0, 2))
def veta(m, x, y, tipo): m.poner("Veta", x * T, y * T, anim=tipo); m.ocupar(x, y)
def papa(m, x, y, tipo="Normal"):
    m.poner("Papa", x * T + 16, y * T + 26, variables=[var("Tipo", "string", tipo)])
def interactivo(m, anim_nombre, px, py, dialogo, solido=True, w_base=None):
    m.poner("Interactivo", px, py, anim=INTER.index(anim_nombre), variables=[var("Dialogo", "string", dialogo), var("Solido", "boolean", solido)])
def decorado(m, anim_nombre, px, py): m.poner("Decorado", px, py, anim=DECO.index(anim_nombre))
def teleport(m, px, py, w, h, destino, ax, ay):
    m.poner("Teletransportador", px, py, 0, w=w, h=h, variables=[var("Direccion", "string", destino), var("PosicionX", "number", ax), var("PosicionY", "number", ay)])
def deco_flores(m, celdas, n, zona, margen=0):
    def f(x, y): celdas[(x, y)] = m.r.choice([0, 1, 2, 0, 1, 2, 3])
    x0, y0, x1, y1 = zona; k = 0
    for _ in range(n * 6):
        x, y = m.r.randint(x0, x1), m.r.randint(y0, y1)
        if m.get(x, y) == "." and (x, y) not in m.ocupado and (x, y) not in celdas: f(x, y); k += 1
        if k >= n: break

INTER = ["Estatua", "Buzon", "Cartel", "Tablon", "Cueva", "CabanaRuina", "Puerta"]
DECO = ["Granero", "Barril1", "Barril2", "Charco"]

# =====================================================================================
# GRANJA (48 x 32)
# =====================================================================================
g = Mapa(48, 32, 7)
g.borde(2)
g.rect(22, 0, 26, 3, ".")                                   # salida al bosque
g.rect(0, 0, 47, 0, "T"); g.rect(22, 0, 26, 0, ".")
g.camino([(21, 7), (21, 9), (24, 9), (24, 0)])              # puerta de la casa -> bosque
g.camino([(10, 12), (17, 12)])                              # entrada del campo
# casa (Casa1 128x128, origen 58,101): ocupa casillas 19..22 x 3..6
CASA = (19, 3)
g.poner("Casa1", CASA[0] * T + 58, CASA[1] * T + 101); g.ocupar(19, 3, 4, 4)
g.colisiones.append((CASA[0] * T + 12, CASA[1] * T + 56, 98, 44))
interactivo(g, "Puerta", 20 * T + 16, 6 * T + 8, "Dormir", solido=False)
g.poner("MesaTrabajo", 23 * T + 8, 6 * T + 4); g.ocupar(23, 6, 2, 1)
g.poner("AvisoMesa", 23 * T - 6, 5 * T + 20, 100000)
decorado(g, "Granero", 28 * T, 3 * T); g.ocupar(28, 3, 4, 4); g.colisiones.append((28 * T + 8, 3 * T + 60, 114, 50))
interactivo(g, "Buzon", 18 * T + 6, 7 * T + 2, "Buzon"); g.ocupar(18, 7, 1, 1)
interactivo(g, "Cartel", 26 * T, 2 * T + 6, "CartelBosque"); g.ocupar(26, 2)
interactivo(g, "Cartel", 25 * T, 9 * T + 8, "CartelGranja"); g.ocupar(25, 9)
# campo cercado (Vayas 9 piezas) 4..17 x 13..25 con portillo arriba en 10..11
VALLA = {}
for x in range(4, 18):
    for y in (13, 25):
        if y == 13 and x in (10, 11): continue
        VALLA[(x, y)] = (0 if x == 4 else 2 if x == 17 else 1) + (0 if y == 13 else 6)
for y in range(14, 25):
    VALLA[(4, y)] = 3; VALLA[(17, y)] = 5
for (x, y) in VALLA: g.g[y][x] = "v"
g.esparcir(14, (5, 14, 16, 24), lambda x, y: hierba(g, x, y), margen=0)
g.esparcir(6, (5, 14, 16, 24), lambda x, y: roca(g, x, y), margen=0)
# estanque
for y in range(18, 25):
    for x in range(33, 41):
        if (x in (33, 40) and y in (18, 24)): continue
        g.g[y][x] = "~"
g.rect(36, 25, 37, 25, "~")
# jardin de la estatua de HetolMimiao
g.rect(38, 6, 43, 10, "#")
interactivo(g, "Estatua", 40 * T + 7, 6 * T - 10, "Estatua"); g.ocupar(40, 5, 2, 3)
# zona contaminada (suroeste)
for (x, y) in [(4, 27), (8, 28), (12, 27), (6, 29)]: decorado(g, "Charco", x * T, y * T + 8); g.ocupar(x, y)
for (x, y, b) in [(3, 28, "Barril1"), (10, 29, "Barril2"), (14, 28, "Barril1"), (7, 27, "Barril2")]:
    decorado(g, b, x * T + 4, y * T + 2); g.ocupar(x, y); g.colisiones.append((x * T + 6, y * T + 18, 20, 12))
interactivo(g, "Cartel", 16 * T, 27 * T, "CartelZona"); g.ocupar(16, 27)
papa(g, 9, 28); papa(g, 25, 26, "Brillante"); papa(g, 42, 14)
# herramientas y semillas para empezar (junto a la casa)
g.poner("Herramientas", 16 * T, 8 * T, 0, anim=0); g.ocupar(16, 8)          # azadon
g.poner("Herramientas", 15 * T, 10 * T, 0, anim=2); g.ocupar(15, 10)        # hacha
g.poner("Herramientas", 27 * T, 11 * T, 0, anim=1); g.ocupar(27, 11)        # pico
g.poner("Caja_de_Semillas", 18 * T, 11 * T, 0, anim=1, variables=[var("Cantidad", "number", 6)]); g.ocupar(18, 11)
# arboles, arbustos, rocas y hierba alrededor
g.esparcir(12, (3, 3, 15, 11), lambda x, y: arbol(g, x, y), margen=1)
g.esparcir(14, (41, 11, 45, 28), lambda x, y: arbol(g, x, y), margen=1)
g.esparcir(6, (26, 13, 31, 29), lambda x, y: arbol(g, x, y), margen=1)
g.esparcir(8, (3, 3, 45, 29), lambda x, y: arbusto(g, x, y), margen=1)
g.esparcir(8, (19, 13, 45, 29), lambda x, y: roca(g, x, y), margen=1)
g.esparcir(16, (3, 3, 45, 29), lambda x, y: hierba(g, x, y), margen=0)
FLORES_G = {}
deco_flores(g, FLORES_G, 30, (36, 4, 45, 12)); deco_flores(g, FLORES_G, 25, (3, 3, 45, 29))
HIERBITAS_G = {}
for _ in range(220):
    x, y = g.r.randint(2, 45), g.r.randint(2, 29)
    if g.get(x, y) == "." and (x, y) not in g.ocupado and (x, y) not in FLORES_G: HIERBITAS_G[(x, y)] = g.r.choice([9, 10, 11, 12, 1, 4])
SPAWN_GRANJA = (21 * T + 16, 8 * T + 28)
BOSQUE_DESDE_GRANJA = (27 * T + 16, 36 * T + 28)
GRANJA_DESDE_BOSQUE = (24 * T + 16, 3 * T + 28)
teleport(g, 22 * T, 0, 5 * T, 16, "Nivel 02", *BOSQUE_DESDE_GRANJA)
g.poner("Personaje_jugador", *SPAWN_GRANJA)
g.poner("AvisoInteractivo", 0, 0, 100000)

# =====================================================================================
# BOSQUE (56 x 40)
# =====================================================================================
b = Mapa(56, 40, 11)
b.borde(2)
# bloques de bosque espeso que separan los claros
for (x0, y0, x1, y1) in [(15, 2, 17, 14), (2, 14, 13, 18), (17, 13, 24, 17), (29, 2, 33, 12), (15, 22, 22, 33), (2, 22, 3, 37),
                         (29, 23, 33, 37), (40, 9, 46, 12), (49, 22, 53, 30), (40, 24, 45, 30), (23, 29, 25, 37)]:
    b.rect(x0, y0, x1, y1, "T")
for (x, y) in [(15, 15), (13, 14), (24, 16), (29, 13), (22, 34), (33, 22), (46, 13), (45, 31)]:
    b.g[y][x] = "T"
# entradas: sur (granja) y este (pueblo)
b.rect(25, 36, 29, 39, "."); b.rect(52, 18, 55, 22, ".")
# rio de norte a sur con una curva
RIO = []
for y in range(40):
    x = 35 if y < 13 else (36 if y < 27 else 37)
    for k in (x, x + 1): b.g[y][k] = "~"; RIO.append((k, y))
# caminos: sur -> centro -> puente -> este
b.camino([(27, 39), (27, 20), (34, 20)])
b.camino([(39, 20), (55, 20)])
for y in (19, 20, 21):
    for x in (36, 37):
        b.g[y][x] = "p"          # bajo el puente se puede pasar
b.rect(35, 19, 35, 21, "."); b.rect(38, 19, 38, 21, ".")
b.poner("Puente", 36 * T - 1, 20 * T + 16 - 25, 1)
interactivo(b, "Cartel", 40 * T, 18 * T + 8, "CartelPueblo"); b.ocupar(40, 18)
interactivo(b, "Cartel", 28 * T, 35 * T, "CartelGranjaBosque"); b.ocupar(28, 35)
# cantera (noroeste): rocas y vetas
for (x, y, t) in [(5, 4, 0), (9, 5, 0), (12, 8, 1), (6, 9, 0), (10, 11, 2), (4, 12, 1)]: veta(b, x, y, t)
b.esparcir(9, (3, 3, 14, 13), lambda x, y: roca(b, x, y), margen=0)
interactivo(b, "Cartel", 13 * T, 3 * T, "CartelCantera"); b.ocupar(13, 3)
# cabana en ruinas (claro del norte)
interactivo(b, "CabanaRuina", 20 * T, 3 * T, "Cabana"); b.ocupar(20, 3, 4, 4); b.colisiones.append((20 * T + 8, 3 * T + 50, 98, 44))
b.esparcir(5, (18, 3, 28, 11), lambda x, y: arbusto(b, x, y), margen=1)
# claro de los hongos (suroeste)
HONGOS = []
def hongo(x, y): HONGOS.append((x, y)); b.poner("Recursos", x * T, y * T, 5, anim=None, variables=[var("Nuevo", "boolean", False)])
b.esparcir(9, (4, 21, 14, 35), hongo, margen=1)
papa(b, 8, 27); papa(b, 11, 32, "Brillante")
# este del rio: prado, cueva y papa gigante
interactivo(b, "Cueva", 46 * T, 2 * T + 10, "Cueva"); b.ocupar(46, 2, 3, 3); b.colisiones.append((46 * T, 2 * T + 10, 98, 60))
papa(b, 46, 7, "Gigante"); papa(b, 43, 16); papa(b, 50, 34, "Brillante"); papa(b, 20, 20); papa(b, 41, 35)
b.esparcir(26, (3, 3, 52, 37), lambda x, y: arbol(b, x, y), margen=1)
b.esparcir(10, (3, 3, 52, 37), lambda x, y: arbusto(b, x, y), margen=1)
b.esparcir(8, (18, 18, 52, 37), lambda x, y: roca(b, x, y), margen=1)
b.esparcir(20, (3, 3, 52, 37), lambda x, y: hierba(b, x, y), margen=0)
FLORES_B = {}
deco_flores(b, FLORES_B, 40, (3, 3, 52, 37))
for (x, y) in HONGOS: pass
HIERBITAS_B = {}
for _ in range(320):
    x, y = b.r.randint(2, 53), b.r.randint(2, 37)
    if b.get(x, y) == "." and (x, y) not in b.ocupado and (x, y) not in FLORES_B: HIERBITAS_B[(x, y)] = b.r.choice([9, 10, 11, 12, 5, 6, 8])
PUEBLO_DESDE_BOSQUE = (-53, 190)
BOSQUE_DESDE_PUEBLO = (53 * T - 8, 20 * T + 28)
teleport(b, 26 * T, 39 * T + 16, 3 * T, 16, "Nivel 01", *GRANJA_DESDE_BOSQUE)
teleport(b, 55 * T + 16, 18 * T, 16, 5 * T, "Pueblo", *PUEBLO_DESDE_BOSQUE)
b.poner("Personaje_jugador", *BOSQUE_DESDE_GRANJA)
b.poner("AvisoInteractivo", 0, 0, 100000)

# =====================================================================================
# Objetos nuevos
# =====================================================================================
for f in ["Granero", "Estatua", "Buzon", "Barril1", "Barril2", "Charco1", "Charco2", "Puente", "CabanaRuina", "Cueva", "Tablon", "Cartel", "Hongo"]:
    add_resource(d, "image", "Escenarios/%s.png" % f, "Escenarios/%s.png" % f)
for f in ["Ramiro1", "Ramiro2", "Lupita1", "Lupita2", "Tomas1", "Tomas2"]:
    add_resource(d, "image", "Pueblo/%s.png" % f, "Pueblo/%s.png" % f)
for f in ["Ramiro", "Lupita", "Tomas"]:
    add_resource(d, "image", "Intro/Retrato%sHD.png" % f, "Intro/Retrato%sHD.png" % f)
YSORT = {"name": "YSort", "type": "YSort::YSort"}
def base_mask(img, w, h, alto=12): return frame(img, (0, 0), rect(4, h - alto, w - 4, h - 1))
inter = sprite_obj("Interactivo", [
    anim_def("Estatua", [base_mask("Escenarios/Estatua.png", 50, 74, 20)]), anim_def("Buzon", [base_mask("Escenarios/Buzon.png", 22, 32, 10)]),
    anim_def("Cartel", [base_mask("Escenarios/Cartel.png", 32, 32, 10)]), anim_def("Tablon", [base_mask("Escenarios/Tablon.png", 50, 46, 10)]),
    anim_def("Cueva", [frame("Escenarios/Cueva.png", (0, 0), rect(20, 30, 78, 74))]), anim_def("CabanaRuina", [frame("Escenarios/CabanaRuina.png", (0, 0), rect(8, 40, 106, 98))]),
    anim_def("Puerta", [frame("Intro/Blanco.png", (0, 0), rect(0, 0, 8, 8))])],
    [var("Dialogo", "string", ""), var("Solido", "boolean", True)], tween=False)
inter["behaviors"] = [YSORT]
deco = sprite_obj("Decorado", [anim_def("Granero", [frame("Escenarios/Granero.png")]), anim_def("Barril1", [frame("Escenarios/Barril1.png")]),
                               anim_def("Barril2", [frame("Escenarios/Barril2.png")]),
                               anim_def("Charco", [frame("Escenarios/Charco%d.png" % i, (0, 0), rect(4, 3, 28, 13)) for i in (1, 2)], loop=True, dt=0.33)], tween=False)
deco["behaviors"] = [YSORT]
for o in [inter, deco, sprite_obj("Puente", [anim_def("", [frame("Escenarios/Puente.png")])], tween=False),
          text_obj("AvisoInteractivo", "Clic: mirar", 9, (255, 246, 210), (36, 21, 13)),
          sprite_obj("Cortina", [anim_def("", [frame("Menu/Negro.png")])])]:
    set_global_object(d, o)
# los objetos del mapa que se recogen tambien pueden ser hongos
for nombre, origen in (("Recursos", (0, 0)), ("IconoItem", (16, 16))):
    o = O[nombre]; o["animations"] = [a for a in o["animations"] if a["name"] != "Hongo"]
    o["animations"].append(anim_def("Hongo", [frame("Escenarios/Hongo.png", origen, None if nombre == "IconoItem" else rect(6, 6, 26, 26))]))
items = next(v for v in d["variables"] if v["name"] == "Items")
items["children"] = [c for c in items["children"] if c["name"] != "Hongo"] + [struct("Hongo", [
    var("Nombre", "string", "Hongo silvestre"), var("Tipo", "string", "Forraje"), var("Rareza", "string", "Común"), var("Max", "number", 99),
    var("Precio", "number", 15), var("Descripcion", "string", "Crece en el claro del bosque. Doña Rosa lo compra bien.")])]
# la instancia de hongo necesita su animacion (indice) en Recursos
idx_hongo = [a["name"] for a in O["Recursos"]["animations"]].index("Hongo")
for i in b.inst:
    if i["name"] == "Recursos": i["numberProperties"] = [{"name": "animation", "value": idx_hongo}]
# NPC nuevos
npc = O["NPC"]
def parpadeo(nombre):
    f1 = frame("Pueblo/%s1.png" % nombre, (0, 0), rect(10, 4, 22, 26)); f2 = frame("Pueblo/%s2.png" % nombre, (0, 0), rect(10, 4, 22, 26))
    return anim_def(nombre, [f1] * 5 + [f2], loop=True, dt=0.5)
npc["animations"] = [a for a in npc["animations"] if a["name"] not in ("Ramiro", "Lupita", "Tomas")] + [parpadeo(n) for n in ("Ramiro", "Lupita", "Tomas")]
ret = O["Retrato"]
ret["animations"] = [a for a in ret["animations"] if a["name"] not in ("Ramiro", "Lupita", "Tomas")] + \
                    [anim_def(n, [frame("Intro/Retrato%sHD.png" % n)]) for n in ("Ramiro", "Lupita", "Tomas")]
papa_obj = O["Papa"]
if not any(v["name"] == "Tipo" for v in papa_obj["variables"]): papa_obj["variables"].append(var("Tipo", "string", "Normal"))

# =====================================================================================
# Dialogos nuevos
# =====================================================================================
N = "Narrador"
NUEVOS = {
    "Estatua": [(N, "«HetolMimiao (1801 - 1879). Fundador de Papayork. Amó las papas como nadie.»"),
                ("Pedro", "Mi tatarabuelo... dicen que sonreía hasta en las peores cosechas.")],
    "Buzon": [("Pedro", "El buzón está vacío. Algún día llegarán cartas del pueblo.")],
    "CartelGranja": [(N, "«Granja Gutiérrez. Antes, tierras de HetolMimiao.»")],
    "CartelBosque": [(N, "«Al norte: Bosque de Papayork. Más allá del río: el Pueblo.»")],
    "CartelZona": [(N, "«¡PELIGRO! Tierra contaminada. No pises los charcos que brillan.»"),
                   ("Pedro", "Aquí la radiación todavía se siente... por eso salen tantas papas.")],
    "CartelPueblo": [(N, "«Al este: Pueblo de Papayork.»")],
    "CartelGranjaBosque": [(N, "«Al sur: Granja Gutiérrez.»")],
    "CartelCantera": [(N, "«Cantera vieja. Cobre, hierro... y algo que brilla.»")],
    "Cabana": [(N, "Una cabaña de la época de HetolMimiao. Entre los escombros hay una tabla tallada:"),
               (N, "«Aquí vivió la familia de HetolMimiao, hasta el día en que el cielo se volvió verde.»")],
    "Cueva": [("Pedro", "Unas rocas enormes tapan la entrada. Se oyen ruidos raros allá adentro..."),
              ("Pedro", "Necesitaré algo más fuerte que mi pico para entrar aquí. (Próximamente)")],
    "Tablon": [(N, "«SE BUSCAN valientes que libren al valle de las papas radiactivas. Recompensa en monedas. — El Alcalde»"),
               (N, "«Doña Rosa compra cosechas frescas. Don Fermín forja mejoras con lingotes.»")],
    "Ramiro": [("Ramiro", "¡Pedro Gutiérrez! El tataranieto de HetolMimiao. Bienvenido a Papayork."),
               ("Ramiro", "Desde que volvió la radiación, las papas mutantes no nos dejan en paz."),
               ("Ramiro", "Si limpias el valle, Papayork volverá a ser lo que era. ¡Cuento contigo!")],
    "Lupita": [("Lupita", "¿Tú eres el de la granja? ¡Mi abuelo dice que allá las papas brillan de noche!"),
               ("Lupita", "Si encuentras una papa radiactiva bonita... ¿me la enseñas? ¡Prometo no comérmela!")],
    "Tomas": [("Tomas", "Ah, joven Pedro. Pesco en este lago desde antes de que nacieras."),
              ("Tomas", "Dicen que en el fondo del bosque hay una cueva... y que de ahí sale la radiación."),
              ("Tomas", "Yo que tú, me prepararía bien antes de ir a husmear.")],
    "Dormir": [("Pedro", "Ha sido un día largo... mejor me voy a dormir.")],
}
dlg = next(v for v in d["variables"] if v["name"] == "Dialogos")
dlg["children"] = [c for c in dlg["children"] if c["name"] not in NUEVOS] + [
    {"name": k, "type": "array", "children": [{"type": "structure", "children": [var("Quien", "string", q_), var("Texto", "string", t)]} for q_, t in v]}
    for k, v in NUEVOS.items()]
nom = next(v for v in d["variables"] if v["name"] == "NombresPersonajes")
nom["children"] = [c for c in nom["children"] if c["name"] not in ("Ramiro", "Lupita", "Tomas")] + \
                  [var("Ramiro", "string", "Alcalde Ramiro"), var("Lupita", "string", "Lupita"), var("Tomas", "string", "Abuelo Tomás")]

# =====================================================================================
# Aplicar a las escenas
# =====================================================================================
def construir(nombre, m, flores, hierbitas, limites):
    lay = next(l for l in d["layouts"] if l["name"] == nombre)
    pasto = inst("Suelo_Pasto", 0, 0, "", -1000, m.w * T, m.h * T)
    camino = {k: v for k, v in autotile_camino(m).items()}
    piedra = {(x, y): (x * 7 + y * 3) % 9 for y in range(m.h) for x in range(m.w) if m.g[y][x] == "#"}
    nuevas = [pasto, tilemap("SueloPasto", m, camino, -900), tilemap("SueloPiedra", m, piedra, -899),
              tilemap("TileSet_Decorativo_Bosque", m, hierbitas, -880), tilemap("Decoraciones", m, flores, -870),
              tilemap("Bosque_Delimitador", m, autotile_bosque(m), 1)]
    if nombre == "Nivel 01":
        nuevas.append(tilemap("Vayas", m, VALLA, 5))
    agua = [inst("Agua2", x * T, y * T, "", -950) for y in range(m.h) for x in range(m.w) if m.g[y][x] in "~p"]
    lay["instances"] = nuevas + agua + m.inst + colisiones(m, "T~v")
    for v in lay["variables"]:
        if v["name"] == "LimiteCamara":
            for c in v["children"]:
                c["value"] = {"Izquierda": 0, "Arriba": 0, "Derecha": limites[0], "Abajo": limites[1]}[c["name"]]
    return lay
construir("Nivel 01", g, FLORES_G, HIERBITAS_G, (g.w * T, g.h * T))
construir("Nivel 02", b, FLORES_B, HIERBITAS_B, (b.w * T, b.h * T))

# Pueblo: nuevos vecinos, tablon y el teletransportador que vuelve al bosque nuevo
pue = next(l for l in d["layouts"] if l["name"] == "Pueblo")
pue["instances"] = [i for i in pue["instances"] if not (i["name"] in ("Interactivo", "AvisoInteractivo") or
                    (i["name"] == "NPC" and any(v["name"] == "Tienda" and v["value"] in ("Ramiro", "Lupita", "Tomas") for v in i["initialVariables"])))]
ianim = {a["name"]: k for k, a in enumerate(npc["animations"])}
for nombre, x, y in (("Ramiro", 690, 150), ("Lupita", 1010, 290), ("Tomas", 300, 330)):
    i = inst("NPC", x, y, "", y + 32, variables=[var("Tienda", "string", nombre), var("Saludo", "string", "")])
    i["numberProperties"] = [{"name": "animation", "value": ianim[nombre]}]; pue["instances"].append(i)
t = inst("Interactivo", 850, 290, "", 336, variables=[var("Dialogo", "string", "Tablon"), var("Solido", "boolean", True)])
t["numberProperties"] = [{"name": "animation", "value": INTER.index("Tablon")}]; pue["instances"].append(t)
pue["instances"].append(inst("AvisoInteractivo", 0, 0, "", 100000))
for i in pue["instances"]:
    if i["name"] == "Teletransportador":
        for v in i["initialVariables"]:
            if v["name"] == "PosicionX": v["value"] = BOSQUE_DESDE_PUEBLO[0]
            if v["name"] == "PosicionY": v["value"] = BOSQUE_DESDE_PUEBLO[1]

# Posicion inicial de una partida nueva (puerta de la casa)
for v in d["variables"]:
    if v["name"] == "Posicion_Inicial_Jugador":
        for c in v["children"]: c["value"] = SPAWN_GRANJA[0] if c["name"] == "X" else SPAWN_GRANJA[1]
menu = next(l for l in d["layouts"] if l["name"] == "Menu Principal")
for e in recorrer(menu["events"]):
    for a in e.get("actions") or []:
        if a["type"]["value"] == "JSONToGlobalVariableStructure" and a["parameters"][1] == "Posicion_Inicial_Jugador":
            a["parameters"][0] = q(json.dumps({"X": SPAWN_GRANJA[0], "Y": SPAWN_GRANJA[1]}, separators=(",", ":")))

# =====================================================================================
# Eventos: interactuar, dormir, charcos, papas especiales, NPC sin tienda
# =====================================================================================
DIST = "DistanceBetweenPositions(Personaje_jugador.X(), Personaje_jugador.Y(), Interactivo.X() + Interactivo.Width() / 2, Interactivo.Y() + Interactivo.Height() - 8)"
H24 = "mod(Reloj.Hora, 12)"
M = [COM("MUNDO: objetos con los que se interactua (clic estando cerca), dormir en la casa, charcos radiactivos y papas especiales")]
M.append(EV([C("SceneJustBegins", "")], [hide("AvisoInteractivo"), A("ResetTimer", "", q("Charco")), A("ResetObjectTimer", "Recursos", q("Soltado"))], [
    EV([C("AnimatableCapability::AnimatableBehavior::Name", "Interactivo", "Animation", "=", q("Puerta"))], [hide("Interactivo"),
        A("ResizableCapability::ResizableBehavior::SetWidth", "Interactivo", "Resizable", "=", "32"),
        A("ResizableCapability::ResizableBehavior::SetHeight", "Interactivo", "Resizable", "=", "24")]),
    EV([objv_s("Papa", "Tipo", q("Brillante"))], [A("ChangeColor", "Papa", q("170;255;130")), set_objv_n("Papa", "Velocidad", "48"), set_objv_n("Papa", "Vida", "50")]),
    EV([objv_s("Papa", "Tipo", q("Gigante"))], [A("ChangeColor", "Papa", q("255;190;190")), set_objv_n("Papa", "Velocidad", "18"), set_objv_n("Papa", "Vida", "160"),
                                               A("ScalableCapability::ScalableBehavior::SetValue", "Papa", "Scale", "=", "2")]),
    EV([objv_s("NPC", "Tienda", q("Mercado"), "!="), objv_s("NPC", "Tienda", q("Herreria"), "!=")], [anim("NPC", "NPC.Tienda"), A("SetZOrder", "NPC", "=", "NPC.Y() + 32")])]))
M.append(COM("Aviso y clic para mirar / leer / dormir"))
M.append(EV([], [hide("AvisoInteractivo")], [
    EV([ibv("InventarioAbierto", "False"), ibv("DialogoAbierto", "False"),
        C("PickNearest", "Interactivo", "Personaje_jugador.X()", "Personaje_jugador.Y()", ""), cmp(DIST, "<", "60")], [
        show("AvisoInteractivo"), A("SetX", "AvisoInteractivo", "=", "Interactivo.X() + Interactivo.Width() / 2 - 22"),
        A("SetY", "AvisoInteractivo", "=", "Interactivo.Y() - 12"), txt("AvisoInteractivo", q("Clic: mirar"))], [
        EV([objv_s("Interactivo", "Dialogo", q("Dormir"))], [txt("AvisoInteractivo", q("Clic: dormir")), A("SetY", "AvisoInteractivo", "=", "Interactivo.Y() - 20")]),
        EV([cursor("Interactivo"), released()], [sv("DialogoPedido", "Interactivo.Dialogo"), bv("DialogoPausa", "True")])])]))
M.append(EV([objv_b("Interactivo", "Solido", "True"), C("CollisionNP", "Personaje_jugador", "Interactivo", "", "", "")],
            [A("SeparateFromObjects", "Personaje_jugador", "Interactivo", "")]))
M.append(COM("Dormir: pasa la noche hasta las 6 AM, los cultivos crecen esas horas, se recupera la vida y se guarda la partida"))
M.append(EV([isv("DialogoTerminado", q("Dormir"))], [
    sv("DialogoTerminado", '""'), nv("Hora24", H24), nv("Salto", "0")], [
    EV([isv("Reloj.M", q("PM"))], [nv("Hora24", "12", "+")]),
    EV([], [nv("Salto", "mod(24 - Hora24 + 6, 24)")]),
    EV([isv("Reloj.M", q("PM"))], [nv("Calendario.Dia", "1", "+"), nv("Calendario.DiaTotal", "1", "+")], [
        EV([inv_("Calendario.Dia", "28", ">")], [nv("Calendario.Dia", "1"), nv("Calendario.Estacion", "1", "+")], [
            EV([inv_("Calendario.Estacion", "3", ">")], [nv("Calendario.Estacion", "0"), nv("Calendario.Anio", "1", "+")])])]),
    {"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Granja", "valueIteratorVariableName": "CeldaGranja",
     "keyIteratorVariableName": "ClaveGranja", "conditions": [isv("CeldaGranja.Planta", '""', "!=")],
     "actions": [nv("Granja[ClaveGranja].Horas", "Salto", "+")],
     "events": [EV([ibv("CeldaGranja.Abono", "True")], [nv("Granja[ClaveGranja].Horas", "Salto", "+")]),
                EV([], [nv("Granja[ClaveGranja].Etapa", "min(3, floor(Granja[ClaveGranja].Horas / Cultivos[CeldaGranja.Planta].HorasEtapa))")])]},
    EV([], [nv("Reloj.Hora", "6"), nv("Reloj.Minuto", "0"), sv("Reloj.M", q("AM")), bv("Reloj.Mediodia", "False"), nv("HoraVista", "6"),
            nv("LuzExterior.R", "68"), nv("LuzExterior.G", "118"), nv("LuzExterior.B", "223"),
            nv("Vida", "50"), set_objv_n("Personaje_jugador", "Vida", "50"),
            nv("Posicion_Inicial_Jugador.X", "Personaje_jugador.X()"), nv("Posicion_Inicial_Jugador.Y", "Personaje_jugador.Y()"),
            sv("EscenaAGuardar", "CurrentSceneName()"),
            A("Create", "", "Cortina", "0", "0", q("DialogoHD")), A("ResizableCapability::ResizableBehavior::SetWidth", "Cortina", "Resizable", "=", "960"),
            A("ResizableCapability::ResizableBehavior::SetHeight", "Cortina", "Resizable", "=", "540"), A("SetZOrder", "Cortina", "=", "999"),
            tw_op("Cortina", "Amanecer", 0, "easeInQuad", 2.5, "yes"),
            A("Create", "", "TextoFlotante", "Personaje_jugador.CenterX() - 40", "Personaje_jugador.Y() - 40", q("")),
            txt("TextoFlotante", '"¡Buenos días! Día " + ToString(Calendario.Dia)'), color("TextoFlotante", "251;242;54"),
            A("SetZOrder", "TextoFlotante", "=", "100000"), tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", 2),
            tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 3, "yes"), snd("HUD/SubirNivel.wav", 50)])],
    variables=[var("Hora24", "number", 0), var("Salto", "number", 0)]))
M.append(COM("Los charcos radiactivos hacen dano"))
M.append(EV([C("AnimatableCapability::AnimatableBehavior::Name", "Decorado", "Animation", "=", q("Charco")),
             C("CollisionNP", "Personaje_jugador", "Decorado", "", "", ""), C("CompareTimer", "", q("Charco"), ">", "0.8"),
             ibv("InventarioAbierto", "False")], [
    A("ResetTimer", "", q("Charco")), set_objv_n("Personaje_jugador", "Vida", "3", "-"), nv("Vida", "Personaje_jugador.Vida"),
    A("ChangeColor", "Personaje_jugador", q("170;255;130")), snd("Cultivos/Comer.wav", 40),
    A("Create", "", "TextoFlotante", "Personaje_jugador.CenterX() - 4", "Personaje_jugador.Y() - 30", q("")), txt("TextoFlotante", q("-3")),
    color("TextoFlotante", "153;229;80"), A("SetZOrder", "TextoFlotante", "=", "100000"),
    tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 14", "easeOutQuad", 0.6), tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 0.8, "yes")]))
M.append(EV([C("CompareTimer", "", q("Charco"), ">", "0.4")], [A("ChangeColor", "Personaje_jugador", q("255;255;255"))]))
external_events(d, "Mundo2", M)
pers = ext("Personaje")
if not any(e.get("target") == "Mundo2" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("Mundo2"))
for lay in d["layouts"]:
    if lay["name"] in ("Nivel 01", "Nivel 02", "Pueblo") and not any(v["name"] == "HoraVista" for v in lay["variables"]):
        lay["variables"].append(var("HoraVista", "number", -1))

# las tiendas solo abren para los NPC que tienen tienda (Ramiro, Lupita y Tomas solo conversan)
tienda = ext("Tienda")
for e in tienda["events"]:
    conds = e.get("conditions") or []
    if any(c["type"]["value"] == "StringVariable" and c["parameters"][:1] == ["DialogoTerminado"] for c in conds) and \
            not any(c["type"]["value"] == "VariableChildExists2" for c in conds):
        conds.append(C("VariableChildExists2", "Tiendas", "TipoTienda"))
# la papa gigante suelta un gran botin
for e in recorrer(pers["events"]):
    if any(c["type"]["value"] == "NumberObjectVariable" and c["parameters"][:3] == ["Papa", "Vida", "<="] for c in e.get("conditions") or []) \
            and e.get("events") and not any("Gigante" in json.dumps(s.get("conditions", [])) for s in e["events"]):
        def soltar(item, veces):
            return REPEAT(veces, [], [A("Create", "", "Recursos", "Papa.X() + RandomInRange(-10, 10)", "Papa.Y()", q("")), anim("Recursos", q(item))])
        e["events"].insert(len(e["events"]) - 1, EV([objv_s("Papa", "Tipo", q("Gigante"))], [nv("Exp", "40", "+"), nv("Monedas", "RandomInRange(30, 50)", "+")], [
            soltar("Nucleo", "1"), soltar("Cristal", "3")]))
        break

json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: granja", len(g.inst), "objetos | bosque", len(b.inst), "objetos")
