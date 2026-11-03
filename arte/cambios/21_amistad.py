"""Etapa 5: amistad propia de PapaYork. Hablar, regalar, corazones en la pestaña Vecinos, premios y diálogos según la amistad."""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
if any(e["name"] == "Amistad" for e in d["externalEvents"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}; EXT = {e["name"]: e for e in d["externalEvents"]}; L = {l["name"]: l for l in d["layouts"]}; V = {v["name"]: v for v in d["variables"]}
def img(r):
    n = "Natural/" + r + ".png"; add_resource(d, "image", n, n); return n
VEC = ("Rosa", "Fermin", "Ramiro", "Lupita", "Tomas")
GUSTOS = {  # ama, gusta, disgusta, odia, premio (id, cantidad) a los 2 corazones
 "Rosa": ("|Zanahorias|PezPapa|", "|Papa|Carpita|Fibra|Hongo|", "|Piedra|Carbon|", "|PapaRadiactiva|Mojarra|", "Abono", 5),
 "Fermin": ("|LingoteHierro|Cristal|", "|LingoteCobre|Carbon|Hierro|Cobre|", "|Zanahorias|Fibra|", "|Hongo|PezPapa|", "Carbon", 6),
 "Ramiro": ("|Trucha|Cristal|", "|Papa|Carpita|Bagre|", "|Fibra|Resina|", "|PapaRadiactiva|Nucleo|", "Antorcha", 4),
 "Lupita": ("|Hongo|PezPapa|", "|Zanahorias|Mojarra|Fibra|", "|Carbon|Piedra|", "|Bagre|Anguila|", "Semillas de Papa", 4),
 "Tomas": ("|Anguila|Lucio|ReyTuberculo|", "|Bagre|Carpita|Trucha|Papa|", "|Cristal|Cobre|", "|Nucleo|Resina|", "Trucha", 2),
}
FRASES = {
 "Rosa": ("¡Ay, mijo! Esto es justo lo que necesitaba. Eres un sol.", "Qué detalle, gracias. Lo voy a poner en el puesto.", "Bueno... gracias, supongo.", "¡Saca eso de mi puesto! ¿Quieres espantar a los clientes?", "Muchas gracias, Pedro."),
 "Fermin": ("¡Por el yunque! Esto sí es material de verdad.", "Buen material. Me sirve.", "Mmm. Esto no se forja.", "¿Me estás tomando el pelo, muchacho?", "Hm. Gracias."),
 "Ramiro": ("¡Extraordinario! Lo mencionaré en el próximo discurso.", "El pueblo agradece su gesto, joven Gutiérrez.", "Ah... qué... particular.", "¡Esto es radiactivo! ¡Llamen al consejo!", "Un gesto cívico. Gracias."),
 "Lupita": ("¡¿Para mí?! ¡Es lo mejor del mundo mundial!", "¡Qué chévere! Gracias, Pedro.", "Ew. Pero bueno, gracias.", "¡Guácala! ¡Eso huele horrible!", "¡Gracias!"),
 "Tomas": ("Ahh... este lo pesqué una vez, cuando tenía tu edad. Gracias, hijo.", "Buen ejemplar. Se ve que tienes paciencia.", "No tengo dientes para esto, muchacho.", "Eso no debería existir. Devuélvelo a donde lo sacaste.", "Gracias, hijo."),
}
DIAS = {
 "Rosa_2": ["Ya te conozco la cara de hambre, Pedro. Come bien, que el campo cobra.", "Riega temprano. La tierra agradece más la mañana que la tarde."],
 "Rosa_4": ["Tu tatarabuelo me compraba semillas a mí... bueno, a mi abuela. Decía que una papa bien cuidada nunca traiciona.", "Por eso me da miedo lo que les pasa ahora. Algo las está cambiando desde abajo."],
 "Fermin_2": ["No hablo mucho, muchacho. Pero tus herramientas se ven usadas, y eso me gusta.", "Tráeme hierro del bosque y verás lo que sale de este yunque."],
 "Fermin_4": ["Yo mismo ayudé a sellar la cueva del bosque, hace años. Esas rocas no se pusieron solas.", "Con un buen pico y un núcleo radiactivo se podría abrir. Pero piensa bien si quieres ver lo que hay adentro."],
 "Ramiro_2": ["Debo admitirlo: el pueblo habla bien de usted, joven Gutiérrez.", "Si sigue así, hasta le pongo una placa. Pequeña, claro. El presupuesto no da."],
 "Ramiro_4": ["Entre nosotros: los informes del reactor nunca se cerraron del todo.", "Hay una caja con papeles en la alcaldía. Tal vez algún día deba leerlos."],
 "Lupita_2": ["¿Sabías que las papas chiquitas se esconden cuando pasas? ¡Yo las he visto!", "No le digas a mi mamá que voy al bosque, ¿sí?"],
 "Lupita_4": ["Eres mi mejor amigo grande, Pedro.", "Te voy a contar un secreto: de noche la cueva brilla verde. ¡Yo la vi desde el puente!"],
 "Tomas_2": ["Pescar es esperar sin apurarse. Lo mismo vale para casi todo.", "En el río hay uno grande, viejo y mañoso. Le dicen el Rey Tubérculo. A mí nunca me dejó ganarle."],
 "Tomas_4": ["Yo estaba aquí la noche del reactor, ¿sabes? La luz se veía desde el lago.", "Tu familia se fue y yo me quedé. Alguien tenía que acordarse de cómo era esto antes."],
}
BASE = {"Rosa_0": "Mercado", "Fermin_0": "Herreria", "Ramiro_0": "Ramiro", "Lupita_0": "Lupita", "Tomas_0": "Tomas"}
linea = lambda q_, t: {"type": "structure", "children": [var("Quien", "string", q_), var("Texto", "string", t)]}
hijos = V["Dialogos"]["children"]
for nuevo, viejo in BASE.items():
    copia = json.loads(json.dumps(next(c for c in hijos if c["name"] == viejo))); copia["name"] = nuevo; hijos.append(copia)
for k, lineas in DIAS.items():
    hijos.append({"name": k, "type": "array", "children": [linea(k.split("_")[0], t) for t in lineas]})
hijos.append({"name": "RegaloTemp", "type": "array", "children": [linea("Rosa", "")]})
set_global_var(d, struct("Amistad", [struct(n, [var("Puntos", "number", 0), var("HabloHoy", "boolean", False), var("RegalosHoy", "number", 0), var("RegalosSemana", "number", 0), var("Premio2", "boolean", False)]) for n in VEC]))
set_global_var(d, struct("Gustos", [struct(n, [var("Ama", "string", g[0]), var("Gusta", "string", g[1]), var("Disgusta", "string", g[2]), var("Odia", "string", g[3]), var("PremioId", "string", g[4]), var("PremioCant", "number", g[5]),
    var("FraseAma", "string", FRASES[n][0]), var("FraseGusta", "string", FRASES[n][1]), var("FraseDisgusta", "string", FRASES[n][2]), var("FraseOdia", "string", FRASES[n][3]), var("FraseNeutra", "string", FRASES[n][4])]) for n, g in GUSTOS.items()]))
set_global_var(d, struct("VecinoIter", [var("Puntos", "number", 0), var("HabloHoy", "boolean", False), var("RegalosHoy", "number", 0), var("RegalosSemana", "number", 0), var("Premio2", "boolean", False)]))
for v in (var("ClaveVecino", "string", ""), var("VecinoActual", "string", ""), var("DialogoVecino", "string", ""), var("PuntosRegalo", "number", 0), var("CorazonesHoy", "number", 0), var("PremioFalta", "number", 0)):
    set_global_var(d, v)
for n_, g_ in GUSTOS.items():
    assert g_[4] in {a["name"] for a in O["Recursos"]["animations"]}, g_[4]
# Objetos
set_global_object(d, sprite_obj("Corazon", [anim_def("Vacio", [frame(img("UI/CorazonVacio"))]), anim_def("Lleno", [frame(img("UI/CorazonLleno"))])], variables=[var("Vecino", "string", ""), var("N", "number", 0)], tween=False))
set_global_object(d, sprite_obj("RetratoMini", [anim_def(n, [frame(img("Retratos/" + n))]) for n in VEC], tween=False))
set_global_object(d, sprite_obj("CorazonSube", [anim_def("N", [frame(img("UI/CorazonLleno"))])]))
lay = next(l for l in d["externalLayouts"] if l["name"] == "InventarioStardew")
def tx(x, y, clave, z=560): return inst("TextoPausa", x, y, layer="Inventario", z=z, variables=[var("Clave", "string", clave), var("Pestana", "string", "Vecinos"), var("CX", "number", 0)])
lay["instances"].append(tx(66, 46, "TituloVecinos"))
for f, n in enumerate(VEC):
    y = 62 + f * 27
    r = inst("RetratoMini", 66, y, layer="Inventario", z=556, w=24, h=24); r["numberProperties"] = [{"name": "animation", "value": f}]
    lay["instances"].append(r)
    lay["instances"].append(tx(96, y + 6, "Nombre" + n))
    lay["instances"].append(tx(290, y + 6, "Estado" + n))
    for k in range(5):
        lay["instances"].append(inst("Corazon", 190 + k * 18, y + 5, layer="Inventario", z=556, variables=[var("Vecino", "string", n), var("N", "number", k + 1)]))
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
PJ = "Personaje_jugador"
def flot(texto, color, dur=1.4):
    return [A("Create", "", "TextoFlotante", f"{PJ}.CenterX() - 40", f"{PJ}.Y() - 58", q("")), txt("TextoFlotante", texto), A("TextObject::ChangeColor", "TextoFlotante", q(color)), A("SetZOrder", "TextoFlotante", "=", "100000"),
            tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", dur), tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", dur + .8, "yes")]
SUBE = [A("Create", "", "CorazonSube", "NPC.X() + 10", "NPC.Y() - 28", q("")), A("SetZOrder", "CorazonSube", "=", "90000"), tw_y("CorazonSube", "Subir", "CorazonSube.Y() - 24", "easeOutQuad", 1.1), tw_op("CorazonSube", "Desaparecer", 0, "easeInQuad", 1.3, "yes")]
A_ = "Amistad[VecinoActual]"
tipo = lambda lista, pts, frase: EV([cmp_(f'StrFind(Gustos[VecinoActual].{lista}, "|" + ItemEnMano + "|")', "!=", "-1")], [nv("PuntosRegalo", str(pts)), sv("Dialogos.RegaloTemp[0].Texto", f"Gustos[VecinoActual].{frase}")])
cerca = cmp_(f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), NPC.X(), NPC.Y())", "<", "60")
FILA = []
for n in VEC:
    FILA += [EV([objv_s("TextoPausa", "Clave", q("Nombre" + n))], [txt("TextoPausa", f"NombresPersonajes.{n}")]),
             EV([objv_s("TextoPausa", "Clave", q("Estado" + n))], [txt("TextoPausa", f'"Regalos " + ToString(Amistad.{n}.RegalosSemana) + "/2"')]),
             EV([objv_s("TextoPausa", "Clave", q("Estado" + n)), ibv(f"Amistad.{n}.HabloHoy", "True")], [txt("TextoPausa", f'"Hablaron hoy  " + ToString(Amistad.{n}.RegalosSemana) + "/2"')])]
eventos = [
    COM("AMISTAD. Amistad[nombre] guarda Puntos (250 = un corazon, maximo 5), HabloHoy, regalos y premio. F entrega el objeto de la mano al vecino cercano."),
    EV([C("SceneJustBegins", "")], [A("Hide", "Corazon"), A("Hide", "RetratoMini")], [
        EV([objv_s("TextoPausa", "Pestana", q("Vecinos"))], [A("TextObject::Text::SetFontSize", "TextoPausa", "=", "11"), A("TextObject::ChangeColor", "TextoPausa", q("70;40;20")), A("TextObject::Text::SetOutlineEnabled", "TextoPausa", "no")]),
        EV([objv_s("TextoPausa", "Clave", q("TituloVecinos"))], [txt("TextoPausa", q("Vecinos de Papayork")), A("TextObject::Text::SetFontSize", "TextoPausa", "=", "14"), A("TextObject::ChangeColor", "TextoPausa", q("70;40;20"))])]),
    COM("Hablar al abrir el dialogo: el primero del dia da 20 puntos. El dialogo cambia con la amistad"),
    EV([ibv("InventarioAbierto", "False"), C("IsCursorOnObject", "NPC", "", "", ""), C("MouseButtonFromTextReleased", "", q("Left")), cerca],
       [sv("VecinoActual", "NPC.Animation::Name()")], [
        EV([], [sv("DialogoVecino", 'VecinoActual + "_" + ToString(min(4, floor(Amistad[VecinoActual].Puntos / 500) * 2))'), sv("DialogoPedido", "DialogoVecino")]),
        EV([ibv(f"{A_}.HabloHoy", "False")], [bv(f"{A_}.HabloHoy", "True"), nv(f"{A_}.Puntos", f"min(1249, {A_}.Puntos + 20)")] + SUBE),
        EV([inv_(f"{A_}.Puntos", "500", ">="), ibv(f"{A_}.Premio2", "False")], [bv(f"{A_}.Premio2", "True")], [
            C and {"type": "BuiltinCommonInstructions::Repeat", "repeatExpression": "Gustos[VecinoActual].PremioCant", "conditions": [], "actions": [A("Create", "", "Recursos", f"{PJ}.X() - 16", f"{PJ}.Y() - 30", q("")), A("SetAnimationName", "Recursos", "Gustos[VecinoActual].PremioId")]},
            EV([], flot('"¡Te dio un regalo!"', "251;242;54", 2))])]),
    COM("Regalar con F"),
    EV([ibv("InventarioAbierto", "False"), ibv("DialogoAbierto", "False"), C("KeyFromTextReleased", "", q("f")), C("PickNearest", "NPC", f"{PJ}.X()", f"{PJ}.Y()", ""), cerca,
        isv("ItemEnMano", q(""), "!="), isv("Items[ItemEnMano].Tipo", q("Herramienta"), "!="), inv_("Mochila[RanuraSeleccionada].Cantidad", "1", ">=")],
       [sv("VecinoActual", "NPC.Animation::Name()")], [
        EV([inv_(f"{A_}.RegalosHoy", "1", ">=")], flot('"Ya le diste un regalo hoy"', "230;170;60")),
        EV([inv_(f"{A_}.RegalosHoy", "1", "<"), inv_(f"{A_}.RegalosSemana", "2", ">=")], flot('"Ya van dos regalos esta semana"', "230;170;60")),
        EV([inv_(f"{A_}.RegalosHoy", "1", "<"), inv_(f"{A_}.RegalosSemana", "2", "<")],
           [nv("PuntosRegalo", "20"), sv("Dialogos.RegaloTemp[0].Quien", "VecinoActual"), sv("Dialogos.RegaloTemp[0].Texto", "Gustos[VecinoActual].FraseNeutra")], [
            tipo("Ama", 80, "FraseAma"), tipo("Gusta", 45, "FraseGusta"), tipo("Disgusta", -20, "FraseDisgusta"), tipo("Odia", -40, "FraseOdia"),
            EV([], [nv(f"{A_}.Puntos", f"max(0, min(1249, {A_}.Puntos + PuntosRegalo))"), nv(f"{A_}.RegalosHoy", "1", "+"), nv(f"{A_}.RegalosSemana", "1", "+"), nv("Mochila[RanuraSeleccionada].Cantidad", "1", "-"),
                    sv("DialogoPedido", q("RegaloTemp")), bv("DialogoPausa", "True"), sv("DialogoVecino", q(""))]),
            EV([inv_("PuntosRegalo", "0", ">")], SUBE)])]),
    COM("Aviso cerca de un vecino"),
    EV([C("Visible", "AvisoNPC"), isv("ItemEnMano", q(""), "!="), isv("Items[ItemEnMano].Tipo", q("Herramienta"), "!=")], [txt("AvisoNPC", q("Clic: hablar   F: regalar"))]),
    EV([C("Visible", "AvisoNPC"), isv("ItemEnMano", q(""))], [txt("AvisoNPC", q("Clic: hablar"))]),
    EV([C("Visible", "AvisoNPC"), isv("Items[ItemEnMano].Tipo", q("Herramienta"))], [txt("AvisoNPC", q("Clic: hablar"))]),
    COM("Pestana de vecinos: corazones y estado"),
    EV([ibv("VerPausa", "True"), isv("PestanaActual", q("Vecinos"))], [show("Corazon"), show("RetratoMini")], [
        FOREACH("Corazon", [], [anim("Corazon", q("Vacio"))], [EV([cmp_("Amistad[Corazon.Vecino].Puntos", ">=", "Corazon.N * 250")], [anim("Corazon", q("Lleno"))])])] + FILA),
    EV([ibv("VerPausa", "False")], [A("Hide", "Corazon"), A("Hide", "RetratoMini")]),
    EV([isv("PestanaActual", q("Vecinos"), "!=")], [A("Hide", "Corazon"), A("Hide", "RetratoMini")]),
]
external_events(d, "Amistad", eventos)
per = EXT["Personaje"]["events"]
per.insert(next(k for k, e in enumerate(per) if e.get("target") == "Tienda"), LINK("Amistad"))
# La tienda ya no pide su dialogo: lo hace Amistad, y se abre al terminar cualquier dialogo de ese vecino
tie = EXT["Tienda"]["events"]
tie[5]["actions"] = [a for a in tie[5]["actions"] if a["parameters"][0] != "DialogoPedido"]
tie[6]["conditions"][0]["parameters"][2] = "DialogoVecino"
tie[6]["conditions"].append(isv("DialogoVecino", q(""), "!="))
tie[6]["actions"].append(sv("DialogoVecino", q("")))
# Cada noche: amistad que se enfría sin hablar, y contadores
for e in EXT["NuevoDia"]["events"]:
    if e.get("conditions") and e["conditions"][0]["parameters"][0] == "PedirNuevoDia":
        e["events"].append({"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Amistad", "valueIteratorVariableName": "VecinoIter", "keyIteratorVariableName": "ClaveVecino", "conditions": [], "actions": [], "events": [
            EV([ibv("VecinoIter.HabloHoy", "False")], [nv("Amistad[ClaveVecino].Puntos", "max(0, Amistad[ClaveVecino].Puntos - 2)")]),
            EV([], [bv("Amistad[ClaveVecino].HabloHoy", "False"), nv("Amistad[ClaveVecino].RegalosHoy", "0")]),
            EV([cmp_("mod(Calendario.DiaTotal, 7)", "=", "1")], [nv("Amistad[ClaveVecino].RegalosSemana", "0")])]})
# Guardar y cargar
gu = EXT["Guardado"]["events"][2]["events"][8]["actions"]
gu.insert(next(k for k, a in enumerate(gu) if a["type"]["value"] == "SetStringVariable"), A("EcrireFichierTxt", q("PapayorkPartidas"), '"Ranura" + ToString(RanuraActual) + "/Amistad"', "ToJSON(Amistad)"))
menu = L["Menu Principal"]["events"]; carga = menu[37]["events"]
idx = next(k for k, e in enumerate(carga) if "/Granja" in json.dumps(e, ensure_ascii=False))
carga.insert(idx + 1, json.loads(json.dumps(carga[idx], ensure_ascii=False).replace('/Granja\\"', '/Amistad\\"').replace('"Granja"', '"Amistad"')))
limpia = {n: {"Puntos": 0, "HabloHoy": False, "RegalosHoy": 0, "RegalosSemana": 0, "Premio2": False} for n in VEC}
menu[35]["actions"].insert(0, A("JSONToGlobalVariableStructure", q(json.dumps(limpia, separators=(",", ":"))), "Amistad"))
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
