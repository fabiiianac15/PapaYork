"""Ningún árbol tapa las calles nuevas del Pueblo: los grandes se mueven y los pequeños que estorban se quitan."""
import json, sys
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
pu = next(l for l in d["layouts"] if l["name"] == "Pueblo")
CALLES = [(1200, 368, 1400, 64), (1760, 368, 224, 160), (2272, 304, 64, 96), (2336, 400, 64, 192), (2352, 560, 192, 64), (2464, 112, 64, 288), (1680, 352, 80, 32), (1984, 352, 72, 32), (1640, 432, 40, 200), (2180, 432, 40, 200), (1040, 430, 40, 180)]
def caja(i, x=None, y=None):
    x, y = i["x"] if x is None else x, i["y"] if y is None else y
    ex, ey = (i["width"] / 64, i["height"] / 80) if i.get("customSize") else (1, 1)
    return x - 26 * ex, y - 76 * ey, x + 26 * ex, y
def pisa(c): return any(c[0] < a + w and c[2] > a and c[1] < b + h and c[3] > b for a, b, w, h in CALLES)
mov, quit_ = [], []
nuevos = []
for i in pu["instances"]:
    if i["name"] in ("Arbol", "Arbol_2", "Arbol_3") and pisa(caja(i)):
        if i.get("customSize"):
            for dy in range(32, 480, 32):
                if not pisa(caja(i, y=i["y"] + dy)):
                    mov.append((i["x"], i["y"], i["y"] + dy)); i["y"] += dy; i["zOrder"] = i["y"]; break
            nuevos.append(i)
        else:
            quit_.append((i["x"], i["y"]))
            continue
        continue
    nuevos.append(i)
pu["instances"] = nuevos
print("movidos", mov, "quitados", quit_)
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
