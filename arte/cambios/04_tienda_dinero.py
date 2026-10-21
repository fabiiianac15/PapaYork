"""El dinero de la tienda va a la derecha de las ofertas (no encima del saludo del vendedor)."""
import json, sys
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
lay = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
for i in lay["instances"]:
    if i["name"] == "DineroTienda": i["x"], i["y"] = 360, 12 + 40
tienda = next(e for e in d["externalEvents"] if e["name"] == "Tienda")
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
for e in recorrer(tienda["events"]):
    for a in e.get("actions") or []:
        if a["parameters"][:1] == ["DineroTienda"] and a["type"]["value"].endswith("SetValue"):
            a["parameters"][3] = '"Tienes" + NewLine() + ToString(Monedas) + " monedas"'
json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok")
