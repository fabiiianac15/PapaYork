"""Etapas 6 y 7: rutinas de los vecinos y escenas de historia con condiciones.
Rutinas[vecino].Pasos = lista por hora. Eventos[id] = condiciones y Pasos con Cmd, A, B, C.
Comandos: hablar, mover, moverya, colocar, mirar, esperar, sonido, fundido, dar_objeto, marcar."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
if any(e["name"] == "Eventos" for e in d["externalEvents"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}; EXT = {e["name"]: e for e in d["externalEvents"]}; L = {l["name"]: l for l in d["layouts"]}; V = {v["name"]: v for v in d["variables"]}
PUEBLO = L["Pueblo"]; PJ = "Personaje_jugador"
def img(r):
    n = "Natural/" + r + ".png"; add_resource(d, "image", n, n); return n
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)

# ---------- Rutas, en coordenadas de los pies ----------
RUTAS = {
 "Rosa": [(6, 806, 300), (8.7, 822, 325), (8.9, 822, 381), (17, 822, 325), (17.2, 806, 300), (18.5, 890, 340), (20.5, 806, 300)],
 "Fermin": [(6, 716, 300), (8.3, 716, 330), (8.6, 887, 345), (8.9, 887, 384), (18, 887, 345), (18.3, 716, 330), (18.5, 716, 300)],
 "Ramiro": [(6, 706, 179), (8, 975, 185), (8.5, 975, 330), (8.8, 900, 345), (12, 1060, 400), (14, 900, 345), (17, 975, 330), (17.3, 975, 185), (17.8, 706, 179)],
 "Lupita": [(6, 1120, 302), (8.5, 1005, 319), (10, 1080, 430), (11.5, 960, 430), (13, 1005, 319), (14.8, 960, 430), (15, 700, 430), (16.5, 960, 430), (16.7, 1005, 319), (19, 1120, 302)],
 "Tomas": [(6, 316, 359), (12, 330, 395), (15, 316, 359)],
}
HORARIO = {"Rosa": (9, 17), "Fermin": (9, 18)}
# Comprobación: ninguna ruta cruza una casa ni el agua
casas = [(i["x"] - 58, i["y"] - 100, i["x"] + 70, i["y"]) for i in PUEBLO["instances"] if i["name"] == "Casa1"]
agua = {(i["x"], i["y"]) for i in PUEBLO["instances"] if i["name"] == "Agua2"}
muelle = {(i["x"], i["y"]) for i in PUEBLO["instances"] if i["name"] == "PlatPesc"}
for n, ruta in RUTAS.items():
    for (_, x0, y0), (_, x1, y1) in zip(ruta, ruta[1:]):
        for k in range(61):
            x, y = x0 + (x1 - x0) * k / 60, y0 + (y1 - y0) * k / 60
            for c in casas:
                assert not (c[0] < x < c[2] and c[1] < y < c[3]), (n, "casa", x, y)
            if n != "Tomas":
                assert not any(a <= x < a + 32 and b <= y < b + 32 for a, b in agua), (n, "agua", x, y)
set_global_var(d, struct("Rutinas", [{"name": n, "type": "structure", "children": [var("Abre", "number", HORARIO.get(n, (0, 0))[0]), var("Cierra", "number", HORARIO.get(n, (0, 0))[1]),
    {"name": "Pasos", "type": "array", "children": [{"type": "structure", "children": [var("Hora", "number", h), var("X", "number", x - 16), var("Y", "number", y - 29)]} for h, x, y in r]}]} for n, r in RUTAS.items()]))
for v in (var("HoraDec", "number", 6), var("DestX", "number", 0), var("DestY", "number", 0), var("DistNPC", "number", 0), var("KRut", "number", 0), var("NPCSnap", "boolean", True), var("EventoActivo", "boolean", False)):
    set_global_var(d, v)

# ---------- Animaciones y variables de los vecinos ----------
npc = O["NPC"]
base = next(a for a in npc["animations"] if a["name"] == "Rosa")["directions"][0]["sprites"][0]
for n in RUTAS:
    for dir_ in ("Abajo", "Arriba", "Izquierda", "Derecha"):
        fs = []
        for f in range(1, 5):
            fr = json.loads(json.dumps(base)); fr["image"] = img(f"Vecinos/{n}_{dir_}{f}"); fs.append(fr)
        npc["animations"].append({"name": f"{n}_{dir_}", "useMultipleDirections": False, "directions": [{"looping": True, "timeBetweenFrames": 0.13, "sprites": fs}]})
npc["variables"] += [var("Vecino", "string", ""), var("GuionActivo", "boolean", False), var("GX", "number", 0), var("GY", "number", 0)]
POR_TIENDA = {"Mercado": "Rosa", "Herreria": "Fermin", "Ramiro": "Ramiro", "Lupita": "Lupita", "Tomas": "Tomas"}
for i in PUEBLO["instances"]:
    if i["name"] == "NPC":
        t = next(v["value"] for v in i["initialVariables"] if v["name"] == "Tienda")
        i["initialVariables"].append(var("Vecino", "string", POR_TIENDA[t]))
def reemplazar(evs):
    for e in evs:
        for k in ("conditions", "actions"):
            for a in e.get(k, []) or []:
                a["parameters"] = [p.replace("NPC.Animation::Name()", "NPC.Vecino") for p in a["parameters"]]
        reemplazar(e.get("events", []) or [])
reemplazar(EXT["Amistad"]["events"])

# ---------- Evento externo Rutinas ----------
RP = "Rutinas[NPC.Vecino].Pasos"
SET = lambda t: A("SetAnimationName", "NPC", t)
rutina = [
    COM("RUTINAS. Cada vecino va al ultimo punto de su lista cuya hora ya paso. Al entrar a la escena aparece directamente alli."),
    EV([C("SceneJustBegins", "")], [bv("NPCSnap", "True")]),
    EV([], [nv("HoraDec", "mod(Reloj.Hora, 12) + Reloj.Minuto / 60")], [
        EV([isv("Reloj.M", q("PM"))], [nv("HoraDec", "12", "+")]),
        EV([isv("Reloj.M", q("AM")), inv_("HoraDec", "6", "<")], [nv("HoraDec", "24", "+")])]),
    FOREACH("NPC", acts=[nv("DestX", "NPC.X()"), nv("DestY", "NPC.Y()")], subs=[
        EV([objv_b("NPC", "GuionActivo", "True")], [nv("DestX", "NPC.GX"), nv("DestY", "NPC.GY")]),
        EV([objv_b("NPC", "GuionActivo", "False")], [nv("KRut", "0")], [
            REPEAT(f"VariableChildCount({RP})", subs=[
                EV([cmp_(f"{RP}[KRut].Hora", "<=", "HoraDec")], [nv("DestX", f"{RP}[KRut].X"), nv("DestY", f"{RP}[KRut].Y")]),
                EV([], [nv("KRut", "1", "+")])])]),
        EV([ibv("NPCSnap", "True")], [A("SetXY", "NPC", "=", "DestX", "=", "DestY")]),
        EV([], [nv("DistNPC", "DistanceBetweenPositions(NPC.X(), NPC.Y(), DestX, DestY)")]),
        EV([inv_("DistNPC", "1.5", "<=")], [SET("NPC.Vecino"), A("SetXY", "NPC", "=", "DestX", "=", "DestY")]),
        EV([inv_("DistNPC", "1.5", ">"), ibv("DialogoAbierto", "False"), ibv("TiendaAbierta", "False")], [
            A("SetXY", "NPC", "=", "NPC.X() + (DestX - NPC.X()) / DistNPC * 45 * TimeDelta()", "=", "NPC.Y() + (DestY - NPC.Y()) / DistNPC * 45 * TimeDelta()")], [
            EV([cmp_("abs(DestX - NPC.X())", ">", "abs(DestY - NPC.Y())"), cmp_("DestX", ">", "NPC.X()")], [SET('NPC.Vecino + "_Derecha"')]),
            EV([cmp_("abs(DestX - NPC.X())", ">", "abs(DestY - NPC.Y())"), cmp_("DestX", "<=", "NPC.X()")], [SET('NPC.Vecino + "_Izquierda"')]),
            EV([cmp_("abs(DestX - NPC.X())", "<=", "abs(DestY - NPC.Y())"), cmp_("DestY", ">", "NPC.Y()")], [SET('NPC.Vecino + "_Abajo"')]),
            EV([cmp_("abs(DestX - NPC.X())", "<=", "abs(DestY - NPC.Y())"), cmp_("DestY", "<=", "NPC.Y()")], [SET('NPC.Vecino + "_Arriba"')])]),
        EV([], [A("SetZOrder", "NPC", "=", "NPC.Y() + 29")])]),
    EV([], [bv("NPCSnap", "False")]),
]
external_events(d, "Rutinas", rutina)

# ---------- La tienda abre en su horario y con el vecino en su puesto ----------
tie = EXT["Tienda"]["events"]
cerrada = EV([ibv("InventarioAbierto", "False"), C("IsCursorOnObject", "NPC", "", "", ""), C("MouseButtonFromTextReleased", "", q("Left")),
              cmp_(f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), NPC.X(), NPC.Y())", "<", "60"), C("VariableChildExists2", "Tiendas", "NPC.Tienda")], [], [
    EV([cmp_("HoraDec", "<", "Rutinas[NPC.Vecino].Abre")], [sv("TipoTienda", q("Cerrada"))]),
    EV([cmp_("HoraDec", ">=", "Rutinas[NPC.Vecino].Cierra")], [sv("TipoTienda", q("Cerrada"))]),
    EV([isv("TipoTienda", q("Cerrada"))], [A("Create", "", "TextoFlotante", "NPC.X() - 40", "NPC.Y() - 30", q("")),
        txt("TextoFlotante", '"Abre de " + ToString(Rutinas[NPC.Vecino].Abre) + " a " + ToString(Rutinas[NPC.Vecino].Cierra - 12) + " PM"'),
        A("TextObject::ChangeColor", "TextoFlotante", q("251;242;54")), A("SetZOrder", "TextoFlotante", "=", "100000"),
        tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 16", "easeOutQuad", 1.5), tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 2.2, "yes")])])
tie.insert(6, cerrada)

# ---------- Escenas de historia ----------
def linea(q_, t): return {"type": "structure", "children": [var("Quien", "string", q_), var("Texto", "string", t)]}
DIA = {
 "EvLlegada1": [("Ramiro", "¡Alto ahí, forastero! ...Ah, no. Ese sombrero... ¡usted es el hijo de Chuchini!"), ("Lupita", "¡Es el sombrero del cuadro de la alcaldía! ¡El del viejo Hetol!")],
 "EvLlegada2": [("Ramiro", "Bienvenido a Papayork, joven. Doña Rosa y Don Fermín atienden en la plaza. Salude, que aquí nos conocemos todos."), ("Ramiro", "Y no ande de noche sin espada. Las papas están... raras."), ("Lupita", "¡Dicen que muerden!"), ("Pedro", "¿Las papas... muerden?")],
 "EvMuta": [("Pedro", "¡Esa planta se movió! Salió de la tierra sola... y tenía ojos."), ("Pedro", "Entonces era verdad. Lo que brillaba anoche no era mi imaginación."), ("Pedro", "Tengo que proteger los cultivos. Un espantapapas, quizá. Y averiguar de dónde sale todo esto.")],
 "EvCueva": [("Fermin", "Muchacho, ven acá. Ya te vi preguntando por la cueva del bosque."), ("Fermin", "Yo mismo ayudé a tapar esa entrada. El pueblo me pagó para no hacer preguntas."), ("Fermin", "Con un pico de hierro y un núcleo radiactivo esas rocas se abren. Toma, para que empieces."), ("Pedro", "¿Qué hay allá adentro, Don Fermín?"), ("Fermin", "Algo que tu tatarabuelo no quiso que nadie encontrara. O que solo uno de los suyos encontrara.")],
 "EvReactor": [("Tomas", "Siéntate, hijo. Ya es hora de que sepas cómo fue aquella tarde."), ("Tomas", "Mi abuelo vio a los de la ciudad enterrar barriles bajo el valle, meses antes de la explosión. Nadie le creyó."), ("Tomas", "Cuando el reactor reventó, lo que estaba enterrado siguió ahí. Dormido. Y las raíces de las papas son muy largas."), ("Pedro", "Entonces no vuelve la radiación... nunca se fue."), ("Tomas", "Tu tatarabuelo lo sospechaba. Por eso escribió aquel diario.")],
 "EvJefe": [("Pedro", "Ahí está. Las rocas tiemblan cuando me acerco."), ("Pedro", "Algo enorme respira ahí abajo. Todas las papas del valle vienen de lo mismo."), ("Pedro", "Papá me dejó esta tierra para cuidarla, no para huir como hicimos la otra vez."), ("Pedro", "Voy a entrar. Y voy a terminar con esto.")],
}
for k, l in DIA.items():
    V["Dialogos"]["children"].append({"name": k, "type": "array", "children": [linea(a, b) for a, b in l]})
cueva = next(i for i in L["Nivel 02"]["instances"] if i["name"] == "Interactivo" and any(v.get("value") == "Cueva" for v in i.get("initialVariables", [])))
def paso(cmd, a="", b=0, c_=0): return {"type": "structure", "children": [var("Cmd", "string", cmd), var("A", "string", a), var("B", "number", b), var("C", "number", c_)]}
def evento(id_, escena, pasos, hmin=6, hmax=30, personaje="", puntos=0, previo="", marca="", zx=0, zy=0, zr=0):
    return {"name": id_, "type": "structure", "children": [var("Escena", "string", escena), var("HoraMin", "number", hmin), var("HoraMax", "number", hmax), var("Personaje", "string", personaje), var("PuntosMin", "number", puntos),
        var("EventoPrevio", "string", previo), var("Marca", "string", marca), var("ZonaX", "number", zx), var("ZonaY", "number", zy), var("ZonaR", "number", zr), {"name": "Pasos", "type": "array", "children": pasos}]}
set_global_var(d, struct("Eventos", [
  evento("Llegada", "Pueblo", [paso("esperar", "", .5), paso("colocar", "Ramiro", 150, 161), paso("colocar", "Lupita", 190, 161), paso("moverya", "Lupita", 0, 161), paso("mover", "Ramiro", -20, 161), paso("mirar", "Pedro", 1),
      paso("hablar", "EvLlegada1"), paso("hablar", "EvLlegada2"), paso("fundido", "negro"), paso("esperar", "", .7), paso("soltar"), paso("fundido", "claro")], zx=-53, zy=190, zr=160),
  evento("PrimeraMutacion", "Nivel 01", [paso("sonido", "temblor"), paso("esperar", "", .8), paso("hablar", "EvMuta")], marca="PapaMuto"),
  evento("CuevaFermin", "Pueblo", [paso("mirar", "Pedro", 1), paso("hablar", "EvCueva"), paso("dar_objeto", "Nucleo", 1), paso("sonido", "exito")], hmin=9, hmax=18, personaje="Fermin", puntos=500, zx=887, zy=384, zr=110),
  evento("TomasReactor", "Pueblo", [paso("hablar", "EvReactor"), paso("sonido", "exito")], hmin=17, hmax=23, personaje="Tomas", puntos=1000, zx=316, zy=359, zr=120),
  evento("DecisionCueva", "Nivel 02", [paso("sonido", "temblor"), paso("esperar", "", 1), paso("hablar", "EvJefe")], previo="CuevaFermin", zx=cueva["x"] + 49, zy=cueva["y"] + 74, zr=120),
]))
set_global_var(d, struct("EventoIter", [var("Escena", "string", "")]))
for v in (var("ClaveEvento", "string", ""), var("EvId", "string", ""), var("EvPaso", "number", 0), var("EvIniciado", "boolean", False), var("EvCmd", "string", ""), var("EvA", "string", ""), var("EvB", "number", 0), var("EvC", "number", 0),
          var("EvOk", "boolean", False), var("EvSaltar", "boolean", False), var("EvPX", "number", 0), var("EvPY", "number", 0), var("EvMoverPedro", "boolean", False)):
    set_global_var(d, v)
set_global_var(d, {"name": "EventosVistos", "type": "structure", "children": [var("Inicio", "number", 1)]})

K = "Eventos[ClaveEvento]"
malo = lambda *c: EV(list(c), [bv("EvOk", "False")])
revisa = {"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Eventos", "valueIteratorVariableName": "EventoIter", "keyIteratorVariableName": "ClaveEvento", "conditions": [ibv("EventoActivo", "False")], "actions": [bv("EvOk", "True")], "events": [
    malo(isv(f"{K}.Escena", "CurrentSceneName()", "!=")),
    malo(C("VariableChildExists2", "EventosVistos", "ClaveEvento")),
    malo(cmp_("HoraDec", "<", f"{K}.HoraMin")), malo(cmp_("HoraDec", ">", f"{K}.HoraMax")),
    EV([isv(f"{K}.Personaje", q(""), "!="), cmp_(f"Amistad[{K}.Personaje].Puntos", "<", f"{K}.PuntosMin")], [bv("EvOk", "False")]),
    EV([isv(f"{K}.EventoPrevio", q(""), "!="), C("VariableChildExists2", "EventosVistos", f"{K}.EventoPrevio", inv=True)], [bv("EvOk", "False")]),
    EV([isv(f"{K}.Marca", q(""), "!="), C("VariableChildExists2", "EventosVistos", f"{K}.Marca", inv=True)], [bv("EvOk", "False")]),
    EV([cmp_(f"{K}.ZonaR", ">", "0"), cmp_(f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), {K}.ZonaX, {K}.ZonaY)", ">", f"{K}.ZonaR")], [bv("EvOk", "False")]),
    EV([ibv("EvOk", "True")], [bv("EventoActivo", "True"), sv("EvId", "ClaveEvento"), nv("EvPaso", "0"), bv("EvIniciado", "False"), bv("EvSaltar", "False"), bv("EvMoverPedro", "False"), bv("InventarioAbierto", "True"), A("PauseTimer", "", q("PasoTiempo")), nv(f"EventosVistos[EvId]", "1"), hide("AvisoNPC")]),
]}
sig = lambda: [nv("EvPaso", "1", "+"), bv("EvIniciado", "False")]
es = lambda c_: isv("EvCmd", q(c_))
quien = objv_s("NPC", "Vecino", "EvA")
PS = "Eventos[EvId].Pasos[EvPaso]"
ejecutar = EV([ibv("EventoActivo", "True"), ibv("EvIniciado", "False"), cmp_("EvPaso", "<", "VariableChildCount(Eventos[EvId].Pasos)")],
    [bv("EvIniciado", "True"), sv("EvCmd", f"{PS}.Cmd"), sv("EvA", f"{PS}.A"), nv("EvB", f"{PS}.B"), nv("EvC", f"{PS}.C"), A("ResetTimer", "", q("EvPaso"))], [
    EV([es("hablar"), ibv("EvSaltar", "False")], [sv("DialogoTerminado", q("")), sv("DialogoPedido", "EvA"), bv("DialogoPausa", "False")]),
    EV([es("colocar")], [], [EV([quien], [set_objv_b("NPC", "GuionActivo", "True"), set_objv_n("NPC", "GX", "EvB"), set_objv_n("NPC", "GY", "EvC"), A("SetXY", "NPC", "=", "EvB", "=", "EvC")])]),
    EV([es("moverya")], [], [EV([quien], [set_objv_b("NPC", "GuionActivo", "True"), set_objv_n("NPC", "GX", "EvB"), set_objv_n("NPC", "GY", "EvC")])]),
    EV([es("mover"), isv("EvA", q("Pedro"), "!=")], [], [EV([quien], [set_objv_b("NPC", "GuionActivo", "True"), set_objv_n("NPC", "GX", "EvB"), set_objv_n("NPC", "GY", "EvC")])]),
    EV([es("mover"), isv("EvA", q("Pedro"))], [bv("EvMoverPedro", "True"), nv("EvPX", "EvB"), nv("EvPY", "EvC")]),
    EV([es("mirar"), isv("EvA", q("Pedro"))], [set_objv_n(PJ, "Direccion", "EvB")]),
    EV([es("sonido"), isv("EvA", q("temblor"))], [snd("Cultivos/Temblor.wav", 80)]),
    EV([es("sonido"), isv("EvA", q("exito"))], [snd("HUD/SubirNivel.wav", 60)]),
    EV([es("fundido"), isv("EvA", q("negro"))], [A("Create", "", "Cortina", "0", "0", q("DialogoHD")), A("ResizableCapability::ResizableBehavior::SetWidth", "Cortina", "Resizable", "=", "960"), A("ResizableCapability::ResizableBehavior::SetHeight", "Cortina", "Resizable", "=", "540"),
        A("SetZOrder", "Cortina", "=", "999"), opacity("Cortina", 0), tw_op("Cortina", "Oscurecer", 255, "easeInQuad", .6)]),
    EV([es("fundido"), isv("EvA", q("claro"))], [tw_op("Cortina", "Aclarar", 0, "easeOutQuad", .8, "yes")]),
    EV([es("dar_objeto")], [], [REPEAT("EvB", acts=[A("Create", "", "Recursos", f"{PJ}.X() - 16", f"{PJ}.Y() - 30", q("")), A("SetAnimationName", "Recursos", "EvA")])]),
    EV([es("marcar")], [nv("EventosVistos[EvA]", "1")]),
    EV([es("soltar")], [set_objv_b("NPC", "GuionActivo", "False"), bv("NPCSnap", "True")]),
])
siguiente = [
    EV([es("colocar")], sig()), EV([es("moverya")], sig()), EV([es("mirar")], sig()), EV([es("sonido")], sig()), EV([es("dar_objeto")], sig()), EV([es("marcar")], sig()), EV([es("soltar")], sig()),
    EV([es("fundido")], sig()),
    EV([es("esperar"), cmp_('TimerElapsedTime("EvPaso")', ">=", "EvB")], sig()),
    EV([es("esperar"), ibv("EvSaltar", "True")], sig()),
    EV([es("hablar"), isv("DialogoTerminado", "EvA")], [sv("DialogoTerminado", q(""))] + sig()),
    EV([es("hablar"), ibv("EvSaltar", "True")], sig()),
    EV([es("mover"), isv("EvA", q("Pedro")), ibv("EvMoverPedro", "False")], sig()),
    EV([es("mover"), isv("EvA", q("Pedro"), "!="), quien, cmp_("DistanceBetweenPositions(NPC.X(), NPC.Y(), EvB, EvC)", "<=", "2")], sig()),
    EV([es("mover"), isv("EvA", q("Pedro"), "!="), ibv("EvSaltar", "True")], sig()),
    EV([es("mover"), isv("EvA", q("Pedro"), "!="), cmp_('TimerElapsedTime("EvPaso")', ">", "14")], sig()),
]
CAJA = ("CajaTexto", "CajaRetrato", "Retrato", "NombreDialogo", "TextoDialogo", "FlechaDialogo")
eventos = [
    COM("ESCENAS DE HISTORIA. Cada 2 segundos se busca una que cumpla sus condiciones y no se haya visto. Mientras corre, Pedro no se mueve y el reloj se detiene. Esc la salta."),
    EV([C("SceneJustBegins", "")], [bv("EventoActivo", "False"), A("ResetTimer", "", q("EvRevisar"))]),
    EV([C("CompareTimer", "", q("EvRevisar"), ">=", "2"), ibv("EventoActivo", "False"), ibv("InventarioAbierto", "False"), ibv("DialogoAbierto", "False"), ibv("TiendaAbierta", "False"), ibv("Pescando", "False"), ibv("FabricarAbierto", "False"), isv("DialogoPedido", q(""))],
       [A("ResetTimer", "", q("EvRevisar"))], [revisa]),
    COM("Saltar con Esc"),
    EV([ibv("EventoActivo", "True"), C("KeyFromTextReleased", "", q("Escape"))], [bv("EvSaltar", "True")], [
        EV([ibv("DialogoAbierto", "True")], [bv("DialogoAbierto", "False"), sv("DialogoPedido", q(""))] + [hide(o) for o in CAJA])]),
    ejecutar,
    EV([ibv("EventoActivo", "True"), ibv("EvIniciado", "True")], [], siguiente),
    COM("Pedro durante la escena"),
    EV([ibv("EventoActivo", "True")], [A("SetBooleanObjectVariable", PJ, "Invencible", "True", ""), A("AnimatableCapability::AnimatableBehavior::SetName", PJ, "Animation", "=", f'"Quieto" + NombresDir[{PJ}.Direccion]')]),
    EV([ibv("EventoActivo", "True"), ibv("EvMoverPedro", "True")], [A("SetXY", PJ, "=", f"{PJ}.X() + (EvPX - {PJ}.X()) / max(1, DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), EvPX, EvPY)) * 50 * TimeDelta()", "=", f"{PJ}.Y() + (EvPY - {PJ}.Y()) / max(1, DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), EvPX, EvPY)) * 50 * TimeDelta()"),
        A("AnimatableCapability::AnimatableBehavior::SetName", PJ, "Animation", "=", f"NombresDir[{PJ}.Direccion]")], [
        EV([cmp_(f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), EvPX, EvPY)", "<=", "2")], [bv("EvMoverPedro", "False")]),
        EV([ibv("EvSaltar", "True")], [A("SetXY", PJ, "=", "EvPX", "=", "EvPY"), bv("EvMoverPedro", "False")]),
        EV([cmp_('TimerElapsedTime("EvPaso")', ">", "10")], [bv("EvMoverPedro", "False")])]),
    COM("Fin de la escena"),
    EV([ibv("EventoActivo", "True"), cmp_("EvPaso", ">=", "VariableChildCount(Eventos[EvId].Pasos)")], [bv("EventoActivo", "False"), bv("InventarioAbierto", "False"), A("UnPauseTimer", "", q("PasoTiempo")), A("SetBooleanObjectVariable", PJ, "Invencible", "False", ""),
        set_objv_b("NPC", "GuionActivo", "False"), A("ResetTimer", "", q("EvRevisar"))]),
]
external_events(d, "Eventos", eventos)
per = EXT["Personaje"]["events"]
per.insert(next(k for k, e in enumerate(per) if e.get("target") == "Amistad"), LINK("Rutinas"))
per.insert(next(k for k, e in enumerate(per) if e.get("target") == "Dialogo"), LINK("Eventos"))
# Compuertas: durante una escena no se abre la mochila ni se guarda
EXT["Inventario"]["events"][5]["conditions"].append(ibv("EventoActivo", "False"))
pau = EXT["Pausa"]["events"][3]; assert "VerPausa" in json.dumps(pau["actions"]); pau["conditions"].append(ibv("EventoActivo", "False"))
EXT["Guardado"]["events"][1]["conditions"].append(ibv("EventoActivo", "False"))
# La primera mutación deja una marca para su escena
def marcar_muta(evs):
    n = 0
    for e in evs:
        if any(a["type"]["value"] == "Create" and a["parameters"][1] == "PapaEmerge" for a in e.get("actions", []) or []):
            e["actions"].append(nv('EventosVistos["PapaMuto"]', "1")); n += 1
        n += marcar_muta(e.get("events", []) or [])
    return n
assert marcar_muta(EXT["NuevoDia"]["events"]) == 1
# Guardar y cargar
gu = EXT["Guardado"]["events"][2]["events"][8]["actions"]
gu.insert(next(k for k, a in enumerate(gu) if a["type"]["value"] == "SetStringVariable"), A("EcrireFichierTxt", q("PapayorkPartidas"), '"Ranura" + ToString(RanuraActual) + "/EventosVistos"', "ToJSON(EventosVistos)"))
menu = L["Menu Principal"]["events"]; carga = menu[37]["events"]
idx = next(k for k, e in enumerate(carga) if "/Granja" in json.dumps(e, ensure_ascii=False))
carga.insert(idx + 1, json.loads(json.dumps(carga[idx], ensure_ascii=False).replace('/Granja\\"', '/EventosVistos\\"').replace('"Granja"', '"EventosVistos"')))
menu[35]["actions"].insert(0, A("JSONToGlobalVariableStructure", q('{"Inicio":1}'), "EventosVistos"))
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
