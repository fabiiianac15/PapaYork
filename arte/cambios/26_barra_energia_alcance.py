"""La barra rápida sube cuando Pedro está abajo en pantalla, las herramientas gastan menos energía y la espada alcanza más."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
if any(e["name"] == "BarraMovil" for e in d["externalEvents"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
EXT = {e["name"]: e for e in d["externalEvents"]}; L = {l["name"]: l for l in d["layouts"]}; V = {v["name"]: v for v in d["variables"]}
PJ = "Personaje_jugador"
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
# ---------- Barra que se aparta ----------
for v in (var("BarraOff", "number", 0), var("BarraMeta", "number", 0), var("PedroPantY", "number", 0)):
    set_global_var(d, v)
grupo = lambda o: objv_s(o, "Grupo", q("Barra"))
external_events(d, "BarraMovil", [
    COM("Si Pedro baja hasta la zona de la barra rapida, la barra sube a la parte de arriba para no tapar nada. Vuelve cuando el sube."),
    EV([], [nv("PedroPantY", f'({PJ}.Y() - CameraCenterY("")) * CameraZoom("") + 270')]),
    EV([inv_("PedroPantY", "345", ">")], [nv("BarraMeta", "-484")]),
    EV([inv_("PedroPantY", "290", "<")], [nv("BarraMeta", "0")]),
    EV([], [nv("BarraOff", "lerp(BarraOff, BarraMeta, min(1, TimeDelta() * 14))"), A("SetY", "BarraRapida", "=", "492 + BarraOff"), A("SetY", "EtiquetaItem", "=", "472 + BarraOff * 0.86"), A("SetY", "TextoEtiqueta", "=", "474 + BarraOff * 0.86")]),
    EV([grupo("SlotUI")], [A("SetY", "SlotUI", "=", "496 + BarraOff")]),
    EV([grupo("IconoItem")], [A("SetY", "IconoItem", "=", "513 + BarraOff")]),
    EV([grupo("CantidadItem")], [A("SetY", "CantidadItem", "=", "516 + BarraOff")]),
])
per = EXT["Personaje"]["events"]
per.insert(next(k for k, e in enumerate(per) if e.get("target") == "HUD"), LINK("BarraMovil"))
# ---------- Energía: rinde bastante más ----------
def gasto(evs):
    n = 0
    for e in evs:
        for a in e.get("actions", []) or []:
            if a["type"]["value"] == "SetNumberVariable" and a["parameters"][0] == "Energia" and a["parameters"][1] == "-":
                a["parameters"][2] = {"3": "1", "2": "1", "1": "0.5"}.get(a["parameters"][2], a["parameters"][2]); n += 1
        n += gasto(e.get("events", []) or [])
    return n
print("gastos ajustados:", sum(gasto(EXT[k]["events"]) for k in ("Herramientas", "NuevoDia", "Pesca")))
V["Energia"]["value"] = 150; V["EnergiaMax"]["value"] = 150
def nueva(evs):
    for a in evs[35]["actions"]:
        if a["type"]["value"] == "SetNumberVariable" and a["parameters"][0] == "Energia": a["parameters"][2] = "150"
nueva(L["Menu Principal"]["events"])
# ---------- Espada: alcance casi doble ----------
n = 0
def alcance(evs):
    global n
    for e in evs:
        acts = e.get("actions", []) or []
        for k, a in enumerate(list(acts)):
            if a["type"]["value"] == "Create" and a["parameters"][1] == "CajaDaño":
                a["parameters"][2] = a["parameters"][2].replace("-15", "-24").replace("+15", "+24")
                a["parameters"][3] = a["parameters"][3].replace("-15", "-24").replace("+15", "+24")
                acts.insert(acts.index(a) + 1, A("ScalableCapability::ScalableBehavior::SetValue", "CajaDaño", "Scale", "=", "2.4")); n += 1
        alcance(e.get("events", []) or [])
alcance(per)
assert n == 4
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
