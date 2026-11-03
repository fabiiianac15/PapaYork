"""Etapas 1 y 2: el día cambia al dormir, desmayo a las 2 AM, energía, cultivos por días, riego y regadera.

Todo lo nocturno vive en el evento externo NuevoDia, que se activa con la variable PedirNuevoDia.
Las partidas viejas siguen cargando: Energia y RegaderaAgua solo se leen si existen en la ranura, y un cultivo
viejo conserva la etapa que tenía.
"""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *

P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
if any(e["name"] == "NuevoDia" for e in d["externalEvents"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")

EXT = {e["name"]: e for e in d["externalEvents"]}
L = {l["name"]: l for l in d["layouts"]}
OBJ = {o["name"]: o for o in d["objects"]}


def en(evs, *ruta):
    e = evs[ruta[0]]
    for i in ruta[1:]:
        e = e["events"][i]
    return e


def params(e):
    return json.dumps([e.get("conditions"), e.get("actions")], ensure_ascii=False)


# ---------- Variables nuevas ----------
for v in (var("Energia", "number", 100), var("EnergiaMax", "number", 100), var("RegaderaAgua", "number", 20),
          var("RegaderaMax", "number", 20), var("PedirNuevoDia", "boolean", False), var("DesmayoSueno", "boolean", False),
          var("CreceHoy", "number", 0), var("Protegido", "boolean", False)):
    set_global_var(d, v)

# ---------- Datos de cultivos: la mutación se tira una vez por noche ----------
V = {v["name"]: v for v in d["variables"]}
DATOS = {"Zanahoria": (4, "012", 0), "Papa": (6, "012", 10), "PapaMutante": (8, "0123", 30)}
for c in V["Cultivos"]["children"]:
    dias, estaciones, prob = DATOS[c["name"]]
    c["children"] += [var("DiasMadurar", "number", dias), var("Estaciones", "string", estaciones),
                      var("NecesitaRiego", "boolean", True)]
    next(x for x in c["children"] if x["name"] == "ProbMutante")["value"] = prob

# ---------- Comida y regadera en los objetos ----------
ITEMS = {c["name"]: c for c in V["Items"]["children"]}
for nombre, energia in (("Zanahorias", 15), ("Papa", 20), ("Hongo", 10)):
    it = ITEMS[nombre]
    it["children"].append(var("Energia", "number", energia))
    des = next(x for x in it["children"] if x["name"] == "Descripcion")
    des["value"] += f" Clic derecho: comer (+{energia} de energía)."
V["Items"]["children"].append(struct("Regadera", [
    var("Descripcion", "string", "Clic en tierra arada para regarla. Se rellena con clic en el agua. Hay que regar cada día."),
    var("Max", "number", 1), var("Nombre", "string", "Regadera"), var("Precio", "number", 30),
    var("Rareza", "string", "Común"), var("Tipo", "string", "Herramienta")]))
V["Tiendas"]["children"][[c["name"] for c in V["Tiendas"]["children"]].index("Mercado")]["children"].append(
    {"type": "structure", "children": [var("Id", "string", "Regadera"), var("Precio", "number", 60), var("Tipo", "string", "Item")]})
add_resource(d, "image", "Natural/Objetos/Regadera.png", "Natural/Objetos/Regadera.png")
OBJ["IconoItem"]["animations"].append(anim_def("Regadera", [frame("Natural/Objetos/Regadera.png", (16, 16))]))

# ---------- Barra de energía ----------
for nombre, arch in (("EnergiaMarco", "EnergiaMarco"), ("EnergiaRelleno", "EnergiaRelleno")):
    add_resource(d, "image", f"Natural/Objetos/{arch}.png", f"Natural/Objetos/{arch}.png")
    set_global_object(d, sprite_obj(nombre, [anim_def("Normal", [frame(f"Natural/Objetos/{arch}.png")])], tween=False))


def flotante(texto, color, dy=-52, dur=2):
    return [A("Create", "", "TextoFlotante", "Personaje_jugador.CenterX() - 40", f"Personaje_jugador.Y() {dy}", q("")),
            txt("TextoFlotante", texto), A("TextObject::ChangeColor", "TextoFlotante", q(color)),
            A("SetZOrder", "TextoFlotante", "=", "100000"),
            tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", dur),
            tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", dur + 1, "yes")]


# ---------- Bloque de mutación: se reutiliza tal cual desde el evento por horas ----------
cul = EXT["Cultivos"]["events"]
assert "Reloj.Hora" in params(cul[11]) and cul[11]["events"][0]["type"].endswith("ForEachChildVariable")
por_hora = cul[11]["events"][0]
mutacion = copy.deepcopy(por_hora["events"][2])
assert "ProbMutante" in params(mutacion)
del cul[10:12]
cul[0]["comment"] = ("CULTIVOS Granja[celda] = {X, Y, Escena, Planta, Etapa, Abono, Regada, DiasCrecidos}. "
                     "Crecen de noche en el evento externo NuevoDia. Cultivos[tipo] tiene los datos de cada planta.")
assert "Semilla" in params(cul[3])
cul[3]["actions"].append(nv("Granja[SueloPreparado.MiCelda].DiasCrecidos", "0"))
assert "Etapa" in params(cul[7]) and "Cosechar" in params(cul[7])
cul[7]["actions"].append(nv("Granja[Cultivo.MiCelda].DiasCrecidos", "0"))

# ---------- Crecimiento de cada noche ----------
K = "Granja[ClaveGranja]"
T = "Cultivos[CeldaGranja.Planta]"
EST = f"StrFind({T}.Estaciones, ToString(Calendario.Estacion))"
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)

muere = EV([cmp_(EST, "=", "-1")],
           [sv(f"{K}.Planta", q("")), nv(f"{K}.Etapa", "0"), nv(f"{K}.DiasCrecidos", "0")],
           [EV([objv_s("Cultivo", "MiCelda", "ClaveGranja")], [A("Delete", "Cultivo", "")]),
            EV([objv_s("SueloPreparado", "MiCelda", "ClaveGranja")], [set_objv_b("SueloPreparado", "Plantada", "False")])])
crece = EV([cmp_(EST, "!=", "-1")], [nv("CreceHoy", "0")], [
    EV([ibv(f"{K}.Regada", "True")], [nv("CreceHoy", "1")]),
    EV([ibv(f"{T}.NecesitaRiego", "False")], [nv("CreceHoy", "1")]),
    EV([inv_("CreceHoy", "1")], [nv(f"{K}.DiasCrecidos", "1", "+")],
       [EV([ibv(f"{K}.Abono", "True")], [nv(f"{K}.DiasCrecidos", "1", "+")])]),
    EV([], [nv(f"{K}.Etapa", f"max({K}.Etapa, min(3, floor({K}.DiasCrecidos * 3 / {T}.DiasMadurar)))")]),
    mutacion])
celda = copy.deepcopy(por_hora)
celda["conditions"], celda["actions"] = [], []
celda["events"] = [EV([isv("CeldaGranja.Planta", q(""), "!=")], [], [muere, crece]),
                   EV([], [bv(f"{K}.Regada", "False")])]

estacion = EV([inv_("Calendario.Dia", "28", ">")], [nv("Calendario.Dia", "1"), nv("Calendario.Estacion", "1", "+")],
              [EV([inv_("Calendario.Estacion", "3", ">")], [nv("Calendario.Estacion", "0"), nv("Calendario.Anio", "1", "+")])])

noche = EV([ibv("PedirNuevoDia", "True")],
           [bv("PedirNuevoDia", "False"), nv("Calendario.Dia", "1", "+"), nv("Calendario.DiaTotal", "1", "+"),
            nv("Energia", "EnergiaMax"), nv("Reloj.Hora", "6"), nv("Reloj.Minuto", "0"), sv("Reloj.M", q("AM")),
            bv("Reloj.Mediodia", "False"), nv("LuzExterior.R", "68"), nv("LuzExterior.G", "118"), nv("LuzExterior.B", "223")],
           [estacion, celda, EV([], flotante('"¡Buenos días! Día " + ToString(Calendario.Dia)', "251;242;54"))])

# ---------- Clics ----------
sin_ui = [ibv("InventarioAbierto", "False"), ibv("MouseSobreUI", "False")]
izq, una = C("MouseButtonFromTextPressed", "", q("Left")), ONCE()
cerca = C("Rejilla::Rejilla::Vicelda", "Rejilla", "=", "1", "")

eventos = [
    COM("NUEVO DIA: todo lo que pasa de noche sale de aqui. Dormir o desmayarse pide PedirNuevoDia = true."),
    EV([C("SceneJustBegins", "")], [], [
        EV([], [A("Create", "", "EnergiaMarco", "930", "418", q("UIHD")), A("SetZOrder", "EnergiaMarco", "=", "5000")]),
        EV([], [A("Create", "", "EnergiaRelleno", "934", "422", q("UIHD")), A("SetZOrder", "EnergiaRelleno", "=", "5001")])]),
    noche,
    COM("A las 2 AM Pedro cae rendido: se reutiliza la pantalla de desmayo"),
    EV([isv("Reloj.M", q("AM")), inv_("Reloj.Hora", "2", ">="), inv_("Reloj.Hora", "6", "<")],
       [bv("DesmayoSueno", "True"), A("Scene", "", q("GameOver"), "no")]),
    COM("Barra de energia"),
    EV([], [A("ResizableCapability::ResizableBehavior::SetHeight", "EnergiaRelleno", "Resizable", "=", "max(0, 88 * Energia / EnergiaMax)"),
            A("SetY", "EnergiaRelleno", "=", "510 - EnergiaRelleno.Height()"),
            A("ChangeColor", "EnergiaRelleno", q("126;190;80"))]),
    EV([inv_("Energia", "40", "<=")], [A("ChangeColor", "EnergiaRelleno", q("230;170;60"))]),
    EV([inv_("Energia", "15", "<=")], [A("ChangeColor", "EnergiaRelleno", q("214;80;72"))]),
    COM("Sin energia no se usan las herramientas"),
    EV(sin_ui + [inv_("Energia", "0", "<="), isv("Items[ItemEnMano].Tipo", q("Herramienta")), izq, una],
       [snd("Inventario/Seleccion.wav", 40)] + flotante('"¡Estoy agotado! Come algo o duerme."', "230;170;60", dur=1)),
    COM("Comer: clic derecho con comida en la mano"),
    EV(sin_ui + [ibv("TiendaAbierta", "False"), ibv("FabricarAbierto", "False"), ibv("DialogoAbierto", "False"),
                 cmp_("Items[ItemEnMano].Energia", ">", "0"), inv_("Mochila[RanuraSeleccionada].Cantidad", "1", ">="),
                 C("MouseButtonFromTextPressed", "", q("Right")), una],
       [nv("Energia", "min(EnergiaMax, Energia + Items[ItemEnMano].Energia)"),
        nv("Mochila[RanuraSeleccionada].Cantidad", "1", "-"), snd("Natural/Audio/Comer.ogg", 70)]
       + flotante('"+" + ToString(Items[ItemEnMano].Energia) + " energía"', "153;229;80", dur=1)),
    COM("Regar: regadera en la mano y clic en tierra arada al lado de Pedro"),
    EV(sin_ui + [isv("ItemEnMano", q("Regadera")), C("IsCursorOnObject", "SueloPreparado", "", "", ""), cerca,
                 inv_("RegaderaAgua", "0", ">"), inv_("Energia", "0", ">"),
                 ibv("Granja[SueloPreparado.MiCelda].Regada", "False"), izq, una],
       [bv("Granja[SueloPreparado.MiCelda].Regada", "True"), nv("RegaderaAgua", "1", "-"), nv("Energia", "1", "-"),
        snd("Natural/Audio/Regar.ogg", 60)]),
    EV(sin_ui + [isv("ItemEnMano", q("Regadera")), C("IsCursorOnObject", "SueloPreparado", "", "", ""), cerca,
                 inv_("RegaderaAgua", "0", "<="), izq, una],
       flotante('"La regadera está vacía"', "95;205;228", dur=1)),
    COM("Rellenar la regadera en el agua o en el pozo"),
    EV(sin_ui + [isv("ItemEnMano", q("Regadera")), C("IsCursorOnObject", "Agua2", "", "", ""), cerca, izq, una],
       [nv("RegaderaAgua", "RegaderaMax"), snd("Natural/Audio/Regar.ogg", 70)]
       + flotante('"Regadera llena"', "95;205;228", dur=1)),
    EV(sin_ui + [isv("ItemEnMano", q("Regadera")), C("IsCursorOnObject", "Pozo", "", "", ""), cerca, izq, una],
       [nv("RegaderaAgua", "RegaderaMax"), snd("Natural/Audio/Regar.ogg", 70)]
       + flotante('"Regadera llena"', "95;205;228", dur=1)),
    COM("La tierra muestra si esta seca, abonada o regada"),
    FOREACH("SueloPreparado", subs=[
        EV([], [anim("SueloPreparado", q("Seca"))]),
        EV([ibv("Granja[SueloPreparado.MiCelda].Abono", "True")], [anim("SueloPreparado", q("Abonado"))]),
        EV([ibv("Granja[SueloPreparado.MiCelda].Regada", "True")], [anim("SueloPreparado", q("Regada"))])]),
]
external_events(d, "NuevoDia", eventos)
per = EXT["Personaje"]["events"]
i = next(k for k, e in enumerate(per) if e.get("target") == "Cultivos")
per.insert(i, LINK("NuevoDia"))

# ---------- El reloj ya no cambia de día a medianoche ----------
rel = EXT["RelojProg"]["events"]
dentro = en(rel, 4, 1)["events"]
assert "12 AM" in dentro[2]["comment"] and "Calendario.Dia" in params(dentro[3])
del dentro[2:4]

# ---------- Luz más suave: amanecer rosado, atardecer dorado y noche azul en la que aún se ve ----------
TONOS = {("68", "118", "223"): ("176", "164", "206"), ("255", "169", "5"): ("255", "196", "136"), ("26", "22", "65"): ("82", "84", "136")}
def cambiar_luz(evs):
    n = 0
    for e in evs:
        acts = e.get("actions", []) or []
        for viejo, nuevo in TONOS.items():
            for canal, v, w in zip("RGB", viejo, nuevo):
                for a in acts:
                    if a["type"]["value"] == "SetNumberVariable" and a["parameters"][0] == "LuzExterior." + canal:
                        t = a["parameters"][2]
                        if t == v or t.endswith("," + v + ",LuzExterior.VelTran)"):
                            a["parameters"][2] = t.replace(v, w) if t == v else t.replace("," + v + ",", "," + w + ",")
                            n += 1
        n += cambiar_luz(e.get("events", []) or [])
    return n
print("tonos de luz cambiados:", cambiar_luz(rel) + cambiar_luz(EXT["Mundo2"]["events"]) + cambiar_luz(eventos))

# ---------- Las pestañas de pausa no deben salir durante un diálogo ----------
pau = EXT["Pausa"]["events"][3]
assert "VerPausa" in params(pau)
pau["conditions"].append(ibv("DialogoAbierto", "False"))

# ---------- Dormir pide un día nuevo ----------
mun = EXT["Mundo2"]["events"]
dormir = mun[6]
assert 'Dormir' in params(dormir)
sub = dormir["events"]
assert "Calendario.Dia" in params(sub[2]) and sub[3]["type"].endswith("ForEachChildVariable") and "Reloj.Hora" in params(sub[4])
sub[4]["actions"] = [a for a in sub[4]["actions"] if "TextoFlotante" not in a["parameters"]]
sub[2:4] = [EV([], [bv("PedirNuevoDia", "True")])]

# ---------- Las herramientas gastan energía ----------
her = EXT["Herramientas"]["events"]
her[3]["conditions"].append(inv_("Energia", "0", ">"))
for ruta, gasto, marca in (((3, 1, 1), 3, "Talando"), ((3, 3, 0), 2, "Labrando"), ((3, 5, 1), 3, "Picando")):
    e = en(her, *ruta)
    assert marca in params(e), marca
    e["actions"].append(nv("Energia", str(gasto), "-"))

# ---------- Guardar y cargar ----------
gu = en(EXT["Guardado"]["events"], 2, 8)["actions"]
pos = next(k for k, a in enumerate(gu) if a["type"]["value"] == "SetStringVariable")
for n in ("RegaderaAgua", "Energia"):
    gu.insert(pos, A("EcrireFichierTxt", q("PapayorkPartidas"), f'"Ranura" + ToString(RanuraActual) + "/{n}"', f"ToJSON({n})"))
menu = L["Menu Principal"]["events"]
carga = menu[37]["events"]
idx = next(k for k, e in enumerate(carga) if '/Granja' in params(e))
for n in ("RegaderaAgua", "Energia"):
    copia = json.loads(json.dumps(carga[idx], ensure_ascii=False).replace('/Granja\\"', f'/{n}\\"').replace('"Granja"', f'"{n}"'))
    carga.insert(idx + 1, copia)
    assert n in params(copia) and "Granja" not in params(copia)
nueva = menu[35]
nueva["actions"][:0] = [nv("Energia", "100"), nv("RegaderaAgua", "20"), bv("PedirNuevoDia", "False"), bv("DesmayoSueno", "False")]
# La partida nueva empieza con regadera, en la primera casilla libre
acc = next(a for a in nueva["actions"] if a["type"]["value"] == "JSONToGlobalVariableStructure" and a["parameters"][1] == "Mochila")
crudo = acc["parameters"][0]
moch = json.loads(crudo[1:-1].replace('\\"', '"'))
libre = next(k for k, c in enumerate(moch) if not c["Id"])
moch[libre] = {"Id": "Regadera", "Cantidad": 1}
acc["parameters"][0] = q(json.dumps(moch, ensure_ascii=False, separators=(",", ":")))
print("regadera en casilla", libre, [c["Id"] for c in moch if c["Id"]])

# ---------- Pantalla de desmayo: mensaje propio y paso del día ----------
go = L["GameOver"]["events"]
go[1]["events"].append(EV([ibv("DesmayoSueno", "True"), objv_s("TextoGO", "Clave", q("Sub"))],
                          [txt("TextoGO", q("Eran las 2 de la mañana y el sueño te venció..."))]))
i15 = next(k for k, e in enumerate(go) if 'Nivel 01' in params(e) and any(a["type"]["value"] == "Scene" for a in e.get("actions", [])))
go.insert(i15, EV([ibv("DesmayoSueno", "True"), isv("Destino", q("Nivel 01")), C("CompareTimer", "", q("Salida"), ">=", "0.7")],
                  [bv("DesmayoSueno", "False"), bv("PedirNuevoDia", "True")]))
go.insert(i15 + 2, EV([ibv("DesmayoSueno", "True"), isv("Destino", q("Menu Principal"))], [bv("DesmayoSueno", "False")]))

with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok")
