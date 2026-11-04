"""Menú nuevo con su historia, interfaz del menú con el estilo del inventario, espada más larga, papas con menos vida y mina en un claro."""
import json, sys, os, copy
from collections import deque
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
from PIL import Image
P = sys.argv[1]
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = json.load(open(P, encoding="utf8"))
L = {l["name"]: l for l in d["layouts"]}; M = L["Menu Principal"]
if any(o["name"] == "ZombieMenu" for o in M["objects"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}; EXT = {e["name"]: e for e in d["externalEvents"]}; OM = {o["name"]: o for o in M["objects"]}
PJ = "Personaje_jugador"
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def img(r):
    n = "Natural/" + r + ".png"; add_resource(d, "image", n, n); return n
# ---------- Espada larga ----------
ped = O[PJ]
base = next(a for a in ped["animations"] if a["name"] == "Abajo")["directions"][0]["sprites"][0]
MASC = [[{"x": v["x"] + 25, "y": v["y"] + 20} for v in pol] for pol in base["customCollisionMask"]]
for dir_ in ("Izquierda", "Derecha", "Arriba", "Abajo"):
    a = next(x for x in ped["animations"] if x["name"] == "Ataque " + dir_)
    a["directions"][0]["sprites"] = [{"hasCustomCollisionMask": True, "image": img(f"Pedro2/Espada{dir_}{i}"), "points": [], "originPoint": {"name": "origine", "x": 41.5, "y": 63}, "centerPoint": {"automatic": False, "name": "centre", "x": 41, "y": 53}, "customCollisionMask": copy.deepcopy(MASC)} for i in (1, 2, 3)]
# ---------- Papas con menos vida ----------
next(v for v in O["Papa"]["variables"] if v["name"] == "Vida")["value"] = 30
NUEVA = {"40": "20", "50": "25", "160": "70"}
def vida(evs):
    n = 0
    for e in evs:
        for a in e.get("actions", []) or []:
            if a["parameters"][:3] == ["Papa", "Vida", "="] and a["parameters"][3] in NUEVA:
                a["parameters"][3] = NUEVA[a["parameters"][3]]; n += 1
        n += vida(e.get("events", []) or [])
    return n
assert vida(EXT["Cultivos"]["events"]) + vida(EXT["Mundo2"]["events"]) == 3
# ---------- Mina en un claro ----------
N2 = L["Nivel 02"]; X, Y = 790, 606
dec = next(i for i in N2["instances"] if i["name"] == "Decorado" and i["x"] == 490 and i["y"] == 36)
dec["x"], dec["y"], dec["zOrder"] = X, Y, Y + 84
pu = next(i for i in N2["instances"] if i["name"] == "Interactivo" and any(v.get("value") == "Mina" for v in i["initialVariables"]))
pu["x"], pu["y"], pu["zOrder"] = X + 39, Y + 62, Y + 86
rx, ry = X + 55, Y + 110
vuelta = next(i for i in L["Mina"]["instances"] if i["name"] == "Interactivo")
for v in vuelta["initialVariables"]:
    if v["name"] == "DestX": v["value"] = rx
    if v["name"] == "DestY": v["value"] = ry
# La escalera de salida solo se podía pulsar en sus últimos 10 píxeles: ahora responde en toda la escalera
esc = next(a for a in O["Interactivo"]["animations"] if a["name"] == "EscaleraArriba")["directions"][0]["sprites"][0]
ew, eh = Image.open(os.path.join(RAIZ, esc["image"])).size
esc["hasCustomCollisionMask"] = True; esc["customCollisionMask"] = [rect(0, 0, ew, eh)]
# Comprobación: se llega caminando desde la entrada del Pueblo
paredes = [(i["x"], i["y"], i["x"] + (i.get("width") or 32), i["y"] + (i.get("height") or 32)) for i in N2["instances"] if i["name"] == "Colision"]
libre = lambda x, y: not any(a - 8 < x < c + 8 and b - 6 < y < e + 6 for a, b, c, e in paredes)
ini = (880 // 16 * 16, 1180 // 16 * 16)  # donde se llega desde la Granja
vis = {ini}; q_ = deque([ini]); ok = False
while q_:
    x, y = q_.popleft()
    if abs(x - rx) < 20 and abs(y - ry) < 20: ok = True; break
    for a, b in ((16, 0), (-16, 0), (0, 16), (0, -16)):
        n = (x + a, y + b)
        if 0 <= n[0] < 1792 and 0 <= n[1] < 1280 and n not in vis and libre(*n): vis.add(n); q_.append(n)
assert ok, "la mina no se alcanza caminando"
# ---------- Interfaz del menú ----------
def poner(obj, anim_, r):
    next(a for a in OM[obj]["animations"] if a["name"] == anim_)["directions"][0]["sprites"][0]["image"] = img("Menu/" + r)
for nom in ("Cargar", "Nueva", "Ajustes"):
    for suf in ("", "Hover", "Presionado"): poner("BotonMenu", nom + suf, f"Boton{nom}{suf}")
poner("PanelMadera", "", "Panel"); poner("RanuraPartida", "Normal", "Ranura"); poner("RanuraPartida", "Hover", "RanuraHover")
for an, r in (("Normal", "BotonPeq"), ("Hover", "BotonPeqHover"), ("MiniNormal", "BotonMini"), ("MiniHover", "BotonMiniHover"), ("BorrarNormal", "BorrarNormal"), ("BorrarHover", "BorrarHover")): poner("BotonUI", an, r)
tp = OM["TituloPanel"]; tp["content"]["isOutlineEnabled"] = False; tp["content"]["color"] = "63;36;24"; tp["color"] = {"r": 63, "g": 36, "b": 24}
# ---------- Objetos de la presentación ----------
F = "Natural/IntroN/"
def capa(n, suf): return sprite_obj(n, [anim_def("N", [frame(img(f"IntroN/Valle_{suf}"))])], tween=False)
M["objects"] += [capa("MenuCielo", "Cielo"), capa("MenuMontes", "Montes"), capa("MenuValle", "Valle"), capa("MenuFrente", "Frente"),
    sprite_obj("NubeM", [anim_def(n, [frame(img(f"IntroN/{n}"))]) for n in ("Nube1", "Nube2", "Nube3")], variables=[var("Vel", "number", 4)], tween=False),
    sprite_obj("AveM", [anim_def("N", [frame(img(f"IntroN/Ave{k}")) for k in (1, 2, 3, 2)], loop=True, dt=.13)]),
    sprite_obj("HumoM", [anim_def("N", [frame(img(f"IntroN/Humo{k}")) for k in range(1, 5)], loop=True, dt=.28)], tween=False),
    sprite_obj("HaloMenu", [anim_def("N", [frame(img("Menu/HaloVerde"), (170, 170))])]),
    sprite_obj("ZombieMenu", [anim_def("N", [frame(img(f"Menu/Zombie{k}"), (35, 72)) for k in range(1, 5)], loop=True, dt=.24)]),
    sprite_obj("PedroMenu", [anim_def("Corre", [frame(img(f"Pedro2/CorrerDerecha{k}"), (16.5, 43)) for k in range(1, 9)], loop=True, dt=.05),
        anim_def("Ataque", [frame(img(f"Pedro2/EspadaDerecha{k}"), (41.5, 63)) for k in (1, 2, 3)], loop=False, dt=.09),
        anim_def("Quieto", [frame(img(f"Pedro2/QuietoDerecha{k}"), (16.5, 43)) for k in (1, 2)], loop=True, dt=.6)]),
    sprite_obj("FlashMenu", [anim_def("N", [frame(img("Menu/Blanco"))])]),
    sprite_obj("EsporaM", [anim_def("N", [frame("Menu/Espora.png")])])]
M["instances"] = [i for i in M["instances"] if i["name"] != "FondoInicio"]
for n, z in (("MenuCielo", 0), ("MenuMontes", 2), ("MenuValle", 3), ("MenuFrente", 5)): M["instances"].append(inst(n, -30, 0, z=z))
for k, (x, y, v) in enumerate(((40, 18, 4), (250, 8, 2.5), (410, 42, 5.5), (120, 54, 3))):
    i = inst("NubeM", x, y, z=1, variables=[var("Vel", "number", v)]); i["numberProperties"] = [{"name": "animation", "value": k % 3}]; M["instances"].append(i)
M["instances"] += [inst("HaloMenu", 398, 200, layer="Fundido", z=5), inst("ZombieMenu", 398, 234, layer="Fundido", z=7), inst("PedroMenu", -40, 232, layer="Fundido", z=8), inst("HumoM", 0, 28, z=4), inst("FlashMenu", 0, 0, layer="Fundido", z=20, w=480, h=270)]
set_global_var(d, var("MenuVisto", "boolean", False))
M["variables"] += [var("TI", "number", 0), var("OffsetMenu", "number", 0), var("SwayM", "number", 0), var("DistM", "number", 300), var("TonoM", "number", 30), var("SaltadoM", "boolean", False), var("VueloM", "number", 12), var("AltoM", "number", 40)]
# ---------- Secuencia ----------
ev = M["events"]
ini_ev = ev[4]
ini_ev["actions"] = [a for a in ini_ev["actions"] if not ("FondoInicio" in a["parameters"] or a["type"]["value"].endswith("TweenCameraPosition2") or "Fundido" in a["parameters"])]
ini_ev["actions"] += [opacity("Fundido", 255), opacity("HaloMenu", 0), opacity("ZombieMenu", 0), opacity("FlashMenu", 0), anim("PedroMenu", q("Corre")), nv("OffsetMenu", "0"), bv("SaltadoM", "False")]
ini_ev["events"] = [e for e in ini_ev["events"] if not (e.get("actions") and e["actions"][0]["type"]["value"] == "PlayMusicOnChannel")]
ini_ev["events"].append(EV([ibv("MenuVisto", "True")], [nv("OffsetMenu", "5.4"), A("Delete", "HaloMenu", ""), A("Delete", "ZombieMenu", ""), A("Delete", "PedroMenu", "")]))
paso = lambda t, acts=(), subs=(), pro=False: EV(([ibv("MenuVisto", "False")] if pro else []) + [cmp_("TI", ">=", str(t)), ibv("SaltadoM", "False"), ONCE()], list(acts), list(subs))
tw_x = lambda o, id_, x, ease, dur: A("Tween::TweenBehavior::AddObjectPositionXTween2", o, "Tween", q(id_), str(x), q(ease), str(dur), "no")
def ataque(): return [anim("PedroMenu", q("Ataque")), A("ChangeSprite", "PedroMenu", "=", "0"), A("AnimatableCapability::AnimatableBehavior::PlayAnimation", "PedroMenu", "Animation"), snd("Natural/Audio/Espada.ogg", 80)]
burst = REPEAT(18, acts=[A("Create", "", "EsporaM", "RandomInRange(372, 424)", "RandomInRange(180, 228)", q("Fundido")), A("SetZOrder", "EsporaM", "=", "12"), A("ScalableCapability::ScalableBehavior::SetValue", "EsporaM", "Scale", "=", "RandomInRange(1, 3)"), A("ChangeColor", "EsporaM", q("168;236;74")),
    tw_y("EsporaM", "Subir", "EsporaM.Y() - RandomInRange(30, 90)", "easeOutQuad", .9), tw_x("EsporaM", "Lado", "EsporaM.X() + RandomInRange(-40, 40)", "easeOutQuad", .9), tw_op("EsporaM", "Apagar", 0, "easeInQuad", 1.1, "yes")])
MUS = [A("PlayMusicOnChannel", "", "Natural/Audio/TemaPapayork.ogg", "0", "yes", "VolumenMusica", "1"), sv("MusicaActual", q("Natural/Audio/TemaPapayork.ogg"))]
linea = [
    COM("MENU. Oscuridad, una papa zombie alumbra la esquina, Pedro la vence, se abre el valle, baja el logo y salen las opciones. Clic, Espacio o Esc lo saltan. Al volver al menu se va directo al valle."),
    EV([], [nv("TI", 'TimerElapsedTime("Intro") + OffsetMenu'), nv("SwayM", "sin(TimeFromStart() * 0.14)")]),
    EV([], [A("SetX", "MenuCielo", "=", "-30 + SwayM * 6"), A("SetX", "MenuMontes", "=", "-30 + SwayM * 14"), A("SetX", "MenuValle", "=", "-30 + SwayM * 24"), A("SetX", "MenuFrente", "=", "-30 + SwayM * 30"), A("SetX", "HumoM", "=", "-30 + SwayM * 24 + 194")]),
    FOREACH("NubeM", acts=[A("SetX", "NubeM", "=", "NubeM.X() + NubeM.Vel * TimeDelta()")], subs=[EV([cmp_("NubeM.X()", ">", "500")], [A("SetX", "NubeM", "=", "-110")])]),
    COM("Pedro sale de la oscuridad a medida que se acerca a la luz verde"),
    EV([ibv("MenuVisto", "False"), ibv("SaltadoM", "False")], [nv("DistM", "abs(398 - PedroMenu.X())"), nv("TonoM", "round(26 + 229 * min(1, max(0, 1 - (DistM - 50) / 210)))"), A("ChangeColor", "PedroMenu", 'ToString(TonoM) + ";" + ToString(TonoM) + ";" + ToString(TonoM)')]),
    paso(.5, [tw_op("HaloMenu", "Luz", 255, "easeOutQuad", 1.3), tw_op("ZombieMenu", "Ver", 255, "easeInQuad", 1.3)], pro=True),
    paso(1, [snd("Cultivos/Temblor.wav", 75)], pro=True),
    paso(2.1, [tw_x("PedroMenu", "Correr", 330, "linear", 1.45)], pro=True),
    paso(3.55, ataque() + [A("ChangeColor", "ZombieMenu", q("255;120;120")), tw_x("ZombieMenu", "Empujon", 412, "easeOutQuad", .2), snd("Cultivos/Comer.wav", 80)], pro=True),
    paso(3.85, [A("ChangeColor", "ZombieMenu", q("255;255;255"))], pro=True),
    paso(4.05, ataque() + [A("ChangeColor", "ZombieMenu", q("255;90;90")), opacity("FlashMenu", 170), tw_op("FlashMenu", "Pasar", 0, "easeOutQuad", .45), snd("Intro/Explosion.wav", 60), tw_op("ZombieMenu", "Morir", 0, "easeInQuad", .5), tw_y("ZombieMenu", "Caer", 244, "easeInQuad", .5), tw_op("HaloMenu", "Apagar", 0, "easeInQuad", .9)], [burst], pro=True),
    paso(4.45, [anim("PedroMenu", q("Quieto"))], pro=True),
    COM("Se abre el valle y entra la musica"),
    EV([cmp_("TI", ">=", "5.4"), C("StringVariable", "MusicaActual", "!=", q("Natural/Audio/TemaPapayork.ogg"))], MUS),
    EV([ibv("SaltadoM", "True"), C("StringVariable", "MusicaActual", "!=", q("Natural/Audio/TemaPapayork.ogg"))], MUS),
    paso(5.4, [tw_op("Fundido", "Aclarar", 0, "easeInOutSine", 2)], [EV([ibv("MenuVisto", "False")], [tw_op("PedroMenu", "Irse", 0, "easeInQuad", 1.1)])]),
    EV([cmp_("TI", ">=", "5.8"), C("CompareTimer", "", q("AvesM"), ">=", "3.5")], [A("ResetTimer", "", q("AvesM")), nv("VueloM", "RandomFloatInRange(10, 15)"), nv("AltoM", "RandomInRange(14, 70)")], [REPEAT(3, acts=[A("Create", "", "AveM", "-20 - RandomInRange(0, 46)", "AltoM + RandomInRange(0, 16)", q("")), A("SetZOrder", "AveM", "=", "1"), A("ScalableCapability::ScalableBehavior::SetValue", "AveM", "Scale", "=", "1.5"), tw_x("AveM", "Volar", 530, "linear", "VueloM")])]),
    EV([C("PosX", "AveM", ">", "510")], [A("Delete", "AveM", "")]),
    COM("El logo baja poco a poco"),
    paso(7.2, [tw_y("LogoPapayork", "Caer", "20", "easeOutSine", 3.2)]),
    paso(10.4, [snd("Menu/GolpeLogo.wav", 45), A("Tween::TweenBehavior::AddObjectScaleTween3", "LogoPapayork", "Tween", q("Pulso"), "1.03", q("easeOutQuad"), "0.14", "no", "yes")]),
    EV([C("Tween::HasFinished", "LogoPapayork", "Tween", q("Pulso")), ONCE()], [A("Tween::TweenBehavior::AddObjectScaleTween3", "LogoPapayork", "Tween", q("Pulso2"), "1", q("easeOutBack"), "0.25", "no", "yes")]),
    COM("Las opciones"),
]
for k, t in enumerate((10.8, 10.98, 11.16)):
    linea.append(paso(t, [], [EV([C("NumberObjectVariable", "BotonMenu", "Orden", "=", str(k + 1))], [A("Tween::TweenBehavior::AddObjectScaleTween3", "BotonMenu", "Tween", q("Aparecer"), "1", q("easeOutBack"), "0.35", "no", "no"), snd("Menu/Hover.wav", 35)])]))
linea.append(paso(11.5, [A("Delete", "HaloMenu", ""), A("Delete", "ZombieMenu", ""), A("Delete", "PedroMenu", ""), sv("Pantalla", q("Principal")), bv("MenuVisto", "True"), tw_op("MiNombre", "Aparecer", 255, "linear", .6), tw_op("NombreAsignatura", "Aparecer", 255, "linear", .6)]))
i0 = next(k for k, e in enumerate(ev) if e.get("comment", "").startswith("INTRO"))
i1 = next(k for k, e in enumerate(ev) if e.get("comment", "").startswith("Esporas"))
ev[i0:i1] = linea
ev[4]["actions"].append(A("ResetTimer", "", q("AvesM")))
# Saltar: al final de todo, para que el mismo clic no presione un botón
TW = ["Aclarar"]
salto = [bv("SaltadoM", "True"), A("Tween::RemoveTween", "Fundido", "Tween", q("Aclarar")), opacity("Fundido", 0), opacity("FlashMenu", 0), A("Delete", "HaloMenu", ""), A("Delete", "ZombieMenu", ""), A("Delete", "PedroMenu", ""), A("Delete", "EsporaM", ""),
    A("Tween::RemoveTween", "LogoPapayork", "Tween", q("Caer")), A("SetY", "LogoPapayork", "=", "20"), A("Tween::RemoveTween", "BotonMenu", "Tween", q("Aparecer")), A("ScalableCapability::ScalableBehavior::SetValue", "BotonMenu", "Scale", "=", "1"),
    sv("Pantalla", q("Principal")), bv("MenuVisto", "True"), opacity("MiNombre", 255), opacity("NombreAsignatura", 255)]
base_s = [isv("Pantalla", q("Intro")), ibv("SaltadoM", "False"), cmp_("TI", ">", ".4")]
ev += [COM("Saltar la presentacion"), EV(base_s + [C("MouseButtonFromTextReleased", "", q("Left"))], salto), EV(base_s + [C("KeyFromTextReleased", "", q("Space"))], salto), EV(base_s + [C("KeyFromTextReleased", "", q("Escape"))], salto)]
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
