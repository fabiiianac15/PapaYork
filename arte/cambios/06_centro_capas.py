"""Con zoom 2, las capas de interfaz deben mirar al centro de la pantalla original (240, 135)."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
for lay in d["layouts"]:
    i = next(k for k, e in enumerate(lay["events"]) if e.get("type", "").endswith("Comment") and "Zoom 2" in e.get("comment", ""))
    ev = lay["events"][i + 1]
    capas = [l["name"] for l in lay["layers"] if l["name"] != "UIHD"]
    acts = [A("ZoomCamera", "", "2", q(c), "0") for c in capas]
    for c in capas:
        if c == "Luz Exterior" or (c == "" and lay["name"] in ("Nivel 01", "Nivel 02", "Pueblo")): continue   # siguen a Pedro
        acts += [A("SetCameraCenterX", "", "=", "240", q(c), "0"), A("SetCameraCenterY", "", "=", "135", q(c), "0")]
    ev["actions"] = acts
json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok")
