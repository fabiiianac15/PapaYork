"""Mundo persistente, calendario y panel de la esquina (estilo Stardew).

Se aplica despues de generar_recursos.py y antes de generar_menu.py.

- Calendario: 28 dias por estacion (Primavera, Verano, Otono, Invierno). Pasa un dia cuando el reloj llega a las 12 AM.
- Lo que destruyes se queda destruido: arboles, rocas y vetas vuelven cuando cambia la estacion; la hierba a los 3 dias.
  Si en ese lugar ahora hay tierra arada, no vuelve a salir. Lo que recoges del mapa no reaparece nunca.
- La granja se guarda: tierra arada y cultivos (con su etapa) siguen ahi al volver a la zona.
- Panel de la esquina con el cielo del momento del dia, fecha, estacion, hora, monedas, nivel y barra de experiencia.
  Reemplaza al Score: ahora se gana experiencia al pelear, talar, picar y cosechar, y monedas al vencer papas.

Uso: python3 arte/generar_mundo.py "Legado Radioactivo-Papayork.json"
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gdutil import *

PROJ = sys.argv[1]
d = json.load(open(PROJ, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
def cmp(a, op, b): return C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
def accion(e, tipo, *params):
    return any(a["type"]["value"] == tipo and a["parameters"][:len(params)] == list(params) for a in e.get("actions") or [])
def tiene(e, tipo, *params):
    return any(c["type"]["value"] == tipo and c["parameters"][:len(params)] == list(params) for c in e.get("conditions") or [])
def ext(nombre): return next(e for e in d["externalEvents"] if e["name"] == nombre)
def arr(name, values): return {"name": name, "type": "array", "children": [{"type": "string", "value": v} for v in values]}

# ---------- variables globales ----------
set_global_var(d, struct("Calendario", [var("Dia", "number", 1), var("Estacion", "number", 0), var("Anio", "number", 1),
                                        var("DiaTotal", "number", 1)]))
set_global_var(d, arr("NombresDia", ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]))
set_global_var(d, arr("NombresEstacion", ["Primavera", "Verano", "Otoño", "Invierno"]))
set_global_var(d, struct("Granja", []))
for v in [var("Exp", "number", 0), var("NivelJugador", "number", 1), var("ExpSiguiente", "number", 50),
          var("Monedas", "number", 0), var("MonedasGanadas", "number", 0)]:
    set_global_var(d, v)

# ---------- recursos ----------
HUD_IMG = ["HudPanel", "HudExpMarco", "HudExpRelleno", "HudMoneda"] + ["Dial%d" % i for i in range(6)] + ["Estacion%d" % i for i in range(4)]
for n in HUD_IMG: add_resource(d, "image", "HUD/" + n + ".png", "HUD/" + n + ".png")
for n in ["Moneda", "SubirNivel"]: add_resource(d, "audio", "HUD/" + n + ".wav", "HUD/" + n + ".wav")

# ---------- objetos del panel ----------
for o in [
    sprite_obj("HudPanel", [anim_def("", [frame("HUD/HudPanel.png")])], tween=False),
    sprite_obj("HudDial", [anim_def(str(i), [frame("HUD/Dial%d.png" % i)]) for i in range(6)], tween=False),
    sprite_obj("HudEstacion", [anim_def(str(i), [frame("HUD/Estacion%d.png" % i)]) for i in range(4)], tween=False),
    sprite_obj("HudMoneda", [anim_def("", [frame("HUD/HudMoneda.png")])], tween=False),
    sprite_obj("HudExpMarco", [anim_def("", [frame("HUD/HudExpMarco.png")])], tween=False),
    sprite_obj("HudExpRelleno", [anim_def("", [frame("HUD/HudExpRelleno.png")])], tween=False),
    text_obj("HudFecha", "Lun. 1", 11, (255, 246, 210), None),
    text_obj("HudHora", "12:00 PM", 11, (255, 246, 210), None),
    text_obj("HudMonedas", "0", 11, (251, 242, 54), None),
    text_obj("HudNivel", "Nv 1", 10, (214, 255, 106), None),
]:
    set_global_object(d, o)
X0, Y0 = 326, 4
lay_inv = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
lay_inv["instances"] = [i for i in lay_inv["instances"] if not i["name"].startswith("Hud")] + [
    inst("HudPanel", X0, Y0, "Inventario", 40), inst("HudDial", X0 + 4, Y0 + 4, "Inventario", 41),
    inst("HudFecha", X0 + 45, Y0 + 5, "Inventario", 42), inst("HudEstacion", X0 + 126, Y0 + 5, "Inventario", 42),
    inst("HudHora", X0 + 45, Y0 + 23, "Inventario", 42), inst("HudMoneda", X0 + 7, Y0 + 42, "Inventario", 42),
    inst("HudMonedas", X0 + 40, Y0 + 42, "Inventario", 42), inst("HudNivel", X0 + 80, Y0 + 42, "Inventario", 42),
    inst("HudExpMarco", X0 + 102, Y0 + 45, "Inventario", 42),
    inst("HudExpRelleno", X0 + 103, Y0 + 46, "Inventario", 43, 38, 6)]

# ---------- quitar el Score viejo ----------
for x in d["externalLayouts"]:
    x["instances"] = [i for i in x["instances"] if i["name"] not in ("NombreScore", "Text_Score")]
pers = ext("Personaje")
for e in recorrer(pers["events"]):
    if accion(e, "SetNumberVariable", "Score", "+"):
        e["actions"] = [nv("Exp", "1", "+")]       # cada golpe a una papa da 1 de experiencia
for lay in d["layouts"]:
    for e in recorrer(lay["events"]):
        if e.get("actions"):
            e["actions"] = [a for a in e["actions"] if not (a["type"]["value"] == "SetNumberVariable" and a["parameters"][0] == "Score")]

# ---------- reloj: el texto viejo se reemplaza por el panel y pasa el dia a las 12 AM ----------
reloj = ext("RelojProg")
for e in recorrer(reloj["events"]):
    if e.get("actions"):
        e["actions"] = [a for a in e["actions"] if "RelojText" not in json.dumps(a)]
pasa_dia = EV([isv("Reloj.M", q("AM"))], [nv("Calendario.Dia", "1", "+"), nv("Calendario.DiaTotal", "1", "+")], [
    EV([inv_("Calendario.Dia", "28", ">")], [nv("Calendario.Dia", "1"), nv("Calendario.Estacion", "1", "+")], [
        EV([inv_("Calendario.Estacion", "3", ">")], [nv("Calendario.Estacion", "0"), nv("Calendario.Anio", "1", "+")])])])
for e in recorrer(reloj["events"]):
    if tiene(e, "NumberVariable", "Reloj.Hora", ">", "11") and accion(e, "SetBooleanVariable", "Reloj.Mediodia"):
        if not any(s.get("conditions") == pasa_dia["conditions"] for s in e.get("events", [])):
            e.setdefault("events", []).append(COM("A las 12 AM empieza un dia nuevo"))
            e["events"].append(pasa_dia)
        break
else:
    raise SystemExit("no encontre el cambio de AM/PM en RelojProg")

# ---------- Herramientas: lo destruido guarda el dia, y la granja se registra ----------
herr = ext("Herramientas")
for e in recorrer(herr["events"]):
    for a in e.get("actions") or []:
        if a["type"]["value"] == "SetBooleanVariable" and a["parameters"][0].startswith("Destruidos["):
            a["type"]["value"] = "SetNumberVariable"; a["parameters"] = [a["parameters"][0], "=", "Calendario.DiaTotal"]
CLAVE_REJILLA = 'CurrentSceneName() + "_" + ToString(Rejilla.X() + Rejilla.Xcelda()) + "_" + ToString(Rejilla.Y() + Rejilla.Ycelda())'
CLAVE_SUELO = 'CurrentSceneName() + "_" + ToString(SueloPreparado.X()) + "_" + ToString(SueloPreparado.Y())'
for e in recorrer(herr["events"]):
    if accion(e, "Create", "", "SueloPreparado") and not tiene(e, "VariableChildExists2", "Granja"):
        e["conditions"].append(C("VariableChildExists2", "Granja", CLAVE_REJILLA, inv=True))   # no arar dos veces la misma casilla
        e["events"].append(EV([C("CollisionNP", "SueloPreparado", "Objetos_Fisicos", "", "", "", inv=True)], [
            set_objv_s("SueloPreparado", "MiCelda", CLAVE_SUELO),
            nv("Granja[SueloPreparado.MiCelda].X", "SueloPreparado.X()"), nv("Granja[SueloPreparado.MiCelda].Y", "SueloPreparado.Y()"),
            sv("Granja[SueloPreparado.MiCelda].Escena", "CurrentSceneName()"),
            sv("Granja[SueloPreparado.MiCelda].Planta", '""'), nv("Granja[SueloPreparado.MiCelda].Etapa", "0")], [
            COM("Si habia hierba en esa casilla, se corta sola"),
            EV([C("CollisionNP", "Hierba", "SueloPreparado", "", "", "")], [set_objv_b("Hierba", "Cortar", "True")])]))
for n in ["SueloPreparado"]:
    o = O[n]
    if not any(v["name"] == "MiCelda" for v in o["variables"]): o["variables"].append(var("MiCelda", "string", ""))
if not any(v["name"] == "MiID" for v in O["Hierba"]["variables"]): O["Hierba"]["variables"].append(var("MiID", "string", ""))

# ---------- Personaje: reconstruir la granja y decidir que vuelve a crecer ----------
inicio = next(e for e in pers["events"] if tiene(e, "SceneJustBegins"))
subs = inicio["events"]
subs[:] = [s for s in subs if not (s.get("type") == "BuiltinCommonInstructions::ForEachChildVariable")
           and not (s.get("type", "").endswith("Comment") and "granja" in s.get("comment", "").lower())]
granja = {"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Granja",
          "valueIteratorVariableName": "CeldaGranja", "keyIteratorVariableName": "ClaveGranja",
          "conditions": [isv("CeldaGranja.Escena", "CurrentSceneName()")],
          "actions": [A("Create", "", "SueloPreparado", "CeldaGranja.X", "CeldaGranja.Y", q("")),
                      A("SetZOrder", "SueloPreparado", "=", "0"), set_objv_s("SueloPreparado", "MiCelda", "ClaveGranja")],
          "events": []}  # los cultivos se agregan en generar_cultivos.py
subs[0:0] = [COM("Reconstruir la granja de esta zona (tierra arada y cultivos)"), granja]

def temporada(v): return "floor((" + v + " - 1) / 28)"
for fe in subs:
    obj = fe.get("object")
    if fe.get("type") != "BuiltinCommonInstructions::ForEach" or obj not in ("Objetos_Fisicos", "Rocas"): continue
    clave = "Destruidos[" + obj + ".MiID]"
    fe["events"] = [EV([C("VariableChildExists2", "Destruidos", obj + ".MiID")], [], [
        EV([cmp(temporada(clave), "=", temporada("Calendario.DiaTotal"))], [A("Delete", obj, "")]),
        EV([cmp(temporada(clave), "!=", temporada("Calendario.DiaTotal"))], [], [
            COM("Cambio la estacion: vuelve a salir, salvo que ahora haya tierra arada ahi"),
            EV([C("CollisionNP", obj, "SueloPreparado", "", "", "")], [A("Delete", obj, "")]),
            EV([C("CollisionNP", obj, "SueloPreparado", "", "", "", inv=True)], [A("VariableRemoveChild", "Destruidos", obj + ".MiID")])])])]
if not any(fe.get("object") == "Hierba" for fe in subs):
    subs.append(FOREACH("Hierba", [], [set_objv_s("Hierba", "MiID", 'CurrentSceneName() + "_" + ToString(round(Hierba.X())) + "_" + ToString(round(Hierba.Y()))')], [
        EV([C("VariableChildExists2", "Destruidos", "Hierba.MiID")], [], [
            EV([cmp("Calendario.DiaTotal - Destruidos[Hierba.MiID]", "<", "3")], [A("Delete", "Hierba", "")]),
            EV([cmp("Calendario.DiaTotal - Destruidos[Hierba.MiID]", ">=", "3")], [A("VariableRemoveChild", "Destruidos", "Hierba.MiID")])]),
        EV([C("CollisionNP", "Hierba", "SueloPreparado", "", "", "")], [A("Delete", "Hierba", "")])]))

for lay in d["layouts"]:
    if lay["name"] in ("Nivel 01", "Nivel 02", "Pueblo"):
        lay["variables"] = [v for v in lay["variables"] if v["name"] not in ("CeldaGranja", "ClaveGranja")]
        lay["variables"] += [struct("CeldaGranja", [var("X", "number", 0), var("Y", "number", 0), var("Escena", "string", ""),
                                                     var("Planta", "string", ""), var("Etapa", "number", 0)]),
                             var("ClaveGranja", "string", "")]

# ---------- eventos externos HUD ----------
H = [COM("PANEL DE LA ESQUINA: cielo segun la hora, fecha, estacion, hora, monedas y experiencia")]
H.append(EV([], [], [
    EV([inv_("Reloj.Minuto", "10", "<")], [sv("MinTxt", '"0" + ToString(Reloj.Minuto)')]),
    EV([inv_("Reloj.Minuto", "10", ">=")], [sv("MinTxt", "ToString(Reloj.Minuto)")]),
    EV([], [nv("H24", "mod(Reloj.Hora, 12)")]),
    EV([isv("Reloj.M", q("PM"))], [nv("H24", "12", "+")]),
    EV([], [txt("HudHora", 'ToString(Reloj.Hora) + ":" + MinTxt + " " + Reloj.M'),
            txt("HudFecha", 'NombresDia[mod(Calendario.DiaTotal - 1, 7)] + ". " + ToString(Calendario.Dia)'),
            anim("HudEstacion", "ToString(Calendario.Estacion)"),
            txt("HudMonedas", "ToString(Monedas)"), A("SetX", "HudMonedas", "=", "%d - HudMonedas.Width()" % (X0 + 71)),
            txt("HudNivel", '"Nv " + ToString(NivelJugador)'),
            A("ResizableCapability::ResizableBehavior::SetWidth", "HudExpRelleno", "Resizable", "=", "max(0, 38 * min(1, Exp / ExpSiguiente))"),
            anim("HudDial", q("0"))]),
    *[EV([inv_("H24", str(a), ">="), inv_("H24", str(b), "<")], [anim("HudDial", q(str(k)))])
      for k, (a, b) in enumerate([(6, 9), (9, 12), (12, 15), (15, 18), (18, 21)], start=1)],
], variables=[var("H24", "number", 0), var("MinTxt", "string", "")]))
H.append(COM("Subir de nivel: cada nivel pide mas experiencia y da +1 de daño maximo"))
H.append(EV([cmp("Exp", ">=", "ExpSiguiente")], [
    nv("Exp", "ExpSiguiente", "-"), nv("NivelJugador", "1", "+"), nv("ExpSiguiente", "50 + (NivelJugador - 1) * 30"),
    nv('Estadisticas["Daño Max"]', "1", "+"),
    A("Create", "", "TextoFlotante", "Personaje_jugador.CenterX() - 28", "Personaje_jugador.Y() - 40", q("")),
    txt("TextoFlotante", '"¡Nivel " + ToString(NivelJugador) + "!"'), color("TextoFlotante", "214;255;106"),
    A("SetZOrder", "TextoFlotante", "=", "100000"),
    tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 24", "easeOutQuad", 1.2),
    tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 1.8, "yes"),
    snd("HUD/SubirNivel.wav", 70)]))
external_events(d, "HUD", H)
if not any(e.get("target") == "HUD" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("HUD"))

# ---------- limpiar objetos y variables que ya no se usan ----------
texto = json.dumps([d["layouts"], d["externalEvents"], d["externalLayouts"]], ensure_ascii=False)
for viejo in ["NombreScore", "Text_Score", "RelojText"]:
    if viejo not in texto:
        d["objects"] = [o for o in d["objects"] if o["name"] != viejo]
        d["objectsFolderStructure"]["children"] = [c for c in d["objectsFolderStructure"]["children"] if c.get("objectName") != viejo]

json.dump(d, open(PROJ, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: mundo, calendario y panel")
