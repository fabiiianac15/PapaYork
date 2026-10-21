"""Rebuilds the 'Menu Principal' scene of Papayork and adds the save system.

Edits the GDevelop project JSON in place (a backup must be made before running).
"""
import json, sys, uuid, copy

PROJ = sys.argv[1]
d = json.load(open(PROJ, encoding="utf8"))

def uid(): return str(uuid.uuid4())
def q(s): return '"' + s.replace('\\', '\\\\').replace('"', '\\"') + '"'

# ---------- event helpers ----------
def I(t, *p, inv=False, sub=None):
    i = {"type": {"value": t}, "parameters": [str(x) for x in p]}
    if inv: i["type"]["inverted"] = True
    if sub is not None: i["subInstructions"] = sub
    return i
def C(t, *p, inv=False): return I(t, *p, inv=inv)
def A(t, *p): return I(t, *p)
def EV(conds=(), acts=(), subs=(), variables=None):
    e = {"type": "BuiltinCommonInstructions::Standard", "conditions": list(conds), "actions": list(acts)}
    if subs: e["events"] = list(subs)
    if variables: e["variables"] = variables
    return e
def FOREACH(obj, conds=(), acts=(), subs=()):
    e = {"type": "BuiltinCommonInstructions::ForEach", "object": obj, "conditions": list(conds), "actions": list(acts)}
    if subs: e["events"] = list(subs)
    return e
def COM(text):
    return {"type": "BuiltinCommonInstructions::Comment",
            "color": {"b": 109, "g": 230, "r": 255, "textB": 0, "textG": 0, "textR": 0}, "comment": text}
def LINK(name): return {"type": "BuiltinCommonInstructions::Link", "include": {"includeConfig": 0}, "target": name}
def ONCE(): return C("BuiltinCommonInstructions::Once")
def var(name, typ, value):
    return {"name": name, "type": typ, "value": value}

# common instructions
def sv(v, val, op="="): return A("SetStringVariable", v, op, val)
def nv(v, val, op="="): return A("SetNumberVariable", v, op, val)
def isv(v, val, op="="): return C("StringVariable", v, op, val)
def inv_(v, val, op="="): return C("NumberVariable", v, op, val)
def anim(o, name): return A("SetAnimationName", o, name)
def txt(o, val): return A("TextContainerCapability::TextContainerBehavior::SetValue", o, "Text", "=", val)
def snd(f, vol=60): return A("PlaySound", "", f, "no", str(vol), "1")
def cursor(o, inv=False): return C("IsCursorOnObject", o, "", "", "", inv=inv)
def released(): return C("MouseButtonFromTextReleased", "", q("Left"))
def held(): return C("MouseButtonFromTextPressed", "", q("Left"))
def timer(name, op, val): return C("CompareTimer", "", q(name), op, str(val))
def tw_y(o, ident, to, ease, dur, destroy="no"): return A("Tween::TweenBehavior::AddObjectPositionYTween2", o, "Tween", q(ident), to, q(ease), str(dur), destroy)
def tw_x(o, ident, to, ease, dur, destroy="no"): return A("Tween::TweenBehavior::AddObjectPositionXTween2", o, "Tween", q(ident), to, q(ease), str(dur), destroy)
def tw_scale(o, ident, to, ease, dur, center="no"): return A("Tween::TweenBehavior::AddObjectScaleTween3", o, "Tween", q(ident), str(to), q(ease), str(dur), "no", center)
def tw_op(o, ident, to, ease, dur, destroy="no"): return A("Tween::TweenBehavior::AddObjectOpacityTween2", o, "Tween", q(ident), str(to), q(ease), str(dur), destroy)
def tw_done(o, ident): return C("Tween::HasFinished", o, "Tween", q(ident))
def cam_ui(y): return A("Tween::TweenCameraPosition2", "", q("CambioPantalla"), "240", str(y), q("UI"), q("easeInOutCubic"), "0.6")
def opacity(o, v): return A("OpacityCapability::OpacityBehavior::SetValue", o, "Opacity", "=", str(v))
def scale(o, v): return A("ScalableCapability::ScalableBehavior::SetValue", o, "Scale", "=", str(v))
def objv_s(o, v, val, op="="): return C("StringObjectVariable", o, v, op, val)
def objv_n(o, v, val, op="="): return C("NumberObjectVariable", o, v, op, val)
def objv_b(o, v, val): return C("BooleanObjectVariable", o, v, val, "")
def set_objv_b(o, v, val): return A("SetBooleanObjectVariable", o, v, val, "")
def set_objv_n(o, v, val, op="="): return A("SetNumberObjectVariable", o, v, op, val)

SAVE = q("PapayorkPartidas")
AJUSTES = q("PapayorkAjustes")
def slot_key(numexpr, key): return '"Ranura" + ToString(' + numexpr + ') + "/' + key + '"'

# ---------- resources ----------
res = d["resources"]["resources"]
have = {r["name"] for r in res}
def add_img(name, file):
    if name not in have:
        res.append({"file": file, "kind": "image", "metadata": "{\"extension\":\".png\"}", "name": name, "smoothed": False, "userAdded": True})
        have.add(name)
def add_audio(name, file):
    if name not in have:
        res.append({"file": file, "kind": "audio", "metadata": "", "name": name, "preloadAsMusic": False, "preloadAsSound": True, "preloadInCache": False, "userAdded": True})
        have.add(name)
def add_font(name, file):
    if name not in have:
        res.append({"file": file, "kind": "font", "metadata": "", "name": name, "userAdded": True})
        have.add(name)

IMGS = ["FondoInicio", "FondoInicioSinLogo", "LogoPapayork", "Negro", "Espora", "PanelMadera", "Ranura", "RanuraHover",
        "BotonPeq", "BotonPeqHover", "BotonMini", "BotonMiniHover"]
for b in ["Cargar", "Nueva", "Ajustes"]:
    IMGS += ["Boton" + b, "Boton" + b + "Hover", "Boton" + b + "Presionado"]
for n in IMGS: add_img("Menu/" + n + ".png", "Menu/" + n + ".png")
for n in ["Hover", "Click", "GolpeLogo", "Guardado"]: add_audio("Menu/" + n + ".wav", "Menu/" + n + ".wav")
FONT = "Fuentes/PixelifySans.ttf"
add_font(FONT, FONT)

# image sizes (needed for origins and collision masks)
SIZES = {"BotonCargar": (155, 126), "BotonNueva": (155, 127), "BotonAjustes": (155, 128)}

# ---------- object helpers ----------
TWEEN = {"name": "Tween", "type": "Tween::TweenBehavior"}
def frame(img, origin=(0, 0), mask=None):
    f = {"hasCustomCollisionMask": mask is not None, "image": img, "points": [],
         "originPoint": {"name": "origine", "x": origin[0], "y": origin[1]},
         "centerPoint": {"automatic": True, "name": "centre", "x": 0, "y": 0},
         "customCollisionMask": [mask] if mask else []}
    return f
def rect(x0, y0, x1, y1): return [{"x": x0, "y": y0}, {"x": x1, "y": y0}, {"x": x1, "y": y1}, {"x": x0, "y": y1}]
def anim_def(name, frames, loop=False, dt=0.08):
    return {"name": name, "useMultipleDirections": False,
            "directions": [{"looping": loop, "timeBetweenFrames": dt, "sprites": frames}]}
def sprite_obj(name, anims, variables=(), tween=True):
    return {"adaptCollisionMaskAutomatically": False, "assetStoreId": "", "name": name, "persistentUuid": uid(),
            "type": "Sprite", "updateIfNotVisible": False, "variables": list(variables), "effects": [],
            "behaviors": [TWEEN] if tween else [], "animations": anims}
def text_obj(name, text, size=12, color=(255, 255, 255), outline=(36, 21, 13), align="left", variables=(), tween=False, bold=False):
    col = f"{color[0]};{color[1]};{color[2]}"
    return {"assetStoreId": "", "bold": bold, "italic": False, "name": name, "persistentUuid": uid(), "smoothed": False,
            "type": "TextObject::Text", "underlined": False, "variables": list(variables), "effects": [],
            "behaviors": [TWEEN] if tween else [],
            "string": text, "font": FONT, "textAlignment": align, "characterSize": size,
            "color": {"r": color[0], "g": color[1], "b": color[2]},
            "content": {"bold": bold, "isOutlineEnabled": outline is not None,
                        "isShadowEnabled": False, "italic": False,
                        "outlineColor": f"{outline[0]};{outline[1]};{outline[2]}" if outline else "0;0;0",
                        "outlineThickness": 2, "shadowAngle": 90, "shadowBlurRadius": 2, "shadowColor": "0;0;0",
                        "shadowDistance": 4, "shadowOpacity": 127, "smoothed": False, "underlined": False,
                        "text": text, "font": FONT, "textAlignment": align, "verticalTextAlignment": "top",
                        "characterSize": size, "lineHeight": 0, "color": col}}
def inst(name, x, y, layer="", z=0, w=None, h=None, variables=()):
    i = {"angle": 0, "customSize": w is not None, "height": h or 0, "keepRatio": True, "layer": layer, "name": name,
         "persistentUuid": uid(), "width": w or 0, "x": x, "y": y, "zOrder": z,
         "numberProperties": [], "stringProperties": [], "initialVariables": list(variables)}
    return i

# ---------- objects ----------
botones_anims = []
for b in ["Cargar", "Nueva", "Ajustes"]:
    w, h = SIZES["Boton" + b]
    org = (w // 2, h // 2)
    mask = rect(14, 10, w - 14, h - 12)
    for st in ["", "Hover", "Presionado"]:
        botones_anims.append(anim_def(b + st, [frame("Menu/Boton" + b + st + ".png", org, mask)]))

objects = [
    sprite_obj("FondoInicio", [anim_def("SinLogo", [frame("Menu/FondoInicioSinLogo.png")]),
                               anim_def("ConLogo", [frame("Menu/FondoInicio.png")])], tween=False),
    sprite_obj("LogoPapayork", [anim_def("", [frame("Menu/LogoPapayork.png")])]),
    sprite_obj("Espora", [anim_def("", [frame("Menu/Espora.png", (1, 1))])]),
    sprite_obj("BotonMenu", botones_anims, [var("Accion", "string", ""), var("Orden", "number", 0),
                                            var("BaseY", "number", 0), var("Hover", "boolean", False)]),
    sprite_obj("Fundido", [anim_def("", [frame("Menu/Negro.png")])]),
    sprite_obj("Oscurecer", [anim_def("", [frame("Menu/Negro.png")])], tween=False),
    sprite_obj("PanelMadera", [anim_def("", [frame("Menu/PanelMadera.png")])], tween=False),
    sprite_obj("RanuraPartida", [anim_def("Normal", [frame("Menu/Ranura.png")]),
                                 anim_def("Hover", [frame("Menu/RanuraHover.png")])],
               [var("Numero", "number", 0), var("Hover", "boolean", False)]),
    sprite_obj("BotonUI", [anim_def("Normal", [frame("Menu/BotonPeq.png")]),
                           anim_def("Hover", [frame("Menu/BotonPeqHover.png")]),
                           anim_def("MiniNormal", [frame("Menu/BotonMini.png")]),
                           anim_def("MiniHover", [frame("Menu/BotonMiniHover.png")])],
               [var("Accion", "string", ""), var("Tipo", "string", ""), var("Pantalla", "string", ""),
                var("Hover", "boolean", False)], tween=False),
    text_obj("TextoRanura", "Partida", 12, (60, 34, 18), None, variables=[var("Numero", "number", 0)]),
    text_obj("TituloPanel", "Titulo", 18, (255, 236, 170), (60, 30, 12), variables=[var("Pantalla", "string", "")]),
    text_obj("TextoUI", "", 12, (60, 34, 18), None,
             variables=[var("Clave", "string", ""), var("CX", "number", 0), var("CY", "number", 0)]),
    text_obj("MiNombre", "Fabian Jose Acosta - 192168", 11, (255, 246, 210), (36, 21, 13), tween=True),
    text_obj("NombreAsignatura", "Desarrollo de Videojuegos 193607", 11, (255, 246, 210), (36, 21, 13), tween=True),
]

# ---------- instances ----------
instances = [inst("FondoInicio", 0, 0, "", 0),
             inst("LogoPapayork", 26, -150, "", 20),
             inst("Fundido", 0, 0, "Fundido", 0, 480, 270),
             inst("MiNombre", 6, 4, "UI", 10),
             inst("NombreAsignatura", 300, 4, "UI", 10)]
for i, (acc, cx) in enumerate([("Cargar", 92), ("Nueva", 240), ("Ajustes", 388)]):
    instances.append(inst("BotonMenu", cx, 203, "UI", 10, variables=[var("Accion", "string", acc), var("Orden", "number", i + 1)]))

# Screen 2: saved games (UI layer, y 270..540)
P2 = 270
instances += [inst("Oscurecer", 0, P2, "UI", 1, 480, 270), inst("PanelMadera", 90, P2 + 15, "UI", 2),
              inst("TituloPanel", 120, P2 + 27, "UI", 5, variables=[var("Pantalla", "string", "Partidas")])]
for n in range(3):
    y = P2 + 15 + 38 + n * 48
    instances.append(inst("RanuraPartida", 108, y, "UI", 3, variables=[var("Numero", "number", n + 1)]))
    instances.append(inst("TextoRanura", 120, y + 8, "UI", 5, variables=[var("Numero", "number", n + 1)]))
def boton_ui(x, y, accion, pantalla, etiqueta, mini=False, clave=None):
    w, h = (18, 18) if mini else (84, 22)
    out = [inst("BotonUI", x, y, "UI", 3, variables=[var("Accion", "string", accion), var("Pantalla", "string", pantalla),
                                                    var("Tipo", "string", "Mini" if mini else "")])]
    out.append(inst("TextoUI", x + 4, y + 3, "UI", 5, variables=[var("Clave", "string", clave or ("Lbl" + accion + pantalla)),
                                                               var("CX", "number", x + w / 2), var("CY", "number", y + h / 2)]))
    return out, (clave or ("Lbl" + accion + pantalla), etiqueta)
labels = []
o, l = boton_ui(198, P2 + 15 + 190, "Atras", "Partidas", "Atrás"); instances += o; labels.append(l)

# Screen 3: settings (y 540..810)
P3 = 540
instances += [inst("Oscurecer", 0, P3, "UI", 1, 480, 270), inst("PanelMadera", 90, P3 + 15, "UI", 2),
              inst("TituloPanel", 120, P3 + 27, "UI", 5, variables=[var("Pantalla", "string", "Ajustes")])]
instances.append(inst("TextoUI", 112, P3 + 15 + 62, "UI", 5, variables=[var("Clave", "string", "Volumen")]))
o, l = boton_ui(318, P3 + 15 + 58, "VolMenos", "Ajustes", "-", mini=True); instances += o; labels.append(l)
o, l = boton_ui(342, P3 + 15 + 58, "VolMas", "Ajustes", "+", mini=True); instances += o; labels.append(l)
instances.append(inst("TextoUI", 112, P3 + 15 + 98, "UI", 5, variables=[var("Clave", "string", "Completa")]))
o, l = boton_ui(278, P3 + 15 + 94, "Pantalla", "Ajustes", "Cambiar"); instances += o; labels.append(l)
instances.append(inst("TextoUI", 112, P3 + 15 + 130, "UI", 5, variables=[var("Clave", "string", "Ayuda")]))
o, l = boton_ui(150, P3 + 15 + 190, "Salir", "Ajustes", "Salir"); instances += o; labels.append(l)
o, l = boton_ui(246, P3 + 15 + 190, "Atras", "Ajustes", "Atrás"); instances += o; labels.append(l)

# ---------- layers ----------
base_layer = next(l for l in d["layouts"] if l["name"] == "Menu Principal")["layers"][0]
def layer(name):
    L = copy.deepcopy(base_layer); L["name"] = name; L["effects"] = []
    return L
layers = [copy.deepcopy(base_layer), layer("UI"), layer("Fundido")]

# ---------- default values for a new game (taken from the project's globals) ----------
def to_py(v):
    t = v["type"]
    if t == "structure": return {c["name"]: to_py(c) for c in v.get("children", [])}
    if t == "array": return [to_py(c) for c in v.get("children", [])]
    return v["value"]
G = {v["name"]: v for v in d["variables"]}
GUARDADAS = ["Mochila", "Mano", "RanuraSeleccionada", "Reloj", "LuzExterior", "Destruidos", "Estadisticas", "Posicion_Inicial_Jugador",
             "Calendario", "Granja", "Construcciones", "Exp", "NivelJugador", "ExpSiguiente", "Monedas"]
reset_actions = [A("JSONToGlobalVariableStructure", q(json.dumps(to_py(G[k]), ensure_ascii=False, separators=(",", ":"))), k) for k in GUARDADAS]
reset_actions += [nv("Vida", str(G["Vida"]["value"]))]

# ---------- events ----------
E = []
E.append(COM("PAPAYORK - Menu principal.\nCapa base: fondo, logo y esporas (la camara baja como en una pelicula).\n"
             "Capa UI: tres pantallas apiladas: principal (y 0), partidas guardadas (y 270) y ajustes (y 540). "
             "Cambiar de pantalla = mover la camara de la capa UI.\nCapa Fundido: negro para entrar y salir."))
E.append(EV([C("SceneJustBegins", "")], [
    A("SetFullScreen", "", "yes", ""),
    A("SetCameraCenterX", "", "=", "240", "", "0"), A("SetCameraCenterY", "", "=", "135", "", "0"),
    anim("FondoInicio", q("SinLogo")),
    scale("BotonMenu", 0), set_objv_n("BotonMenu", "BaseY", "BotonMenu.Y()"),
    opacity("MiNombre", 0), opacity("NombreAsignatura", 0),
    opacity("Oscurecer", 165),
    A("SetX", "NombreAsignatura", "=", "474 - NombreAsignatura.Width()"),
    tw_op("Fundido", "Aclarar", 0, "easeInQuad", 1.4),
    A("Tween::TweenCameraPosition2", "", q("Paneo"), "240", "275", q(""), q("easeInOutSine"), "2.8"),
    A("ResetTimer", "", q("Intro")), A("ResetTimer", "", q("Espora")),
    sv("Pantalla", q("Intro")),
], [
    COM("Volumen guardado en Ajustes"),
    EV([C("GroupExists", AJUSTES, q("Volumen"))], [A("ReadNumberFromStorage", AJUSTES, q("Volumen"), "", "TempNumero"),
                                                  A("SetGlobalVolume", "", "=", "TempNumero")]),
    COM("Textos fijos de los botones y paneles"),
    *[EV([objv_s("TextoUI", "Clave", q(k))], [txt("TextoUI", q(v))]) for k, v in labels],
    EV([objv_s("TextoUI", "Clave", q("Ayuda"))], [txt("TextoUI", q("En el juego: G guarda la partida.\nTambién se guarda al cambiar de zona."))]),
    EV([objv_s("TituloPanel", "Pantalla", q("Ajustes"))], [txt("TituloPanel", q("Ajustes"))]),
    EV([isv("MusicaActual", q("Stardew Valley OST - Stardew Valley Overture.mp3"), "!=")], [
        A("PlayMusic", "", "Stardew Valley OST - Stardew Valley Overture.mp3", "", "100", "1"),
        sv("MusicaActual", q("Stardew Valley OST - Stardew Valley Overture.mp3"))]),
]))

E.append(COM("INTRO: primero aparece el campo, despues cae el logo y al final salen los botones"))
E.append(EV([timer("Intro", ">=", 0.6), ONCE()], [tw_y("LogoPapayork", "Caer", "160", "easeOutBounce", 1.2)]))
E.append(EV([timer("Intro", ">=", 1.03), ONCE()], [snd("Menu/GolpeLogo.wav", 80)]))
E.append(EV([tw_done("LogoPapayork", "Caer"), ONCE()], [
    anim("FondoInicio", q("ConLogo")),
    tw_scale("LogoPapayork", "Pulso", 1.04, "easeOutQuad", 0.12, "yes")]))
E.append(EV([tw_done("LogoPapayork", "Pulso"), ONCE()], [tw_scale("LogoPapayork", "Pulso2", 1, "easeOutBack", 0.25, "yes")]))
for k, t in enumerate([2.9, 3.05, 3.2]):
    E.append(EV([timer("Intro", ">=", t), ONCE()], [], [
        EV([objv_n("BotonMenu", "Orden", str(k + 1))], [tw_scale("BotonMenu", "Aparecer", 1, "easeOutBack", 0.35), snd("Menu/Hover.wav", 35)])]))
E.append(EV([timer("Intro", ">=", 3.5), ONCE()], [
    sv("Pantalla", q("Principal")),
    tw_op("MiNombre", "Aparecer", 255, "linear", 0.6), tw_op("NombreAsignatura", "Aparecer", 255, "linear", 0.6)]))

E.append(COM("Esporas radiactivas que suben del campo"))
E.append(EV([timer("Espora", ">=", 0.18)], [
    A("ResetTimer", "", q("Espora")),
    A("Create", "", "Espora", "RandomInRange(0, 480)", "CameraCenterY() + 140", q("")),
    A("SetZOrder", "Espora", "=", "10"),
    scale("Espora", "RandomInRange(1, 2)"), opacity("Espora", "RandomInRange(110, 230)"),
    tw_y("Espora", "Subir", "Espora.Y() - RandomInRange(90, 220)", "easeOutSine", "RandomInRange(3, 6)", "yes"),
    tw_x("Espora", "Deriva", "Espora.X() + RandomInRange(-30, 30)", "easeInOutSine", 4),
    tw_op("Espora", "Apagar", 0, "easeInQuad", 5)]))

# --- main buttons ---
def ir_a(pantalla, y): return [sv("Pantalla", q(pantalla)), cam_ui(y)]
E.append(COM("BOTONES PRINCIPALES: brillo al pasar el mouse, se hunden al presionar"))
E.append(EV([isv("Pantalla", q("Principal"))], [], [
    EV([cursor("BotonMenu"), objv_b("BotonMenu", "Hover", "False")], [
        set_objv_b("BotonMenu", "Hover", "True"), snd("Menu/Hover.wav", 45),
        tw_y("BotonMenu", "Flotar", "BotonMenu.BaseY - 4", "easeOutBack", 0.18)]),
    EV([cursor("BotonMenu", inv=True), objv_b("BotonMenu", "Hover", "True")], [
        set_objv_b("BotonMenu", "Hover", "False"),
        tw_y("BotonMenu", "Flotar", "BotonMenu.BaseY", "easeOutQuad", 0.15)]),
    EV([cursor("BotonMenu")], [anim("BotonMenu", 'BotonMenu.Accion + "Hover"')], [
        EV([held()], [anim("BotonMenu", 'BotonMenu.Accion + "Presionado"')])]),
    EV([cursor("BotonMenu", inv=True)], [anim("BotonMenu", "BotonMenu.Accion")]),
    EV([cursor("BotonMenu"), released()], [snd("Menu/Click.wav", 70)], [
        EV([objv_s("BotonMenu", "Accion", q("Nueva"))], [
            sv("Modo", q("Nueva")), nv("Confirmar", "0"), *ir_a("Partidas", 405)], [
            EV([objv_s("TituloPanel", "Pantalla", q("Partidas"))], [txt("TituloPanel", q("Nueva partida"))])]),
        EV([objv_s("BotonMenu", "Accion", q("Cargar"))], [
            sv("Modo", q("Cargar")), nv("Confirmar", "0"), *ir_a("Partidas", 405)], [
            EV([objv_s("TituloPanel", "Pantalla", q("Partidas"))], [txt("TituloPanel", q("Cargar partida"))])]),
        EV([objv_s("BotonMenu", "Accion", q("Ajustes"))], ir_a("Ajustes", 675)),
    ]),
]))
E.append(EV([isv("Pantalla", q("Principal"), "!=")], [anim("BotonMenu", "BotonMenu.Accion"), set_objv_b("BotonMenu", "Hover", "False")]))
E.append(FOREACH("TituloPanel", [], [A("SetCenterX", "TituloPanel", "=", "240")]))

# --- saved games screen ---
E.append(COM("PARTIDAS GUARDADAS: 3 ranuras. Cada ranura se guarda en el almacenamiento \"PapayorkPartidas\" como Ranura1/..., Ranura2/..., Ranura3/..."))
E.append(EV([isv("Pantalla", q("Partidas")), ONCE()], [], [
    FOREACH("TextoRanura", [], [], [
        EV([C("GroupExists", SAVE, slot_key("TextoRanura.Numero", "Escena"))], [
            A("ReadStringFromStorage", SAVE, slot_key("TextoRanura.Numero", "Zona"), "", "TempTexto"),
            A("ReadStringFromStorage", SAVE, slot_key("TextoRanura.Numero", "Detalle"), "", "TempTexto2"),
            txt("TextoRanura", '"Partida " + ToString(TextoRanura.Numero) + "  -  " + TempTexto + NewLine() + TempTexto2')]),
        EV([C("GroupExists", SAVE, slot_key("TextoRanura.Numero", "Escena"), inv=True)], [
            txt("TextoRanura", '"Partida " + ToString(TextoRanura.Numero) + NewLine() + "Vacía"')]),
    ]),
]))
E.append(EV([isv("Pantalla", q("Partidas"))], [], [
    EV([cursor("RanuraPartida"), objv_b("RanuraPartida", "Hover", "False")], [set_objv_b("RanuraPartida", "Hover", "True"), snd("Menu/Hover.wav", 35)]),
    EV([cursor("RanuraPartida", inv=True)], [set_objv_b("RanuraPartida", "Hover", "False")]),
    EV([cursor("RanuraPartida")], [anim("RanuraPartida", q("Hover"))]),
    EV([cursor("RanuraPartida", inv=True)], [anim("RanuraPartida", q("Normal"))]),
    EV([cursor("RanuraPartida"), released()], [snd("Menu/Click.wav", 70), nv("RanuraElegida", "RanuraPartida.Numero")], [
        COM("Cargar: solo si la ranura tiene datos"),
        EV([isv("Modo", q("Cargar"))], [], [
            EV([C("GroupExists", SAVE, slot_key("RanuraElegida", "Escena"))], [sv("Ejecutar", q("Cargar"))]),
            EV([C("GroupExists", SAVE, slot_key("RanuraElegida", "Escena"), inv=True)], [], [
                EV([objv_n("TextoRanura", "Numero", "RanuraElegida")], [
                    txt("TextoRanura", '"Partida " + ToString(TextoRanura.Numero) + NewLine() + "Vacía: usa Nueva partida"')])]),
        ]),
        COM("Nueva: si la ranura ya tiene una partida se pide un segundo clic para sobrescribirla"),
        EV([isv("Modo", q("Nueva"))], [], [
            EV([C("GroupExists", SAVE, slot_key("RanuraElegida", "Escena"), inv=True)], [sv("Ejecutar", q("Nueva"))]),
            EV([C("GroupExists", SAVE, slot_key("RanuraElegida", "Escena")), inv_("Confirmar", "RanuraElegida")], [sv("Ejecutar", q("Nueva"))]),
            EV([C("GroupExists", SAVE, slot_key("RanuraElegida", "Escena")), inv_("Confirmar", "RanuraElegida", "!=")], [
                nv("Confirmar", "RanuraElegida")], [
                EV([objv_n("TextoRanura", "Numero", "RanuraElegida")], [
                    txt("TextoRanura", '"¿Sobrescribir la partida " + ToString(TextoRanura.Numero) + "?" + NewLine() + "Haz clic otra vez para confirmar"')])]),
        ]),
    ]),
]))

# --- small UI buttons (back, volume, fullscreen, quit) ---
E.append(COM("BOTONES PEQUEÑOS de las pantallas de partidas y ajustes"))
E.append(EV([objv_s("BotonUI", "Pantalla", "Pantalla"), cursor("BotonUI")], [anim("BotonUI", 'BotonUI.Tipo + "Hover"')], [
    EV([objv_b("BotonUI", "Hover", "False")], [set_objv_b("BotonUI", "Hover", "True"), snd("Menu/Hover.wav", 35)])]))
E.append(EV([cursor("BotonUI", inv=True)], [anim("BotonUI", 'BotonUI.Tipo + "Normal"'), set_objv_b("BotonUI", "Hover", "False")]))
E.append(EV([objv_s("BotonUI", "Pantalla", "Pantalla"), cursor("BotonUI"), released()], [snd("Menu/Click.wav", 70)], [
    EV([objv_s("BotonUI", "Accion", q("Atras"))], ir_a("Principal", 135)),
    EV([objv_s("BotonUI", "Accion", q("Salir"))], [A("Quit", "")]),
    EV([objv_s("BotonUI", "Accion", q("VolMenos"))], [A("SetGlobalVolume", "", "-", "10")], [
        EV([C("GlobalVolume", "", "<", "0")], [A("SetGlobalVolume", "", "=", "0")])]),
    EV([objv_s("BotonUI", "Accion", q("VolMas"))], [A("SetGlobalVolume", "", "+", "10")], [
        EV([C("GlobalVolume", "", ">", "100")], [A("SetGlobalVolume", "", "=", "100")])]),
    EV([objv_s("BotonUI", "Accion", q("VolMenos"))], [A("EcrireFichierExp", AJUSTES, q("Volumen"), "GlobalVolume()")]),
    EV([objv_s("BotonUI", "Accion", q("VolMas"))], [A("EcrireFichierExp", AJUSTES, q("Volumen"), "GlobalVolume()")]),
    EV([objv_s("BotonUI", "Accion", q("Pantalla"))], [], [
        EV([C("IsFullScreen", "")], [A("SetBooleanVariable", "TempBool", "True", "")]),
        EV([C("IsFullScreen", "", inv=True)], [A("SetBooleanVariable", "TempBool", "False", "")]),
        EV([C("BooleanVariable", "TempBool", "True", "")], [A("SetFullScreen", "", "no", "")]),
        EV([C("BooleanVariable", "TempBool", "False", "")], [A("SetFullScreen", "", "yes", "")]),
    ]),
]))
E.append(EV([C("KeyFromTextReleased", "", q("Escape")), isv("Pantalla", q("Partidas"))], ir_a("Principal", 135)))
E.append(EV([C("KeyFromTextReleased", "", q("Escape")), isv("Pantalla", q("Ajustes"))], ir_a("Principal", 135)))
E.append(COM("Textos que cambian en Ajustes y centrado de las etiquetas sobre sus botones"))
E.append(EV([objv_s("TextoUI", "Clave", q("Volumen"))], [txt("TextoUI", '"Volumen general: " + ToString(round(GlobalVolume())) + "%"')]))
E.append(EV([objv_s("TextoUI", "Clave", q("Completa")), C("IsFullScreen", "")], [txt("TextoUI", q("Pantalla completa: Sí"))]))
E.append(EV([objv_s("TextoUI", "Clave", q("Completa")), C("IsFullScreen", "", inv=True)], [txt("TextoUI", q("Pantalla completa: No"))]))
E.append(EV([objv_n("TextoUI", "CX", "0", ">")], [A("SetCenterX", "TextoUI", "=", "TextoUI.CX"), A("SetCenterY", "TextoUI", "=", "TextoUI.CY - 1")]))

# --- start / load ---
def salir_a(escena_expr):
    return [A("PlaySound", "", "Menu/Click.wav", "no", "0", "1"),
            tw_op("Fundido", "Oscurecer", 255, "easeInQuad", 0.6), A("Wait", "0.7"), A("Scene", "", escena_expr, "")]
E.append(COM("NUEVA PARTIDA: valores iniciales, la ranura queda elegida y se guarda al entrar al Nivel 01"))
E.append(EV([isv("Ejecutar", q("Nueva")), ONCE()], [
    sv("Pantalla", q("Saliendo")), *reset_actions,
    nv("RanuraActual", "RanuraElegida"), sv("EscenaAGuardar", q("Nivel 01")),
    *salir_a(q("Nivel 01"))]))
E.append(COM("CARGAR PARTIDA: lee la ranura y lleva al jugador a la zona y posicion donde guardo"))
load = [sv("Pantalla", q("Saliendo"))]
LOAD_EVS = [EV([C("GroupExists", SAVE, slot_key("RanuraElegida", k))], [
    A("ReadStringFromStorage", SAVE, slot_key("RanuraElegida", k), "", "TempTexto"),
    A("JSONToGlobalVariableStructure", "TempTexto", k)]) for k in GUARDADAS]
load += [A("ReadStringFromStorage", SAVE, slot_key("RanuraElegida", "Vida"), "", "TempTexto"), nv("Vida", "ToNumber(TempTexto)"),
         A("ReadStringFromStorage", SAVE, slot_key("RanuraElegida", "Escena"), "", "EscenaCargar"),
         nv("RanuraActual", "RanuraElegida"), sv("EscenaAGuardar", q(""))]
E.append(EV([isv("Ejecutar", q("Cargar")), ONCE()], [sv("Pantalla", q("Saliendo"))], [
    COM("Solo se lee lo que exista en la ranura (las partidas viejas no tienen Mochila)"), *LOAD_EVS,
    EV([], load[1:] + salir_a("EscenaCargar"))]))

menu = next(l for l in d["layouts"] if l["name"] == "Menu Principal")
menu["objects"] = objects
menu["instances"] = instances
menu["layers"] = layers
menu["events"] = E
menu["objectsGroups"] = []
menu["variables"] = [var("Pantalla", "string", "Intro"), var("Modo", "string", ""), var("Ejecutar", "string", ""),
                     var("Confirmar", "number", 0), var("RanuraElegida", "number", 0), var("TempTexto", "string", ""),
                     var("TempTexto2", "string", ""), var("TempNumero", "number", 0), var("TempBool", "boolean", False),
                     var("EscenaCargar", "string", "")]
menu["objectsFolderStructure"] = {"folderName": "__ROOT", "children": [{"objectName": o["name"]} for o in objects]}

# ---------- globals ----------
gnames = {v["name"] for v in d["variables"]}
if "RanuraActual" not in gnames: d["variables"].append(var("RanuraActual", "number", 1))
if "EscenaAGuardar" not in gnames: d["variables"].append(var("EscenaAGuardar", "string", ""))
if not any(o["name"] == "AvisoGuardado" for o in d["objects"]):
    d["objects"].append(text_obj("AvisoGuardado", "Partida guardada", 12, (214, 255, 106), (36, 21, 13), tween=True))
    d["objectsFolderStructure"]["children"].append({"objectName": "AvisoGuardado"})

# ---------- in-game saving: external events "Guardado" ----------
def guardar(key, expr): return A("EcrireFichierTxt", SAVE, slot_key("RanuraActual", key), expr)
hora_vars = [var("OHora", "string", ""), var("OMin", "string", ""), var("Zona", "string", "")]
G_EV = [
    COM("GUARDADO DE PARTIDA (incluido al final del evento externo Personaje, asi funciona en todos los niveles).\n"
        "Tecla G = guardar aqui mismo. Al cambiar de zona se guarda solo (EscenaAGuardar lo pone el teletransportador)."),
    EV([C("KeyFromTextReleased", "", q("g")), inv_("RanuraActual", "1", ">="), isv("EscenaAGuardar", q(""))], [
        nv("Posicion_Inicial_Jugador.X", "Personaje_jugador.X()"), nv("Posicion_Inicial_Jugador.Y", "Personaje_jugador.Y()"),
        nv("Vida", "Personaje_jugador.Vida"), sv("EscenaAGuardar", "CurrentSceneName()")], [
        EV([], [A("Create", "", "AvisoGuardado", "CameraCenterX(\"Inventario\") - 48", "CameraCenterY(\"Inventario\") - 112", q("Inventario")),
                A("SetZOrder", "AvisoGuardado", "=", "10000"),
                tw_op("AvisoGuardado", "Desaparecer", 0, "easeInQuart", 2.5, "yes"),
                snd("Menu/Guardado.wav", 60)])]),
    EV([isv("EscenaAGuardar", q(""), "!="), inv_("RanuraActual", "1", ">=")], [], [
        EV([inv_("Reloj.Hora", "10", "<")], [sv("OHora", '"0" + ToString(Reloj.Hora)')]),
        EV([inv_("Reloj.Hora", "10", ">=")], [sv("OHora", "ToString(Reloj.Hora)")]),
        EV([inv_("Reloj.Minuto", "10", "<")], [sv("OMin", '"0" + ToString(Reloj.Minuto)')]),
        EV([inv_("Reloj.Minuto", "10", ">=")], [sv("OMin", "ToString(Reloj.Minuto)")]),
        EV([], [sv("Zona", "EscenaAGuardar")]),
        EV([isv("EscenaAGuardar", q("Nivel 01"))], [sv("Zona", q("La granja"))]),
        EV([isv("EscenaAGuardar", q("Nivel 02"))], [sv("Zona", q("El bosque"))]),
        EV([isv("EscenaAGuardar", q("Pueblo"))], [sv("Zona", q("El pueblo"))]),
        EV([], [guardar("Escena", "EscenaAGuardar"),
                guardar("Zona", "Zona"),
                guardar("Detalle", 'NombresEstacion[Calendario.Estacion] + " " + ToString(Calendario.Dia) + "   " + OHora + ":" + OMin + " " + Reloj.M + "   Nv " + ToString(NivelJugador) + "   " + ToString(Monedas) + " monedas"'),
                guardar("Vida", "ToString(Vida)"),
                *[guardar(k, "ToJSON(" + k + ")") for k in GUARDADAS],
                sv("EscenaAGuardar", q(""))]),
    ], variables=hora_vars),
]
ext = next((e for e in d["externalEvents"] if e["name"] == "Guardado"), None)
if ext is None:
    ext = {"associatedLayout": "Nivel 01", "name": "Guardado", "events": []}
    d["externalEvents"].append(ext)
ext["events"] = G_EV

pers = next(e for e in d["externalEvents"] if e["name"] == "Personaje")
if not any(e.get("type") == "BuiltinCommonInstructions::Link" and e.get("target") == "Guardado" for e in pers["events"]):
    pers["events"].append(LINK("Guardado"))
# autosave when changing zone: the teleporter tells which scene to save
def fix_teleport(evs):
    for e in evs:
        acts = e.get("actions") or []
        if any(a["type"]["value"] == "Scene" and "Teletransportador.Direccion" in a["parameters"][1] for a in acts):
            if not any(a["type"]["value"] == "SetStringVariable" and a["parameters"][0] == "EscenaAGuardar" for a in acts):
                i = next(k for k, a in enumerate(acts) if a["type"]["value"] == "Scene")
                acts.insert(i, sv("EscenaAGuardar", "Teletransportador.Direccion"))
            return True
        if fix_teleport(e.get("events") or []): return True
    return False
assert fix_teleport(pers["events"]), "teleport event not found"

json.dump(d, open(PROJ, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok", len(E), "eventos en el menu,", len(instances), "instancias")
