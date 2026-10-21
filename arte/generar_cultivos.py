"""Siembra de papas, crecimiento por horas y papas radiactivas que salen de la tierra.

Se aplica despues de generar_fabricacion.py y antes de generar_menu.py. Reemplaza el sistema viejo de la zanahoria
(Planta_Zanahoria con temporizadores de 5 segundos) por uno general para todos los cultivos.

- Cultivos[tipo] = {HorasEtapa, Cosecha, Min, Max, Exp, ProbMutante}. Cada hora del reloj del juego suma 1 hora a
  cada cultivo de Granja (2 con abono), aunque estes en otra zona. La etapa (0-3) sale de las horas acumuladas.
- Semillas: Zanahoria, Papa y Papa mutante (Items[semilla].Cultivo dice que planta sale).
- Cada hora, una papa que esta creciendo (etapas 1 y 2) tiene ProbMutante % de convertirse en una papa radiactiva
  que sale de la tierra (animacion PapaEmerge1..10), salvo que haya un espantapapas cerca. Madura ya esta a salvo. Esa papa va hacia el cultivo mas cercano y se lo come
  si se queda pegada 2.5 segundos. Al no quedar cultivos vuelve a pasear como las demas.
- Abono: sobre tierra arada, el cultivo crece el doble de rapido.

Uso: python3 arte/generar_cultivos.py "Legado Radioactivo-Papayork.json"
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
herr = ext("Herramientas")
VICELDA = next(c for e in recorrer(herr["events"]) for c in e.get("conditions") or [] if c["type"]["value"] == "Rejilla::Rejilla::Vicelda")

# ---------- datos ----------
CULTIVOS = {  # horas por etapa, cosecha, min, max, exp, % de papa radiactiva por hora
    "Zanahoria": (3, "Zanahorias", 1, 2, 3, 0),
    "Papa": (4, "Papa", 1, 3, 4, 4),
    "PapaMutante": (5, "PapaRadiactiva", 1, 2, 8, 12),
}
set_global_var(d, struct("Cultivos", [struct(k, [var("HorasEtapa", "number", h), var("Cosecha", "string", c), var("Min", "number", mn),
                                                 var("Max", "number", mx), var("Exp", "number", ex), var("ProbMutante", "number", pm)])
                                      for k, (h, c, mn, mx, ex, pm) in CULTIVOS.items()]))
items = next(v for v in d["variables"] if v["name"] == "Items")
SEMILLA = {"Semillas de Zanahoria": "Zanahoria", "Semillas de Papa": "Papa", "Semillas de Papa Mutante": "PapaMutante", "Semillas de Tomate": ""}
for c in items["children"]:
    if c["name"] in SEMILLA:
        c["children"] = [x for x in c["children"] if x["name"] != "Cultivo"] + [var("Cultivo", "string", SEMILLA[c["name"]])]
NUEVOS = [("Papa", "Papa", "Cultivo", "Común", 99, 20, "Una papa sana de tu granja. Se venderá bien en el pueblo."),
          ("PapaRadiactiva", "Papa radiactiva", "Cultivo", "Raro", 99, 80, "Brilla y vibra. Vale mucho... si alguien se atreve a comprarla.")]
items["children"] = [c for c in items["children"] if c["name"] not in {n[0] for n in NUEVOS}]
for i, n, t, r, m, p, ds in NUEVOS:
    items["children"].append(struct(i, [var("Nombre", "string", n), var("Tipo", "string", t), var("Rareza", "string", r),
                                        var("Max", "number", m), var("Precio", "number", p), var("Descripcion", "string", ds)]))

# ---------- recursos ----------
for f in ["Papa_%d" % i for i in range(4)] + ["PapaMutante_%d" % i for i in range(4)] + ["Papa", "PapaRadiactiva"] + \
         ["PapaEmerge%d" % i for i in range(1, 11)]:
    add_resource(d, "image", "Cultivos/" + f + ".png", "Cultivos/" + f + ".png")
add_resource(d, "image", "Fabricacion/SueloAbonado.png", "Fabricacion/SueloAbonado.png")
for f in ["Sembrar", "Temblor", "Comer", "Cosechar"]:
    add_resource(d, "audio", "Cultivos/" + f + ".wav", "Cultivos/" + f + ".wav")

# ---------- objetos ----------
etapas_zanahoria = [a["directions"][0]["sprites"][0]["image"] for a in O["Planta_Zanahoria"]["animations"]]
anims = [anim_def("Zanahoria_%d" % i, [frame(img)]) for i, img in enumerate(etapas_zanahoria)]
anims += [anim_def("%s_%d" % (t, i), [frame("Cultivos/%s_%d.png" % (t, i))]) for t in ("Papa", "PapaMutante") for i in range(4)]
set_global_object(d, sprite_obj("Cultivo", anims, [var("MiCelda", "string", "")]))
set_global_object(d, sprite_obj("PapaEmerge", [anim_def("", [frame("Cultivos/PapaEmerge%d.png" % i) for i in range(1, 11)], dt=0.09)],
                                [var("MiCelda", "string", "")], tween=False))
for nombre, origen in (("Recursos", (0, 0)), ("IconoItem", (16, 16))):
    o = O[nombre]
    o["animations"] = [a for a in o["animations"] if a["name"] not in ("Papa", "PapaRadiactiva", "Zanahorias")]
    o["animations"] += [anim_def("Papa", [frame("Cultivos/Papa.png", origen)]), anim_def("PapaRadiactiva", [frame("Cultivos/PapaRadiactiva.png", origen)])]
    if nombre == "Recursos": o["animations"].append(anim_def("Zanahorias", [frame("Zanahoria.png", origen, rect(4, 4, 28, 28))]))
suelo = O["SueloPreparado"]
suelo["animations"] = suelo["animations"][:1] + [anim_def("Abonado", [frame("Fabricacion/SueloAbonado.png")])]
papa = O["Papa"]
papa["variables"] = [v for v in papa["variables"] if v["name"] not in ("Hambrienta", "Comiendo")] + \
                    [var("Hambrienta", "boolean", False), var("Comiendo", "number", 0)]
for lay in d["layouts"]:
    if lay["name"] in ("Nivel 01", "Nivel 02", "Pueblo"):
        for v in lay["variables"]:
            if v["name"] == "CeldaGranja":
                v["children"] = [c for c in v["children"] if c["name"] not in ("Horas", "Abono")] + \
                                [var("Horas", "number", 0), var("Abono", "boolean", False)]
        lay["variables"] = [v for v in lay["variables"] if v["name"] != "HoraVista"] + [var("HoraVista", "number", -1)]

# ---------- quitar el sistema viejo de la zanahoria ----------
VIEJO = ("Planta_Zanahoria", '"Plantas"', "Plantas,", "Verduras")
COMENTARIOS_VIEJOS = ("Sembrar Zanahorias", "Cosechar Zanahorias", "Control de Crecimiento", "La planta crece")
def limpiar(evs):
    out = []
    for e in evs:
        if e.get("type", "").endswith("Comment") and any(c in e.get("comment", "") for c in COMENTARIOS_VIEJOS): continue
        propio = json.dumps({k: v for k, v in e.items() if k != "events"}, ensure_ascii=False)
        if any(v in propio for v in VIEJO) or any(c["parameters"][:1] == ["Plantas"] for c in (e.get("conditions") or []) + (e.get("actions") or [])):
            continue
        if e.get("events"): e["events"] = limpiar(e["events"])
        out.append(e)
    return out
herr["events"] = limpiar(herr["events"])

# ---------- eventos ----------
CLAVE = "Cultivo.MiCelda"
def suelo_de(clave):  # elige la tierra arada de esa celda
    return objv_s("SueloPreparado", "MiCelda", clave)
def flotante(texto, x, y, rgb):
    return [A("Create", "", "TextoFlotante", x, y, q("")), txt("TextoFlotante", texto), color("TextoFlotante", rgb),
            A("SetZOrder", "TextoFlotante", "=", "100000"),
            tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 18", "easeOutQuad", 1),
            tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 1.4, "yes")]

E = [COM("CULTIVOS\nGranja[celda] = {X, Y, Escena, Planta, Horas, Etapa, Abono}. Cultivos[tipo] tiene los datos de cada planta.\n"
         "Cada hora del reloj suma horas a todos los cultivos (tambien en otras zonas). El objeto Cultivo solo muestra la etapa.")]
E.append(EV([C("SceneJustBegins", "")], [nv("HoraVista", "Reloj.Hora"), A("ResetTimer", "", q("Cosecha"))]))

E.append(COM("Sembrar: semilla en la mano + clic en tierra arada vacia al lado de Pedro"))
E.append(EV([ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False"), isv("Items[ItemEnMano].Tipo", q("Semilla")),
             isv("Items[ItemEnMano].Cultivo", '""', "!="), isv("Items[ItemEnMano].Cultivo", q("0"), "!="),
             inv_("Mochila[RanuraSeleccionada].Cantidad", "1", ">="), cursor("SueloPreparado"), objv_b("SueloPreparado", "Plantada", "False"),
             VICELDA, C("CompareTimer", "", q("Cosecha"), ">", "0.5"), C("MouseButtonFromTextPressed", "", q("Left")), ONCE()], [
    set_objv_b("SueloPreparado", "Plantada", "True"),
    sv("Granja[SueloPreparado.MiCelda].Planta", "Items[ItemEnMano].Cultivo"),
    nv("Granja[SueloPreparado.MiCelda].Horas", "0"), nv("Granja[SueloPreparado.MiCelda].Etapa", "0"),
    A("Create", "", "Cultivo", "SueloPreparado.X()", "SueloPreparado.Y()", q("")),
    set_objv_s("Cultivo", "MiCelda", "SueloPreparado.MiCelda"), A("SetZOrder", "Cultivo", "=", "Cultivo.Y() + 20"),
    anim("Cultivo", 'Items[ItemEnMano].Cultivo + "_0"'),
    nv("Mochila[RanuraSeleccionada].Cantidad", "1", "-"), snd("Cultivos/Sembrar.wav", 60)]))

E.append(COM("Abono: crecen el doble de rapido"))
E.append(EV([ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False"), isv("ItemEnMano", q("Abono")),
             cursor("SueloPreparado"), ibv("Granja[SueloPreparado.MiCelda].Abono", "False"), VICELDA,
             C("MouseButtonFromTextPressed", "", q("Left")), ONCE()], [
    bv("Granja[SueloPreparado.MiCelda].Abono", "True"), anim("SueloPreparado", q("Abonado")),
    nv("Mochila[RanuraSeleccionada].Cantidad", "1", "-"), snd("Cultivos/Sembrar.wav", 50)]))

E.append(COM("Cosechar: clic en una planta madura (etapa 3)"))
E.append(EV([ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False"), cursor("Cultivo"), inv_("Granja[Cultivo.MiCelda].Etapa", "3", ">="),
             VICELDA, C("MouseButtonFromTextPressed", "", q("Left")), ONCE()], [
    sv("Tipo", "Granja[Cultivo.MiCelda].Planta"), nv("Exp", "Cultivos[Tipo].Exp", "+"), snd("Cultivos/Cosechar.wav", 70),
    A("ResetTimer", "", q("Cosecha")),
    sv("Granja[Cultivo.MiCelda].Planta", '""'), nv("Granja[Cultivo.MiCelda].Horas", "0"), nv("Granja[Cultivo.MiCelda].Etapa", "0")], [
    REPEAT("RandomInRange(Cultivos[Tipo].Min, Cultivos[Tipo].Max)", [], [
        A("Create", "", "Recursos", "Cultivo.X()", "Cultivo.Y()", q("")), anim("Recursos", "Cultivos[Tipo].Cosecha")]),
    EV([suelo_de(CLAVE)], [set_objv_b("SueloPreparado", "Plantada", "False")]),
    EV([], [A("Delete", "Cultivo", "")])], variables=[var("Tipo", "string", "")]))

E.append(COM("Cada cultivo muestra la etapa guardada en Granja"))
E.append(FOREACH("Cultivo", [objv_s("Cultivo", "MiCelda", '""', "!=")], [
    anim("Cultivo", 'Granja[Cultivo.MiCelda].Planta + "_" + ToString(Granja[Cultivo.MiCelda].Etapa)')]))

E.append(COM("Paso de una hora: crecen todos los cultivos y quiza sale una papa radiactiva de la tierra"))
E.append(EV([cmp("Reloj.Hora", "!=", "HoraVista")], [nv("HoraVista", "Reloj.Hora")], [
    {"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Granja",
     "valueIteratorVariableName": "CeldaGranja", "keyIteratorVariableName": "ClaveGranja",
     "conditions": [isv("CeldaGranja.Planta", '""', "!=")],
     "actions": [nv("Granja[ClaveGranja].Horas", "1", "+")],
     "events": [
         EV([ibv("CeldaGranja.Abono", "True")], [nv("Granja[ClaveGranja].Horas", "1", "+")]),
         EV([], [nv("Granja[ClaveGranja].Etapa", "min(3, floor(Granja[ClaveGranja].Horas / Cultivos[CeldaGranja.Planta].HorasEtapa))")]),
         EV([isv("CeldaGranja.Escena", "CurrentSceneName()"), inv_("Granja[ClaveGranja].Etapa", "1", ">="), inv_("Granja[ClaveGranja].Etapa", "3", "<"),
             cmp("RandomInRange(1, 100)", "<=", "Cultivos[CeldaGranja.Planta].ProbMutante"),
             cmp("SceneInstancesCount(PapaEmerge) + SceneInstancesCount(Papa)", "<", "9")], [bv("Protegido", "False")], [
             EV([C("AnimatableCapability::AnimatableBehavior::Name", "Construccion", "Animation", "=", q("Espantapapas")),
                 cmp("DistanceBetweenPositions(Construccion.CeldaX, Construccion.CeldaY, CeldaGranja.X, CeldaGranja.Y)", "<", "100")],
                [bv("Protegido", "True")]),
             EV([ibv("Protegido", "False")], [
                 A("Create", "", "PapaEmerge", "CeldaGranja.X", "CeldaGranja.Y", q("")),
                 set_objv_s("PapaEmerge", "MiCelda", "ClaveGranja"), A("SetZOrder", "PapaEmerge", "=", "PapaEmerge.Y() + 30"),
                 snd("Cultivos/Temblor.wav", 80),
                 sv("Granja[ClaveGranja].Planta", '""'), nv("Granja[ClaveGranja].Horas", "0"), nv("Granja[ClaveGranja].Etapa", "0")], [
                 COM("La planta se transforma en la papa radiactiva: desaparece de su tierra"),
                 EV([objv_s("Cultivo", "MiCelda", "ClaveGranja")], [A("Delete", "Cultivo", "")]),
                 EV([suelo_de("ClaveGranja")], [set_objv_b("SueloPreparado", "Plantada", "False")])])])]}],
    variables=[var("Protegido", "boolean", False)]))

E.append(COM("Cuando termina de salir de la tierra, se convierte en una papa enemiga hambrienta"))
E.append(FOREACH("PapaEmerge", [C("AnimatableCapability::AnimatableBehavior::HasAnimationEnded", "PapaEmerge", "Animation")], [
    A("Create", "", "Papa", "PapaEmerge.X()", "PapaEmerge.Y()", q("")),
    set_objv_b("Papa", "Hambrienta", "True"), set_objv_n("Papa", "Vida", "40"), set_objv_n("Papa", "Velocidad", "26"),
    set_objv_n("Papa", "TiemposAndar", "9999"), set_objv_b("Papa", "PuedeAndar", "False"),
    anim("Papa", q("CaminarAbajo")), A("Delete", "PapaEmerge", ""),
    *flotante(q("¡Tu papa mutó!"), "Papa.X() - 12", "Papa.Y() - 8", "153;229;80")]))

E.append(COM("Papas hambrientas: van al cultivo mas cercano y se lo comen"))
E.append(FOREACH("Papa", [objv_b("Papa", "Hambrienta", "True"), ibv("InventarioAbierto", "False")], [set_objv_b("Papa", "PuedeAndar", "False")], [
    EV([cmp("SceneInstancesCount(Cultivo)", "=", "0")], [set_objv_b("Papa", "Hambrienta", "False"), set_objv_n("Papa", "TiemposAndar", "2")]),
    EV([cmp("SceneInstancesCount(Cultivo)", ">", "0"), C("PickNearest", "Cultivo", "Papa.X()", "Papa.Y()", "")], [
        A("SeparateFromObjects", "Papa", "Colision", "")], [
        EV([C("CollisionNP", "Papa", "Cultivo", "", "", "", inv=True)], [
            A("AddForceTowardPosition", "Papa", "Cultivo.X()", "Cultivo.Y()", "Papa.Velocidad", "0"),
            set_objv_n("Papa", "Comiendo", "0"), A("SetAngle", "Papa", "=", "0")], [
            EV([cmp("abs(Cultivo.X() - Papa.X())", ">", "abs(Cultivo.Y() - Papa.Y())"), cmp("Cultivo.X()", ">", "Papa.X()")], [anim("Papa", q("CaminarDerecha"))]),
            EV([cmp("abs(Cultivo.X() - Papa.X())", ">", "abs(Cultivo.Y() - Papa.Y())"), cmp("Cultivo.X()", "<=", "Papa.X()")], [anim("Papa", q("CaminarIzquierda"))]),
            EV([cmp("abs(Cultivo.X() - Papa.X())", "<=", "abs(Cultivo.Y() - Papa.Y())"), cmp("Cultivo.Y()", ">", "Papa.Y()")], [anim("Papa", q("CaminarAbajo"))]),
            EV([cmp("abs(Cultivo.X() - Papa.X())", "<=", "abs(Cultivo.Y() - Papa.Y())"), cmp("Cultivo.Y()", "<=", "Papa.Y()")], [anim("Papa", q("CaminarArriba"))])]),
        EV([C("CollisionNP", "Papa", "Cultivo", "", "", "")], [
            set_objv_n("Papa", "Comiendo", "TimeDelta()", "+"), A("SetAngle", "Papa", "=", "sin(TimeFromStart() * 30) * 8")], [
            EV([objv_n("Papa", "Comiendo", "2.5", ">=")], [
                set_objv_n("Papa", "Comiendo", "0"), A("SetAngle", "Papa", "=", "0"), snd("Cultivos/Comer.wav", 80),
                sv("Granja[Cultivo.MiCelda].Planta", '""'), nv("Granja[Cultivo.MiCelda].Horas", "0"), nv("Granja[Cultivo.MiCelda].Etapa", "0"),
                *flotante(q("¡Se comió tu cultivo!"), "Cultivo.X() - 20", "Cultivo.Y() - 6", "217;87;99")], [
                EV([suelo_de(CLAVE)], [set_objv_b("SueloPreparado", "Plantada", "False")]),
                EV([], [A("Delete", "Cultivo", "")])])])])]))
external_events(d, "Cultivos", E)

pers = ext("Personaje")
if not any(e.get("target") == "Cultivos" for e in pers["events"] if e.get("type") == "BuiltinCommonInstructions::Link"):
    gi = next((i for i, e in enumerate(pers["events"]) if e.get("target") == "Guardado"), len(pers["events"]))
    pers["events"].insert(gi, LINK("Cultivos"))

# reconstruir cultivos y abono al entrar a la zona (dentro del bucle de Granja que crea la tierra arada)
inicio = next(e for e in pers["events"] if tiene(e, "SceneJustBegins"))
granja = next(s for s in inicio["events"] if s.get("iterableVariableName") == "Granja")
granja["events"] = [
    EV([isv("CeldaGranja.Planta", '""', "!="), isv("CeldaGranja.Planta", q("0"), "!=")], [
        set_objv_b("SueloPreparado", "Plantada", "True"),
        A("Create", "", "Cultivo", "CeldaGranja.X", "CeldaGranja.Y", q("")),
        set_objv_s("Cultivo", "MiCelda", "ClaveGranja"), A("SetZOrder", "Cultivo", "=", "Cultivo.Y() + 20"),
        anim("Cultivo", 'CeldaGranja.Planta + "_" + ToString(CeldaGranja.Etapa)')]),
    EV([ibv("CeldaGranja.Abono", "True")], [anim("SueloPreparado", q("Abonado"))])]

# ---------- borrar lo que ya no se usa ----------
texto = json.dumps([d["layouts"], d["externalEvents"], d["externalLayouts"]], ensure_ascii=False)
assert "Planta_Zanahoria" not in texto, "Planta_Zanahoria todavia se usa"
d["objectsGroups"] = [g for g in d["objectsGroups"] if g["name"] != "Plantas"]
for viejo in ["Planta_Zanahoria", "Verduras"]:
    if viejo == "Verduras" and ('"Verduras"' in texto): continue
    d["objects"] = [o for o in d["objects"] if o["name"] != viejo]
    d["objectsFolderStructure"]["children"] = [c for c in d["objectsFolderStructure"]["children"] if c.get("objectName") != viejo]
    for g in d["objectsGroups"]:
        g["objects"] = [o for o in g["objects"] if o["name"] != viejo]

json.dump(d, open(PROJ, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: cultivos")
