"""Introducción nueva por capas con más historia, pantalla de desmayo nueva e ícono de la zanahoria.
La historia sigue siendo la de PapaYork; el sombrero de paja pasa de generación en generación."""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
from PIL import Image

P = sys.argv[1]
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = json.load(open(P, encoding="utf8"))
L = {l["name"]: l for l in d["layouts"]}
intro = L["Intro"]; go = L["GameOver"]
if any(o["name"] == "IntroCielo" for o in intro["objects"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}; V = {v["name"]: v for v in d["variables"]}
OI = {o["name"]: o for o in intro["objects"]}; OG = {o["name"]: o for o in go["objects"]}


def img(r):
    n = "Natural/" + r + ".png"; add_resource(d, "image", n, n); return n
def tam(r): return Image.open(os.path.join(RAIZ, "Natural", r + ".png")).size


# ---------- Zanahoria: dibujo propio en la mochila y al caer ----------
ref = O["Recursos"]["animations"][0]["directions"][0]["sprites"][0]
z = img("Objetos/Zanahoria")
O["IconoItem"]["animations"].append(anim_def("Zanahorias", [frame(z, (16, 16))]))
next(a for a in O["Recursos"]["animations"] if a["name"] == "Zanahorias")["directions"][0]["sprites"][0]["image"] = z

# ---------- Retratos nuevos ----------
RET = O["Retrato"]["animations"]
for n in ("Hetol", "Chuchini", "ChuchiniViejo"):
    next(a for a in RET if a["name"] == n)["directions"][0]["sprites"][0]["image"] = img("Retratos/" + n)
RET.append(anim_def("PedroSin", [frame(img("Retratos/PedroSin"))]))
next(v for v in V["NombresPersonajes"]["children"] if v["name"] == "Pedro")
V["NombresPersonajes"]["children"].append(var("PedroSin", "string", "Pedro"))

# ---------- Guion ----------
linea = lambda q_, t: {"type": "structure", "children": [var("Quien", "string", q_), var("Texto", "string", t)]}
GUION = {
 "Intro1": [("Narrador", "Valle de Papayork, año 1847. La tierra más fértil que nadie había visto jamás."), ("Hetol", "¡Miren estas papas! ¡Grandes, doradas y perfectas, como un regalo del cielo!"),
            ("Narrador", "HetolMimiao, el tatarabuelo de Pedro, amaba las papas más que a nada en el mundo..."), ("Narrador", "...tanto, que bautizó sus tierras con el nombre que el valle nunca olvidaría: PAPAYORK.")],
 "Intro2": [("Narrador", "Allí crió a sus hijos, entre cosechas doradas y tardes de sol."), ("Hetol", "Algún día todo esto será de ustedes, hijos míos. Y de los hijos de sus hijos."), ("Hetol", "Eso sí: el sombrero no. El sombrero es mío hasta que me entierren con él.")],
 "Intro3": [("Narrador", "Pero al otro lado del valle, unos hombres de ciudad levantaron un extraño reactor."), ("Hetol", "Prometieron luz para todos. A mí me huele a que nos van a salir caras esas velas."), ("Narrador", "Y una tarde de verano, el cielo se volvió verde.")],
 "Intro4": [("Hetol", "¡¿Qué fue eso?! ¡Niños, a la carreta! ¡Nos vamos de aquí!")],
 "Intro4b": [("Narrador", "La radiación lo cubrió todo. La familia tuvo que abandonar Papayork... para siempre, o eso creyeron."), ("Narrador", "Con las prisas, un viejo sombrero de paja se quedó colgado de un clavo.")],
 "Intro5": [("Narrador", "Generaciones más tarde, un descendiente de HetolMimiao regresó a las tierras de la familia."), ("Chuchini", "¡Chuchini Gutiérrez, para servirle! Y mire nomás... ni rastro de radiación.")],
 "Intro5b": [("Chuchini", "¿Y esto? Un sombrero viejísimo... ¡y me queda perfecto! Debe ser cosa de familia."), ("Chuchini", "¡Esta tierra está mejor que nunca! Aquí me quedo.")],
 "Intro6": [("Narrador", "Reparó la casa, levantó un granero, sembró y trabajó de sol a sol... y tuvo un hijo al que llamó Pedro.")],
 "Intro7": [("Narrador", "Los años pasaron. Cuando llegó su momento, Chuchini le dejó la granja a su hijo."), ("ChuchiniViejo", "Pedro, esta tierra es el legado de HetolMimiao. Cuídala como él lo hubiera hecho."),
            ("ChuchiniViejo", "Y toma. Este sombrero ya ha visto más cosechas que nadie en esta familia.")],
 "Intro7b": [("ChuchiniViejo", "Una cosa más. Si un día la tierra vuelve a brillar, busca en la cueva del bosque. Tu tatarabuelo dejó algo allí."), ("Pedro", "¿Brillar? Papá, ¿de qué hablas?"), ("ChuchiniViejo", "Ojalá nunca tengas que saberlo."), ("Pedro", "Lo haré, papá. Te lo prometo.")],
 "Intro8": [("Pedro", "¿Qué... qué es ese brillo verde en la tierra?")],
 "Intro8b": [("Narrador", "La radiación había vuelto. Y con ella... las papas radiactivas."), ("Pedro", "La cueva... eso dijo papá."), ("Narrador", "Ahora Pedro deberá descubrir qué dejó HetolMimiao, y luchar para proteger el legado de Papayork.")],
 "Bienvenida": [("Pedro", "Bueno... aquí estoy. La granja de la familia."), ("Pedro", "Papá decía que esta tierra era especial. Ojalá tuviera razón."), ("Pedro", "Primero, a buscar mis herramientas. Deben estar tiradas por la granja."), ("Pedro", "Y luego... tendré que averiguar cómo abrir esa cueva.")],
}
hijos = V["Dialogos"]["children"]
for k, lineas in GUION.items():
    existe = next((c for c in hijos if c["name"] == k), None)
    nuevo = {"name": k, "type": "array", "children": [linea(a, b) for a, b in lineas]}
    if existe: existe["children"] = nuevo["children"]
    else: hijos.append(nuevo)
# Tomás no pudo estar allí la noche del reactor: quien lo vio fue su abuelo
tom = next(c for c in hijos if c["name"] == "Tomas_4")
tom["children"] = [linea("Tomas", "Mi abuelo se quedó aquí la noche del reactor. Contaba que la luz se veía desde el lago."), linea("Tomas", "Tu familia se fue y la mía no. Alguien tenía que acordarse de cómo era esto antes.")]

# ---------- Objetos de la introducción ----------
FONDOS = ("Valle", "Cosecha", "Reactor", "Verde", "Huida", "Ruina", "Primavera", "Verano", "Otono", "Invierno", "Herencia", "Noche")
def capa(nombre, sufijo):
    return sprite_obj(nombre, [anim_def(f, [frame(img(f"IntroN/{f}_{sufijo}"))]) for f in FONDOS], tween=False)
for n, suf in (("IntroCielo", "Cielo"), ("IntroMontes", "Montes"), ("IntroValle", "Valle"), ("IntroFrente", "Frente")):
    intro["objects"].append(capa(n, suf))
ELENCO = ("Hetol", "Chuchini", "ChuchiniSombrero", "ChuchiniViejo", "ChuchiniViejoSin", "PedroSin", "Tomas")
def pies(r):
    return (16, 47)
anims = []
for n in ELENCO:
    anims.append(anim_def(n + "Camina", [frame(img(f"Actores/{n}_Camina{i}"), pies(0)) for i in range(1, 9)], loop=True, dt=0.09))
    anims.append(anim_def(n + "Lado", [frame(img(f"Actores/{n}_Lado{k}"), pies(0)) for k in (1, 2)], loop=True, dt=0.7))
    anims.append(anim_def(n + "Frente", [frame(img(f"Actores/{n}_Frente{k}"), pies(0)) for k in (1, 2)], loop=True, dt=0.7))
for n in ("Hija", "Hijo", "PedroNino"):
    anims.append(anim_def(n + "Frente", [frame(img(f"Actores/{n}_Frente{k}"), pies(0)) for k in (1, 2)], loop=True, dt=0.6))
anims.append(anim_def("PedroLado", [frame(img(f"Pedro2/QuietoIzquierda{k}"), pies(0)) for k in (1, 2)], loop=True, dt=0.7))
anims.append(anim_def("PedroFrente", [frame(img(f"Pedro2/QuietoAbajo{k}"), pies(0)) for k in (1, 2)], loop=True, dt=0.7))
anims.append(anim_def("PedroCamina", [frame(img(f"Pedro2/Izquierda{k}"), pies(0)) for k in range(1, 9)], loop=True, dt=0.09))
intro["objects"].append(sprite_obj("ActorN", anims, variables=[var("Quien", "string", "")]))
intro["objects"].append(sprite_obj("NubeI", [anim_def(n, [frame(img(f"IntroN/{n}"))]) for n in ("Nube1", "Nube2", "Nube3")], variables=[var("Vel", "number", 4)], tween=False))
intro["objects"].append(sprite_obj("AveI", [anim_def("N", [frame(img(f"IntroN/Ave{k}")) for k in (1, 2, 3, 2)], loop=True, dt=0.13)]))
intro["objects"].append(sprite_obj("HumoI", [anim_def("N", [frame(img(f"IntroN/Humo{k}")) for k in range(1, 5)], loop=True, dt=0.28)], tween=False))
intro["objects"].append(sprite_obj("ExplosionN", [anim_def("N", [frame(img(f"IntroN/Explosion{k}")) for k in range(1, 5)], loop=False, dt=0.28)], tween=True))
intro["objects"].append(sprite_obj("CarretaN", [anim_def("N", [frame(img(f"IntroN/Carreta{k}")) for k in (1, 2)], loop=True, dt=0.2)]))
intro["objects"].append(sprite_obj("PapaBrota", [anim_def("N", [frame(img(f"IntroN/PapaBrota{k}")) for k in range(1, 5)], loop=False, dt=0.55)], tween=False))
intro["objects"].append(sprite_obj("SombreroVuela", [anim_def("N", [frame(img("Actores/Sombrero"))])]))
intro["objects"].append(sprite_obj("CopoI", [anim_def("N", [frame(img("IntroN/Copo"))])]))
for n, z_ in (("IntroCielo", 0), ("IntroMontes", 2), ("IntroValle", 3), ("IntroFrente", 900)):
    intro["instances"].append(inst(n, 0, 0, z=z_))
intro["instances"] = [i for i in intro["instances"] if i["name"] != "FondoIntro"]
for k, (n, x, y, v) in enumerate((("Nube1", 40, 22, 4), ("Nube3", 240, 8, 2.5), ("Nube2", 400, 44, 5.5), ("Nube1", 520, 16, 3))):
    ins = inst("NubeI", x, y, z=1, variables=[var("Vel", "number", v)]); ins["numberProperties"] = [{"name": "animation", "value": ("Nube1", "Nube2", "Nube3").index(n)}]
    intro["instances"].append(ins)
for nom, v in (("Temblor", False), ("Nieve", False)):
    intro["variables"].append(var(nom, "boolean", v))
intro["variables"] += [var("PanX", "number", 0)]

# ---------- Lenguaje del guion ----------
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
pasos = []
def paso(acts=(), subs=(), t=None, dlg=None): pasos.append((list(acts), list(subs), t, dlg))
def fondo(nombre, nubes=True, tinte="255;255;255"):
    a = [anim(o, q(nombre)) for o in ("IntroCielo", "IntroMontes", "IntroValle", "IntroFrente")]
    a += [A("SetCameraCenterX", "", "=", "240", '""', "0"), A("SetCameraCenterY", "", "=", "135", '""', "0"), A("Delete", "ActorN", ""), A("Delete", "HumoI", ""), A("ChangeColor", "NubeI", q(tinte))]
    a.append(show("NubeI") if nubes else hide("NubeI"))
    return a
def abrir(s=1.2): return tw_op("Telon", "Abrir", 0, "easeOutQuad", s)
def cerrar(s=.7): return tw_op("Telon", "Cerrar", 255, "easeInQuad", s)
def titulo(t, y=250): return [txt("TextoCapitulo", q(t)), A("SetCenterX", "TextoCapitulo", "=", "480"), A("SetY", "TextoCapitulo", "=", str(y)), opacity("TextoCapitulo", 0), tw_op("TextoCapitulo", "Mostrar", 255, "easeOutQuad", 1)]
def sin_titulo(): return [tw_op("TextoCapitulo", "Ocultar", 0, "easeInQuad", .7)]
def crea(n, an, x, y=188, flip=False):
    a = [A("Create", "", "ActorN", str(x), str(y), q("")), set_objv_s("ActorN", "Quien", q(n)), anim("ActorN", q(an)), A("SetZOrder", "ActorN", "=", str(y))]
    if flip: a.append(A("FlipX", "ActorN", "yes"))
    return EV([], a)
def ac(n, acts): return EV([objv_s("ActorN", "Quien", q(n))], acts)
def anda(n, base, x, dur, der=True):
    return ac(n, [anim("ActorN", q(base + "Camina")), A("FlipX", "ActorN", "yes" if der else "no"), A("Tween::TweenBehavior::AddObjectPositionXTween2", "ActorN", "Tween", q("Mover"), str(x), q("linear"), str(dur), "no")])
def pose(n, an, der=None):
    a = [anim("ActorN", q(an))]
    if der is not None: a.append(A("FlipX", "ActorN", "yes" if der else "no"))
    return ac(n, a)
def humo(x, y, z_=4): return EV([], [A("Create", "", "HumoI", str(x), str(y), q("")), A("SetZOrder", "HumoI", "=", str(z_))])
def ave(y, dur): return EV([], [A("Create", "", "AveI", "-20", str(y), q("")), A("SetZOrder", "AveI", "=", "1"), A("Tween::TweenBehavior::AddObjectPositionXTween2", "AveI", "Tween", q("Volar"), "560", q("linear"), str(dur), "yes")])
def paneo(x, dur): return A("Tween::TweenCameraPosition2", "", q("Paneo"), str(x), "135", q(""), q("linear"), str(dur))
CHIM = (194, 30)

# I. 1847: el valle dorado
paso([*titulo("Valle de Papayork, 1847"), *fondo("Valle"), abrir(1.6), paneo(270, 16)], [humo(*CHIM), ave(40, 13), ave(52, 15), crea("Hetol", "HetolCamina", -30, flip=True)], t=2.2)
paso([*sin_titulo()], [anda("Hetol", "Hetol", 200, 3.6)], t=3.7)
paso([], [pose("Hetol", "HetolFrente")], dlg="Intro1")
paso([cerrar()], t=.8)
# II. La cosecha en familia
paso([*fondo("Cosecha", tinte="255;210;170"), abrir()], [humo(*CHIM), crea("Hetol", "HetolFrente", 232), crea("Hija", "HijaFrente", 200, 190), crea("Hijo", "HijoFrente", 264, 190)], t=1.2)
paso([], dlg="Intro2")
paso([cerrar()], t=.8)
# III. El reactor al otro lado del valle
paso([*titulo("Pasaron los años..."), *fondo("Reactor", tinte="210;205;190"), abrir()], [humo(290, 34), humo(328, 42), crea("Hetol", "HetolLado", 110, flip=True)], t=2)
paso([*sin_titulo()], dlg="Intro3")
# IV. El cielo verde
paso([A("Create", "", "ExplosionN", "232", "-22", q("")), A("SetZOrder", "ExplosionN", "=", "5"), opacity("Destello", 255), tw_op("Destello", "Pasar", 0, "easeOutQuad", 1.2), bv("Temblor", "True"), snd("Intro/Explosion.wav", 100),
      anim("IntroCielo", q("Verde")), anim("IntroMontes", q("Verde")), anim("IntroValle", q("Verde")), anim("IntroFrente", q("Verde")), A("ChangeColor", "NubeI", q("170;220;110")), bv("Esporas", "True")], t=1.5)
paso([], [pose("Hetol", "HetolFrente")], dlg="Intro4")
paso([bv("Temblor", "False"), A("SetCameraCenterX", "", "=", "240", '""', "0"), A("SetCameraCenterY", "", "=", "135", '""', "0"), cerrar()], t=.8)
# V. La huida en carreta
paso([*fondo("Huida", tinte="150;200;110"), A("Delete", "ExplosionN", ""), A("Create", "", "CarretaN", "300", "142", q("")), A("SetZOrder", "CarretaN", "=", "196"), abrir()], t=1.2)
paso([A("Tween::TweenBehavior::AddObjectPositionXTween2", "CarretaN", "Tween", q("Huir"), "-110", q("easeInQuad"), "5", "no")], dlg="Intro4b")
paso([cerrar(1)], t=1.1)
# VI. Generaciones después
paso([A("Delete", "CarretaN", ""), bv("Esporas", "False"), *titulo("Generaciones después...", 240)], t=2.4)
paso([*sin_titulo(), *fondo("Ruina", tinte="235;240;235"), abrir(1.8)], [ave(36, 17), crea("Chuchini", "ChuchiniCamina", -24, flip=True)], t=1.6)
paso([], [anda("Chuchini", "Chuchini", 158, 3.4)], t=3.5)
paso([], [pose("Chuchini", "ChuchiniFrente")], dlg="Intro5")
paso([], [anda("Chuchini", "Chuchini", 138, .5, der=False)], t=.6)
paso([], [pose("Chuchini", "ChuchiniSombreroFrente")], t=.5)
paso([], dlg="Intro5b")
paso([cerrar(1)], t=1.1)
# VII. Las estaciones de una vida
paso([*fondo("Primavera"), abrir(1)], [humo(*CHIM), crea("Chuchini", "ChuchiniSombreroLado", 300, flip=False), ave(30, 12)], dlg="Intro6")
paso([*titulo("Primavera"), cerrar(.5)], t=.6)
paso([*fondo("Verano"), abrir(.5)], [humo(*CHIM), crea("Chuchini", "ChuchiniSombreroFrente", 300), crea("Nino", "PedroNinoFrente", 332, 190)], t=2)
paso([*sin_titulo(), *titulo("Verano"), cerrar(.5)], t=.6)
paso([*fondo("Otono", tinte="255;225;190"), abrir(.5)], [humo(*CHIM), crea("Chuchini", "ChuchiniSombreroFrente", 280), crea("Nino", "PedroSinFrente", 318)], t=2)
paso([*sin_titulo(), *titulo("Otoño"), cerrar(.5)], t=.6)
paso([*fondo("Invierno", tinte="235;240;250"), bv("Nieve", "True"), abrir(.5)], [humo(*CHIM), crea("Chuchini", "ChuchiniViejoFrente", 262), crea("Nino", "PedroSinFrente", 300)], t=2.2)
paso([*sin_titulo(), cerrar(.8)], t=.9)
# VIII. La herencia
paso([*titulo("Años más tarde..."), bv("Nieve", "False"), A("Delete", "CopoI", ""), *fondo("Herencia", tinte="255;200;165"), abrir(1.2)], [humo(*CHIM), crea("Viejo", "ChuchiniViejoLado", 300, flip=False), crea("Pedro", "PedroSinLado", 226, flip=True)], t=1.8)
paso([*sin_titulo()], dlg="Intro7")
paso([A("Create", "", "SombreroVuela", "285", "146", q("")), A("SetZOrder", "SombreroVuela", "=", "500"), tw_y("SombreroVuela", "Subir", "134", "easeOutQuad", .5),
      A("Tween::TweenBehavior::AddObjectPositionXTween2", "SombreroVuela", "Tween", q("Pasar"), "218", q("easeInOutQuad"), "1", "no")], [pose("Viejo", "ChuchiniViejoSinLado")], t=1.05)
paso([A("Delete", "SombreroVuela", ""), snd("HUD/SubirNivel.wav", 40)], [pose("Pedro", "PedroLado", der=True)], t=.6)
paso([], dlg="Intro7b")
paso([cerrar(1)], t=1.1)
# IX. La primera noche: la radiación vuelve
paso([*fondo("Noche", nubes=False), abrir(1.4)], [crea("Pedro", "PedroCamina", -24, flip=True)], t=1)
paso([], [anda("Pedro", "Pedro", 170, 3.2)], t=3.3)
paso([], [pose("Pedro", "PedroFrente")], dlg="Intro8")
paso([A("Create", "", "PapaBrota", "256", "168", q("")), A("SetZOrder", "PapaBrota", "=", "194"), bv("Temblor", "True"), snd("Cultivos/Temblor.wav", 90), bv("Esporas", "True")], [pose("Pedro", "PedroLado", der=True)], t=2.3)
paso([bv("Temblor", "False"), A("SetCameraCenterX", "", "=", "240", '""', "0"), A("SetCameraCenterY", "", "=", "135", '""', "0")], dlg="Intro8b")
paso([cerrar(1)], t=1.1)
# X. Título
paso([A("Delete", "PapaBrota", ""), bv("Esporas", "False"), A("Create", "", "LogoIntro", "21", "-150", q("Efectos")), A("SetZOrder", "LogoIntro", "=", "300"),
      A("Tween::TweenBehavior::AddObjectPositionYTween2", "LogoIntro", "Tween", q("Caer"), "40", q("easeOutBounce"), "1.2", "no"), snd("Menu/GolpeLogo.wav", 90), *titulo("Legado Radioactivo", 380)], t=3.4)
paso([tw_op("LogoIntro", "Ocultar", 0, "easeInQuad", 1), *sin_titulo()], t=1.2)
paso([sv("EscenaAGuardar", q("Nivel 01")), A("Scene", "", q("Nivel 01"), "")], t=99)

eventos = []
for i, (acts, subs, t, dlg) in enumerate(pasos):
    if dlg: acts = acts + [sv("DialogoPedido", q(dlg))]
    eventos.append(EV([inv_("Paso", str(i)), ONCE()], acts + [A("ResetTimer", "", q("Escena"))], subs))
    fin = C("CompareTimer", "", q("Escena"), ">=", str(t)) if t is not None else isv("DialogoTerminado", q(dlg))
    a2 = [nv("Paso", "1", "+")]
    if dlg: a2.append(sv("DialogoTerminado", q("")))
    eventos.append(EV([inv_("Paso", str(i)), fin], a2))

ev = intro["events"]
i_saltar = next(k for k, e in enumerate(ev) if e.get("comment", "").startswith("Saltar"))
cola = ev[i_saltar:]
cab = ev[:3]
cab[1]["actions"] = [a for a in cab[1]["actions"] if not (a["type"]["value"] == "SetAnimationName" and a["parameters"][0] == "FondoIntro")]
vivo = [
    COM("Cielo, montes y primer plano se mueven a distinta velocidad al desplazar la camara: asi se siente la profundidad"),
    EV([], [nv("PanX", 'CameraCenterX("") - 240'), A("SetX", "IntroCielo", "=", "PanX * 0.85"), A("SetX", "IntroMontes", "=", "PanX * 0.6"), A("SetX", "IntroFrente", "=", "PanX * -0.25")]),
    FOREACH("NubeI", acts=[A("SetX", "NubeI", "=", "NubeI.X() + NubeI.Vel * TimeDelta()")], subs=[EV([cmp_("NubeI.X()", ">", "PanX + 500")], [A("SetX", "NubeI", "=", "PanX - 110")])]),
    EV([ibv("Temblor", "True")], [A("SetCameraCenterX", "", "=", "240 + RandomInRange(-4, 4)", '""', "0"), A("SetCameraCenterY", "", "=", "135 + RandomInRange(-3, 3)", '""', "0")]),
    EV([ibv("Nieve", "True"), C("CompareTimer", "", q("Nieve"), ">=", "0.05")], [A("ResetTimer", "", q("Nieve")), A("Create", "", "CopoI", "RandomInRange(0, 500)", "-4", q("")), A("SetZOrder", "CopoI", "=", "800"),
        tw_y("CopoI", "Caer", "CopoI.Y() + 280", "linear", "RandomFloatInRange(3.5, 6)", "yes"), A("Tween::TweenBehavior::AddObjectPositionXTween2", "CopoI", "Tween", q("Viento"), "CopoI.X() + RandomInRange(-30, 30)", q("linear"), "5", "no")]),
    COM("GUION. Paso = momento de la historia. Cada paso arranca una vez y avanza por tiempo o al terminar su dialogo."),
]
intro["events"] = cab + vivo + eventos + cola
cab[1]["actions"].append(A("ResetTimer", "", q("Nieve")))
# La escena salta al mismo sitio y deja guardar la granja
# ---------- Desmayo ----------
OG["FondoGO"]["animations"][0]["directions"][0]["sprites"][0]["image"] = img("IntroN/DesmayoFondo")
OG["TituloGO"]["animations"][0]["directions"][0]["sprites"][0]["image"] = img("IntroN/TituloDesmayo")
def base_frame(r):
    w, h = tam(r)
    return frame(img(r), (w // 2, h))
OG["PedroGO"]["animations"] = [anim_def("Caido", [base_frame(f"Actores/PedroCae{k}") for k in (1, 2, 3)], loop=False, dt=0.32)]
go["objects"].append(sprite_obj("SombreroGO", [anim_def("N", [base_frame("Actores/SombreroSuelo")])]))
go["objects"].append(sprite_obj("TomasGO", [anim_def("Camina", [frame(img(f"Actores/Tomas_Camina{k}"), (16, 47)) for k in range(1, 9)], loop=True, dt=0.1), anim_def("Frente", [frame(img(f"Actores/Tomas_Frente{k}"), (16, 47)) for k in (1, 2)], loop=True, dt=.7)]))
go["objects"].append(sprite_obj("FarolGO", [anim_def("N", [frame(img("Actores/Farol"))])], tween=False))
go["objects"].append(sprite_obj("HaloGO", [anim_def("N", [frame(img("IntroN/Halo"))])], tween=False))
pgo = next(i for i in go["instances"] if i["name"] == "PedroGO"); pgo["x"], pgo["y"], pgo["zOrder"], pgo["angle"] = 240, 192, 20, 0
go["instances"] += [inst("SombreroGO", 240, 192, z=21), inst("TomasGO", -30, 192, z=22), inst("FarolGO", -30, 172, z=23), inst("HaloGO", -60, 160, z=19)]
evg = go["events"]
for e in evg:
    for a in e.get("actions", []) or []:
        if a["type"]["value"] == "SetX" and a["parameters"][0] == "EstrellaGO":
            a["parameters"][2] = a["parameters"][2].replace("268 +", "240 +")
        if a["type"]["value"] == "SetY" and a["parameters"][0] == "EstrellaGO":
            a["parameters"][2] = a["parameters"][2].replace("150 +", "172 +")
# Tomás llega con su farol después de que Pedro cae
cor = [
    COM("Pedro cae, el sombrero rueda y el abuelo Tomas llega con su farol"),
    EV([C("SceneJustBegins", "")], [A("AnimatableCapability::AnimatableBehavior::PauseAnimation", "PedroGO", "Animation"), opacity("SombreroGO", 0), opacity("TomasGO", 255), A("FlipX", "TomasGO", "yes"), anim("TomasGO", q("Camina")), opacity("HaloGO", 200)]),
    EV([C("CompareTimer", "", q("Escena"), ">=", "1.0"), ONCE()], [A("AnimatableCapability::AnimatableBehavior::PlayAnimation", "PedroGO", "Animation"), snd("Recursos/Soltar.wav", 60)]),
    EV([C("CompareTimer", "", q("Escena"), ">=", "1.7"), ONCE()], [opacity("SombreroGO", 255), A("Tween::TweenBehavior::AddObjectPositionXTween2", "SombreroGO", "Tween", q("Rodar"), "278", q("easeOutQuad"), ".8", "no"), tw_y("SombreroGO", "Saltito", "190", "easeOutQuad", .3)]),
    EV([C("CompareTimer", "", q("Escena"), ">=", "2.4"), ONCE()], [A("Tween::TweenBehavior::AddObjectPositionXTween2", "TomasGO", "Tween", q("Llegar"), "196", q("linear"), "3", "no")]),
    EV([C("CompareTimer", "", q("Escena"), ">=", "5.45"), ONCE()], [anim("TomasGO", q("Frente"))]),
    EV([], [A("SetX", "FarolGO", "=", "TomasGO.X() + 10"), A("SetY", "FarolGO", "=", "TomasGO.Y() - 20"), A("SetX", "HaloGO", "=", "TomasGO.X() - 19"), A("SetY", "HaloGO", "=", "TomasGO.Y() - 48")]),
]
i_com = next(k for k, e in enumerate(evg) if e.get("comment", "").startswith("Aparicion"))
go["events"] = evg[:i_com] + cor + evg[i_com:]
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("pasos:", len(pasos))
print("ok")
