"""Mina con pisos generados al azar, tres zonas, descansos cada 5 pisos y seis enemigos que persiguen a Pedro.
El generador es un evento de JavaScript dentro de la escena Mina. Cada piso se crea de nuevo al bajar."""
import json, sys, os, copy
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *
from PIL import Image
P = sys.argv[1]
RAIZ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
d = json.load(open(P, encoding="utf8"))
if any(l["name"] == "Mina" for l in d["layouts"]):
    sys.exit("Este cambio ya está aplicado; no se cambió nada.")
O = {o["name"]: o for o in d["objects"]}; EXT = {e["name"]: e for e in d["externalEvents"]}; L = {l["name"]: l for l in d["layouts"]}; V = {v["name"]: v for v in d["variables"]}
PJ = "Personaje_jugador"; PU = L["Pueblo"]
cmp_ = lambda a, op, b: C("BuiltinCommonInstructions::CompareNumbers", a, op, b)
def img(r):
    n = "Natural/" + r + ".png"; add_resource(d, "image", n, n); return n
def tam(r): return Image.open(os.path.join(RAIZ, "Natural", r + ".png")).size
# ---------- Datos ----------
DATOS = {"Brotecito": (6, 34, 4, 190, 4, 3, "Fibra"), "Murcipapa": (5, 62, 5, 240, 5, 4, "Resina"), "Topapa": (10, 50, 6, 260, 8, 6, "Carbon"), "Escarabajo": (14, 44, 8, 230, 10, 8, "Cobre"), "Golem": (30, 22, 12, 300, 18, 14, "Hierro"), "Espora": (9, 30, 9, 240, 12, 10, "Cristal")}
set_global_var(d, struct("Enemigos", [struct(k, [var("Vida", "number", v[0]), var("Vel", "number", v[1]), var("Dano", "number", v[2]), var("Alcance", "number", v[3]), var("Exp", "number", v[4]), var("Monedas", "number", v[5]), var("Suelta", "string", v[6])]) for k, v in DATOS.items()]))
for v in (var("MinaPiso", "number", 1), var("MinaCheckpoint", "number", 1), var("MinaGenerar", "boolean", False), var("MinaEscalera", "boolean", False), var("MinaRota", "boolean", False), var("RocaX", "number", 0), var("RocaY", "number", 0), var("DistEn", "number", 0), var("GolpeEn", "number", 0), var("DistEsc", "number", 999)):
    set_global_var(d, v)
# ---------- Objetos ----------
def enem(n):
    w, h = tam(f"Mina/{n}1")
    return anim_def(n, [frame(img(f"Mina/{n}{f}"), (w // 2, h), rect(3, max(0, h - min(h, 22)), w - 3, h)) for f in range(1, 5)], loop=True, dt=0.14)
set_global_object(d, sprite_obj("EnemigoMina", [enem(n) for n in DATOS], variables=[var("Tipo", "string", "Brotecito"), var("Vida", "number", 0), var("Vel", "number", 30), var("Dano", "number", 5), var("Alcance", "number", 200), var("Iniciado", "boolean", False), var("Fase", "number", 0)]))
w_, h_ = tam("Mina/EscaleraBajar")
set_global_object(d, sprite_obj("EscaleraMina", [anim_def("Bajar", [frame(img("Mina/EscaleraBajar"))])], tween=False))
set_global_object(d, {"assetStoreId": "", "name": "MinaMapa", "persistentUuid": uid(), "type": "TileMap::SimpleTileMap", "variables": [], "effects": [], "behaviors": [], "content": {"atlasImage": img("Mina/Atlas"), "rowCount": 3, "columnCount": 20, "tileSize": 32, "tilesWithHitBox": ""}})
set_global_object(d, text_obj("TextoMina", "Piso 1", size=18, rgb=(255, 236, 170), outline=(40, 24, 16)))
for n, r_ in (("EntradaMina", "Mina/Entrada"), ("EscaleraArriba", "Mina/EscaleraSubir")):
    w, h = tam(r_); O["Interactivo"]["animations"].append(anim_def(n, [frame(img(r_), (0, 0), rect(0, max(0, h - 10), w, h))]))
ANIM = {a["name"]: k for k, a in enumerate(O["Interactivo"]["animations"])}
# ---------- Entrada en el Bosque ----------
N2 = L["Nivel 02"]
# El dibujo es decorado; la puerta es una zona pequeña al pie de la entrada, para que el clic no se confunda con otros objetos
w, h = tam("Mina/Entrada")
O["Decorado"]["animations"].append(anim_def("EntradaMina", [frame(img("Mina/Entrada"), (0, 0), rect(0, h - 10, w, h))]))
dec = inst("Decorado", 490, 36, z=120); dec["numberProperties"] = [{"name": "animation", "value": len(O["Decorado"]["animations"]) - 1}]; N2["instances"].append(dec)
ent = inst("Interactivo", 529, 98, z=122, variables=[var("Dialogo", "string", "Puerta"), var("Solido", "boolean", False), var("DestEscena", "string", "Mina"), var("DestSala", "string", ""), var("DestX", "number", 0), var("DestY", "number", 0)])
ent["numberProperties"] = [{"name": "animation", "value": ANIM["Puerta"]}]; N2["instances"].append(ent)
# Enemigos también por el bosque y en la zona contaminada de la granja
papas = [i for i in N2["instances"] if i["name"] == "Papa"]
for k, i in enumerate(papas):
    e_ = inst("EnemigoMina", i["x"] + 70, i["y"] + 40, z=i["y"], variables=[var("Tipo", "string", ("Brotecito", "Brotecito", "Murcipapa")[k % 3])]); N2["instances"].append(e_)
charcos = [i for i in L["Nivel 01"]["instances"] if i["name"] == "Decorado" and i["y"] > 300 and i["x"] > 300][:2]
for i in charcos:
    L["Nivel 01"]["instances"].append(inst("EnemigoMina", i["x"] + 30, i["y"] + 60, z=i["y"], variables=[var("Tipo", "string", "Brotecito")]))
# ---------- Comportamiento de los enemigos ----------
EN = "EnemigoMina"; T_ = lambda t: objv_s(EN, "Tipo", q(t))
FUERZA = lambda v: A("AddForceTowardPosition", EN, f"{PJ}.X()", f"{PJ}.Y() - 8", v, "0")
per_ev = EXT["Personaje"]["events"]
contacto = next(e for e in per_ev if "Invencible" in json.dumps(e.get("conditions", [])) and "CollisionNP" in json.dumps(e.get("conditions", [])))
choque = json.loads(json.dumps(contacto, ensure_ascii=False).replace("Papa.", "EnemigoMina.").replace('"Papa"', '"EnemigoMina"'))
for a in choque["actions"]:
    if a["parameters"][:3] == [PJ, "Vida", "-"]: a["parameters"][3] = "EnemigoMina.Dano"
def flot(t, c):
    return [A("Create", "", "TextoFlotante", f"{EN}.X() - 16", f"{EN}.Y() - 30", q("")), txt("TextoFlotante", t), A("TextObject::ChangeColor", "TextoFlotante", q(c)), A("SetZOrder", "TextoFlotante", "=", "100000"), tw_y("TextoFlotante", "Subir", "TextoFlotante.Y() - 20", "easeOutQuad", .9), tw_op("TextoFlotante", "Desaparecer", 0, "easeInQuad", 1.3, "yes")]
D_ = f"Enemigos[{EN}.Tipo]"
SEP = lambda obj: EV([C("CollisionNP", EN, obj, "", "", ""), objv_s(EN, "Tipo", q("Murcipapa"), "!=")], [A("SeparateFromObjects", EN, obj, "")])
eventos = [
    COM("ENEMIGOS QUE PERSIGUEN. Enemigos[tipo] tiene sus datos. Cada tipo se mueve distinto cuando Pedro entra en su alcance."),
    FOREACH(EN, [objv_b(EN, "Iniciado", "False")], [set_objv_b(EN, "Iniciado", "True"), anim(EN, f"{EN}.Tipo"), set_objv_n(EN, "Vida", f"{D_}.Vida"), set_objv_n(EN, "Vel", f"{D_}.Vel"), set_objv_n(EN, "Dano", f"{D_}.Dano"), set_objv_n(EN, "Alcance", f"{D_}.Alcance"), set_objv_n(EN, "Fase", "RandomFloat(6)"), A("ResetObjectTimer", EN, q("Golpe"))], [
        EV([C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "=", q("Mina"))], [set_objv_n(EN, "Vida", f"{EN}.Vida * (1 + MinaPiso * 0.05)"), set_objv_n(EN, "Dano", f"{EN}.Dano + floor(MinaPiso / 6)")])]),
    FOREACH(EN, [ibv("InventarioAbierto", "False")], [nv("DistEn", f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), {EN}.X(), {EN}.Y())"), A("SetZOrder", EN, "=", f"{EN}.Y()")], [
        EV([cmp_(f"{PJ}.X()", ">", f"{EN}.X()")], [A("FlipX", EN, "yes")]),
        EV([cmp_(f"{PJ}.X()", "<=", f"{EN}.X()")], [A("FlipX", EN, "no")]),
        EV([cmp_("DistEn", "<", f"{EN}.Alcance")], [], [
            EV([T_("Brotecito")], [FUERZA(f"{EN}.Vel * (0.4 + abs(sin(TimeFromStart() * 5 + {EN}.Fase)))")]),
            EV([T_("Murcipapa")], [FUERZA(f"{EN}.Vel"), A("AddForceXY", EN, f"cos(TimeFromStart() * 3 + {EN}.Fase) * 46", f"sin(TimeFromStart() * 4.3 + {EN}.Fase) * 46", "0")]),
            EV([T_("Topapa")], [FUERZA(f"{EN}.Vel")]),
            EV([T_("Escarabajo"), cmp_(f"mod(TimeFromStart() + {EN}.Fase, 2.4)", "<", "0.7")], [FUERZA(f"{EN}.Vel * 3.2")]),
            EV([T_("Escarabajo"), cmp_(f"mod(TimeFromStart() + {EN}.Fase, 2.4)", ">=", "0.7")], [FUERZA(f"{EN}.Vel * 0.5")]),
            EV([T_("Golem")], [FUERZA(f"{EN}.Vel")]),
            EV([T_("Espora")], [FUERZA(f"{EN}.Vel * (0.7 + sin(TimeFromStart() * 2 + {EN}.Fase) * 0.5)")])]),
        COM("El topapa va casi bajo tierra hasta que esta cerca"),
        EV([T_("Topapa"), cmp_("DistEn", ">", "110")], [opacity(EN, 110)]),
        EV([T_("Topapa"), cmp_("DistEn", "<=", "110")], [opacity(EN, 255)]),
        SEP("Colision"), SEP("Rocas"),
        EV([C("CompareObjectTimer", EN, q("Golpe"), ">", "0.15")], [A("ChangeColor", EN, q("255;255;255"))]),
        COM("Recibir un golpe de la espada"),
        EV([C("CollisionNP", "CajaDaño", EN, "", "", ""), C("CompareObjectTimer", EN, q("Golpe"), ">", "0.3")], [A("ResetObjectTimer", EN, q("Golpe")), nv("GolpeEn", 'RandomInRange(Estadisticas["Daño Min"], Estadisticas["Daño Max"])'), set_objv_n(EN, "Vida", "GolpeEn", "-"), A("ChangeColor", EN, q("255;110;110")), snd("Cultivos/Comer.wav", 45),
            A("SetX", EN, "=", f"{EN}.X() + ({EN}.X() - {PJ}.X()) / max(1, DistEn) * 14"), A("SetY", EN, "=", f"{EN}.Y() + ({EN}.Y() - {PJ}.Y()) / max(1, DistEn) * 14"),
            A("Create", "", "Gui_Daño", f"{EN}.X() - 8", f"{EN}.Y() - 34", q("")), txt("Gui_Daño", "GolpeEn"), tw_y("Gui_Daño", "Movimiento Vertical", "Gui_Daño.Y() - 26", "easeOutQuint", .7), tw_op("Gui_Daño", "Desvanecer", 0, "linear", .9, "yes")]),
        EV([inv_(f"{EN}.Vida", "0", "<=") if False else C("NumberObjectVariable", EN, "Vida", "<=", "0")], [nv("Exp", f"{D_}.Exp", "+"), nv("Monedas", f"{D_}.Monedas", "+"), nv("RocaX", f"{EN}.X() - 16"), nv("RocaY", f"{EN}.Y() - 26"), bv("MinaRota", "True"), snd("HUD/Moneda.wav", 55)] + flot(f'"+" + ToString({D_}.Monedas) + " monedas"', "251;242;54") + [
            A("Create", "", "Recursos", f"{EN}.X() - 16", f"{EN}.Y() - 26", q("")), A("SetAnimationName", "Recursos", f"{D_}.Suelta"), set_objv_b("Recursos", "Nuevo", "False"), A("ResetObjectTimer", "Recursos", q("Soltado")), A("Delete", EN, "")])]),
    COM("Tocar a un enemigo hace daño"),
    choque,
    COM("Las papas radiactivas de siempre tambien vienen hacia ti cuando estas cerca"),
    FOREACH("Papa", [ibv("InventarioAbierto", "False"), objv_b("Papa", "Hambrienta", "False")], [nv("DistEn", f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), Papa.X(), Papa.Y())")], [
        EV([cmp_("DistEn", "<", "130")], [set_objv_b("Papa", "PuedeAndar", "False"), set_objv_n("Papa", "TiemposAndar", "9999"), A("AddForceTowardPosition", "Papa", f"{PJ}.X()", f"{PJ}.Y()", "Papa.Velocidad * 1.3", "0")], [
            EV([cmp_(f"abs({PJ}.X() - Papa.X())", ">", f"abs({PJ}.Y() - Papa.Y())"), cmp_(f"{PJ}.X()", ">", "Papa.X()")], [anim("Papa", q("CaminarDerecha"))]),
            EV([cmp_(f"abs({PJ}.X() - Papa.X())", ">", f"abs({PJ}.Y() - Papa.Y())"), cmp_(f"{PJ}.X()", "<=", "Papa.X()")], [anim("Papa", q("CaminarIzquierda"))]),
            EV([cmp_(f"abs({PJ}.X() - Papa.X())", "<=", f"abs({PJ}.Y() - Papa.Y())"), cmp_(f"{PJ}.Y()", ">", "Papa.Y()")], [anim("Papa", q("CaminarAbajo"))]),
            EV([cmp_(f"abs({PJ}.X() - Papa.X())", "<=", f"abs({PJ}.Y() - Papa.Y())"), cmp_(f"{PJ}.Y()", "<=", "Papa.Y()")], [anim("Papa", q("CaminarArriba"))])]),
        EV([cmp_("DistEn", ">=", "130"), C("NumberObjectVariable", "Papa", "TiemposAndar", "=", "9999")], [set_objv_n("Papa", "TiemposAndar", "2")])]),
]
external_events(d, "EnemigosMina", eventos)
per_ev.insert(next(k for k, e in enumerate(per_ev) if e.get("target") == "Cultivos"), LINK("EnemigosMina"))
# ---------- Romper rocas: la escalera puede aparecer ----------
her = EXT["Herramientas"]["events"]
def marca(evs):
    for e in evs:
        acts = e.get("actions", []) or []
        if any(a["type"]["value"] == "Delete" and a["parameters"][0] == "Rocas" for a in acts):
            acts[:0] = [nv("RocaX", "Rocas.X() - 15"), nv("RocaY", "Rocas.Y() - 24"), bv("MinaRota", "True")]; return True
        if marca(e.get("events", []) or []): return True
assert marca(her)
# ---------- Generador de pisos ----------
GEN = r'''
const game = runtimeScene.getGame(), V = game.getVariables();
const piso = V.get("MinaPiso").getAsNumber(), zona = Math.min(2, Math.floor((piso - 1) / 10)), W = 40, H = 24;
for (const n of ["Colision", "Roca_1", "Roca_2", "Veta", "EnemigoMina", "EscaleraMina", "Recursos"]) for (const o of runtimeScene.getObjects(n).slice()) o.deleteFromScene(runtimeScene);
const rnd = (a) => Math.floor(Math.random() * a), elige = (l) => l[rnd(l.length)];
const nueva = (v) => { const m = []; for (let y = 0; y < H; y++) { m.push([]); for (let x = 0; x < W; x++) m[y].push(v); } return m; };
const borde = (x, y) => x < 2 || y < 3 || x >= W - 2 || y >= H - 2;
function cueva(prob, pasos) {
  let m = nueva(1);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) m[y][x] = borde(x, y) || Math.random() < prob ? 1 : 0;
  for (let p = 0; p < pasos; p++) {
    const s = nueva(1);
    for (let y = 1; y < H - 1; y++) for (let x = 1; x < W - 1; x++) {
      let c = 0; for (let a = -1; a <= 1; a++) for (let b = -1; b <= 1; b++) if (a || b) c += m[y + a][x + b];
      s[y][x] = borde(x, y) ? 1 : c >= 5 ? 1 : 0;
    }
    m = s;
  }
  return m;
}
function salas() {
  const m = nueva(1), c = [], n = 6 + rnd(4);
  for (let i = 0; i < n; i++) {
    const w = 5 + rnd(6), h = 4 + rnd(4), x = 3 + rnd(W - w - 6), y = 4 + rnd(H - h - 7);
    for (let a = y; a < y + h; a++) for (let b = x; b < x + w; b++) m[a][b] = 0;
    c.push([x + (w >> 1), y + (h >> 1)]);
  }
  for (let i = 1; i < c.length; i++) {
    let [x, y] = c[i - 1]; const [x2, y2] = c[i];
    while (x !== x2) { m[y][x] = 0; m[y + 1][x] = 0; x += x < x2 ? 1 : -1; }
    while (y !== y2) { m[y][x] = 0; m[y][x + 1] = 0; y += y < y2 ? 1 : -1; }
  }
  return m;
}
function columnas() {
  const m = nueva(0);
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (borde(x, y)) m[y][x] = 1;
  const paso = 4 + rnd(3);
  for (let y = 5; y < H - 3; y += paso) for (let x = 4 + rnd(2); x < W - 4; x += paso) if (Math.random() < 0.75) { m[y][x] = 1; if (Math.random() < 0.5) m[y][x + 1] = 1; }
  return m;
}
function descanso() {
  const m = nueva(1);
  for (let y = 7; y < 17; y++) for (let x = 12; x < 28; x++) m[y][x] = 0;
  return m;
}
function region(m) {
  const vis = nueva(0); let mejor = [];
  for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
    if (m[y][x] || vis[y][x]) continue;
    const pila = [[x, y]], r = []; vis[y][x] = 1;
    while (pila.length) { const [a, b] = pila.pop(); r.push([a, b]);
      for (const [c, e] of [[a + 1, b], [a - 1, b], [a, b + 1], [a, b - 1]]) if (c >= 0 && e >= 0 && c < W && e < H && !m[e][c] && !vis[e][c]) { vis[e][c] = 1; pila.push([c, e]); } }
    if (r.length > mejor.length) mejor = r;
  }
  return mejor;
}
const esDescanso = piso % 5 === 0;
let mapa, libres = [];
for (let i = 0; i < 12; i++) {
  mapa = esDescanso ? descanso() : elige([() => cueva(0.45, 4), () => cueva(0.42, 3), salas, columnas])();
  libres = region(mapa);
  if (libres.length >= (esDescanso ? 100 : 170)) break;
}
if (libres.length < 60) { mapa = descanso(); libres = region(mapa); }
const dentro = {}; for (const [x, y] of libres) dentro[y * W + x] = 1;
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) if (!mapa[y][x] && !dentro[y * W + x]) mapa[y][x] = 1;
const pared = (x, y) => x < 0 || y < 0 || x >= W || y >= H || mapa[y][x] === 1;
// Dibujar
const tm = runtimeScene.getObjects("MinaMapa")[0], base = zona * 20;
for (let y = 0; y < H; y++) for (let x = 0; x < W; x++) {
  let t;
  if (!mapa[y][x]) t = 17 + (Math.random() < 0.7 ? 0 : 1 + rnd(2));
  else if (y + 1 < H && !mapa[y + 1][x]) t = 16;
  else t = (pared(x, y - 1) ? 1 : 0) + (pared(x + 1, y) ? 2 : 0) + (pared(x, y + 1) ? 4 : 0) + (pared(x - 1, y) ? 8 : 0);
  tm.setTileAtGridCoordinates(base + t, x, y);
}
// Colisiones agrupadas por filas
for (let y = 0; y < H; y++) { let x = 0; while (x < W) { if (!mapa[y][x]) { x++; continue; } let f = x; while (f < W && mapa[y][f]) f++;
  const c = runtimeScene.createObject("Colision"); c.setPosition(x * 32, y * 32); c.setWidth((f - x) * 32); c.setHeight(32); c.hide(true); x = f; } }
// Entrada: una celda con aire alrededor
const abiertas = libres.filter(([x, y]) => !pared(x, y + 1) && !pared(x, y - 1) && !pared(x + 1, y) && !pared(x - 1, y) && !pared(x, y + 2));
const [ex, ey] = elige(abiertas.length ? abiertas : libres);
const subir = runtimeScene.getObjects("Interactivo")[0]; subir.setPosition(ex * 32 + 1, ey * 32 - 12); subir.setZOrder(ey * 32 + 20);
const ped = runtimeScene.getObjects("Personaje_jugador")[0]; ped.setPosition(ex * 32 + 16, (ey + 1) * 32 + 24);
const lejos = (x, y, r) => Math.abs(x - ex) + Math.abs(y - ey) >= r;
const celdas = libres.filter(([x, y]) => !pared(x, y - 1) && lejos(x, y, 3));
for (let i = celdas.length - 1; i > 0; i--) { const j = rnd(i + 1); [celdas[i], celdas[j]] = [celdas[j], celdas[i]]; }
let ci = 0; const sig = () => celdas[ci++ % Math.max(1, celdas.length)];
function piedra(tipo) {
  const [x, y] = sig();
  if (tipo === "Roca") { const o = runtimeScene.createObject(Math.random() < 0.5 ? "Roca_1" : "Roca_2"); o.setPosition(x * 32 + 16, y * 32 + 28); o.setZOrder(y * 32 + 28); }
  else { const o = runtimeScene.createObject("Veta"); o.setAnimationName(tipo); o.setPosition(x * 32, y * 32 + 2); o.setZOrder(y * 32 + 26); }
}
function objeto(x, y, id) { const o = runtimeScene.createObject("Recursos"); o.setAnimationName(id); o.setPosition(x, y); o.setZOrder(y + 28); o.getVariables().get("Nuevo").setBoolean(false); o.resetTimer("Soltado"); }
V.get("MinaEscalera").setBoolean(false);
const tabla = [["Roca","Roca","Roca","Roca","Cobre"], ["Roca","Roca","Roca","Hierro","Cobre"], ["Roca","Roca","Hierro","Cristal"]][zona];
if (esDescanso) {
  V.get("MinaCheckpoint").setNumber(piso); V.get("MinaEscalera").setBoolean(true);
  const e = runtimeScene.createObject("EscaleraMina"); const [lx, ly] = sig(); e.setPosition(lx * 32 + 1, ly * 32 + 1); e.setZOrder(ly * 32 + 30);
  const premio = [["Cobre","Carbon","Madera","Zanahorias"], ["Hierro","Carbon","Cobre","PanZanahoria"], ["Cristal","Hierro","SopaPapa","Nucleo"]][zona];
  for (let i = 0; i < 4 + zona; i++) { const [x, y] = sig(); objeto(x * 32, y * 32, premio[i % premio.length]); }
} else {
  const rica = Math.random() < 0.15, plaga = Math.random() < 0.12;
  const nr = Math.min(celdas.length >> 1, 14 + rnd(14) + Math.floor(piso / 3));
  for (let i = 0; i < nr; i++) piedra(rica && i % 2 ? tabla[tabla.length - 1] : elige(tabla));
  const tipos = [["Brotecito","Brotecito","Murcipapa","Topapa"], ["Topapa","Murcipapa","Escarabajo","Golem"], ["Escarabajo","Espora","Golem","Murcipapa"]][zona];
  let ne = Math.min(14, 3 + Math.floor(piso / 2) + rnd(3)); if (plaga) ne = Math.min(18, ne * 2);
  for (let i = 0, k = 0; i < ne && k < 400; k++) { const [x, y] = sig(); if (!lejos(x, y, 8)) continue; const o = runtimeScene.createObject("EnemigoMina"); o.getVariables().get("Tipo").setString(elige(tipos)); o.setPosition(x * 32 + 16, y * 32 + 28); i++; }
}
runtimeScene.getObjects("TextoMina").forEach((t) => t.setString("Piso " + piso + (esDescanso ? " - Descanso" : "")));
'''
JS = {"type": "BuiltinCommonInstructions::JsCode", "inlineCode": GEN, "parameterObjects": "", "useStrict": True, "eventsSheetExpanded": False}
# ---------- Escena ----------
M = copy.deepcopy(PU); M["name"] = "Mina"; M["r"], M["v"], M["b"] = 14, 10, 16; M["objects"] = []
fs = M.get("objectsFolderStructure")
if fs: fs["children"] = []
mapa = inst("MinaMapa", 0, 0, z=-9000)
mapa["stringProperties"] = [{"name": "tilemap", "value": json.dumps({"tileWidth": 32, "tileHeight": 32, "dimX": 40, "dimY": 24, "layers": [{"id": 0, "alpha": 1, "tiles": [[-1] * 40 for _ in range(24)]}]}, separators=(",", ":"))}]
sub_i = inst("Interactivo", 0, 0, z=10, variables=[var("Dialogo", "string", "Puerta"), var("Solido", "boolean", False), var("DestEscena", "string", "Nivel 02"), var("DestSala", "string", ""), var("DestX", "number", 545), var("DestY", "number", 140)])
sub_i["numberProperties"] = [{"name": "animation", "value": ANIM["EscaleraArriba"]}]
M["instances"] = [mapa, sub_i, inst(PJ, 640, 400, z=403), inst("AvisoNPC", -900, -900, z=100000), inst("AvisoInteractivo", -900, -900, z=100000), inst("TextoMina", 812, 80, layer="UIHD", z=60)]
for c in next(v for v in M["variables"] if v["name"] == "LimiteCamara")["children"]:
    c["value"] = {"Izquierda": 0, "Arriba": 0, "Derecha": 1280, "Abajo": 768}[c["name"]]
ev = M["events"]
txt_ = json.dumps(ev[2], ensure_ascii=False).replace("PlazaDelPueblo", "Profundidades")
ev[2] = json.loads(txt_)
add_resource(d, "audio", "Natural/Audio/Profundidades.ogg", "Natural/Audio/Profundidades.ogg")
ev.insert(2, EV([C("SceneJustBegins", "")], [nv("MinaPiso", "max(1, MinaCheckpoint)"), bv("MinaGenerar", "True"), A("Create", "", "LuzAntorcha", f"640", "400", q("Luz Exterior")), A("ScalableCapability::ScalableBehavior::SetValue", "LuzAntorcha", "Scale", "=", "3.4")]))
FUND = [A("Create", "", "Cortina", "0", "0", q("DialogoHD")), A("ResizableCapability::ResizableBehavior::SetWidth", "Cortina", "Resizable", "=", "960"), A("ResizableCapability::ResizableBehavior::SetHeight", "Cortina", "Resizable", "=", "540"), A("SetZOrder", "Cortina", "=", "999"), tw_op("Cortina", "Bajar", 0, "easeOutQuad", .6, "yes")]
ev += [
    COM("MINA. El piso se genera despues de cargar la escena y cada vez que se baja."),
    EV([ibv("MinaGenerar", "True")], [bv("MinaGenerar", "False")], [JS]),
    COM("Oscuridad por zonas y luz alrededor de Pedro"),
    EV([], [A("SetXY", "LuzAntorcha", "=", f"{PJ}.CenterX()", "=", f"{PJ}.Y() - 18"), A("SetLayerAmbientLightColor", "", q("Luz Exterior"), q("168;158;170"))]),
    EV([inv_("MinaPiso", "11", ">=")], [A("SetLayerAmbientLightColor", "", q("Luz Exterior"), q("140;158;190"))]),
    EV([inv_("MinaPiso", "21", ">=")], [A("SetLayerAmbientLightColor", "", q("Luz Exterior"), q("136;170;138"))]),
    COM("Las rocas estorban el paso"),
    EV([C("CollisionNP", PJ, "Rocas", "", "", "")], [A("SeparateFromObjects", PJ, "Rocas", "")]),
    COM("La escalera aparece al romper rocas o vencer enemigos. Si no queda nada mas, aparece seguro."),
    EV([ibv("MinaRota", "True")], [bv("MinaRota", "False")], [
        EV([ibv("MinaEscalera", "False"), cmp_("RandomInRange(1, 100)", "<=", "9")], [bv("MinaEscalera", "True"), A("Create", "", "EscaleraMina", "RocaX", "RocaY", q("")), A("SetZOrder", "EscaleraMina", "=", "RocaY + 30"), snd("HUD/SubirNivel.wav", 40)])]),
    EV([ibv("MinaEscalera", "False"), cmp_("SceneInstancesCount(Roca_1) + SceneInstancesCount(Roca_2) + SceneInstancesCount(Veta)", "=", "0"), C("Once" if False else "BuiltinCommonInstructions::Once")], [bv("MinaEscalera", "True"), A("Create", "", "EscaleraMina", f"{PJ}.X() + 30", f"{PJ}.Y()", q("")), A("SetZOrder", "EscaleraMina", "=", f"{PJ}.Y()")]),
    COM("Bajar por la escalera"),
    FOREACH("EscaleraMina", [ibv("InventarioAbierto", "False"), cmp_(f"DistanceBetweenPositions({PJ}.X(), {PJ}.Y(), EscaleraMina.X() + 15, EscaleraMina.Y() + 20)", "<", "70")], [show("AvisoInteractivo"), txt("AvisoInteractivo", q("Clic: bajar")), A("SetX", "AvisoInteractivo", "=", "EscaleraMina.X() - 8"), A("SetY", "AvisoInteractivo", "=", "EscaleraMina.Y() - 14")], [
        EV([C("IsCursorOnObject", "EscaleraMina", "", "", ""), C("MouseButtonFromTextReleased", "", q("Left"))], [nv("MinaPiso", "1", "+"), bv("MinaGenerar", "True"), snd("Menu/GolpeLogo.wav", 45)] + FUND)]),
]
ev[:] = [e for e in ev]
d["layouts"].append(M)
# ---------- Puerta de la mina y bloqueos ----------
mun = EXT["Mundo2"]["events"]; vis = mun[3]["events"][0]
tex = next(e for e in vis["events"] if "Clic: entrar" in json.dumps(e.get("actions", []), ensure_ascii=False))
tex["events"][0]["conditions"].append(objv_s("Interactivo", "DestEscena", q("Mina"), "!="))
tex["events"].append(EV([objv_s("Interactivo", "DestEscena", q("Mina"))], [txt("AvisoInteractivo", q("Clic: bajar a la mina"))]))
her3 = EXT["Herramientas"]["events"][3]["events"][3]
her3["conditions"].append(C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "!=", q("Mina")))
def no_mina(evs):
    for e in evs:
        if any(a["type"]["value"] == "Create" and a["parameters"][1] == "Construccion" for a in e.get("actions", []) or []):
            e["conditions"] = (e.get("conditions") or []) + [C("BuiltinCommonInstructions::CompareStrings", "CurrentSceneName()", "!=", q("Mina"))]
        no_mina(e.get("events", []) or [])
no_mina(EXT["Fabricacion"]["events"])
# ---------- Guardar ----------
gu = EXT["Guardado"]["events"][2]["events"]
k_ = next(k for k, e in enumerate(gu) if any(a["type"]["value"] == "EcrireFichierTxt" for a in e.get("actions", [])))
acc = gu[k_]["actions"]
acc.insert(next(j for j, a in enumerate(acc) if a["type"]["value"] == "SetStringVariable"), A("EcrireFichierTxt", q("PapayorkPartidas"), '"Ranura" + ToString(RanuraActual) + "/MinaCheckpoint"', "ToJSON(MinaCheckpoint)"))
gu.insert(k_, EV([isv("EscenaAGuardar", q("Mina"))], [sv("Zona", q("La mina"))]))
menu = L["Menu Principal"]["events"]; carga = menu[37]["events"]
idx = next(k for k, e in enumerate(carga) if "/Granja" in json.dumps(e, ensure_ascii=False))
carga.insert(idx + 1, json.loads(json.dumps(carga[idx], ensure_ascii=False).replace('/Granja\\"', '/MinaCheckpoint\\"').replace('"Granja"', '"MinaCheckpoint"')))
menu[35]["actions"].insert(0, nv("MinaCheckpoint", "1"))
# ---------- Primera visita ----------
linea = lambda q_, t: {"type": "structure", "children": [var("Quien", "string", q_), var("Texto", "string", t)]}
V["Dialogos"]["children"].append({"name": "EvMina", "type": "array", "children": [linea("Pedro", "Esta mina lleva años cerrada. Cada vez que entro parece distinta, como si la tierra se moviera."), linea("Pedro", "Rompiendo rocas o venciendo bichos a veces aparece una escalera. Cada cinco pisos hay un lugar seguro desde donde podré volver a empezar.")]})
next(v for v in d["variables"] if v["name"] == "Eventos")["children"].append({"name": "PrimeraMina", "type": "structure", "children": [var("Escena", "string", "Mina"), var("HoraMin", "number", 6), var("HoraMax", "number", 30), var("Personaje", "string", ""), var("PuntosMin", "number", 0), var("EventoPrevio", "string", ""), var("Marca", "string", ""), var("ZonaX", "number", 0), var("ZonaY", "number", 0), var("ZonaR", "number", 0), var("Sala", "string", ""),
    {"name": "Pasos", "type": "array", "children": [{"type": "structure", "children": [var("Cmd", "string", "hablar"), var("A", "string", "EvMina"), var("B", "number", 0), var("C", "number", 0)]}]}]})
with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2); f.write("\n")
print("ok")
