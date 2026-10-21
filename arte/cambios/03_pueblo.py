"""Paso 4: el pueblo con mercado (Dona Rosa) y herreria (Don Fermin).

- Mercado: compra semillas, abono y antorchas; vende cualquier objeto con precio (clic izquierdo: toda la pila,
  clic derecho: una unidad). El precio de venta es Items[Id].Precio.
- Herreria: mejoras de espada, hacha y pico (cobre y luego hierro) pagadas con monedas y lingotes.
  Se guardan en Estadisticas.NivelEspada / NivelHacha / NivelPico (Estadisticas ya se guarda en la partida).
  Hacha y pico mejorados quitan 1 + nivel de vida por golpe; la espada sube el dano.
- Tiendas[Mercado|Herreria] = lista de ofertas. El panel reutiliza las casillas del inventario con los grupos
  "Oferta" (lo que vende el NPC) y "Venta" (tu mochila).
"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
def cmp(a, op, b): return C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
def ext(n): return next(e for e in d["externalEvents"] if e["name"] == n)

# ---------- datos ----------
MERCADO = [("Semillas de Zanahoria", 20), ("Semillas de Papa", 30), ("Semillas de Papa Mutante", 150), ("Abono", 25), ("Antorcha", 15)]
HERRERIA = [  # icono, nombre, descripcion, monedas, lingote, cantidad, clave, nivel, +dano min, +dano max
    ("EspadaCobre", "Espada de cobre", "Forjada en cobre: +2 de daño mínimo y +4 de daño máximo.", 300, "LingoteCobre", 4, "NivelEspada", 1, 2, 4),
    ("EspadaHierro", "Espada de hierro", "Acero del valle: +3 de daño mínimo y +6 de daño máximo.", 900, "LingoteHierro", 4, "NivelEspada", 2, 3, 6),
    ("HachaCobre", "Hacha de cobre", "Cada hachazo cuenta doble: los árboles caen más rápido.", 200, "LingoteCobre", 3, "NivelHacha", 1, 0, 0),
    ("HachaHierro", "Hacha de hierro", "Cada hachazo cuenta triple.", 600, "LingoteHierro", 3, "NivelHacha", 2, 0, 0),
    ("PicoCobre", "Pico de cobre", "Cada golpe cuenta doble: rocas y vetas se rompen antes.", 200, "LingoteCobre", 3, "NivelPico", 1, 0, 0),
    ("PicoHierro", "Pico de hierro", "Cada golpe cuenta triple.", 600, "LingoteHierro", 3, "NivelPico", 2, 0, 0),
]
def oferta(i, precio, extra=()): return {"type": "structure", "children": [var("Id", "string", i), var("Precio", "number", precio), *extra]}
set_global_var(d, struct("Tiendas", [
    {"name": "Mercado", "type": "array", "children": [oferta(i, p, [var("Tipo", "string", "Item")]) for i, p in MERCADO]},
    {"name": "Herreria", "type": "array", "children": [oferta(i, m, [
        var("Tipo", "string", "Mejora"), var("Nombre", "string", n), var("Descripcion", "string", ds), var("Lingote", "string", l),
        var("Cantidad", "number", c), var("Clave", "string", k), var("Nivel", "number", nv), var("DanoMin", "number", dmin),
        var("DanoMax", "number", dmax)]) for i, n, ds, m, l, c, k, nv, dmin, dmax in HERRERIA]}]))
est = next(v for v in d["variables"] if v["name"] == "Estadisticas")
for k in ("NivelEspada", "NivelHacha", "NivelPico"):
    if not any(c["name"] == k for c in est["children"]): est["children"].append(var(k, "number", 0))
for v in [var("TiendaAbierta", "boolean", False), var("TipoTienda", "string", "Mercado")]: set_global_var(d, v)

# ---------- recursos y objetos ----------
for f in ["Rosa1", "Rosa2", "Fermin1", "Fermin2", "PuestoMercado", "Herreria1", "Herreria2", "PanelTienda",
          "EspadaCobre", "EspadaHierro", "HachaCobre", "HachaHierro", "PicoCobre", "PicoHierro"]:
    add_resource(d, "image", "Pueblo/" + f + ".png", "Pueblo/" + f + ".png")
ico = O["IconoItem"]
ico["animations"] = [a for a in ico["animations"] if a["name"] not in {h[0] for h in HERRERIA}]
ico["animations"] += [anim_def(h[0], [frame("Pueblo/%s.png" % h[0], (16, 16))]) for h in HERRERIA]
def parpadeo(nombre):  # 5 cuadros quieto + 1 parpadeando = parpadea cada 3 segundos
    return anim_def(nombre, [frame("Pueblo/%s1.png" % nombre, (0, 0), rect(10, 4, 22, 26))] * 5 + [frame("Pueblo/%s2.png" % nombre, (0, 0), rect(10, 4, 22, 26))], loop=True, dt=0.5)
npc = sprite_obj("NPC", [parpadeo("Rosa"), parpadeo("Fermin")], [var("Tienda", "string", ""), var("Saludo", "string", "")], tween=False)
puesto = sprite_obj("Puesto", [anim_def("Mercado", [frame("Pueblo/PuestoMercado.png", (0, 0), rect(4, 36, 62, 58))]),
                               anim_def("Herreria", [frame("Pueblo/Herreria%d.png" % i, (0, 0), rect(2, 28, 64, 50)) for i in (1, 2)], loop=True, dt=0.16)],
                    [var("Tienda", "string", "")], tween=False)
TEXTOS = [text_obj("TituloTienda", "", 13, (255, 236, 170), (60, 30, 12)), text_obj("DineroTienda", "", 10, (251, 242, 54), (36, 21, 13)),
          text_obj("NombreTienda", "", 13, (255, 246, 210), None), text_obj("DetalleTienda", "", 10, (235, 220, 190), None),
          text_obj("DescTienda", "", 10, (220, 200, 170), None), text_obj("AvisoNPC", "Clic: hablar", 9, (255, 246, 210), (36, 21, 13))]
for o in [npc, puesto, sprite_obj("PanelTienda", [anim_def("", [frame("Pueblo/PanelTienda.png")])], tween=False)] + TEXTOS:
    set_global_object(d, o)

# ---------- instancias ----------
for lay in d["layouts"]:
    if lay["name"] == "Pueblo":
        lay["instances"] = [i for i in lay["instances"] if i["name"] not in ("NPC", "Puesto", "AvisoNPC")]
        def con(nombre, x, y, z, anim_idx, vars_):
            i = inst(nombre, x, y, "", z, variables=vars_); i["numberProperties"] = [{"name": "animation", "value": anim_idx}]; return i
        lay["instances"] += [
            con("Puesto", 790, 340, 396, 0, [var("Tienda", "string", "Mercado")]),
            con("NPC", 806, 352, 395, 0, [var("Tienda", "string", "Mercado"), var("Saludo", "string", "Doña Rosa: ¡Las mejores semillas del valle!")]),
            con("Puesto", 900, 344, 392, 1, [var("Tienda", "string", "Herreria")]),
            con("NPC", 926, 352, 393, 1, [var("Tienda", "string", "Herreria"), var("Saludo", "string", "Don Fermín: Trae lingotes y te forjo algo bueno.")]),
            inst("AvisoNPC", 0, 0, "", 100000)]
L = "Inventario"
lay_inv = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
lay_inv["instances"] = [i for i in lay_inv["instances"] if i["name"] not in ("PanelTienda",) + tuple(t["name"] for t in TEXTOS)
                        and not any(v["name"] == "Grupo" and v["value"] in ("Oferta", "Venta") for v in i.get("initialVariables", []))]
TX, TY = 50, 12
lay_inv["instances"] += [inst("PanelTienda", TX, TY, L, 510), inst("TituloTienda", TX + 16, TY + 13, L, 550),
                         inst("DineroTienda", TX + 250, TY + 16, L, 550), inst("NombreTienda", TX + 16, TY + 194, L, 550),
                         inst("DetalleTienda", TX + 250, TY + 196, L, 550), inst("DescTienda", TX + 16, TY + 213, L, 550)]
def casilla(x, y, idx, grupo, z):
    g = [var("Indice", "number", idx), var("Grupo", "string", grupo)]
    return [inst("SlotUI", x, y, L, z, variables=g + [var("Puede", "boolean", False)]), inst("IconoItem", x + 17, y + 17, L, z + 10, variables=g),
            inst("CantidadItem", x + 18, y + 20, L, z + 20, variables=g + [var("SX", "number", x + 31)])]
for k in range(6): lay_inv["instances"] += casilla(TX + 24 + k * 48, TY + 30, k, "Oferta", 520)
for r in range(3):
    for c in range(10): lay_inv["instances"] += casilla(TX + 20 + c * 34, TY + 82 + r * 36, r * 10 + c, "Venta", 520)

# ---------- ajustes al inventario y herramientas existentes ----------
inv = ext("Inventario")
for e in recorrer(inv["events"]):
    conds = e.get("conditions") or []
    if any(c["type"]["value"] == "BooleanVariable" and c["parameters"][:2] == ["FabricarAbierto", "False"] for c in conds) \
            and not any(c["parameters"][:1] == ["TiendaAbierta"] for c in conds):
        conds.append(ibv("TiendaAbierta", "False"))
    for c in conds:  # los grupos Oferta, como Receta, no los dibuja el inventario
        if c["type"]["value"] == "StringObjectVariable" and c["parameters"][1:] == ["Grupo", "!=", '"Receta"'] \
                and not any(x["parameters"][1:] == ["Grupo", "!=", '"Oferta"'] for x in conds):
            conds.append(objv_s(c["parameters"][0], "Grupo", q("Oferta"), "!=")); break
herr = ext("Herramientas")
for e in recorrer(herr["events"]):
    for a in e.get("actions") or []:
        if a["type"]["value"] == "SetNumberObjectVariable" and a["parameters"][1:3] == ["Vida", "-"]:
            if a["parameters"][0] == "Objetos_Fisicos": a["parameters"][3] = "1 + Estadisticas.NivelHacha"
            if a["parameters"][0] == "Rocas": a["parameters"][3] = "1 + Estadisticas.NivelPico"

# ---------- eventos de la tienda ----------
UI = ["PanelTienda", "TituloTienda", "DineroTienda", "NombreTienda", "DetalleTienda", "DescTienda", "FondoOscuro"]
def grupos(accion): return [EV([objv_s(o, "Grupo", q(g))], [accion(o)]) for g in ("Oferta", "Venta") for o in ("SlotUI", "IconoItem", "CantidadItem")]
OF = "Tiendas[TipoTienda][SlotUI.Indice]"
def nombres_herramientas():
    ev = []
    for herr_id, clave, nombres in [("Hacha", "NivelHacha", ["Hacha", "Hacha de cobre", "Hacha de hierro"]),
                                    ("Pico", "NivelPico", ["Pico", "Pico de cobre", "Pico de hierro"])]:
        for nv, n in enumerate(nombres):
            ev.append(EV([inv_("Estadisticas." + clave, str(nv))], [sv("Items." + herr_id + ".Nombre", q(n))]))
    return ev
def contar(item):
    return [EV([], [nv("Tienes", "0"), nv("k", "0")]),
            REPEAT(30, [], [], [EV([isv("Mochila[k].Id", item)], [nv("Tienes", "Mochila[k].Cantidad", "+")]), EV([], [nv("k", "1", "+")])])]
def flot(texto, rgb):
    return [A("Create", "", "TextoFlotante", "Personaje_jugador.CenterX() - 30", "Personaje_jugador.Y() - 30", q("")), txt("TextoFlotante", texto),
            color("TextoFlotante", rgb), A("SetZOrder", "TextoFlotante", "=", "100000"),
            tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", 1), tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 1.5, "yes")]
DIST = "DistanceBetweenPositions(Personaje_jugador.X(), Personaje_jugador.Y(), NPC.X() + 16, NPC.Y() + 28)"
LOCALES = [var("k", "number", 0), var("Tienes", "number", 0), var("Ok", "boolean", False), var("Falta", "number", 0), var("Quitar", "number", 0)]

E = [COM("TIENDAS DEL PUEBLO\nTiendas[TipoTienda][i] = oferta. Grupo Oferta = lo que vende el NPC, grupo Venta = tu mochila (clic: vender).")]
E.append(EV([C("SceneJustBegins", "")], [bv("TiendaAbierta", "False"), hide("AvisoNPC"), *[hide(o) for o in UI if o != "FondoOscuro"],
                                         A("SetZOrder", "Puesto", "=", "Puesto.Y() + 50")], [
    *grupos(hide), *nombres_herramientas(),
    EV([objv_s("NPC", "Tienda", q("Mercado"))], [anim("NPC", q("Rosa")), A("SetZOrder", "NPC", "=", "Puesto.Y() + 40")]),
    EV([objv_s("NPC", "Tienda", q("Herreria"))], [anim("NPC", q("Fermin")), A("SetZOrder", "NPC", "=", "NPC.Y() + 60")])]))
E.append(COM("Aviso para hablar cuando Pedro esta cerca"))
E.append(EV([], [hide("AvisoNPC")], [
    EV([ibv("InventarioAbierto", "False"), C("PickNearest", "NPC", "Personaje_jugador.X()", "Personaje_jugador.Y()", ""), cmp(DIST, "<", "60")], [
        show("AvisoNPC"), A("SetX", "AvisoNPC", "=", "NPC.X() - 4"), A("SetY", "AvisoNPC", "=", "NPC.Y() - 10")])]))

E.append(COM("Abrir la tienda: clic en el NPC estando cerca"))
E.append(EV([ibv("InventarioAbierto", "False"), cursor("NPC"), released(), cmp(DIST, "<", "60")], [
    sv("TipoTienda", "NPC.Tienda"), bv("TiendaAbierta", "True"), bv("InventarioAbierto", "True"), sv("GrupoVisible", q("Venta")),
    A("ChangeLayerTimeScale", "", q(""), "0"), A("PauseTimer", "", q("PasoTiempo")), hide("BarraRapida"), hide("AvisoNPC"),
    opacity("EtiquetaItem", 0), opacity("TextoEtiqueta", 0), *[show(o) for o in UI], txt("TituloTienda", "NPC.Saludo"),
    snd("Inventario/AbrirMochila.wav", 60)], grupos(show)))
E.append(COM("Cerrar la tienda (E, I o Esc)"))
E.append(EV([ibv("TiendaAbierta", "True")], [], [
    EV([key_released("e")], [bv("Cerrar", "True")]), EV([key_released("i")], [bv("Cerrar", "True")]),
    EV([key_released("Escape")], [bv("Cerrar", "True")]),
    EV([ibv("Cerrar", "True")], [bv("TiendaAbierta", "False"), bv("InventarioAbierto", "False"), sv("GrupoVisible", q("Barra")),
                                 A("ChangeLayerTimeScale", "", q(""), "1"), A("UnPauseTimer", "", q("PasoTiempo")), show("BarraRapida"),
                                 *[hide(o) for o in UI], snd("Inventario/CerrarMochila.wav", 60)], grupos(hide))],
    variables=[var("Cerrar", "boolean", False)]))

E.append(COM("Con la tienda abierta: ofertas, precios, que se puede comprar y la informacion bajo el mouse"))
E.append(EV([ibv("TiendaAbierta", "True")], [
    txt("DineroTienda", '"Tienes " + ToString(Monedas) + " monedas"'), A("SetX", "DineroTienda", "=", "%d - DineroTienda.Width()" % (TX + 364)),
    txt("NombreTienda", '""'), txt("DetalleTienda", '""'),
    txt("DescTienda", q("Clic en tus objetos para venderlos (clic derecho: solo uno).   E: salir"))], [
    FOREACH("IconoItem", [objv_s("IconoItem", "Grupo", q("Oferta"))], [hide("IconoItem")], [
        EV([cmp("IconoItem.Indice", "<", "VariableChildCount(Tiendas[TipoTienda])")], [show("IconoItem"), anim("IconoItem", "Tiendas[TipoTienda][IconoItem.Indice].Id")])]),
    FOREACH("CantidadItem", [objv_s("CantidadItem", "Grupo", q("Oferta"))], [hide("CantidadItem")], [
        EV([cmp("CantidadItem.Indice", "<", "VariableChildCount(Tiendas[TipoTienda])")], [
            show("CantidadItem"), txt("CantidadItem", "ToString(Tiendas[TipoTienda][CantidadItem.Indice].Precio)"),
            A("SetX", "CantidadItem", "=", "CantidadItem.SX - CantidadItem.Width()")])]),
    FOREACH("SlotUI", [objv_s("SlotUI", "Grupo", q("Oferta"))], [set_objv_b("SlotUI", "Puede", "False")], [
        EV([cmp("SlotUI.Indice", ">=", "VariableChildCount(Tiendas[TipoTienda])")], [hide("SlotUI")]),
        EV([cmp("SlotUI.Indice", "<", "VariableChildCount(Tiendas[TipoTienda])"), cmp("Monedas", ">=", OF + ".Precio")], [set_objv_b("SlotUI", "Puede", "True")], [
            EV([isv(OF + ".Tipo", q("Mejora"))], [], [
                *contar(OF + ".Lingote"),
                EV([cmp("Tienes", "<", OF + ".Cantidad")], [set_objv_b("SlotUI", "Puede", "False")]),
                EV([cmp("Estadisticas[" + OF + ".Clave]", "!=", OF + ".Nivel - 1")], [set_objv_b("SlotUI", "Puede", "False")])])]),
        EV([objv_s("IconoItem", "Grupo", q("Oferta")), objv_n("IconoItem", "Indice", "SlotUI.Indice")], [opacity("IconoItem", 255)], [
            EV([objv_b("SlotUI", "Puede", "False")], [opacity("IconoItem", 80)])])]),
    COM("Informacion de la oferta bajo el mouse"),
    EV([cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Oferta")), cmp("SlotUI.Indice", "<", "VariableChildCount(Tiendas[TipoTienda])")], [], [
        EV([isv(OF + ".Tipo", q("Item"))], [txt("NombreTienda", "Items[" + OF + ".Id].Nombre"), txt("DescTienda", "Items[" + OF + ".Id].Descripcion"),
                                           txt("DetalleTienda", '"Cuesta " + ToString(' + OF + '.Precio) + " monedas"')]),
        EV([isv(OF + ".Tipo", q("Mejora"))], [txt("NombreTienda", OF + ".Nombre"), txt("DescTienda", OF + ".Descripcion")], [
            *contar(OF + ".Lingote"),
            EV([], [txt("DetalleTienda", 'ToString(' + OF + '.Precio) + " monedas + " + ToString(' + OF + '.Cantidad) + " " + Items[' + OF +
                                        '.Lingote].Nombre + " (tienes " + ToString(Tienes) + ")"')]),
            EV([cmp("Estadisticas[" + OF + ".Clave]", ">=", OF + ".Nivel")], [txt("DetalleTienda", q("Ya la tienes"))]),
            EV([cmp("Estadisticas[" + OF + ".Clave]", "<", OF + ".Nivel - 1")], [txt("DetalleTienda", q("Primero compra la mejora de cobre"))])]),
        EV([objv_b("SlotUI", "Puede", "True")], [color("DetalleTienda", "143;220;46")]),
        EV([objv_b("SlotUI", "Puede", "False")], [color("DetalleTienda", "217;87;99")])]),
    COM("Informacion de tus objetos (para vender)"),
    EV([cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Venta")), isv("Mochila[SlotUI.Indice].Id", '""', "!=")], [
        sv("VId", "Mochila[SlotUI.Indice].Id"), txt("NombreTienda", "Items[VId].Nombre"), txt("DescTienda", "Items[VId].Descripcion")], [
        EV([cmp("Items[VId].Precio", ">", "0"), isv("Items[VId].Tipo", q("Herramienta"), "!=")], [
            txt("DetalleTienda", '"Vende a " + ToString(Items[VId].Precio) + " c/u  (todo: " + ToString(Items[VId].Precio * Mochila[SlotUI.Indice].Cantidad) + ")"'),
            color("DetalleTienda", "251;242;54")]),
        EV([cmp("Items[VId].Precio", "<=", "0")], [txt("DetalleTienda", q("No se puede vender")), color("DetalleTienda", "217;87;99")]),
        EV([isv("Items[VId].Tipo", q("Herramienta"))], [txt("DetalleTienda", q("No se puede vender")), color("DetalleTienda", "217;87;99")])]),
    EV([], [A("SetX", "DetalleTienda", "=", "%d - DetalleTienda.Width()" % (TX + 364))]),
], variables=LOCALES + [var("VId", "string", "")]))

E.append(COM("Comprar una oferta"))
E.append(EV([ibv("TiendaAbierta", "True"), cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Oferta")), released()], [], [
    EV([objv_b("SlotUI", "Puede", "False")], [snd("Inventario/Seleccion.wav", 40)]),
    EV([objv_b("SlotUI", "Puede", "True")], [nv("Monedas", OF + ".Precio", "-"), snd("HUD/Moneda.wav", 70)], [
        EV([isv(OF + ".Tipo", q("Item"))], [
            A("Create", "", "Recursos", "Personaje_jugador.X() - 16", "Personaje_jugador.Y() - 22", q("")),
            anim("Recursos", OF + ".Id"), set_objv_b("Recursos", "Nuevo", "False"), A("ResetObjectTimer", "Recursos", q("Soltado"))]),
        EV([isv(OF + ".Tipo", q("Mejora"))], [
            nv("Falta", OF + ".Cantidad"), nv("k", "0"), nv("Estadisticas[" + OF + ".Clave]", OF + ".Nivel"),
            nv('Estadisticas["Daño Min"]', OF + ".DanoMin", "+"), nv('Estadisticas["Daño Max"]', OF + ".DanoMax", "+"),
            snd("HUD/SubirNivel.wav", 60), *flot('"¡" + ' + OF + '.Nombre + " lista!"', "214;255;106")], [
            REPEAT(30, [], [], [
                EV([isv("Mochila[k].Id", OF + ".Lingote"), inv_("Falta", "0", ">")], [
                    nv("Quitar", "min(Falta, Mochila[k].Cantidad)"), nv("Mochila[k].Cantidad", "Quitar", "-"), nv("Falta", "Quitar", "-")]),
                EV([], [nv("k", "1", "+")])]),
            *nombres_herramientas()])])], variables=LOCALES))

E.append(COM("Vender: clic izquierdo vende toda la pila, clic derecho vende una unidad"))
for boton, cuanto in (("Left", "Mochila[SlotUI.Indice].Cantidad"), ("Right", "1")):
    E.append(EV([ibv("TiendaAbierta", "True"), cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Venta")), released(boton),
                 isv("Mochila[SlotUI.Indice].Id", '""', "!="), cmp("Items[Mochila[SlotUI.Indice].Id].Precio", ">", "0"),
                 isv("Items[Mochila[SlotUI.Indice].Id].Tipo", q("Herramienta"), "!=")], [
        nv("Ganas", "Items[Mochila[SlotUI.Indice].Id].Precio * " + cuanto), nv("Monedas", "Ganas", "+"),
        nv("Mochila[SlotUI.Indice].Cantidad", cuanto, "-"), snd("HUD/Moneda.wav", 60),
        *flot('"+" + ToString(Ganas) + " monedas"', "251;242;54")], variables=[var("Ganas", "number", 0)]))

E.append(COM("Las herramientas mejoradas se ven de cobre o de hierro en la mochila y en la barra"))
for herr_id, clave in (("Hacha", "NivelHacha"), ("Pico", "NivelPico")):
    for nv_, metal in ((1, "Cobre"), (2, "Hierro")):
        for suf in ("", "_mini"):
            E.append(EV([inv_("Estadisticas." + clave, str(nv_)),
                         C("AnimatableCapability::AnimatableBehavior::Name", "IconoItem", "Animation", "=", q(herr_id + suf))],
                        [anim("IconoItem", q(herr_id + metal + suf))]))
external_events(d, "Tienda", E)
pers = ext("Personaje")
if not any(e.get("target") == "Tienda" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("Tienda"))
# Pedro no atraviesa los puestos
fab = ext("Fabricacion")
if '"Puesto"' not in json.dumps(fab["events"]):
    fab["events"].append(EV([C("CollisionNP", "Personaje_jugador", "Puesto", "", "", "")], [A("SeparateFromObjects", "Personaje_jugador", "Puesto", "")]))
json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: pueblo con mercado y herreria")
