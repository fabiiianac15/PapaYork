"""Casas en las que se entra, escena Interior con 8 salas, Pueblo más grande con barrio este, vecinos que entran y salen,
dos vecinos nuevos, tienda dentro de cada casa, taberna y las seis páginas del diario de HetolMimiao."""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
from PIL import Image
P = sys.argv[1]
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = json.load(open(P, encoding="utf8"))
if any(l["name"] == "Interior" for l in d["layouts"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}; EXT = {e["name"]: e for e in d["externalEvents"]}; L = {l["name"]: l for l in d["layouts"]}; V = {v["name"]: v for v in d["variables"]}
PU = L["Pueblo"]; PJ = "Personaje_jugador"
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def img(r):
    n = "Natural/" + r + ".png"; add_resource(d, "image", n, n); return n
def tam(r): return Image.open(os.path.join(RAIZ, "Natural", r + ".png")).size
PUERTAS = json.load(open(os.path.join(RAIZ, "Natural/Casas/puertas.json")))
SALAS = ("Pedro", "Mercado", "Herreria", "Alcaldia", "Lupita", "Tomas", "Taberna", "Biblioteca")
OX = {s: i * 1000 for i, s in enumerate(SALAS)}

# ---------- Objetos nuevos ----------
casa_anims = []
for n in PUERTAS:
    w, h = tam("Casas/" + n); casa_anims.append(anim_def(n, [frame(img("Casas/" + n), (w // 2, h))]))
set_global_object(d, sprite_obj("CasaN", casa_anims, tween=False))
for v in ("DestEscena", "DestSala"): O["Interactivo"]["variables"].append(var(v, "string", ""))
for v in ("DestX", "DestY"): O["Interactivo"]["variables"].append(var(v, "number", 0))
MUEBLES = ("Estante", "EstanteBajo", "Cama", "Estufa", "Mesa", "MesaChica", "Mostrador", "Armario", "Barril", "Yunque", "Fragua", "Escritorio", "Cuadro", "Mapa", "Planta", "Chimenea", "Piano", "Vitrina", "Juguetes", "Red", "CanaPared", "Fuente", "Tumba", "Reja", "Banco", "Farol", "Pagina")
for m in MUEBLES:
    w, h = tam("Muebles/" + m); fr = frame(img("Muebles/" + m), (0, 0), rect(1, max(0, h - 12), w - 1, h))
    O["Interactivo"]["animations"].append(anim_def(m, [fr]))
ANIM = {a["name"]: k for k, a in enumerate(O["Interactivo"]["animations"])}

# ---------- Textos ----------
linea = lambda q_, t: {"type": "structure", "children": [var("Quien", "string", q_), var("Texto", "string", t)]}
N_ = "Narrador"; Pd = "Pedro"
TXT = {
 "MEstante": [(Pd, "Frascos, semillas y papel de envolver. Todo huele a tierra.")], "MBarril": [(Pd, "Un barril lleno. Mejor no me meto en problemas.")], "MArmario": [(Pd, "Ropa de trabajo y una cobija que aún huele a papá.")], "MEstufa": [(Pd, "Sigue tibia. Una sopa no me caería mal.")], "MMesa": [(Pd, "Una mesa sencilla, gastada de tantos desayunos.")], "MPlanta": [(Pd, "Alguien la cuida mejor de lo que yo cuidaría una.")], "MMapa": [(Pd, "Un mapa del valle. Hay una equis marcada sobre el bosque.")],
 "MCuadroPedro": [(Pd, "El tatarabuelo con su sombrero. Mismo sombrero, misma cara de terco.")], "MCuadroAlc": [(N_, "HetolMimiao, fundador de Papayork. Una placa dice: «Plantó primero, preguntó después».")], "MFragua": [("Fermin", "No toques eso, muchacho. Quema más que mi mal genio.")], "MYunque": [(Pd, "Tiene marcas de cien años de martillazos.")], "MJuguetes": [("Lupita", "¡No toques mi colección! Son para mi investigación de papas.")],
 "MRed": [("Tomas", "Esa red la tejió mi abuelo. Ha sacado más peces que la mitad del pueblo.")], "MCana": [(Pd, "Una caña vieja, reparada una y otra vez.")], "MPiano": [("Beto", "Lo tocaba mi madre. Ahora solo Lupita, y mejor no preguntes cómo.")], "MChimenea": [(Pd, "Da gusto sentarse aquí cuando afuera hace frío.")], "MVitrina": [("Ines", "Lo único que se salvó de la vieja escuela. Por favor, no apoyes las manos en el vidrio.")], "MEscritorio": [(Pd, "Papeles, sellos y un montón de cartas sin responder.")], "MLibros": [(N_, "«Tubérculos del valle: tomo IV». Bastante más emocionante de lo que parece.")],
 "MCamaLupita": [("Lupita", "¡Esa es mi cama! Ahí escondo los dibujos de la cueva.")], "MCamaTomas": [(Pd, "Un colchón duro. Huele a río.")],
 "Fuente": [(N_, "«A los que se fueron y a los que volvieron». Hay monedas en el fondo."), (Pd, "Me pregunto cuántos deseos caben ahí.")], "TumbaHetol": [(N_, "Aquí descansa la memoria de HetolMimiao. Su cuerpo nunca regresó al valle.")], "RejaReactor": [(N_, "PELIGRO. ZONA CERRADA POR ORDEN DE LA ALCALDÍA."), (Pd, "Más allá de esta reja se ve el reactor. La hierba brilla un poco.")], "Banco": [(Pd, "Buen sitio para ver pasar la tarde.")], "Farol": [(Pd, "Dicen que los encienden solos. Nadie ha visto quién.")],
 "CapillaCerrada": [(N_, "La capilla está cerrada desde la evacuación. El candado es muy viejo.")], "CasaCerrada": [(N_, "No hay nadie en casa. O prefieren no abrir.")], "CasaRosada": [(N_, "La familia Morales se fue a la ciudad. Dejaron las macetas regadas por un vecino.")],
 "Pagina1": [(N_, "Diario de HetolMimiao, página suelta:"), ("Hetol", "Hoy encontré una papa distinta a todas. Enorme, tibia al tacto. La llamo la Papa Madre, y de sus brotes salen las mejores cosechas del valle.")],
 "Pagina2": [(N_, "Página del diario, entre los archivos:"), ("Hetol", "Los hombres de la ciudad vinieron a preguntar por el suelo. Les interesa que aquí todo crezca el doble. No les conté de la Papa Madre.")],
 "Pagina3": [(N_, "Página del diario, escondida en un libro de pesca:"), ("Hetol", "Enterraron barriles junto al río de noche. Los peces salen con ojos raros. El reactor no es para dar luz: es para alimentarse de la tierra.")],
 "Pagina4": [(N_, "Página del diario, en la vitrina de Inés:"), ("Hetol", "La Papa Madre ya no está tibia: quema. Sus raíces beben lo que ellos vierten. Bajo la cueva del bosque late como un corazón.")],
 "Pagina5": [(N_, "Página del diario, bajo una piedra junto a la lápida:"), ("Hetol", "Si me pasa algo, que sepan que tapé la cueva con mis propias manos. No la maté. No pude. Es lo que nos dio todo.")],
 "Pagina6": [(N_, "Última página, atascada en la reja:"), ("Hetol", "A quien lleve mi sombrero: no huyas como hice yo. Entra a la cueva con un núcleo, un pico de hierro y valor. Termina lo que yo no pude.")],
 "EvDiario": [(Pd, "Ya están todas las páginas. La Papa Madre... de ahí viene todo."), (Pd, "El tatarabuelo no escapó solo del reactor. Escapó de lo que él mismo había cuidado."), (Pd, "Sé lo que tengo que hacer. La cueva del bosque.")],
 "Ines_0": [("Ines", "Bienvenido a la biblioteca. Silencio, por favor. Soy Inés."), ("Ines", "Si te interesa la historia del valle, aquí guardamos lo poco que quedó.")],
 "Ines_2": [("Ines", "Te he visto leer con cuidado. Eso es raro por aquí."), ("Ines", "HetolMimiao escribía un diario. Las páginas se perdieron por todo el pueblo durante la evacuación.")],
 "Ines_4": [("Ines", "Mi familia guarda una página desde hace generaciones. Está en la vitrina: es tuya por derecho."), ("Ines", "Dicen que otra quedó junto a la lápida del este, y otra en la reja del reactor.")],
 "Beto_0": [("Beto", "¡Bienvenido a La Papa Contenta! Sopa caliente y chismes frescos. Abro a las cuatro."), ("Beto", "Una buena sopa te devuelve más energía que dormir en la silla.")],
 "Beto_2": [("Beto", "Tomás viene todas las noches y nunca paga. Dice que me paga con historias."), ("Beto", "Pregúntale por el reactor cuando te tenga confianza.")],
 "Beto_4": [("Beto", "Mira, te cuento algo: Ramiro guarda archivos de la evacuación en la alcaldía."), ("Beto", "Una vez, tomado, dijo que entre ellos había papeles del mismísimo HetolMimiao.")],
}
hijos = V["Dialogos"]["children"]
for k, l in TXT.items():
    hijos.append({"name": k, "type": "array", "children": [linea(a, b) for a, b in l]})
V["NombresPersonajes"]["children"] += [var("Ines", "string", "Inés"), var("Beto", "string", "Beto")]

# ---------- Vecinos nuevos ----------
npc = O["NPC"]; base = next(a for a in npc["animations"] if a["name"] == "Rosa")["directions"][0]["sprites"][0]
for n in ("Ines", "Beto"):
    fs = []
    for k in (1, 1, 1, 1, 1, 2):
        fr = copy.deepcopy(base); fr["image"] = img(f"Vecinos/{n}{k}"); fs.append(fr)
    npc["animations"].append({"name": n, "useMultipleDirections": False, "directions": [{"looping": True, "timeBetweenFrames": .5, "sprites": fs}]})
    for dir_ in ("Abajo", "Arriba", "Izquierda", "Derecha"):
        fs = []
        for f in range(1, 5):
            fr = copy.deepcopy(base); fr["image"] = img(f"Vecinos/{n}_{dir_}{f}"); fs.append(fr)
        npc["animations"].append({"name": f"{n}_{dir_}", "useMultipleDirections": False, "directions": [{"looping": True, "timeBetweenFrames": .13, "sprites": fs}]})
    O["Retrato"]["animations"].append(anim_def(n, [frame(img("Retratos/" + n))]))
    O["RetratoMini"]["animations"].append(anim_def(n, [frame(img("Retratos/" + n))]))
vacia = lambda: [var("Puntos", "number", 0), var("HabloHoy", "boolean", False), var("RegalosHoy", "number", 0), var("RegalosSemana", "number", 0), var("Premio2", "boolean", False)]
V["Amistad"]["children"] += [struct(n, vacia()) for n in ("Ines", "Beto")]
gust = lambda ama, gusta, dis, odia, pid, pc, fr: struct(fr[5], [var("Ama", "string", ama), var("Gusta", "string", gusta), var("Disgusta", "string", dis), var("Odia", "string", odia), var("PremioId", "string", pid), var("PremioCant", "number", pc),
    var("FraseAma", "string", fr[0]), var("FraseGusta", "string", fr[1]), var("FraseDisgusta", "string", fr[2]), var("FraseOdia", "string", fr[3]), var("FraseNeutra", "string", fr[4])])
V["Gustos"]["children"] += [
  gust("|Cristal|Mojarra|", "|Papa|Resina|Fibra|", "|Bagre|Carbon|", "|PapaRadiactiva|Hongo|", "Semillas de Papa", 3, ("Esto merece su propia ficha en el archivo. Gracias, Pedro.", "Muy amable. Lo anotaré.", "Hm. Interesante... supongo.", "Por favor, saca eso de mi biblioteca.", "Gracias.", "Ines")),
  gust("|Papa|Zanahorias|Carpita|", "|Bagre|Trucha|Hongo|", "|Piedra|Fibra|", "|PapaRadiactiva|Nucleo|", "SopaPapa", 3, ("¡Eso va directo a la olla! Te debo una sopa.", "Buen producto. Se nota la mano.", "¿Y esto cómo se cocina?", "¡Fuera de mi cocina con eso!", "Gracias, compadre.", "Beto"))]
RU = next(v for v in d["variables"] if v["name"] == "Amistad")
# ---------- Comida de la taberna ----------
ref = O["Recursos"]["animations"][0]["directions"][0]["sprites"][0]
for n, nom, en, pre, des in (("SopaPapa", "Sopa de papa", 45, 12, "Espesa y calientita."), ("PanZanahoria", "Pan de zanahoria", 25, 6, "Dulce y recién horneado.")):
    V["Items"]["children"].append(struct(n, [var("Descripcion", "string", f"{des} Clic derecho: comer (+{en} de energía)."), var("Energia", "number", en), var("Max", "number", 99), var("Nombre", "string", nom), var("Precio", "number", pre), var("Rareza", "string", "Común"), var("Tipo", "string", "Comida")]))
    r_ = img("Objetos/" + n); O["IconoItem"]["animations"].append(anim_def(n, [frame(r_, (16, 16))]))
    fr = frame(r_); fr["hasCustomCollisionMask"], fr["customCollisionMask"] = True, copy.deepcopy(ref["customCollisionMask"]); O["Recursos"]["animations"].append(anim_def(n, [fr]))
oferta = lambda i, p_: {"type": "structure", "children": [var("Id", "string", i), var("Precio", "number", p_), var("Tipo", "string", "Item")]}
V["Tiendas"]["children"].append({"name": "Taberna", "type": "array", "children": [oferta("SopaPapa", 25), oferta("PanZanahoria", 14)]})

# ---------- Pueblo: casas ----------
inst_ = PU["instances"]
PU["instances"] = inst_ = [i for i in inst_ if i["name"] not in ("Casa1", "Puesto")]
def colision(lst, x, y, w, h): c = inst("Colision", x, y, w=w, h=h); lst.append(c); return c
def puerta_i(lst, x, y, dialogo="Puerta", dest="", sala="", dx=0, dy=0):
    i = inst("Interactivo", x, y, variables=[var("Dialogo", "string", dialogo), var("Solido", "boolean", False), var("DestEscena", "string", dest), var("DestSala", "string", sala), var("DestX", "number", dx), var("DestY", "number", dy)])
    i["numberProperties"] = [{"name": "animation", "value": ANIM["Puerta"]}]; i["zOrder"] = y + 24; lst.append(i); return i
def mueble(lst, nombre, x, base, dialogo, solido=True):
    w, h = tam("Muebles/" + nombre)
    i = inst("Interactivo", x, base - h, variables=[var("Dialogo", "string", dialogo), var("Solido", "boolean", solido)])
    i["numberProperties"] = [{"name": "animation", "value": ANIM[nombre]}]; i["zOrder"] = base; lst.append(i); return i
CASAS = [  # tipo, centro x, base y, sala (o diálogo si está cerrada)
 ("Nordica", 760, 300, "Mercado"), ("Verde", 885, 296, "!CasaCerrada"), ("Minera", 950, 420, "Herreria"), ("Alcaldia", 1132, 300, "Alcaldia"),
 ("Cottage", 1060, 600, "Lupita"), ("Rosada", 1180, 600, "!CasaRosada"), ("Pescador", 102, 322, "Tomas"), ("Rosada", 1234, 30, "!CasaCerrada"),
 ("Taberna", 1720, 350, "Taberna"), ("Biblioteca", 2020, 350, "Biblioteca"), ("Capilla", 2300, 300, "!CapillaCerrada"), ("Verde", 1560, 300, "!CasaCerrada"), ("Rosada", 2200, 620, "!CasaCerrada"), ("Verde", 1600, 620, "!CasaCerrada")]
HUECOS = []; DOOR = {}
ids = list(PUERTAS)
for tipo, cx, by, sala in CASAS:
    ci = inst("CasaN", cx, by, z=by); ci["numberProperties"] = [{"name": "animation", "value": ids.index(tipo)}]; inst_.append(ci)
    w, h = tam("Casas/" + tipo); dx = PUERTAS[tipo][0] - w // 2; door = cx + dx
    alto = min(70, h - 40)
    colision(inst_, cx - w // 2 + 10, by - alto, w - 20, alto - 2)
    HUECOS.append((cx - w // 2 - 6, by - h + 10, cx + w // 2 + 6, by + 22))
    if sala.startswith("!"):
        puerta_i(inst_, door - 16, by - 14, sala[1:])
    else:
        fx, fy = door, by + 20
        puerta_i(inst_, door - 16, by - 14, "Puerta", "Interior", sala, OX[sala] + 240, 244)
        DOOR[sala] = (door, by + 18, fx, fy)
# Quitar lo que estorbe a las casas nuevas
def dentro(x, y, h_): return h_[0] < x < h_[2] and h_[1] < y < h_[3]
inst_[:] = [i for i in inst_ if not (i["name"] in ("Arbol", "Arbol_2", "Arbol_3", "Arbusto", "Silla", "Roca_1", "Pozo_") and any(dentro(i["x"], i["y"], h_) for h_ in HUECOS))]
inst_[:] = [i for i in inst_ if not (i["name"] == "Interactivo" and any(v.get("value") == "Tablon" for v in i["initialVariables"]) and False)]
# Mover el tablón a la plaza libre
tablon = next(i for i in inst_ if i["name"] == "Interactivo" and any(v.get("value") == "Tablon" for v in i["initialVariables"]))
tablon["x"], tablon["y"] = 690, 330

# ---------- Barrio este: se abre el bosque y se amplía el mapa ----------
limite = next(v for v in PU["variables"] if v["name"] == "LimiteCamara")
for c in limite["children"]:
    if c["name"] == "Derecha": c["value"] = 2780
next(i for i in inst_ if i["name"] == "Suelo_Pasto")["width"] = 2900
inst_[:] = [i for i in inst_ if not (i["name"] == "Colision" and i["x"] >= 1395 and -240 <= i["y"] <= 640)]
for i in inst_:
    if i["name"] == "Bosque_Delimitador":
        p = next(q for q in i["stringProperties"] if q["name"] == "tilemap"); t = json.loads(p["value"])
        for lay in t["layers"]:
            for ry, fila in enumerate(lay["tiles"]):
                for rx in range(len(fila)):
                    if i["x"] + rx * 32 >= 1405 and fila[rx] != -1: fila[rx] = -1
            tl = lay["tiles"]
            hay = lambda a, b: 0 <= b < len(tl) and 0 <= a < len(tl[b]) and tl[b][a] != -1
            col_borde = int((1405 - i["x"]) // 32) - 1
            for ry in range(len(tl)):
                if 0 <= col_borde < len(tl[ry]) and tl[ry][col_borde] != -1:
                    fil = 0 if not hay(col_borde, ry - 1) else 2 if not hay(col_borde, ry + 1) else 1
                    tl[ry][col_borde] = fil * 3 + 2
        p["value"] = json.dumps(t, separators=(",", ":"))
def mapa_autotile(x0, y0, w, h, ocupado, nombre, z):
    fila = lambda ry: [(1 if ocupado(x0 + rx * 32, y0 + ry * 32) else 0) for rx in range(w)]
    M = [fila(r) for r in range(h)]
    hay = lambda a, b: 0 <= b < h and 0 <= a < w and M[b][a]
    tiles = [[(((0 if not hay(a, b - 1) else 2 if not hay(a, b + 1) else 1) * 3 + (0 if not hay(a - 1, b) else 2 if not hay(a + 1, b) else 1)) if M[b][a] else -1) for a in range(w)] for b in range(h)]
    t = {"tileWidth": 32, "tileHeight": 32, "dimX": w, "dimY": h, "layers": [{"id": 0, "alpha": 1, "tiles": tiles}]}
    i = inst(nombre, x0, y0, z=z); i["stringProperties"] = [{"name": "tilemap", "value": json.dumps(t, separators=(",", ":"))}]
    inst_.append(i)
def en_rect(x, y, rs): return any(a <= x < a + w and b <= y < b + h for a, b, w, h in rs)
CALLES = [(1200, 368, 1400, 64), (1760, 368, 224, 160), (2272, 304, 64, 96), (2336, 400, 64, 192), (2352, 560, 192, 64), (2464, 112, 64, 288), (1680, 352, 80, 32), (1984, 352, 72, 32), (1640, 432, 40, 200), (2180, 432, 40, 200), (1040, 430, 40, 180)]
mapa_autotile(1040, 96, 80, 24, lambda x, y: en_rect(x, y, CALLES), "SueloPiedra", -7900)
mapa_autotile(1376, -320, 46, 40, lambda x, y: not (x < 2700 and -224 <= y < 690), "Bosque_Delimitador", -5500)
colision(inst_, 1340, -256, 1400, 32); colision(inst_, 2700, -256, 32, 1000); colision(inst_, 1450, 700, 1282, 32); colision(inst_, 1453, 638, 32, 66)
# Detalles del barrio
for n, x, b, t_ in (("Fuente", 1834, 500, "Fuente"), ("Tumba", 2450, 548, "TumbaHetol"), ("Reja", 2452, 118, "RejaReactor"), ("Banco", 1790, 540, "Banco"), ("Banco", 1930, 540, "Banco"), ("Banco", 1500, 366, "Banco"), ("Farol", 1740, 366, "Farol"), ("Farol", 1990, 366, "Farol"), ("Farol", 2240, 440, "Farol"), ("Farol", 1500, 440, "Farol"), ("Farol", 1240, 362, "Farol")):
    mueble(inst_, n, x, b, t_)
mueble(inst_, "Pagina", 2486, 556, "Pagina5", False); mueble(inst_, "Pagina", 2500, 132, "Pagina6", False)
import random
R_ = random.Random(24); pos = []
ocupado_h = HUECOS + [(a - 26, b - 26, a + w + 26, b + h + 40) for a, b, w, h in CALLES]
tent = 0
while len(pos) < 46 and tent < 2000:
    tent += 1; x, y = R_.randint(1480, 2680), R_.randint(-200, 680)
    if any(dentro(x, y, h_) for h_ in ocupado_h) or any(abs(x - a) < 60 and abs(y - b) < 50 for a, b in pos): continue
    pos.append((x, y)); nm = R_.choice(("Arbol", "Arbol", "Arbol_2", "Arbol_3", "Arbusto", "Arbusto"))
    inst_.append(inst(nm, x, y, z=y))

# ---------- Pedro duerme en su cama: la puerta de la granja ahora entra a casa ----------
N1 = L["Nivel 01"]
pu_n = next(i for i in N1["instances"] if i["name"] == "Interactivo" and any(v.get("value") == "Dormir" for v in i["initialVariables"]))
for v in pu_n["initialVariables"]:
    if v["name"] == "Dialogo": v["value"] = "Puerta"
pu_n["initialVariables"] += [var("DestEscena", "string", "Interior"), var("DestSala", "string", "Pedro"), var("DestX", "number", OX["Pedro"] + 240), var("DestY", "number", 244)]
DOOR["Pedro"] = (pu_n["x"] + 16, pu_n["y"] + 40, pu_n["x"] + 16, pu_n["y"] + 46)

# ---------- Escena Interior ----------
I = copy.deepcopy(PU)
I["name"] = "Interior"; I["instances"] = []; I["r"], I["v"], I["b"] = 20, 14, 20
I["objects"] = [sprite_obj("SalaFondo", [anim_def(s, [frame(img("Salas/" + s))]) for s in SALAS], tween=False)]
I["objectsFolderStructure"] = {"folderName": "__ROOT", "children": [{"objectName": "SalaFondo"}]} if "objectsFolderStructure" in I else None
if I["objectsFolderStructure"] is None: I.pop("objectsFolderStructure")
eis = I["instances"]
eis.append(inst(PJ, 240, 244, z=247)); eis.append(inst("AvisoNPC", -900, -900, z=100000)); eis.append(inst("AvisoInteractivo", -900, -900, z=100000))
MB = {
 "Pedro": [("Cama", 30, 128, "Dormir"), ("Armario", 96, 66, "MArmario"), ("Estufa", 400, 70, "MEstufa"), ("Mesa", 212, 186, "MMesa"), ("Cuadro", 224, 40, "MCuadroPedro", False), ("EstanteBajo", 150, 64, "MLibros"), ("Planta", 432, 244, "MPlanta")],
 "Mercado": [("Mostrador", 155, 150, "MEstante"), ("Estante", 30, 66, "MEstante"), ("Estante", 390, 66, "MEstante"), ("Barril", 24, 232, "MBarril"), ("Barril", 50, 246, "MBarril"), ("Planta", 430, 240, "MPlanta"), ("Pagina", 436, 92, "Pagina1", False)],
 "Herreria": [("Fragua", 40, 84, "MFragua"), ("Yunque", 130, 126, "MYunque"), ("Mostrador", 155, 170, "MEstante"), ("Armario", 410, 66, "MArmario"), ("Barril", 24, 230, "MBarril"), ("Barril", 440, 240, "MBarril")],
 "Alcaldia": [("Escritorio", 204, 120, "MEscritorio"), ("Cuadro", 223, 40, "MCuadroAlc", False), ("Mapa", 60, 40, "MMapa", False), ("Estante", 390, 66, "MLibros"), ("Armario", 340, 66, "MEscritorio"), ("Planta", 30, 80, "MPlanta"), ("Planta", 430, 244, "MPlanta"), ("Pagina", 348, 92, "Pagina2", False)],
 "Lupita": [("Cama", 40, 130, "MCamaLupita"), ("Juguetes", 380, 92, "MJuguetes"), ("Mesa", 212, 176, "MMesa"), ("EstanteBajo", 120, 64, "MLibros"), ("Planta", 430, 244, "MPlanta")],
 "Tomas": [("Cama", 396, 132, "MCamaTomas"), ("Red", 40, 40, "MRed", False), ("CanaPared", 120, 38, "MCana", False), ("Estufa", 300, 68, "MEstufa"), ("Mesa", 150, 176, "MMesa"), ("Barril", 30, 232, "MBarril"), ("Pagina", 176, 136, "Pagina3", False)],
 "Taberna": [("Mostrador", 40, 130, "MBarril"), ("Barril", 20, 74, "MBarril"), ("Barril", 44, 74, "MBarril"), ("Barril", 68, 74, "MBarril"), ("Chimenea", 380, 68, "MChimenea"), ("Mesa", 270, 170, "MMesa"), ("Mesa", 372, 210, "MMesa"), ("Mesa", 100, 230, "MMesa"), ("Piano", 262, 64, "MPiano")],
 "Biblioteca": [("Estante", 20, 66, "MLibros"), ("Estante", 86, 66, "MLibros"), ("Estante", 334, 66, "MLibros"), ("Estante", 400, 66, "MLibros"), ("Escritorio", 204, 130, "MEscritorio"), ("Vitrina", 390, 200, "MVitrina"), ("Mesa", 70, 190, "MLibros"), ("Pagina", 405, 158, "Pagina4", False)],
}
for s in SALAS:
    ox = OX[s]; f = inst("SalaFondo", ox, 0, z=-9000); f["numberProperties"] = [{"name": "animation", "value": SALAS.index(s)}]; eis.append(f)
    for a, b, w, h in ((0, 0, 480, 58), (0, 0, 12, 288), (468, 0, 12, 288), (0, 274, 480, 14)):
        colision(eis, ox + a, b, w, h)
    for m in MB[s]:
        mueble(eis, m[0], ox + m[1], m[2], m[3], (m[4] if len(m) > 4 else True))
    a_ = DOOR[s]
    puerta_i(eis, ox + 224, 254, "Puerta", "Nivel 01" if s == "Pedro" else "Pueblo", "", a_[2], a_[3])
# ---------- Vecinos en Pueblo y en Interior ----------
NPCS = {"Rosa": ("Mercado", "Doña Rosa: ¡Las mejores semillas del valle!"), "Fermin": ("Herreria", "Don Fermín: Trae lingotes y te forjo algo bueno."), "Ramiro": ("Ramiro", ""), "Lupita": ("Lupita", ""), "Tomas": ("Tomas", ""), "Ines": ("Ines", ""), "Beto": ("Taberna", "Beto: ¿Qué te sirvo, compadre?")}
inst_[:] = [i for i in inst_ if i["name"] != "NPC"]
anim_npc = {a["name"]: k for k, a in enumerate(npc["animations"])}
npc["variables"].append(var("Fuera", "boolean", True))
for lst in (inst_, eis):
    for n, (t_, sal) in NPCS.items():
        i = inst("NPC", -5000, -5000, variables=[var("Tienda", "string", t_), var("Saludo", "string", sal), var("Vecino", "string", n)]); i["numberProperties"] = [{"name": "animation", "value": anim_npc[n]}]; lst.append(i)

# ---------- Rutinas con lugar: entran y salen de sus casas ----------
D = DOOR
RUTAS = {
 "Rosa": [(6, "Mercado", 110, 110), (8.8, "Mercado", 240, 136), (17, "Mercado", 240, 250), (17.3, "Pueblo", *D["Mercado"][2:]), (17.6, "Pueblo", 700, 345), (20, "Pueblo", *D["Mercado"][2:]), (20.3, "Mercado", 240, 250), (20.5, "Mercado", 110, 110)],
 "Fermin": [(6, "Herreria", 90, 130), (8.8, "Herreria", 240, 156), (18, "Herreria", 240, 250), (18.3, "Pueblo", *D["Herreria"][2:]), (18.6, "Pueblo", 1060, 460), (20.5, "Pueblo", *D["Herreria"][2:]), (20.8, "Herreria", 240, 250), (21, "Herreria", 90, 130)],
 "Ramiro": [(6, "Alcaldia", 240, 106), (12, "Alcaldia", 240, 250), (12.2, "Pueblo", *D["Alcaldia"][2:]), (12.4, "Pueblo", 1060, 445), (13.5, "Pueblo", *D["Alcaldia"][2:]), (13.8, "Alcaldia", 240, 250), (14, "Alcaldia", 240, 106), (17.5, "Alcaldia", 240, 250), (17.7, "Pueblo", *D["Alcaldia"][2:]), (18, "Pueblo", *D["Taberna"][2:]), (18.6, "Taberna", 240, 250), (18.8, "Taberna", 310, 190), (21, "Taberna", 240, 250), (21.2, "Pueblo", *D["Taberna"][2:]), (21.9, "Pueblo", *D["Alcaldia"][2:]), (22.3, "Alcaldia", 240, 250), (22.5, "Alcaldia", 240, 106)],
 "Lupita": [(6, "Lupita", 300, 190), (8.5, "Lupita", 240, 250), (8.7, "Pueblo", *D["Lupita"][2:]), (8.8, "Pueblo", 1000, 620), (8.95, "Pueblo", 1000, 500), (9.1, "Pueblo", 1010, 445), (11, "Pueblo", 1880, 530), (13, "Pueblo", 1010, 445), (15, "Pueblo", 700, 430), (17, "Pueblo", 1010, 445), (18, "Pueblo", 1000, 500), (18.15, "Pueblo", 1000, 620), (18.3, "Pueblo", *D["Lupita"][2:]), (18.6, "Lupita", 240, 250), (19, "Lupita", 300, 190)],
 "Tomas": [(6, "Tomas", 250, 214), (6.8, "Tomas", 240, 250), (7, "Pueblo", *D["Tomas"][2:]), (7.3, "Pueblo", 316, 359), (12, "Pueblo", 330, 395), (15, "Pueblo", 316, 359), (20, "Pueblo", *D["Tomas"][2:]), (20.4, "Tomas", 240, 250), (20.6, "Tomas", 250, 214)],
 "Ines": [(6, "Biblioteca", 90, 120), (9, "Biblioteca", 240, 116), (18, "Biblioteca", 240, 250), (18.3, "Pueblo", *D["Biblioteca"][2:]), (18.5, "Pueblo", 1880, 530), (20, "Pueblo", *D["Biblioteca"][2:]), (20.2, "Biblioteca", 240, 250), (20.4, "Biblioteca", 90, 120)],
 "Beto": [(6, "Taberna", 420, 120), (15.8, "Taberna", 120, 116)],
}
HOR = {"Rosa": (9, 17), "Fermin": (9, 18), "Beto": (16, 26)}
paredes = [(i["x"], i["y"], i["x"] + (i.get("width") or 32), i["y"] + (i.get("height") or 32)) for i in inst_ if i["name"] == "Colision"]
for n, r in RUTAS.items():
    if n == "Tomas": continue
    for (_, l0, x0, y0), (_, l1, x1, y1) in zip(r, r[1:]):
        if l0 != "Pueblo" or l1 != "Pueblo": continue
        for k in range(81):
            x, y = x0 + (x1 - x0) * k / 80, y0 + (y1 - y0) * k / 80
            for a, b, c_, e in paredes:
                assert not (a < x < c_ and b < y < e), (n, "pared", round(x), round(y), (a, b, c_, e))
def px_(l, x): return x + OX.get(l, 0)
next(v for v in d["variables"] if v["name"] == "Rutinas")["children"] = [{"name": n, "type": "structure", "children": [var("Abre", "number", HOR.get(n, (0, 0))[0]), var("Cierra", "number", HOR.get(n, (0, 0))[1]),
    {"name": "Pasos", "type": "array", "children": [{"type": "structure", "children": [var("Hora", "number", h), var("Lugar", "string", l), var("X", "number", px_(l, x) - 16), var("Y", "number", y - 29)]} for h, l, x, y in ruta]}]} for n, ruta in RUTAS.items()]
for v in (var("SalaActual", "string", ""), var("LugarActual", "string", ""), var("DestLugar", "string", ""), var("EntroPuerta", "boolean", False)):
    set_global_var(d, v)
rut = EXT["Rutinas"]["events"]
fe = next(e for e in rut if e["type"].endswith("ForEach"))
RP = "Rutinas[NPC.Vecino].Pasos"
rut.insert(next(k for k, e in enumerate(rut) if e["type"].endswith("ForEach")), EV([], [sv("LugarActual", "CurrentSceneName()")], [EV([C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "=", q("Interior"))], [sv("LugarActual", "SalaActual")])]))
sub = fe["events"]
sub[0]["actions"].append(sv("DestLugar", "LugarActual"))
rep = sub[1]["events"][0]["events"][0]; assert "KRut" in json.dumps(rep["conditions"])
rep["actions"].append(sv("DestLugar", f"{RP}[KRut].Lugar"))
sub.insert(2, EV([isv("DestLugar", "LugarActual", "!=")], [hide("NPC"), A("SetXY", "NPC", "=", "-5000", "=", "-5000"), set_objv_b("NPC", "Fuera", "True")]))
cont = sub[3:]
fe["events"] = sub[:3] + [EV([isv("DestLugar", "LugarActual")], [show("NPC")], [EV([objv_b("NPC", "Fuera", "True")], [A("SetXY", "NPC", "=", "DestX", "=", "DestY"), set_objv_b("NPC", "Fuera", "False")])] + cont)]
fe["actions"].append(sv("DestLugar", "LugarActual"))
# ---------- Puertas ----------
mun = EXT["Mundo2"]["events"]
vis = mun[3]["events"][0]
click = next(e for e in vis["events"] if any(c["type"]["value"] == "MouseButtonFromTextReleased" for c in e.get("conditions", [])))
click["conditions"].append(objv_s("Interactivo", "Dialogo", q("Puerta"), "!="))
FUND = [A("Create", "", "Cortina", "0", "0", q("DialogoHD")), A("ResizableCapability::ResizableBehavior::SetWidth", "Cortina", "Resizable", "=", "960"), A("ResizableCapability::ResizableBehavior::SetHeight", "Cortina", "Resizable", "=", "540"), A("SetZOrder", "Cortina", "=", "999")]
vis["events"] += [
    EV([objv_s("Interactivo", "Dialogo", q("Puerta"))], [txt("AvisoInteractivo", q("Clic: entrar")), A("SetY", "AvisoInteractivo", "=", "Interactivo.Y() - 26")], [EV([objv_s("Interactivo", "DestEscena", q("Interior"), "!=")], [txt("AvisoInteractivo", q("Clic: salir")), A("SetY", "AvisoInteractivo", "=", "Interactivo.Y() + 10")])]),
    EV([objv_s("Interactivo", "Dialogo", q("Puerta")), C("IsCursorOnObject", "Interactivo", "", "", ""), C("MouseButtonFromTextReleased", "", q("Left"))],
       [nv("Posicion_Inicial_Jugador.X", "Interactivo.DestX"), nv("Posicion_Inicial_Jugador.Y", "Interactivo.DestY"), sv("SalaActual", "Interactivo.DestSala"), nv("Vida", f"{PJ}.Vida"), bv("EntroPuerta", "True"), snd("Menu/Hover.wav", 60), sv("EscenaAGuardar", "Interactivo.DestEscena"), A("Scene", "", "Interactivo.DestEscena", "")])]
mun[1]["events"].append(EV([ibv("EntroPuerta", "True")], [bv("EntroPuerta", "False")] + FUND + [tw_op("Cortina", "Entrar", 0, "easeOutQuad", .5, "yes")]))
# Interior: cámara por sala, sin noche
ie = I["events"]
ie[:] = [e for e in ie if e.get("target") != "PruebaZoom"]
mus = ie[2]; mus["events"] = []
sala_ev = [EV([isv("SalaActual", q(s))], [nv("LimiteCamara.Izquierda", str(OX[s])), nv("LimiteCamara.Derecha", str(OX[s] + 480)), nv("LimiteCamara.Arriba", "0"), nv("LimiteCamara.Abajo", "288")]) for s in SALAS]
ie.insert(2, EV([C("SceneJustBegins", "")], [], sala_ev))
ie.append(EV([], [A("SetLayerAmbientLightColor", "", q("Luz Exterior"), q("255;255;255"))]))
d["layouts"].append(I)
if "layoutsFolderStructure" in d: pass
# ---------- Tienda dentro de la casa; hablar un poco más lejos por el mostrador ----------
tie = EXT["Tienda"]["events"]
cerr = next(e for e in tie if e.get("events") and any("Cerrada" in json.dumps(s.get("conditions", [])) for s in e["events"]))
cerr["events"].insert(0, EV([C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "!=", q("Interior"))], [sv("TipoTienda", q("Cerrada"))]))
aviso = cerr["events"][-1]
aviso["actions"][1] = txt("TextoFlotante", '"Atiende dentro, de " + ToString(Rutinas[NPC.Vecino].Abre) + " a " + ToString(Rutinas[NPC.Vecino].Cierra) + " h"')
def mas_lejos(evs):
    for e in evs:
        for c in e.get("conditions", []) or []:
            if c["type"]["value"].endswith("CompareNumbers") and "NPC.X()" in c["parameters"][0] and c["parameters"][2] == "60": c["parameters"][2] = "72"
        mas_lejos(e.get("events", []) or [])
mas_lejos(tie); mas_lejos(EXT["Amistad"]["events"])
# ---------- Pestaña de vecinos con siete filas ----------
lay = next(l for l in d["externalLayouts"] if l["name"] == "InventarioStardew")
V7 = ("Rosa", "Fermin", "Ramiro", "Lupita", "Tomas", "Ines", "Beto")
lay["instances"] = [i for i in lay["instances"] if not (i["name"] in ("RetratoMini", "Corazon") or (i["name"] == "TextoPausa" and any(v.get("value") == "Vecinos" for v in i["initialVariables"]) and any(str(v.get("value")).startswith(("Nombre", "Estado")) for v in i["initialVariables"])))]
def tx(x, y, clave): return inst("TextoPausa", x, y, layer="Inventario", z=560, variables=[var("Clave", "string", clave), var("Pestana", "string", "Vecinos"), var("CX", "number", 0)])
ianim = {a["name"]: k for k, a in enumerate(O["RetratoMini"]["animations"])}
for f, n in enumerate(V7):
    y = 60 + f * 24
    r = inst("RetratoMini", 66, y, layer="Inventario", z=556, w=22, h=22); r["numberProperties"] = [{"name": "animation", "value": ianim[n]}]; lay["instances"].append(r)
    lay["instances"] += [tx(96, y + 5, "Nombre" + n), tx(290, y + 5, "Estado" + n)]
    for k in range(5): lay["instances"].append(inst("Corazon", 190 + k * 18, y + 4, layer="Inventario", z=556, variables=[var("Vecino", "string", n), var("N", "number", k + 1)]))
am = EXT["Amistad"]["events"]
tab = next(e for e in am if e.get("conditions") and len(e["conditions"]) == 2 and "Vecinos" in json.dumps(e["conditions"]))
for n in ("Ines", "Beto"):
    tab["events"] += [EV([objv_s("TextoPausa", "Clave", q("Nombre" + n))], [txt("TextoPausa", f"NombresPersonajes.{n}")]),
        EV([objv_s("TextoPausa", "Clave", q("Estado" + n))], [txt("TextoPausa", f'"Regalos " + ToString(Amistad.{n}.RegalosSemana) + "/2"')]),
        EV([objv_s("TextoPausa", "Clave", q("Estado" + n)), ibv(f"Amistad.{n}.HabloHoy", "True")], [txt("TextoPausa", f'"Hablaron hoy  " + ToString(Amistad.{n}.RegalosSemana) + "/2"')])]
menu = L["Menu Principal"]["events"]
limpia = {n: {"Puntos": 0, "HabloHoy": False, "RegalosHoy": 0, "RegalosSemana": 0, "Premio2": False} for n in V7}
a0 = next(a for a in menu[35]["actions"] if a["type"]["value"] == "JSONToGlobalVariableStructure" and a["parameters"][1] == "Amistad")
a0["parameters"][0] = q(json.dumps(limpia, separators=(",", ":")))
# ---------- Eventos: condición de sala, diario, mutación diferida ----------
ev_v = next(v for v in d["variables"] if v["name"] == "Eventos")
def cambiar(e_, k, val):
    next(c for c in e_["children"] if c["name"] == k)["value"] = val
for e_ in ev_v["children"]:
    e_["children"].append(var("Sala", "string", ""))
    if e_["name"] == "CuevaFermin":
        cambiar(e_, "Escena", "Interior"); next(c for c in e_["children"] if c["name"] == "Sala")["value"] = "Herreria"; cambiar(e_, "ZonaX", OX["Herreria"] + 240); cambiar(e_, "ZonaY", 200); cambiar(e_, "ZonaR", 120)
    if e_["name"] == "TomasReactor": cambiar(e_, "HoraMax", 20)
    if e_["name"] == "Llegada":
        for s_ in e_["children"]:
            if s_["name"] == "Pasos":
                for pa in s_["children"]:
                    c_ = {c["name"]: c for c in pa["children"]}
ev_v["children"].append({"name": "Diario", "type": "structure", "children": [var("Escena", "string", ""), var("HoraMin", "number", 6), var("HoraMax", "number", 30), var("Personaje", "string", ""), var("PuntosMin", "number", 0), var("EventoPrevio", "string", ""), var("Marca", "string", "DiarioCompleto"), var("ZonaX", "number", 0), var("ZonaY", "number", 0), var("ZonaR", "number", 0), var("Sala", "string", ""),
    {"name": "Pasos", "type": "array", "children": [{"type": "structure", "children": [var("Cmd", "string", "hablar"), var("A", "string", "EvDiario"), var("B", "number", 0), var("C", "number", 0)]}]}]})
K = "Eventos[ClaveEvento]"
eve = EXT["Eventos"]["events"]
rv = next(e for e in eve if e.get("events") and e["events"] and e["events"][0].get("iterableVariableName") == "Eventos")["events"][0]
primero = rv["events"][0]; primero["conditions"].append(isv(f"{K}.Escena", q(""), "!="))
rv["events"].insert(1, EV([isv(f"{K}.Sala", q(""), "!="), isv(f"{K}.Sala", "SalaActual", "!=")], [bv("EvOk", "False")]))
set_global_var(d, var("PaginasTotal", "number", 0))
eve[1:1] = [
    COM("Paginas del diario: al terminar de leer una se guarda y desaparece"),
    FOREACH("Interactivo", [C("BuiltinCommonInstructions::CompareNumbers", 'StrFind(Interactivo.Dialogo, "Pagina")', "=", "0"), C("SceneJustBegins", ""), C("VariableChildExists2", "EventosVistos", "Interactivo.Dialogo")], [A("Delete", "Interactivo", "")]),
    EV([cmp_('StrFind(DialogoTerminado, "Pagina")', "=", "0")], [nv("EventosVistos[DialogoTerminado]", "1"), nv('EventosVistos["Paginas"]', '1', '+'), A("Create", "", "TextoFlotante", f"{PJ}.CenterX() - 40", f"{PJ}.Y() - 58", q("")),
        txt("TextoFlotante", '"Página del diario: " + ToString(EventosVistos.Paginas) + "/6"'), A("TextObject::ChangeColor", "TextoFlotante", q("251;242;54")), A("SetZOrder", "TextoFlotante", "=", "100000"), tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", 2), tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 3, "yes"), snd("HUD/SubirNivel.wav", 50)], [
        EV([objv_s("Interactivo", "Dialogo", "DialogoTerminado")], [A("Delete", "Interactivo", "")]),
        EV([cmp_("EventosVistos.Paginas", ">=", "6")], [nv('EventosVistos["DiarioCompleto"]', "1")]),
        EV([], [sv("DialogoTerminado", q(""))])]),
]
next(v for v in d["variables"] if v["name"] == "EventosVistos")["children"].append(var("Paginas", "number", 0))
a1 = next(a for a in menu[35]["actions"] if a["type"]["value"] == "JSONToGlobalVariableStructure" and a["parameters"][1] == "EventosVistos")
a1["parameters"][0] = q('{"Inicio":1,"Paginas":0}')
# Si se duerme dentro de casa, la planta muta cuando Pedro vuelve a la granja
nd = EXT["NuevoDia"]["events"]
def buscar(evs):
    for e in evs:
        if "ProbMutante" in json.dumps(e.get("conditions", [])): return evs, e
        h_ = buscar(e.get("events", []) or [])
        if h_: return h_
lista, mu = buscar(nd)
bloque = copy.deepcopy(mu)
mu["conditions"] = [c for c in mu["conditions"] if "CurrentSceneName" not in json.dumps(c) and "SceneInstancesCount" not in json.dumps(c)]
mu["actions"] = [bv("Granja[ClaveGranja].Mutar", "True")]; mu["events"] = []
bloque["conditions"] = [c for c in bloque["conditions"] if "ProbMutante" not in json.dumps(c) and "Etapa" not in json.dumps(c)]
bloque["actions"] = [bv("Granja[ClaveGranja].Mutar", "False")] + bloque["actions"]
bloque["conditions"].append(ibv("Granja[ClaveGranja].Mutar", "True"))
cul = EXT["Cultivos"]["events"]
cul += [COM("Las plantas que mutaron de noche salen de la tierra cuando Pedro esta en esa zona"),
        EV([C("CompareTimer", "", q("RevisaMuta"), ">=", "1")], [A("ResetTimer", "", q("RevisaMuta"))], [{"type": "BuiltinCommonInstructions::ForEachChildVariable", "iterableVariableName": "Granja", "valueIteratorVariableName": "CeldaGranja", "keyIteratorVariableName": "ClaveGranja", "conditions": [], "actions": [], "events": [bloque]}])]
cul[1]["actions"].append(A("ResetTimer", "", q("RevisaMuta")))
# No se ara ni se construye dentro de las casas
her = EXT["Herramientas"]["events"]
az = her[3]["events"][3]; assert "Azadon" in json.dumps(az["conditions"])
az["conditions"].append(C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "!=", q("Interior")))
def no_interior(evs, objeto):
    for e in evs:
        if any(a["type"]["value"] == "Create" and a["parameters"][1] == objeto for a in e.get("actions", []) or []):
            e["conditions"] = (e.get("conditions") or []) + [C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "!=", q("Interior"))]
        no_interior(e.get("events", []) or [], objeto)
no_interior(EXT["Fabricacion"]["events"], "Construccion")
# Profundidad de lo nuevo
pr = EXT["Profundidad"]["events"]
pr[1]["actions"].append(A("SetZOrder", "CasaN", "=", "CasaN.Y()"))
# Guardar y cargar la sala
gu = EXT["Guardado"]["events"][2]["events"]
gu[8]["actions"].insert(next(k for k, a in enumerate(gu[8]["actions"]) if a["type"]["value"] == "SetStringVariable"), A("EcrireFichierTxt", q("PapayorkPartidas"), '"Ranura" + ToString(RanuraActual) + "/SalaActual"', "ToJSON(SalaActual)"))
gu.insert(8, EV([isv("EscenaAGuardar", q("Interior"))], [sv("Zona", q("Dentro de una casa"))]))
carga = menu[37]["events"]
idx = next(k for k, e in enumerate(carga) if "/Granja" in json.dumps(e, ensure_ascii=False))
carga.insert(idx + 1, json.loads(json.dumps(carga[idx], ensure_ascii=False).replace('/Granja\\"', '/SalaActual\\"').replace('"Granja"', '"SalaActual"')))
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("casas:", len(CASAS), "arboles nuevos:", len(pos), "instancias Pueblo:", len(inst_), "Interior:", len(eis))
print("ok")
