"""Etapa 4: pesca propia de PapaYork. Lanzar, esperar, picada y minijuego medido en segundos reales."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
if any(e["name"] == "Pesca" for e in d["externalEvents"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}; EXT = {e["name"]: e for e in d["externalEvents"]}; V = {v["name"]: v for v in d["variables"]}
def img(r):
    n = "Natural/" + r + ".png"; add_resource(d, "image", n, n); return n
PECES = {  # nombre, dificultad, movimiento, min, max, hora min, hora max, estaciones, lugares, precio, exp, prob, descripción
 "Carpita": ("Carpita de Papayork", 15, "Suave", 12, 30, 6, 26, "0123", "Nivel 01 Pueblo", 12, 3, 10, "Común en aguas tranquilas. Sabe a tierra y a domingo."),
 "PezPapa": ("Pez Papa", 25, "Suave", 15, 35, 6, 20, "012", "Nivel 01", 22, 5, 6, "Redondo y con ojitos. Nadie sabe si es pez o tubérculo."),
 "Bagre": ("Bagre Terroso", 35, "Hunde", 25, 60, 18, 26, "0123", "Nivel 02 Pueblo", 30, 6, 6, "Vive pegado al fondo y odia subir."),
 "Trucha": ("Trucha Plateada", 45, "Saltos", 20, 45, 6, 12, "012", "Nivel 02", 40, 8, 5, "Le gusta el agua fría de la mañana."),
 "Anguila": ("Anguila Verdosa", 55, "Saltos", 40, 90, 20, 26, "123", "Nivel 02 Pueblo", 55, 10, 4, "Solo sale de noche. Resbala hasta en la mochila."),
 "Mojarra": ("Mojarra Brillante", 50, "Suave", 10, 25, 6, 26, "0123", "Nivel 01", 65, 10, 3, "Brilla en la oscuridad. Mejor no comerla."),
 "Lucio": ("Lucio del Reactor", 72, "Saltos", 50, 110, 15, 22, "12", "Nivel 02", 110, 18, 2, "Nació río abajo del reactor. Muerde con rabia."),
 "ReyTuberculo": ("Rey Tubérculo", 90, "Hunde", 90, 160, 18, 24, "0123", "Nivel 02", 300, 60, 1, "El pez jefe del río. Dicen que HetolMimiao lo vio una vez."),
}
for k, (nom, dif, mov, tmin, tmax, h0, h1, est, lug, pre, xp, prob, des) in PECES.items():
    V["Items"]["children"].append(struct(k, [var("Descripcion", "string", des), var("Max", "number", 99), var("Nombre", "string", nom),
        var("Precio", "number", pre), var("Rareza", "string", "Rara" if prob <= 2 else "Común"), var("Tipo", "string", "Pez")]))
V["Items"]["children"].append(struct("Cana", [var("Descripcion", "string", "Clic en el agua para lanzar. Al picar, clic y mantén pulsado."),
    var("Max", "number", 1), var("Nombre", "string", "Caña de pescar"), var("Precio", "number", 40), var("Rareza", "string", "Común"), var("Tipo", "string", "Herramienta")]))
set_global_var(d, struct("Peces", [struct(k, [var("Dificultad", "number", p[1]), var("Movimiento", "string", p[2]), var("TamanoMin", "number", p[3]), var("TamanoMax", "number", p[4]),
    var("HoraMin", "number", p[5]), var("HoraMax", "number", p[6]), var("Estaciones", "string", p[7]), var("Lugar", "string", p[8]), var("Exp", "number", p[10]), var("Prob", "number", p[11])]) for k, p in PECES.items()]))
set_global_var(d, struct("PezActual", [var("Dificultad", "number", 0), var("Movimiento", "string", ""), var("TamanoMin", "number", 0), var("TamanoMax", "number", 0),
    var("HoraMin", "number", 0), var("HoraMax", "number", 0), var("Estaciones", "string", ""), var("Lugar", "string", ""), var("Exp", "number", 0), var("Prob", "number", 0)]))
for v in (var("ClavePez", "string", ""), var("PezElegido", "string", "Carpita"), var("PescaEstado", "number", 0), var("PescaEspera", "number", 3), var("PescaPeso", "number", 0),
          var("PezY", "number", 84), var("PezVel", "number", 0), var("PezDest", "number", 84), var("BarY", "number", 75), var("BarVel", "number", 0), var("PescaMedida", "number", 0.3),
          var("BarPulsada", "boolean", False), var("HoraPesca", "number", 6), var("TallaPez", "number", 0)):
    set_global_var(d, v)
next(c for c in V["Tiendas"]["children"] if c["name"] == "Mercado")["children"].append(
    {"type": "structure", "children": [var("Id", "string", "Cana"), var("Precio", "number", 80), var("Tipo", "string", "Item")]})
# Iconos y objetos que caen a la mochila
ref = O["Recursos"]["animations"][0]["directions"][0]["sprites"][0]
for k in PECES:
    r = img("Peces/" + k)
    O["IconoItem"]["animations"].append(anim_def(k, [frame(r, (16, 16))]))
    fr = frame(r); fr["hasCustomCollisionMask"], fr["customCollisionMask"] = True, json.loads(json.dumps(ref["customCollisionMask"]))
    O["Recursos"]["animations"].append(anim_def(k, [fr]))
O["IconoItem"]["animations"].append(anim_def("Cana", [frame(img("Pesca/Cana"), (16, 16))]))
# Lo que se compra cae al suelo como Recursos: la caña y la regadera necesitan su dibujo o saldrían como madera
for nom, ruta in (("Cana", "Pesca/Cana"), ("Regadera", "Objetos/Regadera")):
    fr = frame(img(ruta)); fr["hasCustomCollisionMask"], fr["customCollisionMask"] = True, json.loads(json.dumps(ref["customCollisionMask"]))
    O["Recursos"]["animations"].append(anim_def(nom, [fr]))
next(c for c in V["Items"]["children"] if c["name"] == "Regadera")["children"][0]["value"] = "Clic en tierra arada para regar. Se rellena con clic en el agua."
nombres_rec = {a["name"] for a in O["Recursos"]["animations"]}
for t_ in V["Tiendas"]["children"]:
    for o_ in t_["children"]:
        hijos_ = {c["name"]: c.get("value") for c in o_["children"]}
        if hijos_.get("Tipo") == "Item" and hijos_["Id"] not in nombres_rec:
            # Se vende pero no tenía dibujo en el suelo: usa su ícono de la mochila
            icono = next(x for x in O["IconoItem"]["animations"] if x["name"] == hijos_["Id"])["directions"][0]["sprites"][0]["image"]
            fr = frame(icono); fr["hasCustomCollisionMask"], fr["customCollisionMask"] = True, json.loads(json.dumps(ref["customCollisionMask"]))
            O["Recursos"]["animations"].append(anim_def(hijos_["Id"], [fr]))
            nombres_rec.add(hijos_["Id"])
            print("dibujo añadido para:", hijos_["Id"])
# Una herramienta que ya tienes no se puede comprar otra vez
LID = "Tiendas[TipoTienda][SlotUI.Indice].Id"
tie10 = EXT["Tienda"]["events"][10]["events"][2]["events"]
tie10.insert(2, EV([isv("Tiendas[TipoTienda][SlotUI.Indice].Tipo", q("Item")), isv(f"Items[{LID}].Tipo", q("Herramienta"))], [nv("k", "0")], [
    REPEAT(30, subs=[EV([isv("Mochila[k].Id", LID)], [set_objv_b("SlotUI", "Puede", "False")]), EV([], [nv("k", "1", "+")])])]))
# Objetos del minijuego
def sprite_u(n, anims, tw=False): set_global_object(d, sprite_obj(n, anims, tween=tw))
sprite_u("PescaPista", [anim_def("N", [frame(img("Pesca/Pista"))])])
sprite_u("PescaBarra", [anim_def("N", [frame(img("Pesca/Barra"))])])
sprite_u("PescaMedidor", [anim_def("N", [frame(img("Pesca/Medidor"))])])
sprite_u("PescaPez", [anim_def(k, [frame(img("Peces/" + k))]) for k in PECES])
sprite_u("Boya", [anim_def("N", [frame(img("Pesca/Boya1")), frame(img("Pesca/Boya2"))], loop=True, dt=0.4)])
sprite_u("AvisoPesca", [anim_def("N", [frame(img("Pesca/Aviso"))])], tw=True)
lin = frame(img("Pesca/Linea")); lin["centerPoint"] = {"automatic": False, "name": "centre", "x": 0, "y": 0}
sprite_u("LineaPesca", [anim_def("N", [lin])])

PJ = "Personaje_jugador"
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
OCULTOS = ("PescaPista", "PescaBarra", "PescaMedidor", "PescaPez", "Boya", "AvisoPesca", "LineaPesca")
ocultar = [hide(o) for o in OCULTOS]
def crear(o, x, y, capa, z): return EV([], [A("Create", "", o, str(x), str(y), q(capa)), A("SetZOrder", o, "=", str(z)), hide(o)])
def flot(texto, color, dur=1.5):
    return [A("Create", "", "TextoFlotante", f"{PJ}.CenterX() - 50", f"{PJ}.Y() - 58", q("")), txt("TextoFlotante", texto), A("TextObject::ChangeColor", "TextoFlotante", q(color)),
            A("SetZOrder", "TextoFlotante", "=", "100000"), tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", dur), tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", dur + .8, "yes")]
fin = [bv("Pescando", "False"), nv("PescaEstado", "0")] + ocultar
sin_ui = [ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False"), ibv("DialogoAbierto", "False")]
FIJAR = lambda t: A("AnimatableCapability::AnimatableBehavior::SetName", PJ, "Animation", "=", t)
DIR = f"NombresDir[{PJ}.Direccion]"
est = lambda n: inv_("PescaEstado", str(n))
agua_cerca = cmp_(f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), Agua2.X() + 16, Agua2.Y() + 16)", "<", "130")
PX, PY = 690, 130; TOP = PY + 11
mueve_pez = [
    EV([cmp_("RandomFloat(1)", "<", "(0.5 + Peces[PezElegido].Dificultad / 35) * TimeDelta()")], [nv("PezDest", "RandomInRange(0, 168)")]),
    EV([], [nv("PezVel", "(PezDest - PezY) * (1.5 + Peces[PezElegido].Dificultad / 14) * TimeDelta()", "+"), nv("PezVel", "PezVel * 2.6 * TimeDelta()", "-")]),
    EV([isv("Peces[PezElegido].Movimiento", q("Saltos")), cmp_("RandomFloat(1)", "<", "(Peces[PezElegido].Dificultad / 45) * TimeDelta()")], [nv("PezVel", "RandomInRange(-1, 0) * 2 * 220 + 220 + RandomInRange(-40, 40)", "+")]),
    EV([isv("Peces[PezElegido].Movimiento", q("Hunde"))], [nv("PezVel", "70 * TimeDelta()", "+")]),
    EV([], [nv("PezY", "PezVel * TimeDelta()", "+")]),
    EV([inv_("PezY", "0", "<")], [nv("PezY", "0"), nv("PezVel", "abs(PezVel) * 0.4")]),
    EV([inv_("PezY", "168", ">")], [nv("PezY", "168"), nv("PezVel", "-abs(PezVel) * 0.4")]),
]
mueve_barra = [
    EV([], [bv("BarPulsada", "False")]),
    EV([C("MouseButtonFromTextPressed", "", q("Left"))], [bv("BarPulsada", "True")]),
    EV([C("KeyFromTextPressed", "", q("Space"))], [bv("BarPulsada", "True")]),
    EV([ibv("BarPulsada", "True")], [nv("BarVel", "560 * TimeDelta()", "-")]),
    EV([ibv("BarPulsada", "False")], [nv("BarVel", "430 * TimeDelta()", "+")]),
    EV([], [nv("BarY", "BarVel * TimeDelta()", "+")]),
    EV([inv_("BarY", "0", "<")], [nv("BarY", "0"), nv("BarVel", "abs(BarVel) * 0.45")]),
    EV([inv_("BarY", "150", ">")], [nv("BarY", "150"), nv("BarVel", "-abs(BarVel) * 0.45")]),
]
medida = [
    EV([cmp_("PezY + 16", ">=", "BarY"), cmp_("PezY + 16", "<=", "BarY + 50")], [nv("PescaMedida", "0.13 * TimeDelta()", "+")]),
    EV([cmp_("PezY + 16", "<", "BarY")], [nv("PescaMedida", "0.15 * TimeDelta()", "-")]),
    EV([cmp_("PezY + 16", ">", "BarY + 50")], [nv("PescaMedida", "0.15 * TimeDelta()", "-")]),
    EV([], [A("SetY", "PescaBarra", "=", f"{TOP} + BarY"), A("SetY", "PescaPez", "=", f"{TOP} + PezY"), A("SetX", "PescaPez", "=", f"{PX + 9} + sin(TimeFromStart() * 9) * 2"),
            A("ResizableCapability::ResizableBehavior::SetHeight", "PescaMedidor", "Resizable", "=", "max(1, 200 * PescaMedida)"), A("SetY", "PescaMedidor", "=", f"{TOP + 200} - PescaMedidor.Height()"), A("ChangeColor", "PescaMedidor", q("168;236;74"))]),
    EV([inv_("PescaMedida", "0.3", "<")], [A("ChangeColor", "PescaMedidor", q("214;80;72"))]),
]
elegir = C("BuiltinCommonInstructions::Once")
buscar = {"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Peces", "valueIteratorVariableName": "PezActual", "keyIteratorVariableName": "ClavePez",
          "conditions": [cmp_('StrFind(PezActual.Lugar, CurrentSceneName())', "!=", "-1"), cmp_("StrFind(PezActual.Estaciones, ToString(Calendario.Estacion))", "!=", "-1"),
                         cmp_("HoraPesca", ">=", "PezActual.HoraMin"), cmp_("HoraPesca", "<=", "PezActual.HoraMax")],
          "actions": [nv("PescaPeso", "PezActual.Prob", "+")],
          "events": [EV([cmp_("RandomFloat(PescaPeso)", "<", "PezActual.Prob")], [sv("PezElegido", "ClavePez")])]}
eventos = [
    COM("PESCA. PescaEstado: 0 nada, 1 lanzando, 2 esperando, 3 pico, 4 minijuego. Todo el minijuego se mide en segundos reales con TimeDelta()."),
    EV([C("SceneJustBegins", "")], [bv("Pescando", "False"), nv("PescaEstado", "0"), A("ResetTimer", "", q("Pesca"))], [
        crear("PescaPista", PX, PY, "UIHD", 6000), crear("PescaBarra", PX + 10, TOP, "UIHD", 6001), crear("PescaMedidor", PX + 46, TOP, "UIHD", 6001), crear("PescaPez", PX + 9, TOP, "UIHD", 6002),
        crear("Boya", 0, 0, "", -6700), crear("AvisoPesca", 0, 0, "", 95000), crear("LineaPesca", 0, 0, "", 80000)]),
    COM("Lanzar: cana en la mano y clic en agua cercana"),
    EV(sin_ui + [ibv("Pescando", "False"), isv("ItemEnMano", q("Cana")), inv_("Energia", "0", ">"), C("IsCursorOnObject", "Agua2", "", "", ""), agua_cerca,
                 C("MouseButtonFromTextPressed", "", q("Left")), ONCE()],
       [bv("Pescando", "True"), nv("PescaEstado", "1"), A("ResetTimer", "", q("Pesca")), nv("Energia", "2", "-"), snd("Recursos/Soltar.wav", 50),
        A("SetPositionXY", "Boya", "=", "Agua2.X() + 9", "=", "Agua2.Y() + 9") if False else A("SetXY", "Boya", "=", "Agua2.X() + 9", "=", "Agua2.Y() + 9")], [
        EV([cmp_(f"abs(Agua2.X() + 16 - {PJ}.X())", ">=", f"abs(Agua2.Y() + 16 - {PJ}.Y())"), cmp_("Agua2.X() + 16", "<", f"{PJ}.X()")], [set_objv_n(PJ, "Direccion", "0")]),
        EV([cmp_(f"abs(Agua2.X() + 16 - {PJ}.X())", ">=", f"abs(Agua2.Y() + 16 - {PJ}.Y())"), cmp_("Agua2.X() + 16", ">=", f"{PJ}.X()")], [set_objv_n(PJ, "Direccion", "1")]),
        EV([cmp_(f"abs(Agua2.X() + 16 - {PJ}.X())", "<", f"abs(Agua2.Y() + 16 - {PJ}.Y())"), cmp_("Agua2.Y() + 16", "<", f"{PJ}.Y()")], [set_objv_n(PJ, "Direccion", "2")]),
        EV([cmp_(f"abs(Agua2.X() + 16 - {PJ}.X())", "<", f"abs(Agua2.Y() + 16 - {PJ}.Y())"), cmp_("Agua2.Y() + 16", ">=", f"{PJ}.Y()")], [set_objv_n(PJ, "Direccion", "3")])]),
    COM("Pedro segun el momento de la pesca"),
    EV([est(1)], [FIJAR(f'"PescaLanzar" + {DIR}')]),
    EV([est(2)], [FIJAR(f'"PescaEsperar" + {DIR}')]),
    EV([est(3)], [FIJAR(f'"PescaEsperar" + {DIR}')]),
    EV([est(4)], [FIJAR(f'"PescaTirar" + {DIR}')]),
    EV([ibv("Pescando", "True")], [A("AnimatableCapability::AnimatableBehavior::PlayAnimation", PJ, "Animation")]),
    EV([est(1), C("CompareTimer", "", q("Pesca"), ">=", "0.45")], [nv("PescaEstado", "2"), A("ResetTimer", "", q("Pesca")), nv("PescaEspera", "RandomFloatInRange(1.5, 7)"), show("Boya"), show("LineaPesca")]),
    COM("La linea va de la punta de la cana a la boya"),
    EV([inv_("PescaEstado", "2", ">=")], [A("SetXY", "LineaPesca", "=", f'{PJ}.PointX("Punta")', "=", f'{PJ}.PointY("Punta")'),
        A("ResizableCapability::ResizableBehavior::SetWidth", "LineaPesca", "Resizable", "=", f'DistanceBetweenPositions({PJ}.PointX("Punta"), {PJ}.PointY("Punta"), Boya.X() + 7, Boya.Y() + 6)'),
        A("SetAngle", "LineaPesca", "=", f'AngleBetweenPositions({PJ}.PointX("Punta"), {PJ}.PointY("Punta"), Boya.X() + 7, Boya.Y() + 6)')]),
    COM("Esperar. Clic antes de tiempo: recoge la linea"),
    EV([est(2), C("MouseButtonFromTextReleased", "", q("Left")), C("CompareTimer", "", q("Pesca"), ">", "0.3")], fin),
    EV([est(2), cmp_('TimerElapsedTime("Pesca")', ">=", "PescaEspera")], [nv("PescaEstado", "3"), A("ResetTimer", "", q("Pesca")), show("AvisoPesca"), A("SetXY", "AvisoPesca", "=", f"{PJ}.CenterX() - 7", "=", f"{PJ}.Y() - 72"), snd("Cultivos/Temblor.wav", 70),
        nv("HoraPesca", "mod(Reloj.Hora, 12)"), sv("PezElegido", q("Carpita")), nv("PescaPeso", "0")], [
        EV([isv("Reloj.M", q("PM"))], [nv("HoraPesca", "12", "+")]),
        EV([isv("Reloj.M", q("AM")), inv_("HoraPesca", "6", "<")], [nv("HoraPesca", "24", "+")]),
        buscar]),
    COM("Pico: un segundo para reaccionar"),
    EV([est(3), C("MouseButtonFromTextPressed", "", q("Left")), ONCE()], [nv("PescaEstado", "4"), hide("AvisoPesca"), nv("PezY", "84"), nv("PezVel", "0"), nv("PezDest", "84"), nv("BarY", "59"), nv("BarVel", "0"), nv("PescaMedida", "0.3"),
        A("SetAnimationName", "PescaPez", "PezElegido"), show("PescaPista"), show("PescaBarra"), show("PescaMedidor"), show("PescaPez"), snd("Menu/Click.wav", 70)]),
    EV([est(3), C("CompareTimer", "", q("Pesca"), ">=", "1.1")], fin + flot('"Se escapó..."', "217;87;99")),
    COM("Minijuego: mantener pulsado sube la barra, soltar la deja caer"),
    EV([est(4)], [], mueve_pez + mueve_barra + medida + [
        EV([inv_("PescaMedida", "1", ">=")], [nv("TallaPez", "RandomInRange(Peces[PezElegido].TamanoMin, Peces[PezElegido].TamanoMax)"), nv("Exp", "Peces[PezElegido].Exp", "+"),
            A("Create", "", "Recursos", f"{PJ}.X() - 16", f"{PJ}.Y() - 30", q("")), A("SetAnimationName", "Recursos", "PezElegido"), snd("HUD/SubirNivel.wav", 70)] + fin
           + flot('"¡" + Items[PezElegido].Nombre + "! " + ToString(TallaPez) + " cm"', "251;242;54", 2)),
        EV([inv_("PescaMedida", "0", "<=")], fin + flot('"Se soltó..."', "217;87;99"))]),
]
external_events(d, "Pesca", eventos)
per = EXT["Personaje"]["events"]
per.insert(next(k for k, e in enumerate(per) if e.get("target") == "Cultivos"), LINK("Pesca"))
ab = EXT["Inventario"]["events"][5]
ab["conditions"].append(ibv("Pescando", "False"))
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
