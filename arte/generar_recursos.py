"""Recursos de Papayork: objetos nuevos, de donde salen y como caen al suelo.

Se aplica despues de generar_inventario.py (usa Items, IconoItem y el grupo ItemsStardew).

- Hierba alta (granja y bosque): se corta con el hacha o la espada -> Fibra y a veces Semillas de papa.
- Arboles: ademas de madera, a veces Resina.
- Rocas: ademas de piedra, a veces Carbon o Cobre.
- Vetas del bosque (Cobre, Hierro, Cristal): se pican con el pico, necesitan mas golpes.
- Arar: a veces sale Tierra fertil.
- Papa radiactiva: a veces Cristal, Semillas de papa mutante o un Nucleo de uranio (epico).
- Todo lo que cae salta, rebota y luego vuela hacia el jugador cuando esta cerca (estilo Stardew).

Uso: python3 arte/generar_recursos.py "Legado Radioactivo-Papayork.json"
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gdutil import *

PROJ = sys.argv[1]
d = json.load(open(PROJ, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}

# ---------- catalogo ----------
NUEVOS = [
    ("Fibra", "Fibra", "Recurso", "Común", 99, 1, "Sale de la hierba alta. Sirve para sacos, cuerdas y cercas."),
    ("Resina", "Resina", "Recurso", "Poco común", 99, 8, "Savia de los árboles talados. Para antorchas y barriles."),
    ("Carbon", "Carbón", "Recurso", "Poco común", 99, 10, "A veces sale al picar rocas. Es el combustible del horno."),
    ("Cobre", "Mineral de cobre", "Mineral", "Poco común", 99, 12, "De las vetas naranjas del bosque. Mejora tus herramientas."),
    ("Hierro", "Mineral de hierro", "Mineral", "Raro", 99, 25, "De las vetas grises. Para herramientas y armas más fuertes."),
    ("Cristal", "Cristal radiactivo", "Mineral", "Raro", 99, 40, "Brilla en la oscuridad. Para las mejoras más avanzadas."),
    ("Nucleo", "Núcleo de uranio", "Especial", "Épico", 10, 150, "El corazón de una papa mutante. Poder puro y peligroso."),
    ("TierraFertil", "Tierra fértil", "Recurso", "Común", 99, 3, "A veces aparece al arar. Hará crecer más rápido tus cultivos."),
    ("Semillas de Papa", "Semillas de papa", "Semilla", "Común", 99, 6, "Salen de la hierba. ¡Cuidado con lo que sale de la tierra!"),
    ("Semillas de Papa Mutante", "Semillas de papa mutante", "Semilla", "Raro", 99, 30, "Las sueltan las papas radiactivas. Brillan un poco..."),
]
items = next(v for v in d["variables"] if v["name"] == "Items")
items["children"] = [c for c in items["children"] if c["name"] not in {n[0] for n in NUEVOS}]
for i, n, t, r, m, p, ds in NUEVOS:
    items["children"].append(struct(i, [var("Nombre", "string", n), var("Tipo", "string", t), var("Rareza", "string", r),
                                        var("Max", "number", m), var("Precio", "number", p), var("Descripcion", "string", ds)]))
for c in items["children"]:  # para que sirven los recursos de siempre
    if c["name"] in ("Madera", "Piedra"):
        desc = next(x for x in c["children"] if x["name"] == "Descripcion")
        desc["value"] = {"Madera": "Sale de los árboles. Para cercas, cofres y casas.",
                         "Piedra": "Sale de las rocas. Para caminos, hornos y mejoras."}[c["name"]]

# ---------- recursos (imagenes y sonidos) ----------
for i, *_ in NUEVOS: add_resource(d, "image", "Recursos/" + i + ".png", "Recursos/" + i + ".png")
for n in ["VetaCobre", "VetaHierro", "VetaCristal", "Hierba1", "Hierba2", "Hierba3"]:
    add_resource(d, "image", "Recursos/" + n + ".png", "Recursos/" + n + ".png")
for n in ["Cortar", "Talar", "Picar", "Soltar"]:
    add_resource(d, "audio", "Recursos/" + n + ".wav", "Recursos/" + n + ".wav")

# ---------- objetos ----------
rec = O["Recursos"]
rec["animations"] = [a for a in rec["animations"] if a["name"] not in {n[0] for n in NUEVOS}]
rec["animations"] += [anim_def(i, [frame("Recursos/" + i + ".png", (0, 0), rect(6, 6, 26, 26))]) for i, *_ in NUEVOS]
rec["variables"] = [v for v in rec["variables"] if v["name"] not in ("Nuevo", "BaseY")] + [var("Nuevo", "boolean", True), var("BaseY", "number", 0)]
if not any(b["type"] == "Tween::TweenBehavior" for b in rec["behaviors"]): rec["behaviors"].append(TWEEN)

ico = O["IconoItem"]
ico["animations"] = [a for a in ico["animations"] if a["name"] not in {n[0] for n in NUEVOS}]
ico["animations"] += [anim_def(i, [frame("Recursos/" + i + ".png", (16, 16))]) for i, *_ in NUEVOS]

YSORT = {"name": "YSort", "type": "YSort::YSort"}
veta = sprite_obj("Veta", [anim_def("Cobre", [frame("Recursos/VetaCobre.png", (0, 0), rect(4, 7, 28, 24))]),
                           anim_def("Hierro", [frame("Recursos/VetaHierro.png", (0, 0), rect(4, 7, 28, 24))]),
                           anim_def("Cristal", [frame("Recursos/VetaCristal.png", (0, 0), rect(5, 1, 28, 27))])],
                  [var("Vida", "number", 3), var("MiID", "string", "")])
veta["behaviors"] = [TWEEN, YSORT]
set_global_object(d, veta)
hierba_frames = []
for k in (1, 2, 3):
    f = frame("Recursos/Hierba%d.png" % k, (0, 0), rect(4, 16, 28, 30))
    f["centerPoint"] = {"automatic": False, "name": "centre", "x": 16, "y": 29}  # se mece desde la base
    hierba_frames.append(anim_def(str(k), [f]))
hierba = sprite_obj("Hierba", hierba_frames, [var("Cortar", "boolean", False), var("Cortada", "boolean", False),
                                              var("ListaMecer", "boolean", True), var("MiID", "string", "")])
hierba["behaviors"] = [TWEEN, YSORT]
set_global_object(d, hierba)
rocas = next(g for g in d["objectsGroups"] if g["name"] == "Rocas")
if not any(o["name"] == "Veta" for o in rocas["objects"]): rocas["objects"].append({"name": "Veta"})

# ---------- colocar hierba y vetas en los niveles ----------
COLOCAR = {
    "Nivel 01": {"Hierba": [(-96, 160), (-32, 64), (0, 240), (32, 112), (96, 240), (256, 0), (288, 160), (384, 128),
                            (416, 64), (256, 256), (-96, 256), (128, 0)]},
    "Nivel 02": {"Hierba": [(0, 96), (-16, 288), (256, 160), (208, 240), (240, 320), (288, 64), (480, 320), (-16, 192)],
                 "Veta": [(224, 96, 0), (0, 160, 0), (448, 224, 1), (512, 256, 2)]},
}
for lay in d["layouts"]:
    if lay["name"] not in COLOCAR: continue
    lay["instances"] = [i for i in lay["instances"] if i["name"] not in ("Hierba", "Veta")]
    for k, (x, y) in enumerate(COLOCAR[lay["name"]].get("Hierba", [])):
        i = inst("Hierba", x, y, "", y); i["numberProperties"] = [{"name": "animation", "value": k % 3}]
        lay["instances"].append(i)
    for x, y, a in COLOCAR[lay["name"]].get("Veta", []):
        i = inst("Veta", x, y, "", y); i["numberProperties"] = [{"name": "animation", "value": a}]
        lay["instances"].append(i)

# ---------- utilidades de eventos ----------
def cmp(a, op, b): return C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def soltar(item, x, y, veces="1"):
    """Crea 'veces' recursos del tipo item en (x, y); el evento de caida los hace saltar."""
    return REPEAT(veces, [], [A("Create", "", "Recursos", x, y, q("")), anim("Recursos", q(item))])
def probabilidad(pct, item, x, y, veces="1"):
    return EV([cmp("RandomInRange(1, 100)", "<=", str(pct))], [], [soltar(item, x, y, veces)])

# ---------- eventos externos "Recursos" ----------
E = [COM("RECURSOS: vetas, hierba alta y la caida de los objetos.\n"
         "Probabilidades: arbol 30% resina | roca 25% carbon, 12% cobre | hierba 1-2 fibra, 15% semillas de papa |\n"
         "arar 8% tierra fertil | papa radiactiva 35% cristal, 15% semillas mutantes, 6% nucleo de uranio.")]
E.append(EV([C("SceneJustBegins", "")], [], [
    EV([C("AnimatableCapability::AnimatableBehavior::Name", "Veta", "Animation", "=", q("Hierro"))], [set_objv_n("Veta", "Vida", "5")]),
    EV([C("AnimatableCapability::AnimatableBehavior::Name", "Veta", "Animation", "=", q("Cristal"))], [set_objv_n("Veta", "Vida", "8")]),
]))
E.append(COM("Todo lo que cae al suelo salta hacia un lado y rebota"))
E.append(FOREACH("Recursos", [objv_b("Recursos", "Nuevo", "True")], [
    set_objv_b("Recursos", "Nuevo", "False"), set_objv_n("Recursos", "BaseY", "Recursos.Y()"),
    A("ResetObjectTimer", "Recursos", q("Soltado")),
    A("Tween::TweenBehavior::AddObjectPositionXTween2", "Recursos", "Tween", q("Esparcir"), "Recursos.X() + RandomInRange(-24, 24)", q("easeOutQuad"), "0.5", "no"),
    tw_y("Recursos", "Saltar", "Recursos.Y() - RandomInRange(10, 18)", "easeOutQuad", 0.18),
    snd("Recursos/Soltar.wav", 25)]))
E.append(FOREACH("Recursos", [C("Tween::HasFinished", "Recursos", "Tween", q("Saltar"))], [
    A("Tween::RemoveTween", "Recursos", "Tween", q("Saltar")),
    tw_y("Recursos", "Caer", "Recursos.BaseY + RandomInRange(2, 12)", "easeOutBounce", 0.4)]))
E.append(COM("Cuando el jugador se acerca, los objetos vuelan hacia el (los recoge el evento Inventario)"))
E.append(FOREACH("Recursos", [
    C("CompareObjectTimer", "Recursos", q("Soltado"), ">", "0.7"),
    cmp("DistanceBetweenPositions(Recursos.X() + 16, Recursos.Y() + 16, Personaje_jugador.X(), Personaje_jugador.Y() - 6)", "<", "60")], [
    A("SetX", "Recursos", "=", "lerp(Recursos.X(), Personaje_jugador.X() - 16, 0.14)"),
    A("SetY", "Recursos", "=", "lerp(Recursos.Y(), Personaje_jugador.Y() - 22, 0.14)")]))

E.append(COM("Hierba alta: se mece al pasar y se corta con el hacha o con la espada"))
E.append(FOREACH("Hierba", [C("CollisionNP", "Personaje_jugador", "Hierba", "", "", ""), objv_b("Hierba", "ListaMecer", "True")], [
    set_objv_b("Hierba", "ListaMecer", "False"), A("ResetObjectTimer", "Hierba", q("Mecido")),
    A("Tween::TweenBehavior::AddObjectAngleTween2", "Hierba", "Tween", q("Mecer"), "RandomWithStep(-14, 14, 28)", q("easeOutQuad"), "0.12", "no")]))
E.append(FOREACH("Hierba", [C("Tween::HasFinished", "Hierba", "Tween", q("Mecer"))], [
    A("Tween::RemoveTween", "Hierba", "Tween", q("Mecer")),
    A("Tween::TweenBehavior::AddObjectAngleTween2", "Hierba", "Tween", q("Volver"), "0", q("easeOutElastic"), "0.7", "no")]))
E.append(EV([C("CompareObjectTimer", "Hierba", q("Mecido"), ">", "0.9")], [set_objv_b("Hierba", "ListaMecer", "True")]))
E.append(EV([ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False"), isv("ItemEnMano", q("Hacha")), cursor("Hierba"),
             C("MouseButtonFromTextPressed", "", q("Left")), ONCE()], [
    set_objv_b("Hierba", "Cortar", "True"), set_objv_b("Personaje_jugador", "Talando", "True")]))
E.append(EV([C("CollisionNP", "CajaDaño", "Hierba", "", "", "")], [set_objv_b("Hierba", "Cortar", "True")]))
E.append(FOREACH("Hierba", [objv_b("Hierba", "Cortar", "True"), objv_b("Hierba", "Cortada", "False")], [
    set_objv_b("Hierba", "Cortada", "True"), snd("Recursos/Cortar.wav", 60),
    nv("Destruidos[Hierba.MiID]", "Calendario.DiaTotal"),
    A("Tween::TweenBehavior::AddObjectAngleTween2", "Hierba", "Tween", q("Caer"), "RandomWithStep(-40, 40, 80)", q("easeInQuad"), "0.2", "no"),
    tw_op("Hierba", "Desaparecer", 0, "easeInQuad", 0.22, "yes")], [
    soltar("Fibra", "Hierba.X()", "Hierba.Y() + 4", "RandomInRange(1, 2)"),
    probabilidad(15, "Semillas de Papa", "Hierba.X()", "Hierba.Y() + 4")]))
external_events(d, "Recursos", E)

# ---------- Herramientas: sonidos y botin extra de arboles, rocas, vetas y al arar ----------
herr = next(e for e in d["externalEvents"] if e["name"] == "Herramientas")
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
def tiene(e, tipo, *params):
    return any(c["type"]["value"] == tipo and c["parameters"][:len(params)] == list(params) for c in e.get("conditions") or [])
def accion(e, tipo, *params):
    return any(a["type"]["value"] == tipo and a["parameters"][:len(params)] == list(params) for a in e.get("actions") or [])
for e in recorrer(herr["events"]):
    if accion(e, "SetNumberObjectVariable", "Objetos_Fisicos", "Vida", "-") and not accion(e, "PlaySound"):
        e["actions"].append(snd("Recursos/Talar.wav", 60))
    if accion(e, "SetNumberObjectVariable", "Rocas", "Vida", "-") and not accion(e, "PlaySound"):
        e["actions"].append(snd("Recursos/Picar.wav", 55))
    if tiene(e, "NumberObjectVariable", "Objetos_Fisicos", "Vida", "<="):
        e["events"].insert(1, probabilidad(30, "Resina", "Objetos_Fisicos.X() + 8", "Objetos_Fisicos.Y() + 8"))
        e["events"].insert(1, EV([], [nv("Exp", "2", "+")]))
    if tiene(e, "NumberObjectVariable", "Rocas", "Vida", "<="):
        nombre = lambda a: C("AnimatableCapability::AnimatableBehavior::Name", "Rocas", "Animation", "=", q(a))
        x, y = "Rocas.X() + RandomInRange(0, 8)", "Rocas.Y() + 6"
        e["events"][1:1] = [
            COM("Rocas normales: a veces carbon o cobre. Vetas: su mineral"),
            EV([nombre("")], [nv("Exp", "2", "+")], [probabilidad(25, "Carbon", x, y), probabilidad(12, "Cobre", x, y)]),
            EV([nombre("Cobre")], [nv("Exp", "4", "+")], [soltar("Cobre", x, y, "RandomInRange(2, 4)"), probabilidad(20, "Carbon", x, y)]),
            EV([nombre("Hierro")], [nv("Exp", "6", "+")], [soltar("Hierro", x, y, "RandomInRange(1, 3)"), probabilidad(30, "Carbon", x, y)]),
            EV([nombre("Cristal")], [nv("Exp", "10", "+")], [soltar("Cristal", x, y, "RandomInRange(1, 2)"), probabilidad(10, "Nucleo", x, y)])]
    if accion(e, "Create", "", "SueloPreparado"):
        e["events"].append(EV([C("CollisionNP", "SueloPreparado", "Objetos_Fisicos", "", "", "", inv=True)], [], [
            probabilidad(8, "TierraFertil", "SueloPreparado.X()", "SueloPreparado.Y()")]))

# ---------- Personaje: la papa radiactiva suelta botin al morir + incluir Recursos ----------
pers = next(e for e in d["externalEvents"] if e["name"] == "Personaje")
for e in recorrer(pers["events"]):
    if tiene(e, "NumberObjectVariable", "Papa", "Vida", "<=") and accion(e, "Delete", "Papa"):
        x, y = "Papa.X() + 4", "Papa.Y() + 4"
        e["actions"] = [a for a in e["actions"] if not (a["type"]["value"] == "Delete")]
        e["events"] = [probabilidad(35, "Cristal", x, y), probabilidad(15, "Semillas de Papa Mutante", x, y),
                       probabilidad(6, "Nucleo", x, y),
                       EV([], [nv("Exp", "10", "+"), nv("MonedasGanadas", "RandomInRange(3, 8)"), nv("Monedas", "MonedasGanadas", "+"),
                               A("Create", "", "TextoFlotante", "Papa.X()", "Papa.Y() - 8", q("")),
                               txt("TextoFlotante", '"+" + ToString(MonedasGanadas) + " monedas"'), color("TextoFlotante", "251;242;54"),
                               A("SetZOrder", "TextoFlotante", "=", "100000"),
                               tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", 0.9),
                               tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 1.3, "yes"),
                               snd("HUD/Moneda.wav", 60), A("Delete", "Papa", "")])]
        break
else:
    raise SystemExit("no encontre el evento de muerte de la papa")
if not any(e.get("target") == "Recursos" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("Recursos"))

# ---------- arreglo: la camara se limitaba al borde del mapa DESPUES de usar las herramientas ----------
# Cerca de los bordes el mouse apuntaba a un lugar distinto del que se veia. Ahora cada nivel guarda sus
# limites en variables de escena y Personaje limita la camara justo despues de centrarla en el jugador.
for lay in d["layouts"]:
    if lay["name"] not in ("Nivel 01", "Nivel 02", "Pueblo"): continue
    clamp = next((e for e in lay["events"] if any(a["type"]["value"] == "ClampCamera" for a in e.get("actions") or [])), None)
    if clamp is None: continue
    a = next(a for a in clamp["actions"] if a["type"]["value"] == "ClampCamera")
    lay["variables"] = [v for v in lay["variables"] if not v["name"].startswith("LimiteCamara")]
    lay["variables"].append(struct("LimiteCamara", [var(k, "number", float(a["parameters"][i])) for k, i in
                                                    (("Izquierda", 1), ("Arriba", 2), ("Derecha", 3), ("Abajo", 4))]))
    i = lay["events"].index(clamp)
    lay["events"][i - 1:i + 1] = [e for e in lay["events"][i - 1:i] if not (e.get("type", "").endswith("Comment") and "camara" in e.get("comment", "").lower())]
for e in recorrer(pers["events"]):
    acts = e.get("actions") or []
    k = next((j for j, a in enumerate(acts) if a["type"]["value"] == "CenterCameraOnObject"), None)
    if k is not None and not any(a["type"]["value"] == "ClampCamera" for a in acts):
        acts.insert(k + 1, A("ClampCamera", "", "LimiteCamara.Izquierda", "LimiteCamara.Arriba", "LimiteCamara.Derecha",
                             "LimiteCamara.Abajo", "", ""))
        break

json.dump(d, open(PROJ, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: recursos con", len(E), "eventos")
