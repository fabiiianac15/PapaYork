"""La papelera no debe abrir la partida: se calcula SobreBotonUI (mouse sobre un boton visible) antes del clic en la ranura.
(Una condicion invertida "cursor NO sobre BotonUI" es verdadera si existe ALGUN boton sin el mouse, asi que no servia.)"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
menu = next(l for l in d["layouts"] if l["name"] == "Menu Principal")
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
for e in recorrer(menu["events"]):
    conds = e.get("conditions") or []
    if any(c["type"]["value"] == "IsCursorOnObject" and c["parameters"][0] == "RanuraPartida" for c in conds) and \
            any(c["type"]["value"] == "MouseButtonFromTextReleased" for c in conds):
        e["conditions"] = [c for c in conds if not (c["type"]["value"] == "IsCursorOnObject" and c["parameters"][0] == "BotonUI")]
        if not any(c["parameters"][:1] == ["SobreBotonUI"] for c in e["conditions"]): e["conditions"].append(ibv("SobreBotonUI", "False"))
menu["variables"] = [v for v in menu["variables"] if v["name"] != "SobreBotonUI"] + [var("SobreBotonUI", "boolean", False)]
menu["events"] = [e for e in menu["events"] if not any(a["parameters"][:1] == ["SobreBotonUI"] for a in e.get("actions") or [])]
i = next(k for k, e in enumerate(menu["events"]) if any(c["type"]["value"] == "SceneJustBegins" for c in e.get("conditions") or [])) + 1
menu["events"].insert(i, EV([], [bv("SobreBotonUI", "False")], [EV([cursor("BotonUI"), C("Visible", "BotonUI")], [bv("SobreBotonUI", "True")])]))
json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok")
