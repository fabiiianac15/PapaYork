"""Don Fermín quedaba oculto detrás de su letrero y su yunque: ahora está de pie junto al yunque."""
import json, sys
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
pueblo = next(l for l in d["layouts"] if l["name"] == "Pueblo")
fermin = next(i for i in pueblo["instances"] if i["name"] == "NPC" and
              any(v["name"] == "Tienda" and v.get("value") == "Herreria" for v in i.get("initialVariables", [])))
if fermin["x"] != 895:
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
fermin["x"] = 871
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok")
