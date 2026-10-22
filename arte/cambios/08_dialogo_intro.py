"""Caja de dialogo estilo Stardew + introduccion de la historia de Papayork.

DIALOGO (eventos externos "Dialogo", objetos en la capa "DialogoHD" sin zoom para que el texto sea nitido):
- Para hablar: SetStringVariable(DialogoPedido, "Clave") y, si debe pausar el mundo, DialogoPausa = true.
- Dialogos[Clave] = lista de {Quien, Texto}. Quien = Pedro, Hetol, Chuchini, ChuchiniViejo, Rosa, Fermin o Narrador.
- El texto aparece letra por letra; clic / Espacio / Enter completa la frase o pasa a la siguiente.
- Al terminar queda DialogoTerminado = Clave (asi Rosa y Fermin abren su tienda despues de saludar).

INTRO (escena "Intro"): 1847, HetolMimiao y sus hijos en el valle dorado; el reactor explota; la familia huye;
anos despues Chuchini Gutierrez vuelve, tiene a Pedro y le deja la granja; la radiacion vuelve. Esc o el boton
"Saltar" van directo a la granja. "Nueva partida" ahora pasa por la intro.
"""
import json, sys, os, copy
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
def linea(quien, texto): return {"type": "structure", "children": [var("Quien", "string", quien), var("Texto", "string", texto)]}

# ---------- textos ----------
N = "Narrador"
DIALOGOS = {
    "Intro1": [(N, "Valle de Papayork, año 1847. La tierra más fértil que nadie había visto jamás."),
               ("Hetol", "¡Miren estas papas! ¡Grandes, doradas y perfectas, como un regalo del cielo!"),
               (N, "HetolMimiao, el tatarabuelo de Pedro, amaba las papas más que a nada en el mundo..."),
               (N, "...tanto, que bautizó sus tierras con el nombre que el valle nunca olvidaría: PAPAYORK.")],
    "Intro2": [(N, "Allí crió a sus hijos, entre cosechas doradas y tardes de sol."),
               ("Hetol", "Algún día todo esto será de ustedes, hijos míos. Y de los hijos de sus hijos.")],
    "Intro3": [(N, "Pero al otro lado del valle, unos hombres de ciudad levantaron un extraño reactor..."),
               (N, "...y una tarde de verano, el cielo se volvió verde.")],
    "Intro4": [("Hetol", "¡¿Qué fue eso?! ¡Niños, a la carreta! ¡Nos vamos de aquí!"),
               (N, "La radiación lo cubrió todo. La familia tuvo que abandonar Papayork... para siempre, o eso creyeron.")],
    "Intro5": [(N, "Generaciones más tarde, un descendiente de HetolMimiao regresó a las tierras de la familia."),
               ("Chuchini", "¡Chuchini Gutiérrez, para servirle! Y mire nomás... ni rastro de radiación."),
               ("Chuchini", "¡Esta tierra está mejor que nunca! Aquí me quedo.")],
    "Intro6": [(N, "Sembró, trabajó de sol a sol... y tuvo un hijo al que llamó Pedro.")],
    "Intro7": [(N, "Los años pasaron. Cuando llegó su momento, Chuchini le dejó la granja a su hijo."),
               ("ChuchiniViejo", "Pedro, esta tierra es el legado de HetolMimiao. Cuídala como él lo hubiera hecho."),
               ("Pedro", "Lo haré, papá. Te lo prometo.")],
    "Intro8": [("Pedro", "¿Qué... qué es ese brillo verde en la tierra?"),
               (N, "La radiación había vuelto. Y con ella... las papas radiactivas."),
               (N, "Ahora Pedro deberá luchar para proteger el legado de Papayork.")],
    "Bienvenida": [("Pedro", "Bueno... aquí estoy. La granja de la familia."),
                   ("Pedro", "Papá decía que esta tierra era especial. Ojalá tuviera razón."),
                   ("Pedro", "Primero, a buscar mis herramientas. Deben estar tiradas por la granja.")],
    "Mercado": [("Rosa", "¡Hola, Pedro! Qué gusto verte por el pueblo."),
                ("Rosa", "Tengo semillas frescas y te compro todo lo que coseches. ¡Pasa, pasa!")],
    "Herreria": [("Fermin", "¡Pedro! ¿Vienes por una mejora?"),
                 ("Fermin", "Tráeme lingotes y monedas, y te forjo herramientas que no le temen a ninguna papa.")],
}
NOMBRES = {"Pedro": "Pedro", "Hetol": "HetolMimiao", "Chuchini": "Chuchini Gutiérrez", "ChuchiniViejo": "Chuchini Gutiérrez",
           "Rosa": "Doña Rosa", "Fermin": "Don Fermín", N: ""}
set_global_var(d, struct("Dialogos", [{"name": k, "type": "array", "children": [linea(q_, t) for q_, t in v]} for k, v in DIALOGOS.items()]))
set_global_var(d, struct("NombresPersonajes", [var(k, "string", v) for k, v in NOMBRES.items()]))
for v in [var("DialogoPedido", "string", ""), var("DialogoActual", "string", ""), var("DialogoTerminado", "string", ""),
          var("DialogoLinea", "number", 0), var("DialogoLetras", "number", 0), var("DialogoAbierto", "boolean", False),
          var("DialogoPausa", "boolean", False)]:
    set_global_var(d, v)
est = next(v for v in d["variables"] if v["name"] == "Estadisticas")
if not any(c["name"] == "Bienvenida" for c in est["children"]): est["children"].append(var("Bienvenida", "number", 0))

# ---------- recursos ----------
IMG = ["Valle", "ValleRadiactivo", "ValleVerde", "Atardecer", "GranjaNoche", "Reactor", "Carreta", "Blanco",
       "CajaTextoHD", "CajaRetratoHD", "FlechaHD", "Hetol", "Hija", "Hijo", "Chuchini", "ChuchiniViejo"] + \
      ["Explosion%d" % i for i in range(1, 9)] + ["Retrato%sHD" % r for r in ("Pedro", "Hetol", "Chuchini", "ChuchiniViejo", "Rosa", "Fermin")]
for f in IMG: add_resource(d, "image", "Intro/" + f + ".png", "Intro/" + f + ".png")
for f in ("Explosion", "Letra"): add_resource(d, "audio", "Intro/" + f + ".wav", "Intro/" + f + ".wav")

# ---------- objetos globales del dialogo ----------
for o in [
    sprite_obj("CajaTexto", [anim_def("", [frame("Intro/CajaTextoHD.png")])], tween=False),
    sprite_obj("CajaRetrato", [anim_def("", [frame("Intro/CajaRetratoHD.png")])], tween=False),
    sprite_obj("Retrato", [anim_def(r, [frame("Intro/Retrato%sHD.png" % r)]) for r in ("Pedro", "Hetol", "Chuchini", "ChuchiniViejo", "Rosa", "Fermin")], tween=False),
    sprite_obj("FlechaDialogo", [anim_def("", [frame("Intro/FlechaHD.png")])], [var("BaseY", "number", 0)], tween=False),
    text_obj("NombreDialogo", "", 20, (255, 246, 210), (60, 30, 12)),
    text_obj("TextoDialogo", "", 22, (60, 34, 18), None),
]:
    set_global_object(d, o)
CAPA = "DialogoHD"
dui = next((x for x in d["externalLayouts"] if x["name"] == "DialogoUI"), None)
if dui is None:
    dui = copy.deepcopy(next(x for x in d["externalLayouts"] if x["name"] == "InventarioStardew")); dui["name"] = "DialogoUI"
    d["externalLayouts"].append(dui)
dui["instances"] = [inst("CajaTexto", 40, 376, CAPA, 1), inst("CajaRetrato", 712, 346, CAPA, 1), inst("Retrato", 750, 362, CAPA, 2),
                    inst("NombreDialogo", 760, 498, CAPA, 3), inst("TextoDialogo", 72, 404, CAPA, 3),
                    inst("FlechaDialogo", 648, 500, CAPA, 4, variables=[var("BaseY", "number", 500)])]
DOBJ = ["CajaTexto", "CajaRetrato", "Retrato", "NombreDialogo", "TextoDialogo", "FlechaDialogo"]

# ---------- eventos del dialogo ----------
LIN = "Dialogos[DialogoActual][DialogoLinea]"
E = [COM("CAJA DE DIALOGO (estilo Stardew)\nPara hablar: DialogoPedido = clave de Dialogos (y DialogoPausa = true para pausar el mundo).\n"
         "Al terminar, DialogoTerminado = clave.")]
E.append(EV([C("SceneJustBegins", "")], [bv("DialogoAbierto", "False"), sv("DialogoPedido", '""'), *[hide(o) for o in DOBJ],
                                         A("TextObject::SetWrapping", "TextoDialogo", "yes"), A("TextObject::WrappingWidth", "TextoDialogo", "=", "610"),
                                         A("ResetTimer", "", q("Bienvenida"))]))
E.append(COM("Primera vez en la granja: Pedro piensa en voz alta"))
E.append(EV([C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "=", q("Nivel 01")),
             inv_("Estadisticas.Bienvenida", "0"), C("CompareTimer", "", q("Bienvenida"), ">", "1.2"), ibv("DialogoAbierto", "False")], [
    nv("Estadisticas.Bienvenida", "1"), sv("DialogoPedido", q("Bienvenida")), bv("DialogoPausa", "True")]))
E.append(COM("Abrir un dialogo pedido"))
E.append(EV([isv("DialogoPedido", '""', "!="), ibv("DialogoAbierto", "False")], [
    sv("DialogoActual", "DialogoPedido"), sv("DialogoPedido", '""'), nv("DialogoLinea", "0"), nv("DialogoLetras", "0"),
    bv("DialogoAbierto", "True"), sv("DialogoTerminado", '""'), A("ResetTimer", "", q("Dialogo")),
    show("CajaTexto"), show("TextoDialogo"), snd("Menu/Hover.wav", 40)], [
    EV([ibv("DialogoPausa", "True")], [bv("InventarioAbierto", "True"), A("ChangeLayerTimeScale", "", q(""), "0"),
                                      A("PauseTimer", "", q("PasoTiempo"))])]))
E.append(COM("Mostrar la linea actual: texto letra por letra, retrato y nombre"))
E.append(EV([ibv("DialogoAbierto", "True")], [
    sv("Quien", LIN + ".Quien"), sv("Frase", LIN + ".Texto"), nv("DialogoLetras", "min(StrLength(Frase), DialogoLetras + 45 * TimeDelta())"),
    txt("TextoDialogo", "SubStr(Frase, 0, floor(DialogoLetras))"), hide("FlechaDialogo")], [
    EV([isv("Quien", q(N))], [hide("CajaRetrato"), hide("Retrato"), hide("NombreDialogo")]),
    EV([isv("Quien", q(N), "!=")], [show("CajaRetrato"), show("Retrato"), show("NombreDialogo"), anim("Retrato", "Quien"),
                                   txt("NombreDialogo", "NombresPersonajes[Quien]"), A("SetCenterX", "NombreDialogo", "=", "816")]),
    EV([cmp("DialogoLetras", ">=", "StrLength(Frase)")], [show("FlechaDialogo"),
                                                          A("SetY", "FlechaDialogo", "=", "FlechaDialogo.BaseY + sin(TimeFromStart() * 8) * 3")]),
    COM("Pasar: clic, Espacio o Enter. La primera vez completa la frase; la segunda pasa a la siguiente"),
    EV([C("CompareTimer", "", q("Dialogo"), ">", "0.25")], [bv("Pasar", "False")], [
        EV([released()], [bv("Pasar", "True")]), EV([key_released("Space")], [bv("Pasar", "True")]),
        EV([key_released("Return")], [bv("Pasar", "True")]),
        EV([ibv("Pasar", "True")], [A("ResetTimer", "", q("Dialogo"))], [
            EV([cmp("DialogoLetras", "<", "StrLength(Frase)")], [nv("DialogoLetras", "StrLength(Frase)"), bv("Pasar", "False")]),
            EV([ibv("Pasar", "True")], [nv("DialogoLinea", "1", "+"), nv("DialogoLetras", "0"), snd("Intro/Letra.wav", 50)], [
                EV([cmp("DialogoLinea", ">=", "VariableChildCount(Dialogos[DialogoActual])")], [
                    bv("DialogoAbierto", "False"), sv("DialogoTerminado", "DialogoActual"), *[hide(o) for o in DOBJ]], [
                    EV([ibv("DialogoPausa", "True")], [bv("DialogoPausa", "False"), bv("InventarioAbierto", "False"),
                                                      A("ChangeLayerTimeScale", "", q(""), "1"), A("UnPauseTimer", "", q("PasoTiempo"))])])])])],
        variables=[var("Pasar", "boolean", False)])],
    variables=[var("Quien", "string", ""), var("Frase", "string", "")]))
external_events(d, "Dialogo", E)

# ---------- niveles: capa DialogoHD, crear la caja al empezar y enlazar los eventos ----------
pers = ext("Personaje")
for lay in d["layouts"]:
    if lay["name"] in ("Nivel 01", "Nivel 02", "Pueblo") and not any(l["name"] == CAPA for l in lay["layers"]):
        nueva = copy.deepcopy(next(l for l in lay["layers"] if l["name"] == "UIHD")); nueva["name"] = CAPA
        lay["layers"].append(nueva)
inicio = next(e for e in pers["events"] if any(c["type"]["value"] == "SceneJustBegins" for c in e.get("conditions") or []))
if not any(a["type"]["value"] == "BuiltinExternalLayouts::CreateObjectsFromExternalLayout" and a["parameters"][1] == q("DialogoUI") for a in inicio["actions"]):
    inicio["actions"].append(A("BuiltinExternalLayouts::CreateObjectsFromExternalLayout", "", q("DialogoUI"), "", "", ""))
if not any(e.get("target") == "Dialogo" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("Dialogo"))
# con un dialogo abierto no se abre la mochila
for e in recorrer(ext("Inventario")["events"]):
    conds = e.get("conditions") or []
    if any(c["parameters"][:2] == ["TiendaAbierta", "False"] for c in conds) and not any(c["parameters"][:1] == ["DialogoAbierto"] for c in conds):
        conds.append(ibv("DialogoAbierto", "False"))

# ---------- Rosa y Fermin saludan antes de abrir su tienda ----------
tienda = ext("Tienda")
abrir = next(e for e in tienda["events"] if any(c["type"]["value"] == "IsCursorOnObject" and c["parameters"][0] == "NPC" for c in e.get("conditions") or []))
if not any(a["parameters"][:1] == ["DialogoPedido"] for a in abrir["actions"]):
    acciones = [a for a in abrir["actions"] if a["parameters"][:1] != ["TipoTienda"]]
    subs = abrir.get("events", [])
    abrir["actions"] = [sv("TipoTienda", "NPC.Tienda"), sv("DialogoPedido", "NPC.Tienda"), bv("DialogoPausa", "True")]
    abrir["events"] = []
    i = tienda["events"].index(abrir)
    tienda["events"].insert(i + 1, EV([isv("DialogoTerminado", "TipoTienda"), ibv("TiendaAbierta", "False"), ibv("DialogoAbierto", "False")],
                                      acciones + [sv("DialogoTerminado", '""')], subs))

# ---------- escena Intro ----------
menu = next(l for l in d["layouts"] if l["name"] == "Menu Principal")
d["layouts"] = [l for l in d["layouts"] if l["name"] != "Intro"]
base_layer = copy.deepcopy(menu["layers"][0])
def capa(nombre):
    L = copy.deepcopy(base_layer); L["name"] = nombre; L["effects"] = []; return L
ACTORES = {"Hetol": "Intro/Hetol.png", "Hija": "Intro/Hija.png", "Hijo": "Intro/Hijo.png", "Chuchini": "Intro/Chuchini.png",
           "ChuchiniViejo": "Intro/ChuchiniViejo.png", "Pedro": "NewSprite"}
objetos = [
    sprite_obj("FondoIntro", [anim_def(n, [frame("Intro/%s.png" % n)]) for n in ("Valle", "ValleRadiactivo", "ValleVerde", "Atardecer", "GranjaNoche")]),
    sprite_obj("Actor", [anim_def(n, [frame(img)]) for n, img in ACTORES.items()], [var("Quien", "string", ""), var("BaseY", "number", 0)]),
    sprite_obj("ReactorIntro", [anim_def("", [frame("Intro/Reactor.png")])]),
    sprite_obj("Explosion", [anim_def("", [frame("Intro/Explosion%d.png" % i) for i in range(1, 9)], dt=0.13)]),
    sprite_obj("Carreta", [anim_def("", [frame("Intro/Carreta.png")])]),
    sprite_obj("Destello", [anim_def("", [frame("Intro/Blanco.png")])]),
    sprite_obj("Telon", [anim_def("", [frame("Menu/Negro.png")])]),
    sprite_obj("LogoIntro", [anim_def("", [frame("Menu/LogoPapayork.png")])]),
    sprite_obj("EsporaIntro", [anim_def("", [frame("Menu/Espora.png", (1, 1))])]),
    text_obj("TextoCapitulo", "", 36, (255, 246, 210), (36, 21, 13), tween=True),
    text_obj("BotonSaltar", "Saltar intro  (Esc)", 18, (255, 246, 210), (36, 21, 13)),
]
instancias = [inst("FondoIntro", 0, 0, "", 0), inst("Telon", -20, -20, "Efectos", 100, 520, 310), inst("Destello", -20, -20, "Efectos", 90, 520, 310),
              inst("TextoCapitulo", 0, 250, "DialogoHD", 10), inst("BotonSaltar", 760, 14, "DialogoHD", 10)]

def act(nombre, x, y, escala=2):
    return [A("Create", "", "Actor", str(x), str(y), q("")), anim("Actor", q(nombre)), set_objv_s("Actor", "Quien", q(nombre)),
            A("ScalableCapability::ScalableBehavior::SetValue", "Actor", "Scale", "=", str(escala)), set_objv_n("Actor", "BaseY", str(y)),
            A("SetZOrder", "Actor", "=", str(y))]
def quien(n): return objv_s("Actor", "Quien", q(n))
def capitulo(texto): return [txt("TextoCapitulo", q(texto)), A("SetCenterX", "TextoCapitulo", "=", "480"), opacity("TextoCapitulo", 0),
                             tw_op("TextoCapitulo", "Mostrar", 255, "easeOutQuad", 1.2)]
def telon(to, dur): return tw_op("Telon", "Fundido", to, "easeInOutQuad", dur)
def paso(n, acciones, subs=()):
    return EV([inv_("Paso", str(n)), ONCE()], [A("ResetTimer", "", q("Paso"))] + acciones, list(subs))
def en(n, t, acciones, subs=()): return EV([inv_("Paso", str(n)), C("CompareTimer", "", q("Paso"), ">=", str(t)), ONCE()], acciones, list(subs))
def solo(*acciones): return EV([], list(acciones))   # cada personaje en su propio sub-evento (si no, Create acumula instancias)
def tras_dialogo(n, clave): return EV([inv_("Paso", str(n)), isv("DialogoTerminado", q(clave))], [sv("DialogoTerminado", '""'), nv("Paso", str(n + 1))])
def hablar(clave): return [sv("DialogoPedido", q(clave)), bv("DialogoPausa", "False")]

IE = [COM("INTRODUCCION. Paso = momento de la historia; cada paso arranca una vez (Once) y avanza por tiempo o al terminar su dialogo."),
      EV([C("SceneJustBegins", "")], [
          *[A("ZoomCamera", "", "2", q(c), "0") for c in ("", "Efectos")],
          *[a for c in ("", "Efectos") for a in (A("SetCameraCenterX", "", "=", "240", q(c), "0"), A("SetCameraCenterY", "", "=", "135", q(c), "0"))],
          A("BuiltinExternalLayouts::CreateObjectsFromExternalLayout", "", q("DialogoUI"), "", "", ""),
          nv("Paso", "0"), opacity("Telon", 255), opacity("Destello", 0), anim("FondoIntro", q("Valle")),
          A("PlayMusic", "", "Stardew Valley OST - Stardew Valley Overture.mp3", "yes", "70", "1"),
          sv("MusicaActual", q("Stardew Valley OST - Stardew Valley Overture.mp3")), bv("Esporas", "False")]),
      LINK("Dialogo"),
      COM("Los actores respiran (suben y bajan un poquito)"),
      FOREACH("Actor", [], [A("SetY", "Actor", "=", "Actor.BaseY + sin(TimeFromStart() * 5 + Actor.X() * 0.1) * 1.5")]),
      COM("1847: el valle dorado"),
      paso(0, capitulo("Valle de Papayork, 1847")),
      en(0, 3.4, [tw_op("TextoCapitulo", "Ocultar", 0, "easeInQuad", 0.8), nv("Paso", "1")]),
      paso(1, [telon(0, 1.5), *act("Hetol", 200, 108), A("Tween::TweenCameraPosition2", "", q("Paneo"), "252", "135", q(""), q("linear"), "25")]),
      en(1, 1.6, hablar("Intro1")), tras_dialogo(1, "Intro1"),
      paso(2, [], [solo(*act("Hija", 520, 124, 1.5), A("Tween::TweenBehavior::AddObjectPositionXTween2", "Actor", "Tween", q("Llegar"), "286", q("easeOutQuad"), "2.2", "no")),
                   solo(*act("Hijo", 560, 128, 1.5), A("Tween::TweenBehavior::AddObjectPositionXTween2", "Actor", "Tween", q("Llegar"), "322", q("easeOutQuad"), "2.6", "no"))]),
      en(2, 2.4, hablar("Intro2")), tras_dialogo(2, "Intro2"),
      COM("El reactor aparece... y explota"),
      paso(3, [A("Create", "", "ReactorIntro", "392", "86", q("")), opacity("ReactorIntro", 0), A("SetZOrder", "ReactorIntro", "=", "5"),
               tw_op("ReactorIntro", "Aparecer", 255, "easeInQuad", 1.5)]),
      en(3, 1.2, hablar("Intro3")), tras_dialogo(3, "Intro3"),
      paso(4, [A("Create", "", "Explosion", "354", "-4", q("")), A("SetZOrder", "Explosion", "=", "6"), snd("Intro/Explosion.wav", 100)]),
      en(4, 0.45, [opacity("Destello", 255), tw_op("Destello", "Apagar", 0, "easeInQuad", 2.4), anim("FondoIntro", q("ValleRadiactivo")),
                   A("Delete", "ReactorIntro", ""), A("ChangeColor", "Actor", q("190;255;160")), bv("Esporas", "True")]),
      EV([inv_("Paso", "4"), C("CompareTimer", "", q("Paso"), ">=", "0.45"), C("CompareTimer", "", q("Paso"), "<", "2.2")], [
          A("SetCameraCenterX", "", "=", "246 + RandomInRange(-5, 5)", q(""), "0"), A("SetCameraCenterY", "", "=", "135 + RandomInRange(-4, 4)", q(""), "0")]),
      en(4, 2.2, [A("SetCameraCenterY", "", "=", "135", q(""), "0")]),
      en(4, 2.6, hablar("Intro4")), tras_dialogo(4, "Intro4"),
      COM("La familia huye en la carreta"),
      paso(5, [A("Delete", "Explosion", ""), A("Create", "", "Carreta", "300", "108", q("")),
               A("ScalableCapability::ScalableBehavior::SetValue", "Carreta", "Scale", "=", "2"), A("SetZOrder", "Carreta", "=", "200"),
               A("Tween::TweenBehavior::AddObjectPositionXTween2", "Carreta", "Tween", q("Huir"), "-180", q("easeInQuad"), "4.5", "no")], [
          EV([quien("Hetol")], [A("Tween::TweenBehavior::AddObjectPositionXTween2", "Actor", "Tween", q("Huir"), "-120", q("easeInQuad"), "4.2", "no")]),
          EV([quien("Hija")], [A("Delete", "Actor", "")]), EV([quien("Hijo")], [A("Delete", "Actor", "")])]),
      en(5, 3.2, [telon(255, 1.2)]),
      en(5, 4.6, [A("Delete", "Actor", ""), A("Delete", "Carreta", ""), bv("Esporas", "False"), nv("Paso", "6")]),
      COM("Anos despues: Chuchini Gutierrez vuelve a la granja"),
      paso(6, [*capitulo("Aaaaños después..."), anim("FondoIntro", q("ValleVerde")), A("SetCameraCenterX", "", "=", "240", q(""), "0")]),
      en(6, 3.0, [tw_op("TextoCapitulo", "Ocultar", 0, "easeInQuad", 0.8), nv("Paso", "7")]),
      paso(7, [telon(0, 1.5), *act("Chuchini", -60, 108),
               A("Tween::TweenBehavior::AddObjectPositionXTween2", "Actor", "Tween", q("Llegar"), "190", q("easeOutQuad"), "2.6", "no")]),
      en(7, 2.7, hablar("Intro5")), tras_dialogo(7, "Intro5"),
      paso(8, [], [solo(*act("Pedro", 262, 128, 1.3), opacity("Actor", 0), tw_op("Actor", "Aparecer", 255, "easeOutQuad", 1))]),
      en(8, 1.0, hablar("Intro6")), tras_dialogo(8, "Intro6"),
      COM("Atardecer: Chuchini le deja la granja a Pedro"),
      paso(9, [telon(255, 1)]),
      en(9, 1.1, [A("Delete", "Actor", ""), anim("FondoIntro", q("Atardecer")), telon(0, 1.4)],
         [solo(*act("ChuchiniViejo", 180, 108)), solo(*act("Pedro", 262, 108))]),
      en(9, 2.6, hablar("Intro7")), tras_dialogo(9, "Intro7"),
      COM("Hoy: la radiacion vuelve"),
      paso(10, [telon(255, 1.2)]),
      en(10, 1.3, [A("Delete", "Actor", ""), anim("FondoIntro", q("GranjaNoche")), A("ChangeColor", "FondoIntro", q("150;160;230")), telon(0, 1.5)],
         [solo(*act("Pedro", 196, 108), A("ChangeColor", "Actor", q("170;180;235")))]),
      en(10, 3.2, [snd("Cultivos/Temblor.wav", 90)]),
      EV([inv_("Paso", "10"), C("CompareTimer", "", q("Paso"), ">=", "3.2"), C("CompareTimer", "", q("Paso"), "<", "4.2")], [
          A("SetCameraCenterX", "", "=", "240 + RandomInRange(-3, 3)", q(""), "0")]),
      en(10, 4.2, [A("SetCameraCenterX", "", "=", "240", q(""), "0"), A("Create", "", "PapaEmerge", "290", "108", q("")),
                   A("ScalableCapability::ScalableBehavior::SetValue", "PapaEmerge", "Scale", "=", "2"), A("SetZOrder", "PapaEmerge", "=", "160"),
                   bv("Esporas", "True")]),
      en(10, 5.4, hablar("Intro8")), tras_dialogo(10, "Intro8"),
      COM("Titulo final y a la granja"),
      paso(11, [telon(255, 1.2)]),
      en(11, 1.2, [A("Create", "", "LogoIntro", "21", "-150", "\"Efectos\""), A("SetZOrder", "LogoIntro", "=", "300"),
                   tw_y("LogoIntro", "Caer", "40", "easeOutBounce", 1.2), bv("Esporas", "False")]),
      en(11, 1.65, [snd("Menu/GolpeLogo.wav", 90)]),
      en(11, 2.4, [*capitulo("Legado Radioactivo"), A("SetY", "TextoCapitulo", "=", "380")]),
      en(11, 6.5, [tw_op("LogoIntro", "Ocultar", 0, "easeInQuad", 1), tw_op("TextoCapitulo", "Ocultar", 0, "easeInQuad", 1)]),
      en(11, 7.6, [A("Scene", "", q("Nivel 01"), "")]),
      COM("Saltar la intro: Esc o clic en el boton"),
      EV([cursor("BotonSaltar")], [color("BotonSaltar", "214;255;106")]),
      EV([cursor("BotonSaltar", inv=True)], [color("BotonSaltar", "255;246;210")]),
      EV([key_released("Escape")], [bv("Saltar", "True")]),
      EV([cursor("BotonSaltar"), released()], [bv("Saltar", "True")]),
      EV([ibv("Saltar", "True"), ONCE()], [bv("DialogoAbierto", "False"), telon(255, 0.5), A("Wait", "0.6"), A("Scene", "", q("Nivel 01"), "")]),
      COM("Esporas radiactivas"),
      EV([ibv("Esporas", "True"), C("CompareTimer", "", q("Espora"), ">=", "0.1")], [
          A("ResetTimer", "", q("Espora")), A("Create", "", "EsporaIntro", "RandomInRange(0, 480)", "280", q("")),
          A("SetZOrder", "EsporaIntro", "=", "250"), A("ScalableCapability::ScalableBehavior::SetValue", "EsporaIntro", "Scale", "=", "RandomInRange(1, 2)"),
          tw_y("EsporaIntro", "Subir", "EsporaIntro.Y() - RandomInRange(120, 260)", "easeOutSine", "RandomInRange(3, 6)", "yes"),
          tw_op("EsporaIntro", "Apagar", 0, "easeInQuad", 5)])]
intro = {k: copy.deepcopy(v) for k, v in menu.items() if k not in ("objects", "instances", "events", "layers", "variables", "objectsFolderStructure")}
intro.update({"name": "Intro", "mangledName": "Intro", "title": "", "objects": objetos, "instances": instancias, "events": IE,
              "layers": [capa(""), capa("Efectos"), capa("DialogoHD")], "objectsGroups": [],
              "variables": [var("Paso", "number", 0), var("Esporas", "boolean", False), var("Saltar", "boolean", False)],
              "objectsFolderStructure": {"folderName": "__ROOT", "children": [{"objectName": o["name"]} for o in objetos]}})
mi = next(i for i, l in enumerate(d["layouts"]) if l["name"] == "Menu Principal")
d["layouts"].insert(mi + 1, intro)

# ---------- Nueva partida pasa por la intro ----------
for e in recorrer(menu["events"]):
    if any(c["type"]["value"] == "StringVariable" and c["parameters"][:1] == ["Ejecutar"] and c["parameters"][2] == q("Nueva") for c in e.get("conditions") or []):
        for a in e["actions"]:
            if a["type"]["value"] == "Scene": a["parameters"][1] = q("Intro")

json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: dialogo + intro")
