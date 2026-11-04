"""Las papas retroceden al recibir un golpe y la barra de vida pasa a ser un panel de madera con Pedro y sus gestos."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}; EXT = {e["name"]: e for e in d["externalEvents"]}; XL = {x["name"]: x for x in d["externalLayouts"]}
if "VidaPanel" in O:
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
PJ = "Personaje_jugador"
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def img(r):
    n = "Natural/Vida/" + r + ".png"; add_resource(d, "image", n, n); return n
# ---------- Retroceso ----------
O["Papa"]["variables"] += [var("EmpujeT", "number", 0), var("EmpujeVX", "number", 0), var("EmpujeVY", "number", 0)]
per = EXT["Personaje"]["events"]
golpe = next(e for e in per if e.get("conditions") and e["conditions"][0]["parameters"][:2] == ["CajaDaño", "Papa"])
fe = golpe["events"][0]; assert fe.get("object") == "Papa"
ANG = f"AngleBetweenPositions({PJ}.CenterX(), {PJ}.CenterY(), Papa.CenterX(), Papa.CenterY()) * 3.14159 / 180"
fe["actions"][:0] = [set_objv_n("Papa", "EmpujeT", "0.42"), set_objv_n("Papa", "EmpujeVX", f"cos({ANG}) * 430"), set_objv_n("Papa", "EmpujeVY", f"sin({ANG}) * 430"), A("ChangeColor", "Papa", q("255;115;115"))]
fe["events"].insert(0, EV([objv_s("Papa", "Tipo", q("Gigante"))], [set_objv_n("Papa", "EmpujeVX", "0.45", "*"), set_objv_n("Papa", "EmpujeVY", "0.45", "*")]))
# Mientras vuela no hace daño a Pedro
toque = next(e for e in per if e.get("conditions") and e["conditions"][0]["parameters"][:2] == [PJ, "Papa"])
toque["conditions"].insert(1, objv_n("Papa", "EmpujeT", "0", "<="))
# Va al final de MovAuto4Dir: es lo último que mueve a las papas, y así anula su persecución mientras retroceden
EXT["MovAuto4Dir"]["events"] += [COM("Retroceso de las papas al recibir un golpe"), FOREACH("Papa", [objv_n("Papa", "EmpujeT", "0", ">"), ibv("InventarioAbierto", "False")], [
    A("Arreter", "Papa"), A("AddForceXY", "Papa", "Papa.EmpujeVX", "Papa.EmpujeVY", "0"), set_objv_b("Papa", "PuedeAndar", "False"),
    set_objv_n("Papa", "EmpujeVX", "pow(0.001, TimeDelta())", "*"), set_objv_n("Papa", "EmpujeVY", "pow(0.001, TimeDelta())", "*"), set_objv_n("Papa", "EmpujeT", "TimeDelta()", "-"), A("SeparateFromObjects", "Papa", "Colision", "")], [
    EV([objv_n("Papa", "EmpujeT", "0", "<=")], [A("ChangeColor", "Papa", q("255;255;255"))], [
        EV([objv_s("Papa", "Tipo", q("Brillante"))], [A("ChangeColor", "Papa", q("170;255;130"))]),
        EV([objv_s("Papa", "Tipo", q("Gigante"))], [A("ChangeColor", "Papa", q("255;190;190"))])])])]
# ---------- Panel de vida ----------
BX, BY = 81, 42            # donde empieza la barra dentro de la pantalla
for x in ("Interfaz", "Interfaz 2"):
    XL[x]["instances"] = [i for i in XL[x]["instances"] if i["name"] not in ("Marco_Barravida", "BarraVida")]
for ob in (sprite_obj("VidaPanel", [anim_def("N", [frame(img("Panel"))])], tween=False),
           sprite_obj("VidaRelleno", [anim_def(c, [frame(img(c))]) for c in ("Verde", "Amarillo", "Rojo")], tween=False),
           sprite_obj("VidaRastroBar", [anim_def("N", [frame(img("Rastro"))])], tween=False),
           sprite_obj("VidaMarcas", [anim_def("N", [frame(img("Marcas"))])], tween=False),
           sprite_obj("VidaRetrato", [anim_def("Normal", [frame(img("PedroNormal"))] * 16 + [frame(img("PedroParpadeo"))], loop=True, dt=.22), anim_def("Herido", [frame(img("PedroHerido"))]), anim_def("Critico", [frame(img("PedroCritico"))] * 9 + [frame(img("PedroParpadeo"))], loop=True, dt=.2)], tween=False),
           sprite_obj("VidaNum", [anim_def(c, [frame(img("Num" + c))]) for c in "0123456789"], variables=[var("Pos", "number", 0)], tween=False)):
    set_global_object(d, ob)
hud = XL["InventarioStardew"]["instances"]
hud += [inst("VidaPanel", 8, 6, layer="UIHD", z=40), inst("VidaRastroBar", BX, BY, layer="UIHD", z=41), inst("VidaRelleno", BX, BY, layer="UIHD", z=42), inst("VidaMarcas", BX, BY, layer="UIHD", z=43), inst("VidaRetrato", 13, 6, layer="UIHD", z=44), inst("VidaNum", 8 + 165, 15, layer="UIHD", z=44, variables=[var("Pos", "number", 10)]), inst("VidaNum", 8 + 177, 15, layer="UIHD", z=44, variables=[var("Pos", "number", 1)])]
for v, val in (("VidaPct", 1), ("VidaRastro", 50), ("VidaAntes", 50), ("VidaGolpeT", 0), ("VidaEntera", 50)): set_global_var(d, var(v, "number", val))
V_ = f"{PJ}.Vida"; W_ = lambda o, val: A("ResizableCapability::ResizableBehavior::SetWidth", o, "Resizable", "=", val)
EXT["HUD"]["events"] += [COM("PANEL DE VIDA: Pedro cambia de gesto, la barra cambia de color y lo perdido se vacia despacio"),
    EV([C("SceneJustBegins", "")], [nv("VidaRastro", V_), nv("VidaAntes", V_), nv("VidaGolpeT", "0")]),
    EV([], [nv("VidaPct", f"clamp({V_} / 50, 0, 1)"), W_("VidaRelleno", "150 * VidaPct"), nv("VidaEntera", f"clamp(ceil({V_}), 0, 99)"), nv("VidaGolpeT", "max(0, VidaGolpeT - TimeDelta())")]),
    EV([objv_n("VidaNum", "Pos", "1")], [anim("VidaNum", "ToString(mod(VidaEntera, 10))")]),
    EV([objv_n("VidaNum", "Pos", "10")], [anim("VidaNum", "ToString(floor(VidaEntera / 10))"), show("VidaNum")]),
    EV([objv_n("VidaNum", "Pos", "10"), cmp_("VidaEntera", "<", "10")], [hide("VidaNum")]),
    EV([cmp_(V_, "<", "VidaAntes")], [nv("VidaGolpeT", "0.5")]),
    EV([], [nv("VidaAntes", V_), nv("VidaRastro", f"max({V_}, VidaRastro - 22 * TimeDelta())"), W_("VidaRastroBar", "150 * clamp(VidaRastro / 50, 0, 1)"), A("ChangeColor", "VidaRetrato", q("255;255;255")), A("SetX", "VidaRetrato", "=", "13"), opacity("VidaRelleno", 255)]),
    EV([cmp_("VidaPct", ">", "0.5")], [anim("VidaRelleno", q("Verde"))]),
    EV([cmp_("VidaPct", "<=", "0.5"), cmp_("VidaPct", ">", "0.25")], [anim("VidaRelleno", q("Amarillo"))]),
    EV([cmp_("VidaPct", "<=", "0.25")], [anim("VidaRelleno", q("Rojo")), opacity("VidaRelleno", "190 + 65 * sin(TimeFromStart() * 7)")]),
    EV([cmp_("VidaPct", ">", "0.3")], [anim("VidaRetrato", q("Normal"))]),
    EV([cmp_("VidaPct", "<=", "0.3")], [anim("VidaRetrato", q("Critico"))]),
    EV([cmp_("VidaGolpeT", ">", "0")], [anim("VidaRetrato", q("Herido")), A("ChangeColor", "VidaRetrato", q("255;150;150")), A("SetX", "VidaRetrato", "=", "13 + sin(TimeFromStart() * 55) * 2 * VidaGolpeT * 2")])]
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
