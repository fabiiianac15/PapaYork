"""Interfaz nitida: el juego pasa a dibujarse a 960x540.

- Todas las capas que ya existian llevan zoom 2 (el mundo, la barra de vida y los menus grandes se ven igual que antes).
- Capa nueva "UIHD" sin zoom para la barra rapida y el panel de la hora: ocupan poco en pantalla pero usan los
  iconos originales de 32px, asi que se ven nitidos (como la interfaz de Stardew, que va a mas resolucion que el mundo).
- Se deshace la barra con iconos encogidos de 16px (cambio 02).
"""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
def ext(n): return next(e for e in d["externalEvents"] if e["name"] == n)

d["properties"]["windowWidth"], d["properties"]["windowHeight"] = 960, 540

# ---------- capas: UIHD en los niveles y zoom 2 en todas las demas ----------
NIVELES = ("Nivel 01", "Nivel 02", "Pueblo")
for lay in d["layouts"]:
    if lay["name"] in NIVELES and not any(l["name"] == "UIHD" for l in lay["layers"]):
        nueva = copy.deepcopy(next(l for l in lay["layers"] if l["name"] == "Inventario")); nueva["name"] = "UIHD"; nueva["effects"] = []
        i = next(k for k, l in enumerate(lay["layers"]) if l["name"] == "Inventario")
        lay["layers"].insert(i, nueva)
    capas = [l["name"] for l in lay["layers"] if l["name"] != "UIHD"]
    zoom = EV([C("SceneJustBegins", "")], [A("ZoomCamera", "", "2", q(c), "0") for c in capas])
    zoom["_zoom2"] = True
    lay["events"] = [e for e in lay["events"] if not e.get("_zoom2") and not
                     (e.get("type", "").endswith("Comment") and "Zoom 2" in e.get("comment", ""))]
    lay["events"][0:0] = [COM("Zoom 2 en todas las capas: el juego se dibuja a 960x540 y la capa UIHD (barra y reloj) va sin zoom"), zoom]
for lay in d["layouts"]:
    for e in lay["events"]: e.pop("_zoom2", None)

# ---------- volver a las imagenes grandes de la barra y el panel ----------
def cambiar_imagen(obj, anim, img):
    for a in O[obj]["animations"]:
        if a["name"] == anim:
            for s in a["directions"][0]["sprites"]: s["image"] = img
cambiar_imagen("HudPanel", "", "HUD/HudPanel.png")
for i in range(6): cambiar_imagen("HudDial", str(i), "HUD/Dial%d.png" % i)
for i in range(4): cambiar_imagen("HudEstacion", str(i), "HUD/Estacion%d.png" % i)
cambiar_imagen("HudMoneda", "", "HUD/HudMoneda.png")
cambiar_imagen("HudExpMarco", "", "HUD/HudExpMarco.png")
cambiar_imagen("HudExpRelleno", "", "HUD/HudExpRelleno.png")
cambiar_imagen("BarraRapida", "", "Inventario/BarraRapida.png")
cambiar_imagen("EtiquetaItem", "", "Inventario/EtiquetaItem.png")
def tam_texto(obj, size):
    O[obj]["characterSize"] = size
    if "content" in O[obj]: O[obj]["content"]["characterSize"] = size
for t, s in [("HudFecha", 11), ("HudHora", 11), ("HudMonedas", 11), ("HudNivel", 10), ("TextoEtiqueta", 11)]: tam_texto(t, s)

# ---------- posiciones en la capa UIHD (coordenadas de 960x540) ----------
lay = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
X0, Y0 = 804, 6
HUD = {"HudPanel": (X0, Y0), "HudDial": (X0 + 4, Y0 + 4), "HudFecha": (X0 + 45, Y0 + 5), "HudEstacion": (X0 + 126, Y0 + 5),
       "HudHora": (X0 + 45, Y0 + 23), "HudMoneda": (X0 + 7, Y0 + 42), "HudMonedas": (X0 + 40, Y0 + 42), "HudNivel": (X0 + 80, Y0 + 42),
       "HudExpMarco": (X0 + 102, Y0 + 45), "HudExpRelleno": (X0 + 103, Y0 + 46),
       "BarraRapida": (304, 492), "EtiquetaItem": (420, 472), "TextoEtiqueta": (430, 474)}
BX, BY = 310, 496
for i in lay["instances"]:
    if i["name"] in HUD:
        i["x"], i["y"] = HUD[i["name"]]; i["layer"] = "UIHD"
        if i["name"] == "HudExpRelleno": i["width"], i["height"] = 38, 6
    g = {v["name"]: v["value"] for v in i.get("initialVariables", [])}
    if g.get("Grupo") == "Barra":
        k = int(g["Indice"]); x = BX + k * 34; i["layer"] = "UIHD"
        if i["name"] == "SlotUI": i["x"], i["y"] = x, BY
        if i["name"] == "IconoItem": i["x"], i["y"] = x + 17, BY + 17
        if i["name"] == "CantidadItem":
            i["x"], i["y"] = x + 18, BY + 20
            for v in i["initialVariables"]:
                if v["name"] == "SX": v["value"] = x + 31

# ---------- eventos que dependian del tamano ----------
for e in recorrer(ext("HUD")["events"]):
    for a in e.get("actions") or []:
        a["parameters"] = [p.replace("24 * min(1, Exp / ExpSiguiente)", "38 * min(1, Exp / ExpSiguiente)")
                           .replace("424 - HudMonedas.Width()", "%d - HudMonedas.Width()" % (X0 + 71)) for p in a["parameters"]]
for e in recorrer(ext("Inventario")["events"]):
    for a in e.get("actions") or []:
        if a["type"]["value"] == "SetCenterX" and a["parameters"][0] == "TextoEtiqueta": a["parameters"][2] = "480"
pers = ext("Personaje")
pers["events"] = [e for e in pers["events"] if not (e.get("type") == "BuiltinCommonInstructions::Link" and e.get("target") == "UICompacta")]
d["externalEvents"] = [e for e in d["externalEvents"] if e["name"] != "UICompacta"]

json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: interfaz a 960x540")
