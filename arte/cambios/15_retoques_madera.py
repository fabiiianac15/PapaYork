"""Corrige el script 13: cada pieza de cerca vuelve a su forma original, el muelle usa madera en sus dos
animaciones y los cuadritos de agua sueltos dejan de tener orilla."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *

P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}


def img(ruta):
    nombre = "Natural/" + ruta
    add_resource(d, "image", nombre, nombre)
    return nombre


# Orden original de las animaciones de la cerca: 1=Vaya7, 2=Vaya1, 3=Vaya2 ... 7=Vaya6
ORIGINAL = {"1": 7, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6}
for a in O["Vaya"]["animations"]:
    a["directions"][0]["sprites"][0]["image"] = img(f"Madera/Vaya{ORIGINAL[a['name']]}.png")
for a, arch in zip(O["PlatPesc"]["animations"], ("Muelle", "Muelle1")):
    a["directions"][0]["sprites"][0]["image"] = img(f"Madera/{arch}.png")

quitadas = 0
for l in d["layouts"]:
    celdas = {(i["x"], i["y"]) for i in l["instances"] if i["name"] == "Agua2"}
    sueltas = {c for c in celdas if not any((c[0] + a, c[1] + b) in celdas for a, b in ((32, 0), (-32, 0), (0, 32), (0, -32)))}
    antes = len(l["instances"])
    l["instances"] = [i for i in l["instances"] if not (i["name"] == "Orilla" and (i["x"], i["y"]) in sueltas)]
    quitadas += antes - len(l["instances"])
print("orillas quitadas:", quitadas)

with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok")
