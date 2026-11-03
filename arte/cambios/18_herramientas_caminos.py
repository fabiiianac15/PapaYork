"""Una animación distinta para cada herramienta y árboles que ya no pisan los caminos del Pueblo."""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *

P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
ped = O["Personaje_jugador"]
if any(a["name"].startswith("Hacha") for a in ped["animations"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
EXT = {e["name"]: e for e in d["externalEvents"]}
PUEBLO = next(l for l in d["layouts"] if l["name"] == "Pueblo")


def img(ruta):
    n = "Natural/" + ruta
    add_resource(d, "image", n, n)
    return n


base = next(a for a in ped["animations"] if a["name"] == "Abajo")["directions"][0]["sprites"][0]
MASCARA = [[{"x": v["x"] + 15, "y": v["y"] + 14} for v in poli] for poli in base["customCollisionMask"]]
PUNTA = {"Izquierda": (5, 30), "Derecha": (56, 30), "Abajo": (38, 61), "Arriba": (36, 8)}


def grande(ruta, dir_=None):
    pts = [{"name": "Punta", "x": PUNTA[dir_][0], "y": PUNTA[dir_][1]}] if dir_ else []
    return {"hasCustomCollisionMask": True, "image": img(ruta), "points": pts,
            "originPoint": {"name": "origine", "x": 31.5, "y": 57},
            "centerPoint": {"automatic": False, "name": "centre", "x": 31, "y": 47},
            "customCollisionMask": copy.deepcopy(MASCARA)}


def animacion(nombre, cuadros, dt, bucle):
    return {"name": nombre, "useMultipleDirections": False,
            "directions": [{"looping": bucle, "timeBetweenFrames": dt, "sprites": cuadros}]}


DIRS = ("Izquierda", "Derecha", "Arriba", "Abajo")
for dir_ in DIRS:
    for herr, dt in (("Hacha", 0.07), ("Pico", 0.08), ("Azadon", 0.08)):
        ped["animations"].append(animacion(f"{herr} {dir_}", [grande(f"Pedro2/{herr}{dir_}{i}.png") for i in range(1, 6)], dt, False))
    ped["animations"].append(animacion(f"Regar {dir_}", [grande(f"Pedro2/Regar{dir_}{i}.png") for i in range(1, 5)], 0.11, False))
    for nom, t, dt, bucle in (("Lanzar", 3, 0.13, False), ("Esperar", 2, 0.55, True), ("Tirar", 2, 0.14, True)):
        ped["animations"].append(animacion(f"Pesca{nom}{dir_}", [grande(f"Pedro2/Pesca{nom}{dir_}{i}.png", dir_) for i in range(1, t + 1)], dt, bucle))
ped["variables"].append(var("Regando", "boolean", False))
set_global_var(d, var("Pescando", "boolean", False))

# ---------- Cada herramienta usa su propia animación ----------
her = EXT["Herramientas"]["events"]


def renombrar(evs, nuevo):
    n = 0
    for e in evs:
        for a in e.get("actions", []) or []:
            for i, v in enumerate(a["parameters"]):
                if '"Ataque ' in v:
                    a["parameters"][i] = v.replace('"Ataque ', f'"{nuevo} ')
                    n += 1
        n += renombrar(e.get("events", []) or [], nuevo)
    return n


i = {}
for k, e in enumerate(her):
    t = json.dumps(e.get("conditions", []))
    for flag in ("Talando", "Labrando", "Picando"):
        if flag in t and "True" in t and k > 8:
            i[flag] = k
assert len(i) == 3, i
for flag, nombre in (("Talando", "Hacha"), ("Labrando", "Azadon"), ("Picando", "Pico")):
    assert renombrar([her[i[flag]]], nombre) == 4
regar = json.loads(json.dumps(her[i["Talando"]], ensure_ascii=False).replace("Talando", "Regando").replace('\\"Hacha ', '\\"Regar '))
her.insert(i["Picando"] + 1, regar)
nue = EXT["NuevoDia"]["events"]
accion = next(e for e in nue if "Regada" in json.dumps(e.get("actions", []), ensure_ascii=False) and "Regar.ogg" in json.dumps(e.get("actions", [])))
accion["actions"].append(A("SetBooleanObjectVariable", "Personaje_jugador", "Regando", "True", ""))

# ---------- Mientras usa la regadera o pesca, Pedro no camina ni ataca ----------
per = EXT["Personaje"]["events"]
per[5]["conditions"] += [C("BooleanObjectVariable", "Personaje_jugador", "Regando", "False", ""), ibv("Pescando", "False")]
per[10]["conditions"].append(ibv("Pescando", "False"))

# ---------- Caminos del Pueblo despejados ----------
def tilemap(i):
    p = next((x for x in i.get("stringProperties", []) if x["name"] == "tilemap"), None)
    return (p, json.loads(p["value"])) if p else (None, None)


camino = []
for i_ in PUEBLO["instances"]:
    if i_["name"] == "SueloPasto":
        _, t = tilemap(i_)
        ex = i_["width"] / (t["dimX"] * 32) if i_.get("customSize") else 1
        ey = i_["height"] / (t["dimY"] * 32) if i_.get("customSize") else 1
        for lay in t["layers"]:
            for ry, fila in enumerate(lay["tiles"]):
                for rx, v in enumerate(fila):
                    if v != -1 and v != 5:
                        camino.append((i_["x"] + rx * 32 * ex, i_["y"] + ry * 32 * ey, 32 * ex, 32 * ey))


def pisa(l, a, r, b, margen=4):
    return any(x + margen < r and x + w - margen > l and y + margen < b and y + h - margen > a for x, y, w, h in camino)


# Muro de bosque: quitar las piezas sobre el camino y redondear las vecinas
quitadas = 0
for i_ in PUEBLO["instances"]:
    if i_["name"] != "Bosque_Delimitador":
        continue
    p, t = tilemap(i_)
    fuera = set()
    for lay in t["layers"]:
        for ry, fila in enumerate(lay["tiles"]):
            for rx, v in enumerate(fila):
                x, y = i_["x"] + rx * 32, i_["y"] + ry * 32
                if v != -1 and pisa(x, y, x + 32, y + 32, 8):
                    fila[rx] = -1
                    fuera.add((rx, ry))
        tl = lay["tiles"]
        hay = lambda a, b: 0 <= b < len(tl) and 0 <= a < len(tl[b]) and tl[b][a] != -1
        for rx, ry in fuera:
            for a, b in ((rx + 1, ry), (rx - 1, ry), (rx, ry + 1), (rx, ry - 1)):
                if hay(a, b):
                    fil = 0 if not hay(a, b - 1) else 2 if not hay(a, b + 1) else 1
                    col = 0 if not hay(a - 1, b) else 2 if not hay(a + 1, b) else 1
                    tl[b][a] = fil * 3 + col
    quitadas += len(fuera)
    p["value"] = json.dumps(t, separators=(",", ":"))
print("piezas de bosque quitadas del camino:", quitadas)

ocupado = []
for i_ in PUEBLO["instances"]:
    n = i_["name"]
    if n == "Casa1":
        ocupado.append((i_["x"] - 58, i_["y"] - 100, i_["x"] + 70, i_["y"]))
    elif n in ("Agua2", "SueloPiedra", "PlatPesc", "Puesto", "Pozo"):
        ocupado.append((i_["x"] - 4, i_["y"] - 4, i_["x"] + 36, i_["y"] + 36))
    elif n == "Colision":
        ocupado.append((i_["x"], i_["y"], i_["x"] + (i_.get("width") or 0), i_["y"] + (i_.get("height") or 0)))
arboles = [i_ for i_ in PUEBLO["instances"] if i_["name"] in ("Arbol", "Arbol_2", "Arbol_3")]


def caja(i_, x=None, y=None):
    x, y = i_["x"] if x is None else x, i_["y"] if y is None else y
    ex, ey = (i_["width"] / 64, i_["height"] / 80) if i_.get("customSize") else (1, 1)
    return x - 26 * ex, y - 76 * ey, x + 26 * ex, y, ex


movidos = []
for i_ in arboles:
    l, a, r, b, ex = caja(i_)
    if not pisa(l, a, r, b):
        continue
    mejor = None
    for rad in range(16, 240, 16):
        for dx, dy in ((rad, 0), (-rad, 0), (0, rad), (0, -rad), (rad, rad), (-rad, rad), (rad, -rad), (-rad, -rad)):
            l, a, r, b, _ = caja(i_, i_["x"] + dx, i_["y"] + dy)
            nx, ny = i_["x"] + dx, i_["y"] + dy
            tronco = (nx - 10 * ex, ny - 18, nx + 10 * ex, ny)
            libre = not pisa(l, a, r, b) and not any(tronco[0] < o[2] and tronco[2] > o[0] and tronco[1] < o[3] and tronco[3] > o[1] for o in ocupado)
            cerca = any(o is not i_ and abs(o["x"] - nx) < 30 and abs(o["y"] - ny) < 22 for o in arboles)
            if libre and not cerca:
                mejor = (nx, ny)
                break
        if mejor:
            break
    if mejor:
        movidos.append((i_["name"], i_["x"], i_["y"], *mejor))
        i_["x"], i_["y"] = mejor
        i_["zOrder"] = mejor[1]
print("árboles movidos:", movidos)
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok")
