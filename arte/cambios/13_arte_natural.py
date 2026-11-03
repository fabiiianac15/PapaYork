"""Arte natural, música propia y zoom 1 por defecto.

Las imágenes nuevas están en Natural/. Solo se cambian las referencias del proyecto: los archivos viejos
siguen en su sitio, así que restaurar respaldo-antes-13.json devuelve el aspecto anterior.
Los personajes pasan de 32x32 a 32x48: el origen y la colisión se desplazan para que los pies y los choques
queden exactamente donde estaban.
"""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *

P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
if any(r["name"].startswith("Natural/") for r in d["resources"]["resources"]):
    sys.exit("El arte natural ya está aplicado; no se cambió nada.")

O = {o["name"]: o for o in d["objects"]}
L = {l["name"]: l for l in d["layouts"]}
for l in d["layouts"]:
    for o in l["objects"]:
        O.setdefault(o["name"], o)


def img(ruta):
    nombre = "Natural/" + ruta
    add_resource(d, "image", nombre, nombre)
    return nombre


def desplazar(fr, dx, dy):
    fr["originPoint"]["x"] += dx
    fr["originPoint"]["y"] += dy
    for p in fr.get("points", []):
        p["x"] += dx
        p["y"] += dy
    if not fr["centerPoint"].get("automatic"):
        fr["centerPoint"]["x"] += dx
        fr["centerPoint"]["y"] += dy
    for poli in fr.get("customCollisionMask", []):
        for v in poli:
            v["x"] += dx
            v["y"] += dy


def anim(o, nombre):
    return next(a for a in o["animations"] if a["name"] == nombre)


def frames(a):
    return a["directions"][0]["sprites"]


# ---------- Pedro: mismos nombres de animación ----------
ped = O["Personaje_jugador"]
for dir_ in ("Abajo", "Arriba", "Izquierda", "Derecha"):
    for i, fr in enumerate(frames(anim(ped, dir_))):
        fr["image"] = img(f"Pedro/{dir_}{i + 1}.png")
        desplazar(fr, 0, 17)
    for i, fr in enumerate(frames(anim(ped, "Ataque " + dir_))):
        fr["image"] = img(f"Pedro/Ataque{dir_}{i + 1}.png")
        desplazar(fr, 0, 17)
for fr in frames(anim(O["Actor"], "Pedro")):
    fr["image"] = img("Pedro/Abajo1.png")
    desplazar(fr, 0, 17)

# ---------- Vecinos: uno distinto de otro, con parpadeo ----------
for nom in ("Rosa", "Fermin", "Ramiro", "Lupita", "Tomas"):
    fs = frames(anim(O["NPC"], nom))
    for i, fr in enumerate(fs):
        fr["image"] = img(f"Vecinos/{nom}{2 if i == len(fs) - 1 else 1}.png")
        desplazar(fr, 0, 17)
for nom in ("Pedro", "Rosa", "Fermin", "Ramiro", "Lupita", "Tomas"):
    frames(anim(O["Retrato"], nom))[0]["image"] = img(f"Retratos/{nom}.png")

# ---------- Papas enemigas y cultivos ----------
for dir_ in ("Abajo", "Arriba", "Derecha", "Izquierda"):
    for i, fr in enumerate(frames(anim(O["Papa"], "Caminar" + dir_))):
        fr["image"] = img(f"Papa/{dir_}{i + 1}.png")
for t in ("Zanahoria", "Papa", "PapaMutante"):
    for i in range(4):
        frames(anim(O["Cultivo"], f"{t}_{i}"))[0]["image"] = img(f"Cultivos/{t}_{i}.png")

# ---------- Árboles grandes: el tronco queda en el mismo sitio y solo el tronco choca ----------
MASCARA = rect(23, 63, 41, 79)
for nombre, arch in (("Arbol", "Arbol1"), ("Arbol_2", "Arbol2"), ("Arbol_3", "Arbol3")):
    fr = frames(O[nombre]["animations"][0])[0]
    fr["image"] = img(f"Plantas/{arch}.png")
    fr["originPoint"]["x"], fr["originPoint"]["y"] = 32, 79
    fr["hasCustomCollisionMask"] = True
    fr["customCollisionMask"] = [MASCARA]
frames(O["Arbol_4"]["animations"][0])[0]["image"] = img("Plantas/Tocon.png")
for l in d["layouts"]:   # los árboles agrandados a mano conservan su proporción
    for i in l["instances"]:
        if i["name"] in ("Arbol", "Arbol_2", "Arbol_3") and i.get("customSize"):
            i["width"], i["height"] = i["width"] * 2, i["height"] * 2.5
for n, a in zip(("1", "2", "3"), O["Arbusto"]["animations"]):
    frames(a)[0]["image"] = img(f"Plantas/Arbusto{n}.png")
for n, a in zip(("1", "2", "3"), O["Hierba"]["animations"]):
    frames(a)[0]["image"] = img(f"Plantas/Hierba{n}.png")
frames(O["Roca_1"]["animations"][0])[0]["image"] = img("Rocas/Roca1.png")
frames(O["Roca_2"]["animations"][0])[0]["image"] = img("Rocas/Roca2.png")

# ---------- Edificios ----------
frames(O["Casa1"]["animations"][0])[0]["image"] = img("Objetos/Casa.png")
frames(anim(O["Decorado"], "Granero"))[0]["image"] = img("Objetos/Granero.png")

# ---------- Madera con los tonos del mundo ----------
for i, fr in enumerate(f for a_ in O["Vaya"]["animations"] for f in frames(a_)):
    fr["image"] = img(f"Madera/Vaya{min(i + 1, 7)}.png")
O["Vayas"]["content"]["atlasImage"] = img("Madera/VayaAtlas.png")
frames(O["Silla"]["animations"][0])[0]["image"] = img("Madera/Caja.png")
fs = frames(O["PlatPesc"]["animations"][0])
fs[0]["image"] = img("Madera/Muelle.png")
if len(fs) > 1:
    fs[1]["image"] = img("Madera/Muelle1.png")

# ---------- Terreno ----------
O["Suelo_Pasto"]["texture"] = img("Terreno/Pasto.png")
for obj, arch in (("SueloPasto", "Camino"), ("SueloPiedra", "Empedrado"), ("Bosque_Delimitador", "Bosque"),
                  ("TileSet_Decorativo_Bosque", "Detalles"), ("Decoraciones", "Decoraciones")):
    O[obj]["content"]["atlasImage"] = img(f"Terreno/{arch}.png")

# Tierra arada: la animación por defecto recibe nombre para poder cambiarla desde los eventos
sp = O["SueloPreparado"]
sp["animations"][0]["name"] = "Seca"
frames(sp["animations"][0])[0]["image"] = img("Terreno/TierraSeca.png")
frames(anim(sp, "Abonado"))[0]["image"] = img("Terreno/TierraAbonada.png")
regada = copy.deepcopy(sp["animations"][0])
regada["name"] = "Regada"
frames(regada)[0]["image"] = img("Terreno/TierraRegada.png")
sp["animations"].append(regada)

# Agua de 4 cuadros
ag = O["Agua2"]["animations"][0]["directions"][0]
base = ag["sprites"][0]
ag["sprites"] = []
for n in range(1, 5):
    fr = copy.deepcopy(base)
    fr["image"] = img(f"Terreno/Agua{n}.png")
    ag["sprites"].append(fr)
ag["timeBetweenFrames"], ag["looping"] = 0.4, True

# ---------- Orillas: tierra y sombra donde el agua toca el suelo ----------
orilla = sprite_obj("Orilla", [anim_def(k, [frame(img(f"Terreno/Orilla{k}.png"))]) for k in "NSOE"], tween=False)
set_global_object(d, orilla)
total = 0
for l in d["layouts"]:
    agua = [i for i in l["instances"] if i["name"] == "Agua2" and i.get("layer", "") == ""]
    if not agua:
        continue
    celdas = {(i["x"], i["y"]) for i in agua}
    # Muelles y pilares están sobre el agua: junto a ellos no hay tierra de orilla
    celdas_llenas = {(i["x"], i["y"]) for i in l["instances"] if i["name"] in ("PlatPesc", "SueloPiedra", "Puente", "Vaya")}
    z = max(i.get("zOrder", 0) for i in agua) + 1
    for x, y in sorted(celdas):
        for clave, dx, dy in (("N", 0, -32), ("S", 0, 32), ("O", -32, 0), ("E", 32, 0)):
            if (x + dx, y + dy) not in celdas and (x + dx, y + dy) not in celdas_llenas:
                ins = inst("Orilla", x, y, z=z)
                ins["numberProperties"] = [{"name": "animation", "value": "NSOE".index(clave)}]
                l["instances"].append(ins)
                total += 1
print("orillas:", total)

# ---------- Música y efectos propios ----------
for nombre in ("TemaPapayork", "MananaEnLaGranja", "BosqueContaminado", "PlazaDelPueblo", "Espada", "Regar", "Comer"):
    ruta = f"Natural/Audio/{nombre}.ogg"
    add_resource(d, "audio", ruta, ruta)

VIEJA_MENU = "Stardew Valley OST - Stardew Valley Overture.mp3"
VIEJA_VERANO = "Sonido/Stardew Valley OST - Summer (Nature's Crescendo).mp3"
DBZ = "Efecto de sonido de ATAQUE DE ESPADA DBZ.mp3"
MENU = "Natural/Audio/TemaPapayork.ogg"
ZONAS = {"Nivel 01": "Natural/Audio/MananaEnLaGranja.ogg", "Nivel 02": "Natural/Audio/BosqueContaminado.ogg",
         "Pueblo": "Natural/Audio/PlazaDelPueblo.ogg"}


def cambiar(evs, tabla):
    n = 0
    for e in evs:
        for k in ("conditions", "actions"):
            for ins in e.get(k, []) or []:
                for j, v in enumerate(ins["parameters"]):
                    for viejo, nuevo in tabla.items():
                        if viejo in v:
                            ins["parameters"][j] = ins["parameters"][j].replace(viejo, nuevo)
                            n += 1
        n += cambiar(e.get("events", []) or [], tabla)
    return n


cuenta = 0
for l in d["layouts"]:
    cuenta += cambiar(l["events"], {VIEJA_MENU: MENU, VIEJA_VERANO: ZONAS.get(l["name"], MENU)})
print("referencias de música cambiadas:", cuenta)


def espada(evs):
    for e in evs:
        for a in e.get("actions", []) or []:
            if a["type"]["value"] == "PlaySound" and a["parameters"][1] == DBZ:
                a["parameters"][1], a["parameters"][3] = "Natural/Audio/Espada.ogg", "40"
                return True
        if espada(e.get("events", []) or []):
            return True
    return False


assert espada(next(x for x in d["externalEvents"] if x["name"] == "Personaje")["events"])

# Los sonidos de terceros salen de la lista del juego. Los archivos no se borran.
QUITAR = {VIEJA_MENU, VIEJA_VERANO, DBZ, "Stardew Valley OST - Summer (Nature's Crescendo).mp3",
          "meme don cangrejo riendo (plantilla) xd.mp3"}
d["resources"]["resources"] = [r for r in d["resources"]["resources"] if r["name"] not in QUITAR]
restos = json.dumps(d, ensure_ascii=False)
for n in QUITAR:
    assert n not in restos, n

# ---------- Zoom 1 por defecto; la tecla Z sigue disponible para comparar ----------
next(v for v in d["variables"] if v["name"] == "ZoomMundoPrueba")["value"] = 1

with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok")
