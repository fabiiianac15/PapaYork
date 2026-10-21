"""Panel de la esquina y barra rapida mas pequenos (proporcion parecida a Stardew).

- Panel de 98x44 arriba a la derecha con dial, fecha, estacion, hora, monedas y nivel.
- Barra rapida de 10 casillas de 20px con iconos de 16px (animaciones <Id>_mini de IconoItem).
- La mochila abierta y la mesa de trabajo se quedan grandes, como los menus de Stardew.
"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
base = os.path.dirname(os.path.abspath(P))
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
for f in ["HudPanelMini", "HudExpMarcoMini", "HudExpRellenoMini", "HudMonedaMini", "BarraRapidaMini", "EtiquetaItemMini",
          "CasillaMini", "CasillaMiniHover", "CasillaMiniSeleccionada"] + ["DialMini%d" % i for i in range(6)] + ["EstacionMini%d" % i for i in range(4)]:
    add_resource(d, "image", "HUD/" + f + ".png", "HUD/" + f + ".png")
mini = json.load(open(os.path.join(base, "Mini/lista.json")))
for _, f in mini: add_resource(d, "image", f, f)

def cambiar_imagen(obj, anim, img):
    for a in O[obj]["animations"]:
        if a["name"] == anim:
            for s in a["directions"][0]["sprites"]: s["image"] = img; s["hasCustomCollisionMask"] = False
cambiar_imagen("HudPanel", "", "HUD/HudPanelMini.png")
for i in range(6): cambiar_imagen("HudDial", str(i), "HUD/DialMini%d.png" % i)
for i in range(4): cambiar_imagen("HudEstacion", str(i), "HUD/EstacionMini%d.png" % i)
cambiar_imagen("HudMoneda", "", "HUD/HudMonedaMini.png")
cambiar_imagen("HudExpMarco", "", "HUD/HudExpMarcoMini.png")
cambiar_imagen("HudExpRelleno", "", "HUD/HudExpRellenoMini.png")
cambiar_imagen("BarraRapida", "", "HUD/BarraRapidaMini.png")
cambiar_imagen("EtiquetaItem", "", "HUD/EtiquetaItemMini.png")
def tam_texto(obj, size):
    O[obj]["characterSize"] = size
    if "content" in O[obj]: O[obj]["content"]["characterSize"] = size
for t, s in [("HudFecha", 9), ("HudHora", 9), ("HudMonedas", 9), ("HudNivel", 8), ("TextoEtiqueta", 9)]: tam_texto(t, s)

slot = O["SlotUI"]
slot["animations"] = [a for a in slot["animations"] if not a["name"].startswith("Mini")] + [
    anim_def("MiniNormal", [frame("HUD/CasillaMini.png")]), anim_def("MiniHover", [frame("HUD/CasillaMiniHover.png")]),
    anim_def("MiniSeleccionada", [frame("HUD/CasillaMiniSeleccionada.png")])]
ico = O["IconoItem"]
ico["animations"] = [a for a in ico["animations"] if not a["name"].endswith("_mini")] + \
                    [anim_def(n + "_mini", [frame(f, (8, 8))]) for n, f in mini]

# ---------- posiciones ----------
lay = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
X0, Y0 = 380, 2
POS = {"HudPanel": (X0, Y0), "HudDial": (X0 + 2, Y0 + 2), "HudFecha": (X0 + 33, Y0 + 2), "HudEstacion": (X0 + 86, Y0 + 3),
       "HudHora": (X0 + 33, Y0 + 15), "HudMoneda": (X0 + 4, Y0 + 31), "HudMonedas": (X0 + 14, Y0 + 29),
       "HudNivel": (X0 + 50, Y0 + 30), "HudExpMarco": (X0 + 68, Y0 + 33), "HudExpRelleno": (X0 + 69, Y0 + 34),
       "BarraRapida": (136, 242), "EtiquetaItem": (195, 228), "TextoEtiqueta": (205, 228)}
BX, BY = 140, 245
for i in lay["instances"]:
    if i["name"] in POS: i["x"], i["y"] = POS[i["name"]]
    if i["name"] == "HudExpRelleno": i["width"], i["height"] = 24, 3
    g = {v["name"]: v["value"] for v in i.get("initialVariables", [])}
    if g.get("Grupo") == "Barra":
        k = int(g["Indice"]); x = BX + k * 20
        if i["name"] == "SlotUI": i["x"], i["y"] = x, BY
        if i["name"] == "IconoItem": i["x"], i["y"] = x + 10, BY + 10
        if i["name"] == "CantidadItem":
            i["x"], i["y"] = x + 11, BY + 9
            for v in i["initialVariables"]:
                if v["name"] == "SX": v["value"] = x + 19

# ---------- eventos ----------
hud = next(e for e in d["externalEvents"] if e["name"] == "HUD")
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
for e in recorrer(hud["events"]):
    for a in e.get("actions") or []:
        a["parameters"] = [p.replace("38 * min(1, Exp / ExpSiguiente)", "24 * min(1, Exp / ExpSiguiente)")
                           .replace("397 - HudMonedas.Width()", "%d - HudMonedas.Width()" % (X0 + 44)) for p in a["parameters"]]
U = [COM("UI compacta: la barra rapida usa casillas de 20px e iconos <Id>_mini (la mochila abierta sigue en grande)"),
     EV([C("SceneJustBegins", "")], [], [
         EV([objv_s("CantidadItem", "Grupo", q("Barra"))], [A("TextObject::Text::SetFontSize", "CantidadItem", "=", "8")])]),
     EV([objv_s("SlotUI", "Grupo", q("Barra"))], [anim("SlotUI", '"Mini" + SlotUI.Animation::Name()')]),
     FOREACH("IconoItem", [objv_s("IconoItem", "Grupo", q("Barra")), isv("Mochila[IconoItem.Indice].Id", '""', "!=")],
             [anim("IconoItem", 'Mochila[IconoItem.Indice].Id + "_mini"')])]
ext = next((e for e in d["externalEvents"] if e["name"] == "UICompacta"), None)
if ext is None:
    d["externalEvents"].append({"associatedLayout": "Nivel 01", "name": "UICompacta", "events": U})
else:
    ext["events"] = U
pers = next(e for e in d["externalEvents"] if e["name"] == "Personaje")
if not any(e.get("target") == "UICompacta" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("UICompacta"))
json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: interfaz compacta")
