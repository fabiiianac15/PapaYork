"""Musica continua entre escenas, pestanas de pausa en la mochila (Opciones / Salir) y nueva pantalla de "te desmayaste".

- Toda la musica suena en el canal 0 y ninguna escena corta el sonido al empezar. Cada escena solo cambia la cancion
  si MusicaActual es distinta, asi que al pasar de la granja al bosque la musica sigue donde iba.
- Volumen de la musica aparte (global VolumenMusica, guardado en PapayorkAjustes/Musica).
- Al abrir la mochila (E o I) aparecen tres pestanas arriba del panel: Mochila, Opciones y Salir.
- GameOver se rehace: la granja de noche con papas mutantes mirando, Pedro desmayado con estrellitas,
  pierdes el 10% de las monedas (maximo 100) y despiertas en casa, o vuelves al menu.
Se puede volver a ejecutar: reemplaza lo que creo la vez anterior.
"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
def ext(n): return next(e for e in d["externalEvents"] if e["name"] == n)
def layout(n): return next(l for l in d["layouts"] if l["name"] == n)
def timer(name, op, val): return C("CompareTimer", "", q(name), op, str(val))
def visible(o): return C("Visible", o)
def ancho(o, v): return A("ResizableCapability::ResizableBehavior::SetWidth", o, "Resizable", "=", v)

OVERTURE = "Stardew Valley OST - Stardew Valley Overture.mp3"
VERANO = "Sonido/Stardew Valley OST - Summer (Nature's Crescendo).mp3"
AJUSTES = q("PapayorkAjustes")
set_global_var(d, var("VolumenMusica", "number", 100))
set_global_var(d, var("PestanaActual", "string", "Mochila"))
set_global_var(d, var("SalidaPendiente", "string", ""))
set_global_var(d, var("VerPausa", "boolean", False))

def musica(clave, archivo, pitch="1", vol="VolumenMusica"):
    """Cambia la cancion del canal 0 solo si no es la que ya esta sonando."""
    return EV([isv("MusicaActual", q(clave), "!=")], [A("PlayMusicOnChannel", "", archivo, "0", "yes", vol, pitch), sv("MusicaActual", q(clave))])

# =====================================================================================
# 1. Musica continua
# =====================================================================================
for lay in d["layouts"]:
    lay["stopSoundsOnStartup"] = False
for nombre in ("Nivel 01", "Nivel 02", "Pueblo", "Intro"):
    lay = layout(nombre)
    for e in lay["events"]:
        acts = e.get("actions") or []
        if any(a["type"]["value"] in ("PlayMusicOnChannel", "PlayMusic") for a in acts) and \
                any(c["type"]["value"] == "SceneJustBegins" for c in e.get("conditions") or []):
            e["actions"] = [a for a in acts if a["type"]["value"] not in ("PlayMusicOnChannel", "PlayMusic") and
                            not (a["type"]["value"] == "SetStringVariable" and a["parameters"][0] == "MusicaActual")]
            e.setdefault("events", []).insert(0, musica(OVERTURE if nombre == "Intro" else VERANO, OVERTURE if nombre == "Intro" else VERANO))
            break
    else:
        # ya convertido en una ejecucion anterior
        pass
menu = layout("Menu Principal")
for e in recorrer(menu["events"]):
    for a in e.get("actions") or []:
        if a["type"]["value"] == "PlayMusic":
            a["type"]["value"] = "PlayMusicOnChannel"; a["parameters"] = ["", a["parameters"][1], "0", "yes", "VolumenMusica", "1"]
menu["events"] = [e for e in menu["events"] if not e.get("_musica") and
                  not (e.get("type", "").endswith("Comment") and "Volumen de la musica" in e.get("comment", ""))]
cargar = EV([C("SceneJustBegins", "")], [], [
    EV([C("GroupExists", AJUSTES, q("Musica"))], [A("ReadNumberFromStorage", AJUSTES, q("Musica"), "", "TempNumero"), nv("VolumenMusica", "TempNumero")]),
    EV([], [A("SetMusicChannelVolume", "", "0", "=", "VolumenMusica")])])
menu["events"] += [COM("Volumen de la musica guardado en Ajustes (se cambia desde la pestana Opciones de la mochila)"), cargar]

# =====================================================================================
# 2. Pestanas de pausa en la mochila
# =====================================================================================
for f in ["PanelPausa", "PestanaMochila", "PestanaMochilaActiva", "PestanaOpciones", "PestanaOpcionesActiva", "PestanaSalir",
          "PestanaSalirActiva", "BotonPausa", "BotonPausaHover", "BarraVol", "BarraVolRelleno"]:
    add_resource(d, "image", "Inventario/%s.png" % f, "Inventario/%s.png" % f)
for f in ["FondoGameOver", "TituloGameOver", "Estrellita"]:
    add_resource(d, "image", "GameOver/%s.png" % f, "GameOver/%s.png" % f)

PEST = ["Mochila", "Opciones", "Salir"]
set_global_object(d, sprite_obj("PestanaPausa", [anim_def(n + s, [frame("Inventario/Pestana%s%s.png" % (n, s))]) for n in PEST for s in ("", "Activa")],
                                [var("Pestana", "string", "")], tween=False))
set_global_object(d, sprite_obj("PanelPausa", [anim_def("Panel", [frame("Inventario/PanelPausa.png")])], tween=False))
set_global_object(d, sprite_obj("BotonPausa", [anim_def("Normal", [frame("Inventario/BotonPausa.png")]), anim_def("Hover", [frame("Inventario/BotonPausaHover.png")])],
                                [var("Accion", "string", ""), var("Pestana", "string", "")], tween=False))
set_global_object(d, sprite_obj("BotonMiniPausa", [anim_def("Normal", [frame("Menu/BotonMini.png")]), anim_def("Hover", [frame("Menu/BotonMiniHover.png")])],
                                [var("Accion", "string", ""), var("Pestana", "string", "")], tween=False))
set_global_object(d, sprite_obj("BarraVol", [anim_def("Barra", [frame("Inventario/BarraVol.png")])], [var("Pestana", "string", "")], tween=False))
set_global_object(d, sprite_obj("BarraVolRelleno", [anim_def("Relleno", [frame("Inventario/BarraVolRelleno.png")])],
                                [var("Clave", "string", ""), var("Pestana", "string", "")], tween=False))
set_global_object(d, text_obj("TextoPausa", "", 12, (255, 236, 170), (60, 30, 12),
                              variables=[var("Clave", "string", ""), var("Pestana", "string", ""), var("CX", "number", 0), var("CY", "number", 0)]))
PAUSA = ["PestanaPausa", "PanelPausa", "BotonPausa", "BotonMiniPausa", "BarraVol", "BarraVolRelleno", "TextoPausa"]

lay = next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")
lay["instances"] = [i for i in lay["instances"] if i["name"] not in PAUSA]
L = "Inventario"
def pv(p): return var("Pestana", "string", p)
nuevas = [inst("PestanaPausa", 300 + k * 30, 14, L, 505, variables=[pv(n)]) for k, n in enumerate(PEST)]
nuevas.append(inst("PanelPausa", 50, 35, L, 511))
def texto(clave, x, y, pest, size=None, cx=0, cy=0):
    i = inst("TextoPausa", x, y, L, 560, variables=[var("Clave", "string", clave), pv(pest), var("CX", "number", cx), var("CY", "number", cy)])
    return i
def boton(accion, x, y, pest):
    return [inst("BotonPausa", x, y, L, 555, variables=[var("Accion", "string", accion), pv(pest)]),
            texto("Btn" + accion, x, y, pest, cx=x + 75, cy=y + 12)]
# Opciones
nuevas += [texto("TituloOpciones", 66, 46, "Opciones"), texto("Volumen", 76, 79, "Opciones"), texto("Musica", 76, 107, "Opciones"),
           texto("Pantalla", 76, 137, "Opciones"), texto("Teclas", 76, 176, "Opciones"), texto("Ayuda", 76, 200, "Opciones")]
for fila, (clave, y) in enumerate((("Volumen", 76), ("Musica", 104))):
    nuevas += [inst("BotonMiniPausa", 252, y, L, 555, variables=[var("Accion", "string", clave + "Menos"), pv("Opciones")]),
               texto("Signo", 252, y, "Opciones", cx=261, cy=y + 9),
               inst("BarraVol", 274, y + 4, L, 555, variables=[pv("Opciones")]),
               inst("BarraVolRelleno", 276, y + 6, L, 556, w=100, h=6, variables=[var("Clave", "string", clave), pv("Opciones")]),
               inst("BotonMiniPausa", 382, y, L, 555, variables=[var("Accion", "string", clave + "Mas"), pv("Opciones")]),
               texto("SignoMas", 382, y, "Opciones", cx=391, cy=y + 9)]
nuevas += boton("Pantalla", 252, 132, "Opciones")
# Salir
nuevas += [texto("TituloSalir", 66, 46, "Salir"), texto("SalirTexto", 240, 82, "Salir", cx=240, cy=88)]
nuevas += boton("Menu", 165, 116, "Salir") + boton("Cerrar", 165, 150, "Salir")
lay["instances"] += nuevas

FIJOS = {"TituloOpciones": "Opciones", "TituloSalir": "Salir", "Signo": "-", "SignoMas": "+",
         "Teclas": "E o I: mochila     G: guardar     1-0: barra rápida", "Ayuda": "Los ajustes se guardan solos.",
         "SalirTexto": "¿Terminaste por hoy? La partida se guarda antes de salir.",
         "BtnPantalla": "Cambiar", "BtnMenu": "Ir al menú principal", "BtnCerrar": "Cerrar el juego"}
ESTILO = {"TituloOpciones": (14, "255;236;170"), "TituloSalir": (14, "255;236;170"), "Ayuda": (10, "90;55;28"), "Teclas": (10, "90;55;28"),
          "Volumen": (12, "70;40;20"), "Musica": (12, "70;40;20"), "Pantalla": (12, "70;40;20"), "SalirTexto": (12, "70;40;20"),
          "Signo": (12, "255;246;210"), "SignoMas": (12, "255;246;210"),
          "BtnPantalla": (11, "70;40;20"), "BtnMenu": (11, "70;40;20"), "BtnCerrar": (11, "70;40;20")}
CLARO = {"TituloOpciones", "TituloSalir", "Signo", "SignoMas"}

def mostrar_mochila(si):
    objs = ["PanelMochila", "TituloMochila", "AyudaMochila", "TextoInfoNombre", "TextoInfoTipo", "TextoInfoDesc"]
    acts = [show(o) if si else hide(o) for o in objs]
    acts.append(sv("GrupoVisible", q("Mochila") if si else q("Pausa")))
    return EV([], acts, [EV([objv_s("SlotUI", "Grupo", q("Mochila"))], [show("SlotUI") if si else hide("SlotUI")])])

def guardar_y(accion):
    return EV([objv_s("BotonPausa", "Accion", q(accion)), isv("SalidaPendiente", q(""))],
              [sv("SalidaPendiente", q(accion)), A("ResetTimer", "", q("SalidaPausa")), snd("Menu/Guardado.wav", 60)], [
        EV([inv_("RanuraActual", "1", ">=")], [nv("Posicion_Inicial_Jugador.X", "Personaje_jugador.X()"), nv("Posicion_Inicial_Jugador.Y", "Personaje_jugador.Y()"),
                                               nv("Vida", "Personaje_jugador.Vida"), sv("EscenaAGuardar", "CurrentSceneName()")])])

def vol(accion, cambio):
    general = accion.startswith("Volumen")
    if general:
        acts = [A("SetGlobalVolume", "", "+" if cambio > 0 else "-", "10")]
        clamp = [EV([C("GlobalVolume", "", "<", "0")], [A("SetGlobalVolume", "", "=", "0")]),
                 EV([C("GlobalVolume", "", ">", "100")], [A("SetGlobalVolume", "", "=", "100")]),
                 EV([], [A("EcrireFichierExp", AJUSTES, q("Volumen"), "GlobalVolume()")])]
    else:
        acts = [nv("VolumenMusica", "10", "+" if cambio > 0 else "-")]
        clamp = [EV([inv_("VolumenMusica", "0", "<")], [nv("VolumenMusica", "0")]),
                 EV([inv_("VolumenMusica", "100", ">")], [nv("VolumenMusica", "100")]),
                 EV([], [A("SetMusicChannelVolume", "", "0", "=", "VolumenMusica"), A("EcrireFichierExp", AJUSTES, q("Musica"), "VolumenMusica")])]
    return EV([objv_s("BotonMiniPausa", "Accion", q(accion))], acts, clamp)

E = [COM("PAUSA: pestanas Mochila / Opciones / Salir arriba de la mochila (como en Stardew). Solo con la mochila abierta, no en la mesa ni en tiendas.")]
E.append(EV([C("SceneJustBegins", "")], [sv("PestanaActual", q("Mochila")), sv("SalidaPendiente", q("")), bv("VerPausa", "False")] + [hide(o) for o in PAUSA],
            [EV([objv_s("TextoPausa", "Clave", q(k))], [txt("TextoPausa", q(v))]) for k, v in FIJOS.items()] +
            [EV([objv_s("TextoPausa", "Clave", q(k))], [A("TextObject::Text::SetFontSize", "TextoPausa", "=", str(s)), A("TextObject::ChangeColor", "TextoPausa", q(c))])
             for k, (s, c) in ESTILO.items()] +
            [EV([objv_s("TextoPausa", "Clave", q(k))], [A("TextObject::SetOutline", "TextoPausa", q("60;30;12"), "2")]) for k in CLARO] +
            [EV([objv_s("TextoPausa", "Clave", q(k))], [A("TextObject::Text::SetOutlineEnabled", "TextoPausa", "no")]) for k in ESTILO if k not in CLARO]))
E.append(EV([], [bv("VerPausa", "False")]))
E.append(EV([ibv("InventarioAbierto", "True"), ibv("FabricarAbierto", "False"), ibv("TiendaAbierta", "False")], [bv("VerPausa", "True")]))
E.append(EV([ibv("InventarioAbierto", "False"), isv("PestanaActual", q("Mochila"), "!=")], [sv("PestanaActual", q("Mochila"))]))
E.append(EV([ibv("VerPausa", "False")], [hide(o) for o in PAUSA]))
E.append(EV([ibv("VerPausa", "True")], [show("PestanaPausa")], [
    EV([objv_s("PestanaPausa", "Pestana", "PestanaActual")], [anim("PestanaPausa", 'PestanaPausa.Pestana + "Activa"')]),
    EV([objv_s("PestanaPausa", "Pestana", "PestanaActual", "!=")], [anim("PestanaPausa", "PestanaPausa.Pestana")]),
    EV([isv("PestanaActual", q("Mochila"))], [hide("PanelPausa")]),
    EV([isv("PestanaActual", q("Mochila"), "!=")], [show("PanelPausa")]),
    *[EV([objv_s(o, "Pestana", "PestanaActual")], [show(o)]) for o in PAUSA[2:]],
    *[EV([objv_s(o, "Pestana", "PestanaActual", "!=")], [hide(o)]) for o in PAUSA[2:]],
]))
E.append(COM("Cambiar de pestana"))
E.append(EV([ibv("VerPausa", "True"), cursor("PestanaPausa"), released(), objv_s("PestanaPausa", "Pestana", "PestanaActual", "!=")],
            [sv("PestanaActual", "PestanaPausa.Pestana"), snd("Menu/Click.wav", 60)], [
    EV([isv("PestanaActual", q("Mochila"))], [], [mostrar_mochila(True)]),
    EV([isv("PestanaActual", q("Mochila"), "!=")], [], [mostrar_mochila(False)])]))
E.append(COM("Botones: hover y clic"))
E.append(EV([], [anim("BotonPausa", q("Normal")), anim("BotonMiniPausa", q("Normal"))]))
E.append(EV([ibv("VerPausa", "True"), cursor("BotonPausa"), visible("BotonPausa")], [anim("BotonPausa", q("Hover"))]))
E.append(EV([ibv("VerPausa", "True"), cursor("BotonMiniPausa"), visible("BotonMiniPausa")], [anim("BotonMiniPausa", q("Hover"))]))
E.append(EV([ibv("VerPausa", "True"), cursor("BotonMiniPausa"), visible("BotonMiniPausa"), released()], [snd("Menu/Click.wav", 60)],
            [vol("VolumenMenos", -1), vol("VolumenMas", 1), vol("MusicaMenos", -1), vol("MusicaMas", 1)]))
E.append(EV([ibv("VerPausa", "True"), cursor("BotonPausa"), visible("BotonPausa"), released()], [snd("Menu/Click.wav", 60)], [
    EV([objv_s("BotonPausa", "Accion", q("Pantalla"))], [bv("TempPantalla", "False")], [
        EV([C("IsFullScreen", "")], [bv("TempPantalla", "True")]),
        EV([ibv("TempPantalla", "True")], [A("SetFullScreen", "", "no", "")]),
        EV([ibv("TempPantalla", "False")], [A("SetFullScreen", "", "yes", "")])]),
    guardar_y("Menu"), guardar_y("Cerrar")]))
E.append(EV([isv("SalidaPendiente", q("Menu")), timer("SalidaPausa", ">", 0.5)], [sv("SalidaPendiente", q("")), A("Scene", "", q("Menu Principal"), "no")]))
E.append(EV([isv("SalidaPendiente", q("Cerrar")), timer("SalidaPausa", ">", 0.5)], [sv("SalidaPendiente", q("")), A("Quit", "")]))
E.append(COM("Textos que cambian, barras de volumen y etiquetas centradas en sus botones"))
E.append(EV([ibv("VerPausa", "True")], [], [
    EV([objv_s("TextoPausa", "Clave", q("Volumen"))], [txt("TextoPausa", '"Volumen general: " + ToString(round(GlobalVolume())) + "%"')]),
    EV([objv_s("TextoPausa", "Clave", q("Musica"))], [txt("TextoPausa", '"Música: " + ToString(VolumenMusica) + "%"')]),
    EV([objv_s("TextoPausa", "Clave", q("Pantalla")), C("IsFullScreen", "")], [txt("TextoPausa", q("Pantalla completa: Sí"))]),
    EV([objv_s("TextoPausa", "Clave", q("Pantalla")), C("IsFullScreen", "", inv=True)], [txt("TextoPausa", q("Pantalla completa: No"))]),
    EV([objv_s("BarraVolRelleno", "Clave", q("Volumen"))], [ancho("BarraVolRelleno", "max(1, GlobalVolume())")]),
    EV([objv_s("BarraVolRelleno", "Clave", q("Musica"))], [ancho("BarraVolRelleno", "max(1, VolumenMusica)")]),
    EV([objv_n("TextoPausa", "CX", "0", ">")], [A("SetCenterX", "TextoPausa", "=", "TextoPausa.CX"), A("SetCenterY", "TextoPausa", "=", "TextoPausa.CY")]),
]))
external_events(d, "Pausa", E)
set_global_var(d, var("TempPantalla", "boolean", False))

pers = ext("Personaje")
if not any(e.get("target") == "Pausa" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    i = next(k for k, e in enumerate(pers["events"]) if e.get("type") == "BuiltinCommonInstructions::Link" and e.get("target") == "Inventario")
    pers["events"].insert(i + 1, LINK("Pausa"))

# Los clics en las casillas de la mochila solo cuentan en la pestana Mochila
for e in recorrer(ext("Inventario")["events"]):
    cs = e.get("conditions") or []
    tipos = [c["type"]["value"] for c in cs]
    if "IsCursorOnObject" in tipos and any(c["type"]["value"] == "StringObjectVariable" and c["parameters"][:2] == ["SlotUI", "Grupo"] and c["parameters"][-1] == '"Mochila"' for c in cs) \
            and any(c["type"]["value"] == "BooleanVariable" and c["parameters"][0] == "InventarioAbierto" for c in cs) \
            and not any(c["type"]["value"] == "StringVariable" and c["parameters"][0] == "PestanaActual" for c in cs):
        cs.append(isv("PestanaActual", q("Mochila")))

# =====================================================================================
# 3. Game Over: "Te desmayaste"
# =====================================================================================
go = layout("GameOver")
go["stopSoundsOnStartup"] = False
capa = next(l for l in go["layers"] if l["name"] == "")
hd = json.loads(json.dumps(capa)); hd["name"] = "HD"; hd["effects"] = []
go["layers"] = [capa, hd]
go["variables"] = [var("Perdidas", "number", 0), var("Destino", "string", "")]
go["objects"] = [
    sprite_obj("FondoGO", [anim_def("Fondo", [frame("GameOver/FondoGameOver.png")])], tween=False),
    sprite_obj("TituloGO", [anim_def("Titulo", [frame("GameOver/TituloGameOver.png")])]),
    sprite_obj("PedroGO", [anim_def("Caido", [frame("NewSprite", (16, 16))])]),
    sprite_obj("EstrellaGO", [anim_def("Estrella", [frame("GameOver/Estrellita.png", (4, 4))])], [var("Fase", "number", 0)], tween=False),
    sprite_obj("EsporaGO", [anim_def("Espora", [frame("Menu/Espora.png")])]),
    sprite_obj("BotonGO", [anim_def("Normal", [frame("Inventario/BotonPausa.png")]), anim_def("Hover", [frame("Inventario/BotonPausaHover.png")])],
               [var("Accion", "string", "")]),
    sprite_obj("TelonGO", [anim_def("Negro", [frame("Menu/Negro.png")])]),
    text_obj("TextoGO", "", 22, (255, 246, 210), (20, 16, 30), align="center", variables=[var("Clave", "string", ""), var("CX", "number", 0)], tween=True),
]
go["objectsFolderStructure"] = {"folderName": "__ROOT", "children": [{"objectName": o["name"]} for o in go["objects"]]}
pedro = inst("PedroGO", 240, 168, "", 20, w=64, h=64); pedro["angle"] = 90
go["instances"] = [
    inst("FondoGO", 0, 0, "", 0), inst("TituloGO", 121, -60, "", 30), pedro,
    *[inst("EstrellaGO", 260, 150, "", 25, variables=[var("Fase", "number", k * 2.09)]) for k in range(3)],
    inst("BotonGO", 165, 204, "", 30, variables=[var("Accion", "string", "Casa")]),
    inst("BotonGO", 165, 236, "", 30, variables=[var("Accion", "string", "Menu")]),
    inst("TextoGO", 0, 0, "HD", 40, variables=[var("Clave", "string", "Sub"), var("CX", "number", 480)]),
    inst("TextoGO", 0, 0, "HD", 40, variables=[var("Clave", "string", "Detalle"), var("CX", "number", 480)]),
    inst("TextoGO", 0, 0, "HD", 41, variables=[var("Clave", "string", "BtnCasa"), var("CX", "number", 480)]),
    inst("TextoGO", 0, 0, "HD", 41, variables=[var("Clave", "string", "BtnMenu"), var("CX", "number", 480)]),
    inst("TelonGO", 0, 0, "HD", 100, w=960, h=540),
]
POS_Y = {"Sub": 160, "Detalle": 204, "BtnCasa": 2 * (204 + 12) - 10, "BtnMenu": 2 * (236 + 12) - 10}
G = [COM("TE DESMAYASTE: pierdes el 10% de las monedas (maximo 100) y Tomas te lleva a casa"),
     EV([C("SceneJustBegins", "")], [
         A("ZoomCamera", "", "2", q(""), "0"), A("SetCameraCenterX", "", "=", "240", q(""), "0"), A("SetCameraCenterY", "", "=", "135", q(""), "0"),
         nv("Perdidas", "min(100, floor(Monedas * 0.1))"), nv("Monedas", "Perdidas", "-"), nv("Vida", "30"),
         nv("Posicion_Inicial_Jugador.X", "688"), nv("Posicion_Inicial_Jugador.Y", "284"), sv("Destino", q("")),
         opacity("TextoGO", 0), opacity("BotonGO", 0), opacity("TelonGO", 255), opacity("PedroGO", 0),
         tw_op("TelonGO", "Aclarar", 0, "easeInQuad", 1.2),
         tw_y("TituloGO", "Caer", "26", "easeOutBounce", 1.3),
         A("ResetTimer", "", q("Escena")), A("ResetTimer", "", q("Espora")),
         A("PlaySound", "", "Intro/Explosion.wav", "no", "35", "0.5"),
     ], [
         musica("GameOver", OVERTURE, pitch="0.6", vol="VolumenMusica * 0.7"),
         *[EV([objv_s("TextoGO", "Clave", q(k))], [A("SetY", "TextoGO", "=", str(y))]) for k, y in POS_Y.items()],
         EV([objv_s("TextoGO", "Clave", q("Sub"))], [txt("TextoGO", q("Las papas radiactivas te dejaron fuera de combate..."))]),
         EV([objv_s("TextoGO", "Clave", q("Detalle"))], [txt("TextoGO", q("El abuelo Tomás te encontró y te llevó de vuelta a la granja.")),
                                                        A("TextObject::Text::SetFontSize", "TextoGO", "=", "16"), A("TextObject::ChangeColor", "TextoGO", q("170;220;140"))]),
         EV([objv_s("TextoGO", "Clave", q("Detalle")), inv_("Perdidas", "0", ">")],
            [txt("TextoGO", '"El abuelo Tomás te encontró y te llevó de vuelta a la granja.\nSe te cayeron " + ToString(Perdidas) + " monedas por el camino."')]),
         EV([objv_s("TextoGO", "Clave", q("BtnCasa"))], [txt("TextoGO", q("Despertar en casa")), A("TextObject::Text::SetFontSize", "TextoGO", "=", "18"), A("TextObject::ChangeColor", "TextoGO", q("70;40;20")), A("TextObject::Text::SetOutlineEnabled", "TextoGO", "no")]),
         EV([objv_s("TextoGO", "Clave", q("BtnMenu"))], [txt("TextoGO", q("Menú principal")), A("TextObject::Text::SetFontSize", "TextoGO", "=", "18"), A("TextObject::ChangeColor", "TextoGO", q("70;40;20")), A("TextObject::Text::SetOutlineEnabled", "TextoGO", "no")]),
     ]),
     COM("Aparicion por partes"),
     EV([timer("Escena", ">=", 1.0), ONCE()], [tw_op("PedroGO", "Ver", 255, "linear", 0.8)]),
     EV([timer("Escena", ">=", 1.4), ONCE()], [], [EV([objv_s("TextoGO", "Clave", q("Sub"))], [tw_op("TextoGO", "Ver", 255, "linear", 0.8)])]),
     EV([timer("Escena", ">=", 2.0), ONCE()], [], [EV([objv_s("TextoGO", "Clave", q("Detalle"))], [tw_op("TextoGO", "Ver", 255, "linear", 0.8)])]),
     EV([timer("Escena", ">=", 2.6), ONCE()], [tw_op("BotonGO", "Ver", 255, "linear", 0.5)],
        [EV([objv_s("TextoGO", "Clave", q(k))], [tw_op("TextoGO", "Ver", 255, "linear", 0.5)]) for k in ("BtnCasa", "BtnMenu")]),
     EV([], [], [FOREACH("TextoGO", [], [A("SetCenterX", "TextoGO", "=", "TextoGO.CX")])]),
     COM("El titulo flota despues de caer, estrellitas girando sobre la cabeza de Pedro y esporas subiendo"),
     EV([timer("Escena", ">=", 1.4)], [A("SetY", "TituloGO", "=", "26 + sin(TimeFromStart() * 2) * 2")]),
     EV([], [A("SetX", "EstrellaGO", "=", "268 + cos(TimeFromStart() * 3 + EstrellaGO.Fase) * 13 - 4"),
             A("SetY", "EstrellaGO", "=", "150 + sin(TimeFromStart() * 3 + EstrellaGO.Fase) * 4 - 4"),
             A("SetZOrder", "EstrellaGO", "=", "20 + sin(TimeFromStart() * 3 + EstrellaGO.Fase) * 10"),
             opacity("EstrellaGO", "PedroGO.Opacity()")]),
     EV([timer("Espora", ">=", 0.12)], [A("ResetTimer", "", q("Espora")), A("Create", "", "EsporaGO", "RandomInRange(0, 478)", "RandomInRange(180, 270)", q("")),
                                         opacity("EsporaGO", 0),
                                         tw_y("EsporaGO", "Subir", "EsporaGO.Y() - RandomInRange(60, 140)", "easeOutSine", "RandomFloatInRange(2.5, 4.5)", "yes"),
                                         A("Tween::TweenBehavior::AddObjectOpacityTween2", "EsporaGO", "Tween", q("Brillar"), "RandomInRange(120, 230)", q("easeInOutSine"), "1.2", "no")]),
     COM("Botones"),
     EV([], [anim("BotonGO", q("Normal"))]),
     EV([cursor("BotonGO"), C("OpacityCapability::OpacityBehavior::Value", "BotonGO", "Opacity", ">", "200"), isv("Destino", q(""))], [anim("BotonGO", q("Hover"))], [
         EV([released()], [snd("Menu/Click.wav", 70), tw_op("TelonGO", "Oscurecer", 255, "easeInQuad", 0.7), A("ResetTimer", "", q("Salida"))], [
             EV([objv_s("BotonGO", "Accion", q("Casa"))], [sv("Destino", q("Nivel 01"))]),
             EV([objv_s("BotonGO", "Accion", q("Menu"))], [sv("Destino", q("Menu Principal"))])])]),
     EV([isv("Destino", q("Nivel 01")), timer("Salida", ">=", 0.8)], [A("Scene", "", q("Nivel 01"), "no")]),
     EV([isv("Destino", q("Menu Principal")), timer("Salida", ">=", 0.8)], [A("Scene", "", q("Menu Principal"), "no")]),
]
go["events"] = G

json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: musica continua, pestanas de pausa y nueva pantalla de game over")
