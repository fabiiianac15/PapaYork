"""Inventario propio de PapaYork: madera, lino y detalles radiactivos, con la pestaña nueva de Vecinos.
Conserva las posiciones de las casillas, así que toda la lógica de la mochila sigue igual."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
if any(a["name"] == "Vecinos" for a in O["PestanaPausa"]["animations"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
def img(r):
    n = "Natural/UI/" + r + ".png"
    add_resource(d, "image", n, n)
    return n
def poner(obj, anim, r):
    a = next(x for x in O[obj]["animations"] if x["name"] == anim)
    for fr in a["directions"][0]["sprites"]:
        fr["image"] = img(r)
poner("PanelMochila", "", "PanelMochila"); poner("PanelFabricar", "", "PanelMochila"); poner("PanelPausa", "Panel", "PanelPausa")
poner("PanelTienda", "", "PanelTienda"); poner("BarraRapida", "", "BarraRapida"); poner("EtiquetaItem", "", "EtiquetaItem")
for an, r in (("Normal", "Casilla"), ("Hover", "CasillaHover"), ("Seleccionada", "CasillaSeleccionada")):
    poner("SlotUI", an, r)
for n in ("Mochila", "Opciones", "Salir"):
    poner("PestanaPausa", n, "Pestana" + n); poner("PestanaPausa", n + "Activa", f"Pestana{n}Activa")
for n in ("Vecinos", "VecinosActiva"):
    O["PestanaPausa"]["animations"].append(anim_def(n, [frame(img("Pestana" + n))]))
lay = next(l for l in d["externalLayouts"] if l["name"] == "InventarioStardew")
X = {"Mochila": 286, "Vecinos": 316, "Opciones": 346, "Salir": 376}
tabs = [i for i in lay["instances"] if i["name"] == "PestanaPausa"]
for i in tabs:
    i["x"] = X[next(v["value"] for v in i["initialVariables"] if v["name"] == "Pestana")]
n = inst("PestanaPausa", X["Vecinos"], 14, layer="Inventario", z=505, variables=[var("Pestana", "string", "Vecinos")])
lay["instances"].append(n)
# ---------- Textos oscuros y sin borde, legibles sobre el lino ----------
TEXTOS = ("TituloMochila", "AyudaMochila", "TextoInfoNombre", "TextoInfoTipo", "TextoInfoDesc", "TituloTienda", "DineroTienda", "NombreTienda",
          "DetalleTienda", "DescTienda", "TituloFabricar", "AyudaFabricar", "TextoIngredientes")
for t in TEXTOS:
    c = O[t]["content"]
    c["isOutlineEnabled"], c["color"] = False, "70;40;20"
    O[t]["color"] = {"r": 70, "g": 40, "b": 20}


def oscurecer(evs):
    n = 0
    for e in evs:
        for a in e.get("actions", []) or []:
            if a["type"]["value"] == "TextObject::ChangeColor" and a["parameters"][0] in TEXTOS:
                r, g, b_ = map(int, a["parameters"][1].strip('"').split(";"))
                if r * .3 + g * .59 + b_ * .11 > 120:
                    a["parameters"][1] = q(f"{int(r * .55)};{int(g * .55)};{int(b_ * .55)}")
                    n += 1
            if a["type"]["value"] == "TextObject::Text::SetOutlineEnabled" and a["parameters"][0] in TEXTOS:
                a["parameters"][1] = "no"
        n += oscurecer(e.get("events", []) or [])
    return n


print("colores de texto ajustados:", sum(oscurecer(x["events"]) for x in d["externalEvents"]))

# ---------- Una casilla más de oferta en las tiendas (para la caña) y un poco más juntas ----------
def valor(i, nombre):
    return next((v.get("value") for v in i.get("initialVariables", []) if v["name"] == nombre), None)
oferta = [i for i in lay["instances"] if valor(i, "Grupo") == "Oferta"]
assert oferta and max(valor(i, "Indice") for i in oferta) == 5
sextos = []
for i in oferta:
    k = valor(i, "Indice")
    if k == 5:
        sextos.append(json.loads(json.dumps(i)))
    i["x"] -= 8 * k
    for v in i["initialVariables"]:
        if v["name"] == "SX":
            v["value"] -= 8 * k
for i in sextos:
    i["persistentUuid"] = uid()
    for v in i["initialVariables"]:
        if v["name"] == "Indice":
            v["value"] = 6
    lay["instances"].append(i)

# Las descripciones largas pasan a la línea siguiente
ev = next(x for x in d["externalEvents"] if x["name"] == "Dialogo")["events"][1]["actions"]
ajuste = [a for a in ev if a["parameters"] and a["parameters"][0] == "TextoDialogo" and "Wrap" in a["type"]["value"]]
assert len(ajuste) == 2
ini = next(x for x in d["externalEvents"] if x["name"] == "Tienda")["events"][1]["actions"]
for t in ("DescTienda", "TextoInfoDesc"):
    for a in ajuste:
        c = json.loads(json.dumps(a)); c["parameters"][0] = t
        if c["parameters"][-1] == "610": c["parameters"][-1] = "345"
        ini.append(c)
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
