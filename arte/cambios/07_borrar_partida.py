"""Boton de papelera en cada partida guardada: primer clic pide confirmacion, el segundo la borra."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
menu = next(l for l in d["layouts"] if l["name"] == "Menu Principal")
MO = {o["name"]: o for o in menu["objects"]}
SAVE = q("PapayorkPartidas")
def slot(num, extra=""): return '"Ranura" + ToString(' + num + ')' + (' + "/' + extra + '"' if extra else "")
for f in ("BorrarNormal", "BorrarHover"): add_resource(d, "image", "Menu/" + f + ".png", "Menu/" + f + ".png")
b = MO["BotonUI"]
b["animations"] = [a for a in b["animations"] if not a["name"].startswith("Borrar")] + [
    anim_def("BorrarNormal", [frame("Menu/BorrarNormal.png")]), anim_def("BorrarHover", [frame("Menu/BorrarHover.png")])]
if not any(v["name"] == "Numero" for v in b["variables"]): b["variables"].append(var("Numero", "number", 0))
menu["variables"] = [v for v in menu["variables"] if v["name"] != "ConfirmarBorrar"] + [var("ConfirmarBorrar", "number", 0)]
menu["instances"] = [i for i in menu["instances"] if not (i["name"] == "BotonUI" and any(v["name"] == "Accion" and v["value"] == "Borrar" for v in i["initialVariables"]))]
for n in range(3):
    menu["instances"].append(inst("BotonUI", 348, 270 + 15 + 38 + n * 48 + 14, "UI", 6, variables=[
        var("Accion", "string", "Borrar"), var("Pantalla", "string", "Partidas"), var("Tipo", "string", "Borrar"), var("Numero", "number", n + 1)]))

def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
def tipos(e): return [(c["type"]["value"], c["parameters"][:1]) for c in e.get("conditions") or []]
for e in recorrer(menu["events"]):
    t = tipos(e)
    if ("IsCursorOnObject", ["RanuraPartida"]) in t and ("MouseButtonFromTextReleased", [""]) in t \
            and not any(c["type"]["value"] == "IsCursorOnObject" and c["parameters"][0] == "BotonUI" for c in e["conditions"]):
        e["conditions"].append(cursor("BotonUI", inv=True))      # clic en la papelera no abre la partida
    if ("StringObjectVariable", ["BotonUI"]) in t and ("IsCursorOnObject", ["BotonUI"]) in t and ("MouseButtonFromTextReleased", [""]) in t:
        e["events"] = [s for s in e["events"] if "Borrar" not in json.dumps(s.get("conditions", []))]
        e["events"].append(EV([objv_s("BotonUI", "Accion", q("Borrar")), C("GroupExists", SAVE, slot("BotonUI.Numero", "Escena"))], [bv("Hecho", "False")], [
            EV([inv_("ConfirmarBorrar", "BotonUI.Numero")], [A("DeleteGroupFichier", SAVE, slot("BotonUI.Numero")), nv("ConfirmarBorrar", "0"), bv("Hecho", "True")], [
                EV([objv_n("TextoRanura", "Numero", "BotonUI.Numero")], [txt("TextoRanura", '"Partida " + ToString(TextoRanura.Numero) + NewLine() + "Vacía"')])]),
            EV([ibv("Hecho", "False"), inv_("ConfirmarBorrar", "BotonUI.Numero", "!=")], [nv("ConfirmarBorrar", "BotonUI.Numero")], [
                EV([objv_n("TextoRanura", "Numero", "BotonUI.Numero")], [
                    txt("TextoRanura", '"¿Borrar la partida " + ToString(TextoRanura.Numero) + " para siempre?" + NewLine() + "Clic otra vez en la papelera"')])])],
            variables=[var("Hecho", "boolean", False)]))
# la papelera solo se ve si la ranura tiene partida
menu["events"] = [e for e in menu["events"] if not (e.get("type") == "BuiltinCommonInstructions::ForEach" and e.get("object") == "BotonUI")]
menu["events"].append(FOREACH("BotonUI", [objv_s("BotonUI", "Accion", q("Borrar"))], [hide("BotonUI"), A("SetX", "BotonUI", "=", "-100")], [
    EV([C("GroupExists", SAVE, slot("BotonUI.Numero", "Escena"))], [show("BotonUI"), A("SetX", "BotonUI", "=", "348")])]))
json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: borrar partida")
