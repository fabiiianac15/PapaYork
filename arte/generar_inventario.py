"""Inventario estilo Stardew para Papayork.

- Mochila global de 30 casillas (Mochila[0..29] = {Id, Cantidad}); las 10 primeras son la barra rapida.
- Catalogo de objetos en la variable global Items (nombre, tipo, rareza, maximo por pila, descripcion, precio).
- Barra rapida siempre visible; E / I abre la mochila (pausa el mundo); clic para tomar, soltar, juntar o cambiar.
- Las herramientas y la siembra usan ItemEnMano (lo que hay en la casilla seleccionada).

Uso: python3 arte/generar_inventario.py "Legado Radioactivo-Papayork.json"
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gdutil import *

PROJ = sys.argv[1]
d = json.load(open(PROJ, encoding="utf8"))
N = 30

# ---------- catalogo de objetos ----------
# id (= nombre de la animacion del objeto en el mundo y del icono): datos
CATALOGO = [
    ("Azadon", "Azadón", "Herramienta", "Común", 1, 0, "Ara la tierra para poder sembrar. Haz clic en el suelo."),
    ("Hacha", "Hacha", "Herramienta", "Común", 1, 0, "Tala árboles para conseguir madera."),
    ("Pico", "Pico", "Herramienta", "Común", 1, 0, "Rompe rocas para conseguir piedra."),
    ("Madera", "Madera", "Recurso", "Común", 99, 2, "Material básico para cercas, cofres y casas."),
    ("Piedra", "Piedra", "Recurso", "Común", 99, 2, "Sirve para caminos, hornos y mejoras."),
    ("Semillas de Zanahoria", "Semillas de zanahoria", "Semilla", "Común", 99, 5, "Siémbralas en tierra arada. Crecen en 4 etapas."),
    ("Semillas de Tomate", "Semillas de tomate", "Semilla", "Poco común", 99, 10, "Todavía no se pueden sembrar: pronto en Papayork."),
    ("Zanahorias", "Zanahoria", "Cultivo", "Común", 99, 15, "Fresca y crujiente. Se podrá vender en el pueblo."),
]
# icono = imagen que ya usa el objeto del mundo con esa animacion
ICONOS = {}
for o in d["objects"]:
    if o["name"] in ("Herramientas", "Caja_de_Semillas", "Recursos", "Verduras"):
        for a in o["animations"]:
            ICONOS[a["name"]] = a["directions"][0]["sprites"][0]["image"]
RAREZA_COLOR = {"Común": "235;220;190", "Poco común": "143;220;46", "Raro": "110;180;255", "Épico": "214;120;255"}

set_global_var(d, struct("Items", [struct(i, [var("Nombre", "string", n), var("Tipo", "string", t), var("Rareza", "string", r),
                                              var("Max", "number", m), var("Precio", "number", p), var("Descripcion", "string", ds)])
                                   for i, n, t, r, m, p, ds in CATALOGO]))
set_global_var(d, {"name": "Mochila", "type": "array", "children": [
    {"type": "structure", "children": [var("Id", "string", ""), var("Cantidad", "number", 0)]} for _ in range(N)]})
set_global_var(d, struct("Mano", [var("Id", "string", ""), var("Cantidad", "number", 0)]))
set_global_var(d, var("RanuraSeleccionada", "number", 0))
set_global_var(d, var("ItemEnMano", "string", ""))
set_global_var(d, var("InventarioAbierto", "boolean", False))
set_global_var(d, var("MouseSobreUI", "boolean", False))
set_global_var(d, var("FabricarAbierto", "boolean", False))

# ---------- recursos ----------
for n in ["Casilla", "CasillaHover", "CasillaSeleccionada", "BarraRapida", "PanelMochila", "EtiquetaItem"]:
    add_resource(d, "image", "Inventario/" + n + ".png", "Inventario/" + n + ".png")
for n in ["Recoger", "AbrirMochila", "CerrarMochila", "Seleccion"]:
    add_resource(d, "audio", "Inventario/" + n + ".wav", "Inventario/" + n + ".wav")
add_resource(d, "image", "Menu/Negro.png", "Menu/Negro.png")
add_resource(d, "font", FONT, FONT)

# ---------- objetos globales (existen en todos los niveles) ----------
GRUPO = [var("Indice", "number", 0), var("Grupo", "string", "")]
for o in [
    sprite_obj("SlotUI", [anim_def("Normal", [frame("Inventario/Casilla.png")]),
                          anim_def("Hover", [frame("Inventario/CasillaHover.png")]),
                          anim_def("Seleccionada", [frame("Inventario/CasillaSeleccionada.png")])], GRUPO, tween=False),
    sprite_obj("IconoItem", [anim_def(i, [frame(ICONOS[i], (16, 16))]) for i, *_ in CATALOGO], GRUPO, tween=False),
    text_obj("CantidadItem", "", 10, (255, 250, 230), (36, 21, 13), variables=GRUPO + [var("SX", "number", 0)]),
    sprite_obj("BarraRapida", [anim_def("", [frame("Inventario/BarraRapida.png")])], tween=False),
    sprite_obj("PanelMochila", [anim_def("", [frame("Inventario/PanelMochila.png")])], tween=False),
    sprite_obj("FondoOscuro", [anim_def("", [frame("Menu/Negro.png")])], tween=False),
    sprite_obj("EtiquetaItem", [anim_def("", [frame("Inventario/EtiquetaItem.png")])]),
    text_obj("TextoEtiqueta", "", 11, (255, 246, 210), None, tween=True),
    text_obj("TituloMochila", "Mochila", 14, (255, 236, 170), (60, 30, 12)),
    text_obj("AyudaMochila", "Clic: tomar y soltar     E: cerrar", 10, (90, 55, 28), None),
    text_obj("TextoInfoNombre", "", 13, (255, 246, 210), None),
    text_obj("TextoInfoTipo", "", 10, (235, 220, 190), None),
    text_obj("TextoInfoDesc", "", 10, (220, 200, 170), None),
    text_obj("TextoFlotante", "", 10, (255, 250, 220), (36, 21, 13), tween=True),
]:
    set_global_object(d, o)

# ---------- diseño externo InventarioStardew (se crea al empezar cada nivel desde Personaje) ----------
L = "Inventario"
ins = [inst("BarraRapida", 64, 226, L, 100), inst("EtiquetaItem", 180, 208, L, 140), inst("TextoEtiqueta", 190, 210, L, 150),
       inst("FondoOscuro", 0, 0, L, 500, 480, 270), inst("PanelMochila", 50, 35, L, 510),
       inst("TituloMochila", 66, 46, L, 550), inst("AyudaMochila", 250, 49, L, 550),
       inst("TextoInfoNombre", 66, 184, L, 550), inst("TextoInfoTipo", 300, 186, L, 550), inst("TextoInfoDesc", 66, 203, L, 550)]
def casilla(x, y, idx, grupo, z):
    g = [var("Indice", "number", idx), var("Grupo", "string", grupo)]
    return [inst("SlotUI", x, y, L, z, variables=g), inst("IconoItem", x + 17, y + 17, L, z + 10, variables=g),
            inst("CantidadItem", x + 18, y + 20, L, z + 20, variables=g + [var("SX", "number", x + 31)])]
for i in range(10): ins += casilla(70 + i * 34, 230, i, "Barra", 110)
for r in range(3):
    for c in range(10): ins += casilla(70 + c * 34, 65 + r * 36, r * 10 + c, "Mochila", 520)
mano = [var("Indice", "number", -1), var("Grupo", "string", "Mano")]
ins += [inst("IconoItem", 0, 0, L, 600, variables=mano), inst("CantidadItem", 0, 0, L, 610, variables=mano + [var("SX", "number", 0)])]
ext_layout = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
ext_layout["instances"] = ins

# ---------- eventos ----------
def visibilidad(abierta):
    on, off = (show, hide) if abierta else (hide, show)
    return [on("PanelMochila"), on("FondoOscuro"), on("TituloMochila"), on("AyudaMochila"),
            on("TextoInfoNombre"), on("TextoInfoTipo"), on("TextoInfoDesc"), off("BarraRapida"),
            opacity("EtiquetaItem", 0), opacity("TextoEtiqueta", 0)]
def visibilidad_casillas(abierta):
    return [EV([objv_s("SlotUI", "Grupo", q("Mochila"))], [show("SlotUI") if abierta else hide("SlotUI")]),
            EV([objv_s("SlotUI", "Grupo", q("Barra"))], [hide("SlotUI") if abierta else show("SlotUI")])]
def buscar(destino_cond, *extra):
    """Recorre las 30 casillas y guarda en Destino la primera que cumpla las condiciones."""
    return [EV([], [nv("k", "0")]),
            REPEAT(N, [], [], [EV([inv_("Destino", "-1"), *extra], [nv("Destino", "k")]), EV([], [nv("k", "1", "+")])])]
def devolver_mano():
    return [EV([isv("Mano.Id", '""', "!=")], [nv("Destino", "-1")], [
        *buscar(None, isv("Mochila[k].Id", '""')),
        EV([inv_("Destino", "0", ">=")], [sv("Mochila[Destino].Id", "Mano.Id"), nv("Mochila[Destino].Cantidad", "Mano.Cantidad"),
                                         sv("Mano.Id", '""'), nv("Mano.Cantidad", "0")])])]
def cmp(a, op, b): return C("BuiltinCommonInstructions::CompareNumbers", a, op, b)

E = [COM("INVENTARIO ESTILO STARDEW\n"
         "Mochila[0..29] guarda {Id, Cantidad}. Las casillas 0-9 son la barra rapida (teclas 1-0 o rueda del mouse).\n"
         "E o I abre la mochila. Items[Id] tiene el nombre, tipo, rareza, maximo por pila, precio y descripcion.\n"
         "Los objetos del suelo (grupo ItemsStardew) usan como Id el nombre de su animacion.")]

E.append(EV([C("SceneJustBegins", "")], [
    bv("InventarioAbierto", "False"), sv("GrupoVisible", q("Barra")), nv("RanuraAnterior", "-1"),
    A("ChangeLayerTimeScale", "", q(""), "1"), A("ResetTimer", "", q("MochilaLlena")), opacity("FondoOscuro", 150),
    *visibilidad(False)],
    visibilidad_casillas(False)))

E.append(COM("Recoger objetos del suelo: primero se junta con una pila igual, si no hay se usa la primera casilla vacia"))
E.append(EV([], [], [
    FOREACH("ItemsStardew", [C("CollisionNP", "Personaje_jugador", "ItemsStardew", "", "", ""), C("Layer", "ItemsStardew", q(""))],
            [sv("IdNuevo", "ItemsStardew.Animation::Name()"), nv("Destino", "-1")], [
        *buscar(None, isv("Mochila[k].Id", "IdNuevo"), cmp("Mochila[k].Cantidad + ItemsStardew.Cantidad", "<=", "Items[IdNuevo].Max")),
        *buscar(None, isv("Mochila[k].Id", '""')),
        EV([inv_("Destino", "0", ">=")], [
            sv("Mochila[Destino].Id", "IdNuevo"), nv("Mochila[Destino].Cantidad", "ItemsStardew.Cantidad", "+"),
            A("Create", "", "TextoFlotante", "Personaje_jugador.CenterX() - 24", "Personaje_jugador.Y() - 12 - SceneInstancesCount(TextoFlotante) * 11", q("")),
            txt("TextoFlotante", '"+" + ToString(ItemsStardew.Cantidad) + " " + Items[IdNuevo].Nombre'),
            A("SetZOrder", "TextoFlotante", "=", "100000"),
            tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 18", "easeOutQuad", 0.8),
            tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 1.1, "yes"),
            snd("Inventario/Recoger.wav", 55)], [
            COM("Los objetos puestos en el mapa (herramientas, semillas) no vuelven a aparecer"),
            EV([objv_s("ItemsStardew", "MiID", '""', "!="), objv_s("ItemsStardew", "MiID", q("0"), "!=")], [nv("Destruidos[ItemsStardew.MiID]", "-1")]),
            EV([], [A("Delete", "ItemsStardew", "")])]),
        EV([inv_("Destino", "-1"), C("CompareTimer", "", q("MochilaLlena"), ">", "2")], [
            A("ResetTimer", "", q("MochilaLlena")),
            A("Create", "", "TextoFlotante", "Personaje_jugador.CenterX() - 30", "Personaje_jugador.Y() - 12", q("")),
            txt("TextoFlotante", q("¡Mochila llena!")), A("SetZOrder", "TextoFlotante", "=", "100000"),
            tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 18", "easeOutQuad", 0.8),
            tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 1.1, "yes")]),
    ])], variables=[var("IdNuevo", "string", ""), var("Destino", "number", -1), var("k", "number", 0)]))

E.append(COM("Abrir y cerrar la mochila (E, I o Esc). Mientras esta abierta el mundo se pausa"))
E.append(EV([ibv("FabricarAbierto", "False")], [], [
    EV([key_released("e")], [bv("Alternar", "True")]),
    EV([key_released("i")], [bv("Alternar", "True")]),
    EV([key_released("Escape"), ibv("InventarioAbierto", "True")], [bv("Alternar", "True")]),
    EV([ibv("Alternar", "True"), ibv("InventarioAbierto", "True")], [
        bv("Alternar", "False"), bv("InventarioAbierto", "False"), sv("GrupoVisible", q("Barra")),
        A("ChangeLayerTimeScale", "", q(""), "1"), A("UnPauseTimer", "", q("PasoTiempo")),
        snd("Inventario/CerrarMochila.wav", 60), *visibilidad(False)], [*devolver_mano(), *visibilidad_casillas(False)]),
    EV([ibv("Alternar", "True"), ibv("InventarioAbierto", "False")], [
        bv("Alternar", "False"), bv("InventarioAbierto", "True"), sv("GrupoVisible", q("Mochila")),
        A("ChangeLayerTimeScale", "", q(""), "0"), A("PauseTimer", "", q("PasoTiempo")),
        snd("Inventario/AbrirMochila.wav", 60), *visibilidad(True)], visibilidad_casillas(True)),
], variables=[var("Alternar", "boolean", False), var("Destino", "number", -1), var("k", "number", 0)]))

E.append(COM("Barra rapida: teclas 1-9 y 0, rueda del mouse o clic en una casilla"))
E.append(EV([ibv("InventarioAbierto", "False")], [], [
    *[EV([key_released(f"Num{(i + 1) % 10}")], [nv("RanuraSeleccionada", str(i))]) for i in range(10)],
    EV([C("IsMouseWheelScrollingDown", "")], [nv("RanuraSeleccionada", "1", "+")], [
        EV([inv_("RanuraSeleccionada", "9", ">")], [nv("RanuraSeleccionada", "0")])]),
    EV([C("IsMouseWheelScrollingUp", "")], [nv("RanuraSeleccionada", "1", "-")], [
        EV([inv_("RanuraSeleccionada", "0", "<")], [nv("RanuraSeleccionada", "9")])]),
    EV([cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Barra")), released()], [nv("RanuraSeleccionada", "SlotUI.Indice")]),
]))

E.append(COM("Pilas vacias se limpian y se actualiza lo que el jugador tiene en la mano"))
E.append(EV([], [nv("k", "0")], [REPEAT(N, [], [], [
    EV([inv_("Mochila[k].Cantidad", "0", "<=")], [sv("Mochila[k].Id", '""'), nv("Mochila[k].Cantidad", "0")]),
    EV([], [nv("k", "1", "+")])])], variables=[var("k", "number", 0)]))
E.append(EV([], [sv("ItemEnMano", "Mochila[RanuraSeleccionada].Id")]))

E.append(COM("Nombre del objeto sobre la barra cuando cambias de casilla"))
E.append(EV([cmp("RanuraSeleccionada", "!=", "RanuraAnterior"), ibv("InventarioAbierto", "False")], [
    nv("RanuraAnterior", "RanuraSeleccionada"), snd("Inventario/Seleccion.wav", 30)], [
    EV([isv("ItemEnMano", '""', "!=")], [
        txt("TextoEtiqueta", "Items[ItemEnMano].Nombre"), A("SetCenterX", "TextoEtiqueta", "=", "240"),
        opacity("EtiquetaItem", 255), opacity("TextoEtiqueta", 255),
        tw_op("EtiquetaItem", "Ocultar", 0, "easeInQuart", 1.8), tw_op("TextoEtiqueta", "Ocultar", 0, "easeInQuart", 1.8)]),
    EV([isv("ItemEnMano", '""')], [opacity("EtiquetaItem", 0), opacity("TextoEtiqueta", 0)])]))

E.append(COM("Dibujar las casillas: iconos, cantidades y la casilla seleccionada"))
E.append(EV([], [anim("SlotUI", q("Normal"))], [
    EV([cursor("SlotUI"), C("Visible", "SlotUI")], [anim("SlotUI", q("Hover"))]),
    EV([objv_n("SlotUI", "Indice", "RanuraSeleccionada"), objv_s("SlotUI", "Grupo", q("Receta"), "!=")], [anim("SlotUI", q("Seleccionada"))])]))
E.append(FOREACH("IconoItem", [objv_s("IconoItem", "Grupo", "GrupoVisible"), objv_s("IconoItem", "Grupo", q("Receta"), "!=")], [], [
    EV([isv("Mochila[IconoItem.Indice].Id", '""', "!=")], [show("IconoItem"), anim("IconoItem", "Mochila[IconoItem.Indice].Id")]),
    EV([isv("Mochila[IconoItem.Indice].Id", '""')], [hide("IconoItem")])]))
E.append(EV([objv_s("IconoItem", "Grupo", "GrupoVisible", "!="), objv_s("IconoItem", "Grupo", q("Mano"), "!="),
             objv_s("IconoItem", "Grupo", q("Receta"), "!=")], [hide("IconoItem")]))
E.append(FOREACH("CantidadItem", [objv_s("CantidadItem", "Grupo", "GrupoVisible"), objv_s("CantidadItem", "Grupo", q("Receta"), "!=")], [], [
    EV([inv_("Mochila[CantidadItem.Indice].Cantidad", "1", ">")], [
        show("CantidadItem"), txt("CantidadItem", "ToString(Mochila[CantidadItem.Indice].Cantidad)"),
        A("SetX", "CantidadItem", "=", "CantidadItem.SX - CantidadItem.Width()")]),
    EV([inv_("Mochila[CantidadItem.Indice].Cantidad", "1", "<=")], [hide("CantidadItem")])]))
E.append(EV([objv_s("CantidadItem", "Grupo", "GrupoVisible", "!="), objv_s("CantidadItem", "Grupo", q("Mano"), "!="),
             objv_s("CantidadItem", "Grupo", q("Receta"), "!=")], [hide("CantidadItem")]))
E.append(COM("El objeto que llevas agarrado sigue al mouse"))
E.append(EV([objv_s("IconoItem", "Grupo", q("Mano"))], [hide("IconoItem")], [
    EV([ibv("InventarioAbierto", "True"), isv("Mano.Id", '""', "!=")], [
        show("IconoItem"), anim("IconoItem", "Mano.Id"),
        A("SetX", "IconoItem", "=", 'CursorX("Inventario") + 8'), A("SetY", "IconoItem", "=", 'CursorY("Inventario") + 8')])]))
E.append(EV([objv_s("CantidadItem", "Grupo", q("Mano"))], [hide("CantidadItem")], [
    EV([ibv("InventarioAbierto", "True"), inv_("Mano.Cantidad", "1", ">")], [
        show("CantidadItem"), txt("CantidadItem", "ToString(Mano.Cantidad)"),
        A("SetX", "CantidadItem", "=", 'CursorX("Inventario") + 22 - CantidadItem.Width()'),
        A("SetY", "CantidadItem", "=", 'CursorY("Inventario") + 12')])]))

E.append(COM("Mover objetos dentro de la mochila: tomar, soltar, juntar pilas iguales o cambiar de lugar"))
E.append(EV([ibv("InventarioAbierto", "True"), ibv("FabricarAbierto", "False"), cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Mochila")), released()], [
    nv("k", "SlotUI.Indice"), sv("Caso", '""'), snd("Inventario/Seleccion.wav", 45)], [
    EV([isv("Mano.Id", '""'), isv("Mochila[k].Id", '""', "!=")], [sv("Caso", q("Tomar"))]),
    EV([isv("Mano.Id", '""', "!="), isv("Mochila[k].Id", '""')], [sv("Caso", q("Dejar"))]),
    EV([isv("Mano.Id", '""', "!="), isv("Mochila[k].Id", "Mano.Id"), cmp("Mochila[k].Cantidad", "<", "Items[Mano.Id].Max")], [sv("Caso", q("Juntar"))]),
    EV([isv("Mano.Id", '""', "!="), isv("Mochila[k].Id", '""', "!="), isv("Caso", '""')], [sv("Caso", q("Cambiar"))]),
    EV([isv("Caso", q("Tomar"))], [sv("Mano.Id", "Mochila[k].Id"), nv("Mano.Cantidad", "Mochila[k].Cantidad"),
                                   sv("Mochila[k].Id", '""'), nv("Mochila[k].Cantidad", "0")]),
    EV([isv("Caso", q("Dejar"))], [sv("Mochila[k].Id", "Mano.Id"), nv("Mochila[k].Cantidad", "Mano.Cantidad"),
                                   sv("Mano.Id", '""'), nv("Mano.Cantidad", "0")]),
    EV([isv("Caso", q("Juntar"))], [nv("Pasar", "min(Mano.Cantidad, Items[Mano.Id].Max - Mochila[k].Cantidad)"),
                                    nv("Mochila[k].Cantidad", "Pasar", "+"), nv("Mano.Cantidad", "Pasar", "-")], [
        EV([inv_("Mano.Cantidad", "0", "<=")], [sv("Mano.Id", '""'), nv("Mano.Cantidad", "0")])]),
    EV([isv("Caso", q("Cambiar"))], [sv("TmpId", "Mochila[k].Id"), nv("TmpCant", "Mochila[k].Cantidad"),
                                     sv("Mochila[k].Id", "Mano.Id"), nv("Mochila[k].Cantidad", "Mano.Cantidad"),
                                     sv("Mano.Id", "TmpId"), nv("Mano.Cantidad", "TmpCant")]),
], variables=[var("k", "number", 0), var("Caso", "string", ""), var("Pasar", "number", 0),
              var("TmpId", "string", ""), var("TmpCant", "number", 0)]))

E.append(COM("Informacion del objeto bajo el mouse (nombre, tipo, rareza y descripcion)"))
E.append(EV([ibv("InventarioAbierto", "True"), ibv("FabricarAbierto", "False")], [
    txt("TextoInfoNombre", '""'), txt("TextoInfoTipo", '""'),
    txt("TextoInfoDesc", q("Pasa el mouse sobre un objeto para ver qué es.")),
    A("SetX", "AyudaMochila", "=", "414 - AyudaMochila.Width()")], [
    EV([cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Mochila"))], [sv("InfoId", "Mochila[SlotUI.Indice].Id")], [
        EV([isv("InfoId", '""', "!=")], [
            txt("TextoInfoNombre", "Items[InfoId].Nombre"),
            txt("TextoInfoTipo", 'Items[InfoId].Tipo + "  -  " + Items[InfoId].Rareza'),
            A("SetX", "TextoInfoTipo", "=", "414 - TextoInfoTipo.Width()"),
            txt("TextoInfoDesc", "Items[InfoId].Descripcion")], [
            EV([isv("Items[InfoId].Rareza", q(r))], [color("TextoInfoTipo", c)]) for r, c in RAREZA_COLOR.items()])])],
    variables=[var("InfoId", "string", "")]))

E.append(COM("Evita usar herramientas cuando el mouse esta sobre la barra"))
E.append(EV([], [bv("MouseSobreUI", "False")], [
    EV([cursor("BarraRapida"), ibv("InventarioAbierto", "False")], [bv("MouseSobreUI", "True")])]))

external_events(d, "Inventario", E)

# variables de escena que usa el inventario, en cada nivel
for lay in d["layouts"]:
    if lay["name"] in ("Nivel 01", "Nivel 02", "Pueblo"):
        names = {v["name"] for v in lay["variables"]}
        for v in [var("GrupoVisible", "string", "Barra"), var("RanuraAnterior", "number", -1)]:
            if v["name"] not in names: lay["variables"].append(v)
    if lay["name"] == "Nivel 02":  # Personaje ya incluye Inventario: el link directo lo ejecutaba dos veces
        lay["events"] = [e for e in lay["events"] if not (e.get("type") == "BuiltinCommonInstructions::Link" and e.get("target") == "Inventario")]

# ---------- Personaje: quitar la carga del inventario viejo y bloquear movimiento/ataque con la mochila abierta ----------
pers = next(e for e in d["externalEvents"] if e["name"] == "Personaje")
inicio = next(e for e in pers["events"] if any(c["type"]["value"] == "SceneJustBegins" for c in e.get("conditions", [])))
subs = inicio.get("events", [])
cut = next(i for i, e in enumerate(subs) if e.get("type", "").endswith("Comment") and "Cargar inventario visual" in e.get("comment", ""))
inicio["events"] = subs[:cut]
def add_cond(evs, pred, cond):
    for e in evs:
        if pred(e) and cond not in e["conditions"]:
            e["conditions"].insert(0, cond)
        add_cond(e.get("events") or [], pred, cond)
cerrada = ibv("InventarioAbierto", "False")
add_cond(pers["events"], lambda e: any(c["type"]["value"] == "BooleanObjectVariable" and c["parameters"][1] == "Labrando"
                                       for c in e.get("conditions") or []) and len(e.get("conditions") or []) == 4, cerrada)
add_cond(pers["events"], lambda e: any(c["type"]["value"] == "KeyFromTextPressed" and c["parameters"][1] == '"Space"'
                                       for c in e.get("conditions") or []), cerrada)

# ---------- Herramientas: usar lo que hay en la mano ----------
herr = next(e for e in d["externalEvents"] if e["name"] == "Herramientas")
def convertir(evs):
    out = []
    for e in evs:
        if e.get("type", "").endswith("Comment") and any(k in e.get("comment", "") for k in ("Actualiza contador", "Limpia casilla")):
            continue
        conds = []
        for c in e.get("conditions") or []:
            t, p = c["type"]["value"], c["parameters"]
            if t == "BooleanObjectVariable" and p[0] == "CasillaInventario" and p[1] == "Seleccionado":
                conds += [ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False")]
            elif t == "StringObjectVariable" and p[0] == "CasillaInventario" and p[1] == "ItemAlmacenado":
                conds.append(isv("ItemEnMano", p[3]))
            elif t == "NumberVariable" and p[0].startswith("Inventario["):
                conds.append(inv_("Mochila[RanuraSeleccionada].Cantidad", p[2], p[1]))
            else:
                conds.append(c)
        if "conditions" in e: e["conditions"] = conds
        acts = []
        for a in e.get("actions") or []:
            t, p = a["type"]["value"], a["parameters"]
            if t == "SetNumberVariable" and p[0].startswith("Inventario["):
                acts.append(nv("Mochila[RanuraSeleccionada].Cantidad", p[2], p[1]))
            else:
                acts.append(a)
        if "actions" in e: e["actions"] = acts
        if e.get("events"):
            # los sub-eventos "Actualiza contador" y "Limpia casilla" usaban las casillas viejas
            kept, skip = [], False
            for s in e["events"]:
                if s.get("type", "").endswith("Comment"):
                    skip = any(k in s.get("comment", "") for k in ("Actualiza contador", "Limpia casilla"))
                    if skip: continue
                elif skip:
                    skip = False
                    continue
                kept.append(s)
            e["events"] = convertir(kept)
        out.append(e)
    return out
herr["events"] = convertir(herr["events"])
cosecha = next(e for e in herr["events"] if any(c["type"]["value"] == "IsCursorOnObject" and c["parameters"][0] == "Planta_Zanahoria"
                                                for c in e.get("conditions") or []))
cosecha["conditions"] = [ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False")] + cosecha["conditions"]

# ---------- limpiar lo que ya no se usa ----------
texto = json.dumps([d["layouts"], d["externalEvents"], d["externalLayouts"]], ensure_ascii=False)
for viejo in ["CasillaInventario", "ContadorItem", "CursorInventario"]:
    assert viejo not in texto, viejo + " todavia se usa"
    d["objects"] = [o for o in d["objects"] if o["name"] != viejo]
    d["objectsFolderStructure"]["children"] = [c for c in d["objectsFolderStructure"]["children"] if c.get("objectName") != viejo]
assert 'Inventario[' not in texto, "quedan referencias a la variable Inventario vieja"
d["variables"] = [v for v in d["variables"] if v["name"] != "Inventario"]

json.dump(d, open(PROJ, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: inventario con", len(E), "eventos,", len(ins), "instancias en InventarioStardew")
