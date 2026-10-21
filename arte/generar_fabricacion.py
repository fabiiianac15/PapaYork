"""Mesa de trabajo, recetas y construcciones que se colocan en el mundo.

Se aplica despues de generar_mundo.py y antes de generar_cultivos.py y generar_menu.py.

- Mesa de trabajo junto a la casa (Nivel 01). Clic estando cerca -> panel con las recetas (pausa el mundo).
- Recetas: Cerca, Antorcha, Abono, Espantapapas, Horno, Lingote de cobre y Lingote de hierro (estos dos piden un horno).
  Las recetas que no te alcanzan se ven apagadas; al pasar el mouse se ve que falta.
- Construcciones (Cerca, Antorcha, Espantapapas, Horno): se colocan con clic en una casilla al lado de Pedro y
  se recogen golpeandolas con el pico o el hacha. Se guardan en la variable global Construcciones.
- La antorcha alumbra de noche (sprite en la capa de iluminacion "Luz Exterior").

Uso: python3 arte/generar_fabricacion.py "Legado Radioactivo-Papayork.json"
"""
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from gdutil import *

PROJ = sys.argv[1]
d = json.load(open(PROJ, encoding="utf8"))
O = {o["name"]: o for o in d["objects"]}
def cmp(a, op, b): return C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def ext(nombre): return next(e for e in d["externalEvents"] if e["name"] == nombre)
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
def tiene(e, tipo, *params):
    return any(c["type"]["value"] == tipo and c["parameters"][:len(params)] == list(params) for c in e.get("conditions") or [])
def accion(e, tipo, *params):
    return any(a["type"]["value"] == tipo and a["parameters"][:len(params)] == list(params) for a in e.get("actions") or [])
herr = ext("Herramientas")
VICELDA = next(c for e in recorrer(herr["events"]) for c in e.get("conditions") or [] if c["type"]["value"] == "Rejilla::Rejilla::Vicelda")

# ---------- catalogo ----------
NUEVOS = [
    ("Cerca", "Cerca", "Construcción", "Común", 99, 2, "Colócala junto a Pedro. Las papas no pueden cruzarla."),
    ("Antorcha", "Antorcha", "Construcción", "Común", 99, 5, "Colócala en el suelo: ilumina la granja de noche."),
    ("Abono", "Abono", "Fertilizante", "Común", 99, 8, "Échalo sobre tierra arada: el cultivo crece el doble de rápido."),
    ("Espantapapas", "Espantapapas", "Construcción", "Poco común", 10, 50, "Las papas radiactivas no salen de la tierra cerca de él."),
    ("Horno", "Horno", "Construcción", "Poco común", 10, 60, "Colócalo en la granja para poder fundir lingotes."),
    ("LingoteCobre", "Lingote de cobre", "Material", "Poco común", 99, 30, "Cobre fundido. Sirve para mejorar herramientas en el pueblo."),
    ("LingoteHierro", "Lingote de hierro", "Material", "Raro", 99, 60, "Hierro fundido. Para las mejoras más fuertes del pueblo."),
]
RECETAS = [  # (resultado, cantidad, necesita horno, ingredientes)
    ("Cerca", 1, False, [("Madera", 2)]),
    ("Antorcha", 1, False, [("Madera", 1), ("Resina", 1)]),
    ("Abono", 2, False, [("TierraFertil", 1), ("Fibra", 2)]),
    ("Espantapapas", 1, False, [("Madera", 10), ("Fibra", 10), ("Cristal", 1)]),
    ("Horno", 1, False, [("Piedra", 20), ("Cobre", 5)]),
    ("LingoteCobre", 1, True, [("Cobre", 3), ("Carbon", 1)]),
    ("LingoteHierro", 1, True, [("Hierro", 3), ("Carbon", 1)]),
]
ICONO = {"Cerca": ("Decoracion/Vaya1.png", 32, 32), "Antorcha": ("Fabricacion/Antorcha1.png", 18, 34),
         "Abono": ("Fabricacion/Abono.png", 32, 32), "Espantapapas": ("Fabricacion/Espantapapas.png", 34, 42),
         "Horno": ("Fabricacion/Horno1.png", 34, 38), "LingoteCobre": ("Fabricacion/LingoteCobre.png", 32, 32),
         "LingoteHierro": ("Fabricacion/LingoteHierro.png", 32, 32)}

items = next(v for v in d["variables"] if v["name"] == "Items")
items["children"] = [c for c in items["children"] if c["name"] not in {n[0] for n in NUEVOS}]
for i, n, t, r, m, p, ds in NUEVOS:
    items["children"].append(struct(i, [var("Nombre", "string", n), var("Tipo", "string", t), var("Rareza", "string", r),
                                        var("Max", "number", m), var("Precio", "number", p), var("Descripcion", "string", ds)]))
set_global_var(d, {"name": "Recetas", "type": "array", "children": [
    {"type": "structure", "children": [var("Id", "string", res), var("Cantidad", "number", n), var("NecesitaHorno", "boolean", horno),
                                       {"name": "Ingredientes", "type": "array", "children": [
                                           {"type": "structure", "children": [var("Id", "string", i), var("Cantidad", "number", c)]}
                                           for i, c in ing]}]}
    for res, n, horno, ing in RECETAS]})
set_global_var(d, struct("Construcciones", []))
set_global_var(d, var("HornoConstruido", "boolean", False))

# ---------- recursos ----------
for f in ["MesaTrabajo", "Antorcha1", "Antorcha2", "Antorcha3", "Espantapapas", "Horno1", "Horno2", "Abono",
          "LingoteCobre", "LingoteHierro", "LuzAntorcha"]:
    add_resource(d, "image", "Fabricacion/" + f + ".png", "Fabricacion/" + f + ".png")
for f in ["Fabricar", "Colocar"]:
    add_resource(d, "audio", "Fabricacion/" + f + ".wav", "Fabricacion/" + f + ".wav")

# iconos en la mochila y objetos que caen al suelo para cada cosa fabricable
for nombre in ("IconoItem", "Recursos"):
    o = O[nombre]
    o["animations"] = [a for a in o["animations"] if a["name"] not in ICONO]
    for i, (img, w, h) in ICONO.items():
        origen = (w // 2, h // 2) if nombre == "IconoItem" else (0, 0)
        o["animations"].append(anim_def(i, [frame(img, origen, None if nombre == "IconoItem" else rect(4, 4, 28, 28))]))

# ---------- objetos ----------
YSORT = {"name": "YSort", "type": "YSort::YSort"}
mesa = sprite_obj("MesaTrabajo", [anim_def("", [frame("Fabricacion/MesaTrabajo.png", (0, 0), rect(2, 22, 40, 34))])], tween=False)
mesa["behaviors"] = [YSORT]
def base(img, w, h): return frame(img, (0, 0), rect(3, h - 12, w - 3, h - 1))   # solo la base choca: se puede pasar por detras
constr = sprite_obj("Construccion", [
    anim_def("Cerca", [base("Decoracion/Vaya1.png", 32, 32)]),
    anim_def("Antorcha", [base("Fabricacion/Antorcha%d.png" % i, 18, 34) for i in (1, 2, 3)], loop=True, dt=0.12),
    anim_def("Espantapapas", [base("Fabricacion/Espantapapas.png", 34, 42)]),
    anim_def("Horno", [base("Fabricacion/Horno%d.png" % i, 34, 38) for i in (1, 2)], loop=True, dt=0.16),
], [var("MiClave", "string", ""), var("CeldaX", "number", 0), var("CeldaY", "number", 0)], tween=False)
constr["behaviors"] = [YSORT]
luz = sprite_obj("LuzAntorcha", [anim_def("", [frame("Fabricacion/LuzAntorcha.png", (64, 64))])], [var("MiClave", "string", "")], tween=False)
for o in [mesa, constr, luz,
          sprite_obj("PanelFabricar", [anim_def("", [frame("Inventario/PanelMochila.png")])], tween=False),
          text_obj("TituloFabricar", "Mesa de trabajo", 14, (255, 236, 170), (60, 30, 12)),
          text_obj("AyudaFabricar", "Clic: fabricar     E: cerrar", 10, (90, 55, 28), None),
          text_obj("TextoIngredientes", "", 10, (90, 55, 28), None),
          text_obj("AvisoMesa", "Clic: mesa de trabajo", 9, (255, 246, 210), (36, 21, 13))]:
    set_global_object(d, o)

# instancias: mesa y su aviso en la granja; panel y casillas de recetas en el diseño externo del inventario
for lay in d["layouts"]:
    if lay["name"] == "Nivel 01":
        lay["instances"] = [i for i in lay["instances"] if i["name"] not in ("MesaTrabajo", "AvisoMesa")]
        lay["instances"] += [inst("MesaTrabajo", 272, 140, "", 140), inst("AvisoMesa", 258, 126, "", 100000)]
    if lay["name"] in ("Nivel 01", "Nivel 02", "Pueblo"):
        lay["variables"] = [v for v in lay["variables"] if v["name"] not in ("CeldaConstr", "ClaveConstr")]
        lay["variables"] += [struct("CeldaConstr", [var("Id", "string", ""), var("X", "number", 0), var("Y", "number", 0),
                                                    var("Escena", "string", "")]), var("ClaveConstr", "string", "")]
L = "Inventario"
lay_inv = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
lay_inv["instances"] = [i for i in lay_inv["instances"]
                        if i["name"] not in ("PanelFabricar", "TituloFabricar", "AyudaFabricar", "TextoIngredientes")
                        and not any(v["name"] == "Grupo" and v["value"] == "Receta" for v in i.get("initialVariables", []))]
lay_inv["instances"] += [inst("PanelFabricar", 50, 35, L, 510), inst("TituloFabricar", 66, 46, L, 550),
                         inst("AyudaFabricar", 250, 49, L, 550), inst("TextoIngredientes", 74, 116, L, 550)]
for k in range(len(RECETAS)):
    x, y = 74 + k * 48, 74
    g = [var("Indice", "number", k), var("Grupo", "string", "Receta")]
    lay_inv["instances"] += [inst("SlotUI", x, y, L, 520, variables=g + [var("Puede", "boolean", False)]),
                             inst("IconoItem", x + 17, y + 17, L, 530, variables=g),
                             inst("CantidadItem", x + 18, y + 20, L, 540, variables=g + [var("SX", "number", x + 31)])]
for nombre in ("SlotUI",):
    o = O[nombre]
    if not any(v["name"] == "Puede" for v in o["variables"]): o["variables"].append(var("Puede", "boolean", False))

# ---------- eventos ----------
UI = ["PanelFabricar", "TituloFabricar", "AyudaFabricar", "TextoIngredientes", "FondoOscuro",
      "TextoInfoNombre", "TextoInfoTipo", "TextoInfoDesc"]
def receta_grupo(accion):
    return [EV([objv_s(o, "Grupo", q("Receta"))], [accion(o)]) for o in ("SlotUI", "IconoItem", "CantidadItem")]
def ajustar_posicion():   # centrar en la casilla y apoyar la base en el suelo
    return [A("SetX", "Construccion", "=", "Construccion.CeldaX + (32 - Construccion.Width()) / 2"),
            A("SetY", "Construccion", "=", "Construccion.CeldaY + 32 - Construccion.Height()")]
def crear_luz(clave):
    return EV([C("AnimatableCapability::AnimatableBehavior::Name", "Construccion", "Animation", "=", q("Antorcha"))], [
        A("Create", "", "LuzAntorcha", "Construccion.CeldaX + 16", "Construccion.CeldaY + 6", q("Luz Exterior")),
        set_objv_s("LuzAntorcha", "MiClave", clave)])
def contar_ingrediente(receta, j):
    """Suma en Tienes cuantas unidades del ingrediente j de la receta hay en la mochila."""
    return [EV([], [nv("Tienes", "0"), nv("k", "0")]),
            REPEAT(30, [], [], [EV([isv("Mochila[k].Id", receta + ".Ingredientes[" + j + "].Id")], [nv("Tienes", "Mochila[k].Cantidad", "+")]),
                                EV([], [nv("k", "1", "+")])])]

E = [COM("MESA DE TRABAJO Y CONSTRUCCIONES\n"
         "Recetas[i] = {Id, Cantidad, NecesitaHorno, Ingredientes[{Id, Cantidad}]}. Lo fabricado cae a los pies de Pedro\n"
         "y lo recoge el evento Inventario. Construcciones guarda lo colocado: clave escena_x_y -> {Id, X, Y, Escena}.")]
E.append(EV([C("SceneJustBegins", "")], [bv("FabricarAbierto", "False"), hide("AvisoMesa")] + [hide(o) for o in UI[:4]],
            receta_grupo(hide)))

E.append(COM("Aviso cuando Pedro esta cerca de la mesa"))
DIST_MESA = "DistanceBetweenPositions(Personaje_jugador.X(), Personaje_jugador.Y(), MesaTrabajo.X() + 20, MesaTrabajo.Y() + 26)"
E.append(EV([cmp(DIST_MESA, "<", "56"), ibv("InventarioAbierto", "False")], [show("AvisoMesa")]))
E.append(EV([cmp(DIST_MESA, ">=", "56")], [hide("AvisoMesa")]))
E.append(EV([ibv("InventarioAbierto", "True")], [hide("AvisoMesa")]))

E.append(COM("Abrir la mesa (clic estando cerca)"))
E.append(EV([ibv("InventarioAbierto", "False"), cursor("MesaTrabajo"), released(), cmp(DIST_MESA, "<", "56")], [
    bv("FabricarAbierto", "True"), bv("InventarioAbierto", "True"), sv("GrupoVisible", q("Ninguno")),
    A("ChangeLayerTimeScale", "", q(""), "0"), A("PauseTimer", "", q("PasoTiempo")),
    hide("BarraRapida"), opacity("EtiquetaItem", 0), opacity("TextoEtiqueta", 0),
    *[show(o) for o in UI], snd("Inventario/AbrirMochila.wav", 60), bv("HornoConstruido", "False")], [
    *receta_grupo(show),
    {"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Construcciones",
     "valueIteratorVariableName": "CeldaConstr", "keyIteratorVariableName": "ClaveConstr",
     "conditions": [isv("CeldaConstr.Id", q("Horno"))], "actions": [bv("HornoConstruido", "True")], "events": []}]))

E.append(COM("Cerrar la mesa (E, I o Esc)"))
E.append(EV([ibv("FabricarAbierto", "True")], [], [
    EV([key_released("e")], [bv("Cerrar", "True")]), EV([key_released("i")], [bv("Cerrar", "True")]),
    EV([key_released("Escape")], [bv("Cerrar", "True")]),
    EV([ibv("Cerrar", "True")], [
        bv("FabricarAbierto", "False"), bv("InventarioAbierto", "False"), sv("GrupoVisible", q("Barra")),
        A("ChangeLayerTimeScale", "", q(""), "1"), A("UnPauseTimer", "", q("PasoTiempo")),
        show("BarraRapida"), *[hide(o) for o in UI], snd("Inventario/CerrarMochila.wav", 60)], receta_grupo(hide))],
    variables=[var("Cerrar", "boolean", False)]))

E.append(COM("Con la mesa abierta: iconos de las recetas, cuales alcanzan y la informacion de la receta bajo el mouse"))
E.append(EV([ibv("FabricarAbierto", "True")], [], [
    FOREACH("IconoItem", [objv_s("IconoItem", "Grupo", q("Receta"))], [show("IconoItem"), anim("IconoItem", "Recetas[IconoItem.Indice].Id")]),
    FOREACH("CantidadItem", [objv_s("CantidadItem", "Grupo", q("Receta"))], [hide("CantidadItem")], [
        EV([inv_("Recetas[CantidadItem.Indice].Cantidad", "1", ">")], [
            show("CantidadItem"), txt("CantidadItem", '"x" + ToString(Recetas[CantidadItem.Indice].Cantidad)'),
            A("SetX", "CantidadItem", "=", "CantidadItem.SX - CantidadItem.Width()")])]),
    FOREACH("SlotUI", [objv_s("SlotUI", "Grupo", q("Receta"))], [set_objv_b("SlotUI", "Puede", "True"), nv("j", "0")], [
        REPEAT("VariableChildCount(Recetas[SlotUI.Indice].Ingredientes)", [], [], [
            *contar_ingrediente("Recetas[SlotUI.Indice]", "j"),
            EV([cmp("Tienes", "<", "Recetas[SlotUI.Indice].Ingredientes[j].Cantidad")], [set_objv_b("SlotUI", "Puede", "False")]),
            EV([], [nv("j", "1", "+")])]),
        EV([ibv("Recetas[SlotUI.Indice].NecesitaHorno", "True"), ibv("HornoConstruido", "False")], [set_objv_b("SlotUI", "Puede", "False")]),
        EV([objv_s("IconoItem", "Grupo", q("Receta")), objv_n("IconoItem", "Indice", "SlotUI.Indice")], [opacity("IconoItem", 255)], [
            EV([objv_b("SlotUI", "Puede", "False")], [opacity("IconoItem", 80)])]),
    ]),
    EV([], [txt("TextoInfoNombre", '""'), txt("TextoInfoTipo", '""'), txt("TextoIngredientes", '""'),
            txt("TextoInfoDesc", q("Pasa el mouse por una receta para ver qué necesitas.")),
            A("SetX", "AyudaFabricar", "=", "414 - AyudaFabricar.Width()")]),
    EV([cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Receta"))], [
        nv("R", "SlotUI.Indice"), sv("RId", "Recetas[R].Id"),
        txt("TextoInfoNombre", "Items[RId].Nombre"),
        txt("TextoInfoTipo", 'Items[RId].Tipo + "  -  " + Items[RId].Rareza'), A("SetX", "TextoInfoTipo", "=", "414 - TextoInfoTipo.Width()"),
        txt("TextoInfoDesc", "Items[RId].Descripcion"), sv("Lista", q("Necesitas:")), nv("j", "0")], [
        EV([inv_("Recetas[R].Cantidad", "1", ">")], [txt("TextoInfoNombre", 'Items[RId].Nombre + "  x" + ToString(Recetas[R].Cantidad)')]),
        REPEAT("VariableChildCount(Recetas[R].Ingredientes)", [], [], [
            *contar_ingrediente("Recetas[R]", "j"),
            EV([], [sv("Lista", 'Lista + NewLine() + "   " + ToString(Recetas[R].Ingredientes[j].Cantidad) + " " + '
                               'Items[Recetas[R].Ingredientes[j].Id].Nombre + "   (tienes " + ToString(Tienes) + ")"'), nv("j", "1", "+")])]),
        EV([ibv("Recetas[R].NecesitaHorno", "True"), ibv("HornoConstruido", "False")], [
            sv("Lista", 'Lista + NewLine() + "Primero construye y coloca un horno."')]),
        EV([], [txt("TextoIngredientes", "Lista")]),
        EV([objv_b("SlotUI", "Puede", "True")], [color("TextoIngredientes", "48;108;6")]),
        EV([objv_b("SlotUI", "Puede", "False")], [color("TextoIngredientes", "172;50;50")]),
        *[EV([isv("Items[RId].Rareza", q(r))], [color("TextoInfoTipo", c)]) for r, c in
          {"Común": "235;220;190", "Poco común": "143;220;46", "Raro": "110;180;255", "Épico": "214;120;255"}.items()]]),
], variables=[var("j", "number", 0), var("k", "number", 0), var("Tienes", "number", 0), var("R", "number", 0),
              var("RId", "string", ""), var("Lista", "string", "")]))

E.append(COM("Fabricar: se gastan los ingredientes y el resultado cae a los pies de Pedro"))
E.append(EV([ibv("FabricarAbierto", "True"), cursor("SlotUI"), objv_s("SlotUI", "Grupo", q("Receta")), released()], [
    nv("R", "SlotUI.Indice")], [
    EV([objv_b("SlotUI", "Puede", "False")], [snd("Inventario/Seleccion.wav", 40)]),
    EV([objv_b("SlotUI", "Puede", "True")], [nv("j", "0"), snd("Fabricacion/Fabricar.wav", 70), nv("Exp", "1", "+")], [
        REPEAT("VariableChildCount(Recetas[R].Ingredientes)", [], [nv("Falta", "Recetas[R].Ingredientes[j].Cantidad"), nv("k", "0")], [
            REPEAT(30, [], [], [
                EV([isv("Mochila[k].Id", "Recetas[R].Ingredientes[j].Id"), inv_("Falta", "0", ">")], [
                    nv("Quitar", "min(Falta, Mochila[k].Cantidad)"), nv("Mochila[k].Cantidad", "Quitar", "-"), nv("Falta", "Quitar", "-")]),
                EV([], [nv("k", "1", "+")])]),
            EV([], [nv("j", "1", "+")])]),
        REPEAT("Recetas[R].Cantidad", [], [
            A("Create", "", "Recursos", "Personaje_jugador.X() - 16", "Personaje_jugador.Y() - 22", q("")),
            anim("Recursos", "Recetas[R].Id"), set_objv_b("Recursos", "Nuevo", "False"),
            A("ResetObjectTimer", "Recursos", q("Soltado"))])]),
], variables=[var("R", "number", 0), var("j", "number", 0), var("k", "number", 0), var("Falta", "number", 0), var("Quitar", "number", 0)]))

E.append(COM("Colocar una construccion en la casilla senalada (al lado de Pedro)"))
BLOQUEAN = ["Objetos_Fisicos", "Rocas", "Colision", "Casa1", "MesaTrabajo", "Personaje_jugador", "Teletransportador", "Hierba", "SueloPreparado"]
E.append(EV([ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False"), isv("Items[ItemEnMano].Tipo", q("Construcción")), VICELDA,
             C("MouseButtonFromTextPressed", "", q("Left")), ONCE()], [
    nv("CX", "Rejilla.X() + Rejilla.Xcelda()"), nv("CY", "Rejilla.Y() + Rejilla.Ycelda()"),
    sv("Clave", 'CurrentSceneName() + "_" + ToString(CX) + "_" + ToString(CY)'), bv("Bloqueado", "False")], [
    EV([C("VariableChildExists2", "Construcciones", "Clave", inv=True)], [
        A("Create", "", "Construccion", "CX", "CY", q("")), anim("Construccion", "ItemEnMano"),
        set_objv_n("Construccion", "CeldaX", "CX"), set_objv_n("Construccion", "CeldaY", "CY"),
        set_objv_s("Construccion", "MiClave", "Clave"), *ajustar_posicion()], [
        *[EV([C("CollisionNP", "Construccion", o, "", "", "")], [bv("Bloqueado", "True")]) for o in BLOQUEAN],
        EV([ibv("Bloqueado", "True")], [A("Delete", "Construccion", ""), snd("Inventario/Seleccion.wav", 40)]),
        EV([ibv("Bloqueado", "False")], [
            sv("Construcciones[Clave].Id", "ItemEnMano"), nv("Construcciones[Clave].X", "CX"), nv("Construcciones[Clave].Y", "CY"),
            sv("Construcciones[Clave].Escena", "CurrentSceneName()"),
            nv("Mochila[RanuraSeleccionada].Cantidad", "1", "-"), snd("Fabricacion/Colocar.wav", 70)], [crear_luz("Clave")])])
], variables=[var("CX", "number", 0), var("CY", "number", 0), var("Clave", "string", ""), var("Bloqueado", "boolean", False)]))

E.append(COM("Recoger una construccion: golpearla con el pico o el hacha"))
for herramienta in ("Pico", "Hacha"):
    E.append(EV([ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False"), isv("ItemEnMano", q(herramienta)), VICELDA,
                 cursor("Construccion"), C("MouseButtonFromTextPressed", "", q("Left")), ONCE()], [
        A("Create", "", "Recursos", "Construccion.CeldaX", "Construccion.CeldaY", q("")),
        anim("Recursos", "Construccion.Animation::Name()"),
        A("VariableRemoveChild", "Construcciones", "Construccion.MiClave"), snd("Fabricacion/Colocar.wav", 60)], [
        EV([objv_s("LuzAntorcha", "MiClave", "Construccion.MiClave")], [A("Delete", "LuzAntorcha", "")]),
        EV([], [A("Delete", "Construccion", "")])]))

E.append(COM("Nadie atraviesa las construcciones ni la mesa (las cercas protegen los cultivos de las papas)"))
for o in ("Construccion", "MesaTrabajo"):
    E.append(EV([C("CollisionNP", "Personaje_jugador", o, "", "", "")], [A("SeparateFromObjects", "Personaje_jugador", o, "")]))
    E.append(EV([C("CollisionNP", "Mov4Dir", o, "", "", "")], [A("SeparateFromObjects", "Mov4Dir", o, "")]))
E.append(COM("La luz de las antorchas titila"))
E.append(EV([], [A("ScalableCapability::ScalableBehavior::SetValue", "LuzAntorcha", "Scale", "=",
                   "1 + sin(TimeFromStart() * 7 + LuzAntorcha.X()) * 0.05")]))
external_events(d, "Fabricacion", E)

pers = ext("Personaje")
if not any(e.get("target") == "Fabricacion" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("Fabricacion"))

# reconstruir las construcciones de la zona al entrar (antes de decidir que vuelve a crecer)
inicio = next(e for e in pers["events"] if tiene(e, "SceneJustBegins"))
inicio["events"] = [s for s in inicio["events"] if s.get("iterableVariableName") != "Construcciones"]
restaurar = {"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Construcciones",
             "valueIteratorVariableName": "CeldaConstr", "keyIteratorVariableName": "ClaveConstr",
             "conditions": [isv("CeldaConstr.Escena", "CurrentSceneName()")],
             "actions": [A("Create", "", "Construccion", "CeldaConstr.X", "CeldaConstr.Y", q("")),
                         anim("Construccion", "CeldaConstr.Id"),
                         set_objv_n("Construccion", "CeldaX", "CeldaConstr.X"), set_objv_n("Construccion", "CeldaY", "CeldaConstr.Y"),
                         set_objv_s("Construccion", "MiClave", "ClaveConstr"), *ajustar_posicion()],
             "events": [crear_luz("ClaveConstr")]}
i = next(k for k, s in enumerate(inicio["events"]) if s.get("iterableVariableName") == "Granja") + 1
inicio["events"].insert(i, restaurar)

# el azadon no ara donde hay una construccion ni al hacer clic en la mesa
for e in recorrer(herr["events"]):
    if accion(e, "Create", "", "SueloPreparado") and not tiene(e, "VariableChildExists2", "Construcciones"):
        clave = next(c["parameters"][1] for c in e["conditions"] if c["type"]["value"] == "VariableChildExists2")
        e["conditions"] += [C("VariableChildExists2", "Construcciones", clave, inv=True), cursor("MesaTrabajo", inv=True)]

json.dump(d, open(PROJ, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: mesa de trabajo con", len(RECETAS), "recetas")
