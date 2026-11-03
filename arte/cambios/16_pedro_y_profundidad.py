"""Pedro con esqueleto y sombrero: corre por defecto, camina con Shift, respira en reposo.
Orden de profundidad único para todo el mundo (ver arte/ORDEN_PROFUNDIDAD.md).
Corrige el punto Center de Pedro, que el script 13 subió 9 píxeles y desplazaba el golpe de la espada."""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
from PIL import Image

P = sys.argv[1]
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = json.load(open(P, encoding="utf8"))
if any(e["name"] == "Profundidad" for e in d["externalEvents"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}
for l in d["layouts"]:
    for o in l["objects"]:
        O.setdefault(o["name"], o)
EXT = {e["name"]: e for e in d["externalEvents"]}
L = {l["name"]: l for l in d["layouts"]}


def img(ruta):
    nombre = "Natural/" + ruta
    add_resource(d, "image", nombre, nombre)
    return nombre


# ---------- Animaciones de Pedro ----------
ped = O["Personaje_jugador"]
MASCARA = copy.deepcopy(next(a for a in ped["animations"] if a["name"] == "Abajo")["directions"][0]["sprites"][0]["customCollisionMask"])


def cuadro(ruta):
    return {"hasCustomCollisionMask": True, "image": img(ruta), "points": [],
            "originPoint": {"name": "origine", "x": 16.5, "y": 43},
            "centerPoint": {"automatic": False, "name": "centre", "x": 16, "y": 33},
            "customCollisionMask": copy.deepcopy(MASCARA)}


def animacion(nombre, rutas, dt, bucle):
    return {"name": nombre, "useMultipleDirections": False,
            "directions": [{"looping": bucle, "timeBetweenFrames": dt, "sprites": [cuadro(r) for r in rutas]}]}


# Respira despacio y parpadea de vez en cuando
RESPIRA = [1, 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1, 3, 1, 2]
nuevas = []
for dir_ in ("Izquierda", "Derecha", "Arriba", "Abajo"):
    nuevas.append(animacion(dir_, [f"Pedro2/{dir_}{i}.png" for i in range(1, 9)], 0.075, True))
    nuevas.append(animacion("Correr" + dir_, [f"Pedro2/Correr{dir_}{i}.png" for i in range(1, 9)], 0.05, True))
    nuevas.append(animacion("Quieto" + dir_, [f"Pedro2/Quieto{dir_}{k}.png" for k in RESPIRA], 0.32, True))
    nuevas.append(animacion("Ataque " + dir_, [f"Pedro2/Ataque{dir_}{i}.png" for i in range(1, 4)], 0.12, False))
ped["animations"] = nuevas

actor = next(a for a in O["Actor"]["animations"] if a["name"] == "Pedro")
actor["directions"][0]["sprites"][0]["image"] = img("Pedro2/QuietoAbajo1.png")
next(a for a in O["Retrato"]["animations"] if a["name"] == "Pedro")["directions"][0]["sprites"][0]["image"] = img("Retratos/Pedro.png")
O["Marco_Barravida"]["animations"][0]["directions"][0]["sprites"][0]["image"] = img("Objetos/MarcoVida.png")

# Polvo al correr
set_global_object(d, sprite_obj("PolvoPaso", [anim_def("Normal", [frame(img("Pedro2/PolvoPaso.png"))])]))

# ---------- Variables ----------
set_global_var(d, var("VelPedro", "number", 130))
set_global_var(d, var("CorrePedro", "boolean", True))
set_global_var(d, {"name": "NombresDir", "type": "array", "children": [var("", "string", n) for n in ("Izquierda", "Derecha", "Arriba", "Abajo")]})
for c in next(v for v in d["variables"] if v["name"] == "NombresDir")["children"]:
    del c["name"]

# ---------- Movimiento: correr por defecto, Shift camina a la velocidad original ----------
per = EXT["Personaje"]["events"]
mov = per[5]["events"]
assert per[5]["conditions"][0]["parameters"][0] == "InventarioAbierto" and len(mov) == 12
PERSONA = "Personaje_jugador"
tecla = lambda t: C("KeyFromTextPressed", "", q(t))
o_ = lambda *cs: {"type": {"value": "BuiltinCommonInstructions::Or"}, "parameters": [], "subInstructions": list(cs)}

calculo = [
    COM("Corre por defecto. Con Shift camina a la velocidad original. En diagonal no va mas rapido."),
    EV([], [nv("VelPedro", "130"), bv("CorrePedro", "True")]),
    EV([tecla("LShift")], [nv("VelPedro", "50"), bv("CorrePedro", "False")]),
    EV([tecla("RShift")], [nv("VelPedro", "50"), bv("CorrePedro", "False")]),
    EV([o_(tecla("a"), tecla("d")), o_(tecla("w"), tecla("s"))], [nv("VelPedro", "VelPedro * 0.7071")]),
]
for e in mov[:4]:
    assert e["actions"][0]["type"]["value"] == "AddForceAL" and e["actions"][0]["parameters"][2] == "50"
    e["actions"][0]["parameters"][2] = "VelPedro"
fijar = lambda t: A("AnimatableCapability::AnimatableBehavior::SetName", PERSONA, "Animation", "=", t)
NOMBRE = f"NombresDir[{PERSONA}.Direccion]"
animar = [
    COM("Quieto respira; al moverse camina o corre segun Shift. Las animaciones se llaman Quieto, nada o Correr + direccion."),
    EV([C("HasNoForces", PERSONA)], [fijar(f'"Quieto" + {NOMBRE}')]),
    EV([C("HasNoForces", PERSONA, inv=True), ibv("CorrePedro", "False")], [fijar(NOMBRE)]),
    EV([C("HasNoForces", PERSONA, inv=True), ibv("CorrePedro", "True")], [fijar(f'"Correr" + {NOMBRE}')]),
    EV([], [A("AnimatableCapability::AnimatableBehavior::PlayAnimation", PERSONA, "Animation")]),
    COM("Polvo a ras de suelo al correr"),
    EV([C("HasNoForces", PERSONA, inv=True), ibv("CorrePedro", "True"), C("CompareTimer", "", q("PolvoPaso"), ">=", "0.24")], [
        A("ResetTimer", "", q("PolvoPaso")),
        A("Create", "", "PolvoPaso", f"{PERSONA}.CenterX() - 3 + RandomInRange(-3, 3)", f"{PERSONA}.Y() - 1", q("")),
        A("SetZOrder", "PolvoPaso", "=", "PolvoPaso.Y()"),
        tw_y("PolvoPaso", "Subir", "PolvoPaso.Y() - 5", "easeOutQuad", 0.4),
        tw_op("PolvoPaso", "Desaparecer", 0, "easeInQuad", 0.4, "yes")]),
]
per[5]["events"] = calculo + mov[:4] + animar

# El punto de los pies decide quién va delante
pz = next(a for a in per[2]["actions"] if a["type"]["value"] == "SetZOrder")
pz["parameters"][2] = f"{PERSONA}.Y() + 3"

# ---------- Profundidad en eventos ----------
def cambiar_z(evs, objeto, nuevo):
    n = 0
    for e in evs:
        for a in e.get("actions", []) or []:
            if a["type"]["value"] == "SetZOrder" and a["parameters"][0] == objeto:
                a["parameters"][2] = nuevo
                n += 1
        n += cambiar_z(e.get("events", []) or [], objeto, nuevo)
    return n


todos = [x["events"] for x in d["externalEvents"]] + [L[n]["events"] for n in ("Nivel 01", "Nivel 02", "Pueblo")]
TABLA = {"SueloPreparado": "-6500", "Rejilla": "-6400", "Cultivo": "Cultivo.Y() + 28", "NPC": "NPC.Y() + 29"}
for obj, val in TABLA.items():
    assert sum(cambiar_z(evs, obj, val) for evs in todos) >= 1, obj

quietos = ["Casa1", "Rocas", "Vaya", "Pozo", "Silla", "Hierba", "MesaTrabajo", "Interactivo", "Decorado", "Puesto"]
base = lambda o: A("SetZOrder", o, "=", f"{o}.BoundingBoxBottom()")
external_events(d, "Profundidad", [
    COM("ORDEN DE PROFUNDIDAD. Tabla completa en arte/ORDEN_PROFUNDIDAD.md.\n"
        "Lo que esta de pie se ordena por el punto donde pisa: mas abajo en pantalla, mas adelante."),
    EV([C("SceneJustBegins", "")], [A("ResetTimer", "", q("PolvoPaso"))] + [base(o) for o in quietos]),
    EV([C("SceneJustBegins", ""), C("AnimatableCapability::AnimatableBehavior::Name", "Decorado", "Animation", "=", q("Charco"))],
       [A("SetZOrder", "Decorado", "=", "-6800")]),
    COM("Lo que se mueve o aparece durante el juego se reordena en cada cuadro"),
    EV([], [base("Construccion"), A("SetZOrder", "ItemsStardew", "=", "ItemsStardew.Y() + ItemsStardew.Height()"),
            A("SetZOrder", "Gui_Daño", "=", "90000"), A("SetZOrder", "FX_Cortada", "=", "90000")]),
    COM("Si Pedro pasa detras de un arbol grande, la copa se vuelve translucida para no perderlo de vista"),
    EV([], [A("OpacityCapability::OpacityBehavior::SetValue", "Objetos_Fisicos", "Opacity", "=", "255")]),
    FOREACH("Objetos_Fisicos", [
        C("BuiltinCommonInstructions::CompareNumbers", "Objetos_Fisicos.Height()", ">", "60"),
        C("BuiltinCommonInstructions::CompareNumbers", f"abs(Objetos_Fisicos.X() - {PERSONA}.X())", "<", "30"),
        C("BuiltinCommonInstructions::CompareNumbers", f"{PERSONA}.Y() + 3", "<", "Objetos_Fisicos.Y()"),
        C("BuiltinCommonInstructions::CompareNumbers", f"Objetos_Fisicos.Y() - {PERSONA}.Y()", "<", "76")],
        [A("OpacityCapability::OpacityBehavior::SetValue", "Objetos_Fisicos", "Opacity", "=", "130")]),
])
per.append(LINK("Profundidad"))

# El comportamiento YSort usaba la parte superior de muchos objetos; ahora lo reemplaza Profundidad
for o in d["objects"]:
    o["behaviors"] = [b for b in o["behaviors"] if "YSort" not in b["type"]]

# ---------- Profundidad en el editor: los mismos valores que tendrá el juego ----------
SUELO = {"Suelo_Pasto": -10000, "Agua2": -9000, "Orilla": -8900, "SueloPasto": -8000, "SueloPiedra": -7900,
         "TileSet_Decorativo_Bosque": -7500, "Decoraciones": -7400, "PlatPesc": -7000, "Puente": -7000,
         "Colision": -6000, "Teletransportador": -6000, "Bosque_Delimitador": -5500, "Vayas": -5400,
         "AvisoInteractivo": 100000, "AvisoMesa": 100000, "AvisoNPC": 100000}
ARCHIVOS = {r["name"]: r["file"] for r in d["resources"]["resources"]}


def pie(i):
    """Coordenada Y donde el objeto toca el suelo."""
    o = O.get(i["name"])
    if not o or not o.get("animations"):
        return i["y"]
    a = i.get("numberProperties", [])
    idx = next((int(p["value"]) for p in a if p["name"] == "animation"), 0)
    an = o["animations"][min(idx, len(o["animations"]) - 1)]
    s = an["directions"][0]["sprites"][0]
    if s.get("hasCustomCollisionMask") and s.get("customCollisionMask"):
        fondo = max(v["y"] for poli in s["customCollisionMask"] for v in poli)
    else:
        fondo = Image.open(os.path.join(RAIZ, ARCHIVOS[s["image"]])).height
    esc = 1
    if i.get("customSize") and fondo:
        alto = Image.open(os.path.join(RAIZ, ARCHIVOS[s["image"]])).height
        esc = i["height"] / alto if alto else 1
    return round(i["y"] + (fondo - s["originPoint"]["y"]) * esc)


cuenta = {}
for nombre in ("Nivel 01", "Nivel 02", "Pueblo"):
    pisos = {}
    for i in L[nombre]["instances"]:
        if i.get("layer", ""):
            continue
        n = i["name"]
        viejo = i.get("zOrder", 0)
        if n in SUELO:
            z = SUELO[n]
            # En el Pueblo, los trozos que ya iban encima del empedrado siguen encima
            if nombre == "Pueblo" and n == "Agua2" and viejo > 2:
                z = -7850
            if nombre == "Pueblo" and n == "SueloPasto" and viejo > 2:
                z = -7800
        elif n == "Personaje_jugador":
            z = i["y"] + 3
        elif n == "Decorado" and i.get("numberProperties") and \
                O[n]["animations"][min(int(next((p["value"] for p in i["numberProperties"] if p["name"] == "animation"), 0)), len(O[n]["animations"]) - 1)]["name"] == "Charco":
            z = -6800
        else:
            z = pie(i)
        i["zOrder"] = z
        cuenta[n] = cuenta.get(n, 0) + 1
print("instancias ordenadas:", sum(cuenta.values()))

with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok")
