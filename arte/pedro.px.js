// Pedro: animacion propia con esqueleto (cadera, rodilla, tobillo, hombro, codo).
// El rebote del cuerpo sale de la pierna apoyada, los brazos van opuestos a las piernas y el sombrero llega un cuadro tarde.
// Compilar: node ~/.claude/skills/pxl-pixel-art/bin/pxl.js build pedro.px.js
pal({ K: "#2a1d2b" })

// Vestuario: Pedro por defecto. Los personajes de la historia usan el mismo esqueleto con otra ropa
const PEDRO = {
  piel: ["#f6d3ae", "#e8b48c", "#c98a6c", "#9c6152"], pelo: ["#8a5a34", "#6b4026", "#4e2c1f", "#35201c"],
  camisa: ["#d65a4a", "#b23c3c", "#842c37", "#5e2230"], overol: ["#5aa6ad", "#3d8390", "#2e6476", "#23495c"],
  bota: ["#c08a5c", "#8f6040", "#6a4430", "#3f2a24"], paja: ["#f7e3a4", "#e3c478", "#bd9a58", "#8d7044"], cinta: ["#4c97a0", "#2e6e7c"],
  ojo: "#3f2a22", sombrero: "paja", peto: true, bigote: null, barba: null,
}
let PIEL, PELO, CAMISA, OVEROL, BOTA, PAJA, CINTA, OJO, ROPA
const vestir = (r) => { ROPA = { ...PEDRO, ...r }; PIEL = ROPA.piel; PELO = ROPA.pelo; CAMISA = ROPA.camisa; OVEROL = ROPA.overol; BOTA = ROPA.bota; PAJA = ROPA.paja; CINTA = ROPA.cinta; OJO = ROPA.ojo }
vestir(PEDRO)
const R = Math.round, RAD = Math.PI / 180, SUELO = 45

// Parametros de cada forma de andar
const MODO = {
  camina: { muslo: 23, adelante: 2, rodilla: 7, alzada: 50, brazo: 20, codo: 14, codoVaiven: 12, inclina: 2, aire: 0, balanceo: 1 },
  corre: { muslo: 40, adelante: 10, rodilla: 18, alzada: 82, brazo: 34, codo: 80, codoVaiven: 12, inclina: 9, aire: 2.2, balanceo: 1 },
}
const MUSLO = 6, ESPINILLA = 6, TOBILLO = 2

// Pierna a partir de su fase. Fase 0: pie delante tocando el suelo. De 0 a 180: apoyo. De 180 a 360: se dobla y vuelve.
function pierna(f, m) {
  const giro = m.adelante + m.muslo * Math.cos(f)
  const vuelo = Math.sin(f) < 0 ? -Math.sin(f) : 0
  const dobla = m.rodilla + m.alzada * Math.pow(vuelo, 1.2)
  const a = giro * RAD, b = (giro - dobla) * RAD
  const rx = -Math.sin(a) * MUSLO, ry = Math.cos(a) * MUSLO
  const tx = rx - Math.sin(b) * ESPINILLA, ty = ry + Math.cos(b) * ESPINILLA
  return { rx, ry, tx, ty, vuelo, punta: vuelo * (Math.cos(f) < 0 ? 1 : 0) }
}

// Altura de la cadera en cada cuadro, para que el pie mas bajo pise el suelo
function pose(fase, m) {
  const cerca = pierna(fase, m), lejos = pierna(fase + Math.PI, m)
  const baja = Math.max(cerca.ty, lejos.ty)
  const aire = m.aire * Math.pow(Math.abs(Math.cos(fase)), 3)   // las dos piernas al aire al cambiar de pie
  return { cerca, lejos, caderaY: SUELO - TOBILLO - baja - aire, baja }
}
const CICLO = 8
const faseDe = (i) => (i * 2 * Math.PI) / CICLO
function caderas(m) { return [...Array(CICLO).keys()].map((i) => pose(faseDe(i), m).caderaY) }

// ---------- dibujo de extremidades ----------
function palo(c, x0, y0, x1, y1, ancho, r) {
  c.line(R(x0), R(y0), R(x1), R(y1), r[1], ancho)
  const m = Math.floor(ancho / 2)
  c.line(R(x0) - m, R(y0), R(x1) - m, R(y1), r[0])
  c.line(R(x0) + ancho - m - 1, R(y0), R(x1) + ancho - m - 1, R(y1), r[2])
}
function botaLado(c, x, y, r, punta) {
  // Pie con puntera a la izquierda, talón y suela oscura
  c.rect(x - 3, y - 2, 6, 3, r[1]); c.hline(x - 3, y - 2, 6, r[0]); c.hline(x - 3, y, 6, r[3])
  c.px(x + 2, y - 2, r[2]); c.px(x + 2, y - 1, r[2]); c.px(x - 3, y - 1, r[0])
  if (punta > 0.55) { c.px(x - 3, y + 1, r[2]); c.px(x - 2, y + 1, r[3]); c.px(x - 3, y - 2, "_") }
}
function piernaLado(c, cx, cy, p, tela, bota) {
  const kx = cx + p.rx, ky = cy + p.ry, ax = cx + p.tx, ay = cy + p.ty
  palo(c, cx, cy, kx, ky, 5, tela)
  palo(c, kx, ky, ax, ay, 4, tela)
  // Caña de la bota: tapa por completo el final del pantalón
  const f = 0.68, ux = ax + (kx - ax) * f, uy = ay + (ky - ay) * f
  c.line(R(ux), R(uy) + 1, R(ax), R(ay), bota[1], 5)
  c.line(R(ux) - 2, R(uy) + 1, R(ax) - 2, R(ay), bota[0])
  c.line(R(ux) + 2, R(uy) + 1, R(ax) + 2, R(ay), bota[2])
  c.hline(R(ux) - 2, R(uy), 5, bota[0])                   // borde que marca dónde termina
  c.hline(R(ux) - 2, R(uy) - 1, 5, bota[3])
  botaLado(c, R(ax), R(ay) + TOBILLO - 1, bota, p.punta)
}
function brazoLado(c, sx, sy, angulo, codo, tela, piel, largo = 4) {
  const a = angulo * RAD, b = (angulo + codo) * RAD      // angulo positivo: hacia delante (izquierda)
  const ex = sx - Math.sin(a) * largo, ey = sy + Math.cos(a) * largo
  const hx = ex - Math.sin(b) * 5, hy = ey + Math.cos(b) * 5
  // contorno interior: separa el brazo del cuerpo
  c.line(R(sx) + 2, R(sy), R(ex) + 2, R(ey), tela[3])
  c.line(R(ex) + 2, R(ey), R(hx) + 2, R(hy), piel[3])
  c.line(R(ex), R(ey), R(hx), R(hy), piel[1], 3)         // antebrazo
  c.line(R(ex) - 1, R(ey), R(hx) - 1, R(hy), piel[0])
  c.line(R(ex) + 1, R(ey), R(hx) + 1, R(hy), piel[2])
  c.rect(R(hx) - 1, R(hy) - 1, 3, 3, piel[1]); c.px(R(hx) - 1, R(hy) - 1, piel[0]); c.px(R(hx) + 1, R(hy) + 1, piel[2])
  c.line(R(sx), R(sy), R(ex), R(ey), tela[1], 3)         // manga corta
  c.line(R(sx) - 1, R(sy), R(ex) - 1, R(ey), tela[0])
  c.hline(R(ex) - 1, R(ey) + 1, 3, tela[2])
  return { hx, hy }
}

// ---------- cabeza con sombrero ----------
function caraFrente(c, x, y, parpadeo) {
  const w = 14, h = 13, s = PIEL
  c.rect(x, y, w, h, s[1]); c.vline(x, y, h, s[0]); c.hline(x + 1, y, w - 2, s[0])
  c.rect(x + w - 3, y + 1, 3, h - 2, s[2]); c.hline(x + 1, y + h - 1, w - 2, s[2]); c.hline(x + 3, y + h - 2, w - 6, s[1])
  for (const [a, b] of [[x, y + h - 1], [x + w - 1, y + h - 1]]) c.px(a, b, "_")
  const ey = y + 7
  for (const ex of [x + 3, x + 9]) {
    if (parpadeo) { c.hline(ex, ey + 1, 2, s[3]) }
    else { c.rect(ex, ey, 2, 2, "#fbf5ea"); c.vline(ex + 1, ey, 2, OJO); c.px(ex + 1, ey, "#1a1320") }
  }
  c.px(x + 6, ey + 2, s[2]); c.px(x + 7, ey + 2, s[2])
  c.hline(x + 5, ey + 4, 4, s[3])
  c.px(x + 2, ey + 2, "#e29a88"); c.px(x + 11, ey + 2, "#d38778")
  // pelo que asoma bajo el ala: flequillo irregular y patillas
  for (const [a, l, t] of [[0, 5, 1], [1, 4, 0], [2, 3, 1], [3, 4, 1], [5, 3, 0], [6, 2, 1], [8, 3, 1], [9, 2, 1], [10, 3, 2], [11, 4, 2], [12, 5, 2], [13, 6, 3]]) c.vline(x + a, y + 2, l, PELO[t])
}
function sombreroFrente(c, x, y) {
  // x, y: esquina superior de la cara. Copa baja y redondeada, ala que cae hacia los lados, cinta azul de Pedro
  const q = PAJA
  c.rect(x + 2, y - 4, 10, 4, q[1]); c.hline(x + 4, y - 5, 6, q[0]); c.vline(x + 2, y - 3, 3, q[0]); c.vline(x + 3, y - 4, 4, q[0]); c.vline(x + 11, y - 3, 3, q[2]); c.vline(x + 10, y - 4, 4, q[2]); c.px(x + 2, y - 4, "_"); c.px(x + 11, y - 4, "_")
  c.hline(x + 2, y - 1, 10, CINTA[0]); c.px(x + 11, y - 1, CINTA[1]); c.px(x + 10, y - 1, CINTA[1])
  // ala: arriba al centro, baja hacia los extremos
  c.hline(x - 1, y, 16, q[1]); c.hline(x - 1, y, 6, q[0])
  c.hline(x - 3, y + 1, 20, q[1]); c.hline(x - 3, y + 1, 9, q[0])
  c.hline(x - 3, y + 2, 3, q[2]); c.hline(x + 14, y + 2, 3, q[3]); c.hline(x, y + 2, 14, q[2])
  c.px(x - 4, y + 2, q[1]); c.px(x + 17, y + 2, q[3])
  for (const a of [5, 8]) c.px(x + a, y - 3, q[2])                    // trenzado de la paja
  for (const a of [-2, 1, 4, 8, 11, 14]) c.px(x + a, y + 1, q[2])
  c.px(x - 3, y + 3, q[3]); c.px(x + 16, y + 3, q[3])                 // hebras sueltas
}
function sombreroAtras(c, x, y, cae) {
  const q = PAJA
  c.rect(x + 2, y - 4, 10, 4, q[1]); c.hline(x + 4, y - 5, 6, q[0]); c.vline(x + 2, y - 3, 3, q[0]); c.vline(x + 11, y - 3, 3, q[2]); c.vline(x + 10, y - 4, 4, q[2]); c.px(x + 2, y - 4, "_"); c.px(x + 11, y - 4, "_")
  c.hline(x + 2, y - 1, 10, CINTA[0]); c.px(x + 11, y - 1, CINTA[1])
  c.hline(x - 1, y + cae, 16, q[1]); c.hline(x - 1, y + cae, 6, q[0])
  c.hline(x - 3, y + 1 + cae, 20, q[1]); c.hline(x - 3, y + 1 + cae, 8, q[0]); c.hline(x - 2, y + 2 + cae, 18, q[2]); c.hline(x + 13, y + 2 + cae, 3, q[3])
  for (const a of [-1, 3, 7, 11, 15]) c.px(x + a, y + 1 + cae, q[2])
  c.px(x - 3, y + 2 + cae, q[3]); c.px(x + 16, y + 2 + cae, q[3])
}
function cabezaAtras(c, x, y) {
  c.rect(x, y, 14, 12, PELO[1]); c.vline(x, y, 12, PELO[0]); c.vline(x + 13, y, 12, PELO[2]); c.vline(x + 12, y, 12, PELO[2])
  c.px(x, y + 11, "_"); c.px(x + 13, y + 11, "_")
  for (const a of [2, 5, 8, 11]) c.vline(x + a, y + 8, 4, PELO[2])
  for (const a of [1, 4, 7, 10]) c.vline(x + a, y + 10, 2, PELO[3])
  c.px(x - 1, y + 7, PIEL[2]); c.px(x + 14, y + 7, PIEL[2])           // orejas
}
function caraLado(c, x, y, parpadeo, vientoPelo) {
  // Mira a la izquierda. Nariz, mejilla y pelo en la nuca.
  const s = PIEL, w = 13, h = 13
  c.rect(x, y, w, h, s[1]); c.vline(x, y + 1, h - 2, s[0]); c.hline(x + 1, y + h - 1, w - 3, s[2]); c.rect(x + 7, y + 1, 2, h - 2, s[2])
  c.px(x, y + h - 1, "_"); c.px(x + w - 1, y + h - 1, "_")
  c.px(x - 1, y + 8, s[1]); c.px(x - 1, y + 9, s[2])                  // nariz
  const ey = y + 7
  if (parpadeo) c.hline(x + 2, ey + 1, 2, s[3])
  else { c.rect(x + 2, ey, 2, 2, "#fbf5ea"); c.vline(x + 2, ey, 2, OJO); c.px(x + 2, ey, "#1a1320") }
  c.hline(x + 1, ey + 4, 3, s[3]); c.px(x + 5, ey + 2, "#e29a88")
  // pelo: nuca, patilla, puntas que se levantan al correr
  c.rect(x + 7, y + 2, w - 7, h - 5, PELO[1]); c.vline(x + w - 1, y + 2, h - 5, PELO[2]); c.vline(x + 7, y + 3, 5, PELO[0]); c.px(x + 6, y + 3, PELO[1]); c.px(x + 6, y + 4, PELO[2])
  for (const a of [8, 10]) c.vline(x + a, y + h - 3, 2, PELO[2])
  for (const a of [1, 3, 5]) c.vline(x + a, y + 2, 2, PELO[1])
  c.px(x + 8, y + 9, s[2]); c.px(x + 8, y + 8, s[1])                  // oreja
  if (vientoPelo) { c.px(x + w, y + 6, PELO[1]); c.px(x + w + 1, y + 5, PELO[2]); c.px(x + w, y + 8, PELO[2]) }
}
function sombreroLado(c, x, y, cae) {
  // Ala delantera 4 pixeles y trasera 3, con caida: cae 0 o 1 cuando rebota
  const q = PAJA
  c.rect(x + 2, y - 4, 9, 4, q[1]); c.hline(x + 4, y - 5, 5, q[0]); c.vline(x + 2, y - 3, 3, q[0]); c.vline(x + 3, y - 4, 4, q[0]); c.vline(x + 10, y - 3, 3, q[2]); c.vline(x + 9, y - 4, 4, q[2]); c.px(x + 2, y - 4, "_"); c.px(x + 10, y - 4, "_")
  c.hline(x + 2, y - 1, 9, CINTA[0]); c.px(x + 10, y - 1, CINTA[1])
  c.hline(x - 2, y + cae, 16, q[1]); c.hline(x - 2, y + cae, 8, q[0])
  c.hline(x - 4, y + 1 + cae, 19, q[1]); c.hline(x - 4, y + 1 + cae, 9, q[0])
  c.hline(x - 4, y + 2 + cae, 3, q[2]); c.hline(x + 12, y + 2 + cae, 3, q[3]); c.hline(x - 1, y + 2 + cae, 13, q[2])
  for (const a of [5, 7]) c.px(x + a, y - 3, q[2])
  for (const a of [-2, 2, 6, 10, 13]) c.px(x + a, y + 1 + cae, q[2])
}

// Pelo a la vista, bigote y barba para los demas personajes
function peloFrente(c, x, y) {
  for (let i = 0; i < 4; i++) { const m = i === 0 ? 2 : 0; c.hline(x + m, y - 1 + i, 14 - m * 2, i < 2 ? PELO[0] : PELO[1]) }
  c.vline(x + 13, y, 3, PELO[2]); c.vline(x + 12, y, 3, PELO[2]); c.px(x + 4, y - 2, PELO[1]); c.px(x + 9, y - 2, PELO[1])
}
function peloLado(c, x, y) {
  for (let i = 0; i < 4; i++) { const m = i === 0 ? 2 : 0; c.hline(x + m, y - 1 + i, 13 - m * 2, i < 2 ? PELO[0] : PELO[1]) }
  c.px(x + 3, y - 2, PELO[1]); c.px(x + 8, y - 2, PELO[1])
}
function adornoFrente(c, x, y) {
  const ey = y + 7
  if (ROPA.barba) { const b = ROPA.barba; c.rect(x + 1, ey + 2, 12, 5, b[1]); c.hline(x + 1, ey + 2, 6, b[0]); c.rect(x + 3, ey + 7, 8, 2, b[1]); c.vline(x + 12, ey + 2, 5, b[2]); c.hline(x + 5, ey + 4, 4, PIEL[3]) }
  if (ROPA.bigote) { const b = ROPA.bigote; c.rect(x + 3, ey + 3, 8, 2, b[1]); c.hline(x + 3, ey + 3, 4, b[0]); c.px(x + 2, ey + 4, b[2]); c.px(x + 11, ey + 4, b[2]) }
}
function adornoLado(c, x, y) {
  const ey = y + 7
  if (ROPA.barba) { const b = ROPA.barba; c.rect(x, ey + 2, 8, 5, b[1]); c.hline(x, ey + 2, 4, b[0]); c.rect(x + 1, ey + 7, 5, 2, b[1]); c.hline(x + 1, ey + 4, 3, PIEL[3]) }
  if (ROPA.bigote) { const b = ROPA.bigote; c.rect(x, ey + 3, 6, 2, b[1]); c.hline(x, ey + 3, 3, b[0]); c.px(x - 1, ey + 4, b[2]) }
}

// ---------- torso de perfil ----------
function torsoLado(c, hx, hy, sx, sy) {
  const ancho = 8, m = 4
  for (let k = 0; k <= 11; k++) {
    const t = k / 11, x = R(hx + (sx - hx) * t) - m, y = R(hy + (sy - hy) * t)
    const peto = ROPA.peto ? k <= 6 : k <= 1
    const r = peto ? OVEROL : CAMISA
    c.hline(x, y, ancho, r[1]); c.px(x, y, r[0]); c.px(x + ancho - 1, y, r[2]); c.px(x + ancho - 2, y, r[2])
    if (k === 6) c.hline(x, y, ancho, OVEROL[0])
  }
  const t = 8 / 11, x = R(hx + (sx - hx) * t), y = R(hy + (sy - hy) * t)
  if (ROPA.peto) { c.vline(x - 1, y - 2, 4, OVEROL[1]); c.px(x - 1, y + 1, "#e8c76f") }     // tirante y boton
  else { c.vline(x - 2, y - 7, 8, CAMISA[3]); c.px(x - 2, y - 3, ROPA.boton || "#e8c76f"); c.px(x - 2, y, ROPA.boton || "#e8c76f") }  // botonadura
}

// ---------- vista de lado ----------
function lado(c, i, m, antes, opts = {}) {
  vestir(opts.ropa || PEDRO)
  const fase = faseDe(i), po = pose(fase, m)
  const hx = 16 + (m === MODO.corre ? -1 : 0), hy = po.caderaY
  const inc = m.inclina * RAD
  const sube = opts.respira || 0
  const sx = hx - Math.sin(inc) * 11, sy = hy - Math.cos(inc) * 11 - sube
  const aC = -m.brazo * Math.cos(fase), aL = m.brazo * Math.cos(fase)   // opuestos a la pierna del mismo lado
  const oscuro = (r) => [r[1], r[2], r[3], r[3]]
  // brazo y pierna del lado lejano, en tono mas oscuro
  if (!opts.mano) brazoLado(c, sx + 1, sy + 1, aL, m.codo - m.codoVaiven * Math.cos(fase), oscuro(CAMISA), [PIEL[2], PIEL[2], PIEL[3], PIEL[3]])
  piernaLado(c, hx + 1, hy, po.lejos, oscuro(OVEROL), oscuro(BOTA))
  torsoLado(c, hx, hy, sx, sy)
  piernaLado(c, hx - 1, hy, po.cerca, OVEROL, BOTA)
  let mano = null
  if (opts.mano) { c.line(R(sx), R(sy) + 2, opts.mano[0], opts.mano[1], CAMISA[1], 3); c.line(R((sx + opts.mano[0]) / 2), R((sy + opts.mano[1]) / 2 + 1), opts.mano[0], opts.mano[1], PIEL[1], 3); mano = opts.mano }
  else brazoLado(c, sx, sy + 1, aC, m.codo + m.codoVaiven * Math.cos(fase), CAMISA, PIEL)
  // cabeza: la recoge el cuerpo con un cuadro de retraso en vertical; sombrero un cuadro mas tarde
  const lista = caderas(m), yAhora = lista[i], yAntes = lista[(i + CICLO - 1) % CICLO]
  const cx = R(sx) - 7 - (m === MODO.corre ? 1 : 0), cy = R(sy) - 12
  caraLado(c, cx, cy, opts.parpadeo, m === MODO.corre && (i % 4 < 2))
  adornoLado(c, cx, cy)
  const cae = Math.max(0, Math.min(1, R((yAntes - yAhora) * -1))) ? 0 : yAhora < yAntes ? 1 : 0
  if (ROPA.sombrero === "paja") sombreroLado(c, cx, cy + 1, cae)
  else peloLado(c, cx, cy)
  return { sx, sy, mano }
}

// ---------- vista de frente y de espalda ----------
// Las piernas no se cruzan: se acortan al levantarse y el pie que avanza baja un poco en pantalla.
function piernaFrente(c, x, caderaY, p, ancho, tela, bota, sentido) {
  const profundidad = -p.tx * 0.22 * sentido               // el pie adelantado se ve mas cerca de la camara
  const pieY = R(caderaY + p.ty + TOBILLO + profundidad)
  const rodillaY = R(caderaY + p.ry), altoBota = 6
  const finTela = pieY - altoBota, yC = R(caderaY), alto = Math.max(1, finTela - yC)
  c.rect(x, yC, ancho, alto, tela[1]); c.vline(x, yC, alto, tela[0]); c.vline(x + ancho - 1, yC, alto, tela[2])
  if (p.vuelo > 0.3 && rodillaY < finTela - 1) { c.hline(x + 1, rodillaY, ancho - 2, tela[0]); c.hline(x + 1, rodillaY + 1, ancho - 2, tela[2]) }
  // Bota entera: linea oscura de separacion, borde claro, caña, pie y suela
  const bx = x < 15 ? x - 1 : x, bw = ancho + 1
  c.hline(x, finTela - 1, ancho, bota[3])
  c.rect(x, finTela, ancho, altoBota - 3, bota[1]); c.hline(x, finTela, ancho, bota[0]); c.vline(x + ancho - 1, finTela + 1, altoBota - 4, bota[2])
  c.rect(bx, pieY - 3, bw, 3, bota[1]); c.hline(bx, pieY - 3, bw, bota[0]); c.px(bx + bw - 1, pieY - 2, bota[2])
  c.hline(bx, pieY, bw, bota[3])
}
function brazoFrente(c, x, y, avance, m, tela, piel, lado) {
  // avance > 0: brazo hacia la camara (mano baja); < 0: hacia atras (mano sube y se oculta un poco)
  const corriendo = m === MODO.corre
  if (corriendo) {
    // Codo doblado: manga corta y antebrazo que apenas sube o baja. La mano nunca pasa de la cadera
    const a_ = Math.max(-1, Math.min(1, avance / 4.25))
    const codoY = y + 4, manoX = x + (lado < 0 ? 2 : -2) * (a_ > 0 ? 1 : 0.5), manoY = y + 6 - R(a_ * 2)
    c.rect(x, y, 3, 5, tela[1]); c.vline(x, y, 5, tela[0]); c.vline(x + 2, y, 5, tela[2])
    c.line(x + 1, codoY, R(manoX) + 1, manoY, piel[1], 3)
    c.rect(R(manoX), manoY - 1, 3, 3, piel[1]); c.px(R(manoX) + 2, manoY + 1, piel[2])
    return
  }
  const largo = 7 + R(avance * 0.5), manoY = y + largo
  c.rect(x, y, 3, 6, tela[1]); c.vline(x, y, 6, tela[0]); c.vline(x + 2, y, 6, tela[2])
  c.rect(x, y + 6, 3, Math.max(1, largo - 6), piel[1]); c.vline(x + 2, y + 6, Math.max(1, largo - 6), piel[2])
  c.rect(x, manoY, 3, 2, piel[1]); c.px(x + 2, manoY + 1, piel[2])
}
function frente(c, i, m, atras, opts = {}) {
  vestir(opts.ropa || PEDRO)
  const fase = faseDe(i), po = pose(fase, m), sentido = atras ? -1 : 1
  const hy = po.caderaY + (m === MODO.corre ? 1 : 0)
  const sway = R(m.balanceo * Math.sin(fase))               // el peso pasa al pie que apoya
  const cx = 15 + sway
  const anchoT = 13, tx = cx - 6, sy = R(hy) - 11 - (opts.respira || 0)
  // piernas: la que va atras se pinta primero
  const izq = po.cerca, der = po.lejos
  const primero = izq.vuelo > der.vuelo ? [der, 15 + 1, izq, 15 - 6] : [izq, 15 - 6, der, 15 + 1]
  piernaFrente(c, primero[3], hy, primero[2], 5, OVEROL, BOTA, sentido)
  piernaFrente(c, primero[1], hy, primero[0], 5, [OVEROL[1], OVEROL[1], OVEROL[2], OVEROL[3]], BOTA, sentido)
  const aI = m.brazo / 8 * Math.cos(fase + Math.PI) * sentido, aD = -aI
  if (atras) {
    if (!opts.ambas) { brazoFrente(c, tx - 3, sy + 1, aI, m, CAMISA, PIEL, -1); brazoFrente(c, tx + anchoT, sy + 1, aD, m, [CAMISA[1], CAMISA[1], CAMISA[2], CAMISA[3]], PIEL, 1) }
  }
  // torso
  const altoT = 12 + (opts.respira || 0)
  c.rect(tx, sy, anchoT, altoT, CAMISA[1]); c.vline(tx, sy, altoT, CAMISA[0]); c.hline(tx, sy, anchoT, CAMISA[0]); c.vline(tx + anchoT - 1, sy, altoT, CAMISA[2]); c.vline(tx + anchoT - 2, sy + 1, altoT - 1, CAMISA[2])
  if (atras) {   // tirantes cruzados y parte trasera del overol
    c.line(tx + 2, sy, tx + anchoT - 3, sy + 6, OVEROL[2]); c.line(tx + anchoT - 3, sy, tx + 2, sy + 6, OVEROL[2])
    c.rect(tx + 1, sy + 7, anchoT - 2, altoT - 7, OVEROL[1]); c.hline(tx + 1, sy + 7, anchoT - 2, OVEROL[0]); c.vline(tx + anchoT - 2, sy + 7, altoT - 7, OVEROL[2])
    c.rect(tx + 3, sy + 9, 3, 2, OVEROL[2]); c.rect(tx + 7, sy + 9, 3, 2, OVEROL[2])     // bolsillos
  } else {       // peto, botones y bolsillo
    if (ROPA.peto) {
      c.rect(tx + 2, sy + 5, anchoT - 4, altoT - 5, OVEROL[1]); c.hline(tx + 2, sy + 5, anchoT - 4, OVEROL[0]); c.vline(tx + anchoT - 3, sy + 5, altoT - 5, OVEROL[2])
      c.vline(tx + 2, sy, 5, OVEROL[1]); c.vline(tx + anchoT - 3, sy, 5, OVEROL[2])
      c.px(tx + 3, sy + 6, "#e8c76f"); c.px(tx + anchoT - 4, sy + 6, "#e8c76f"); c.rect(cx - 2, sy + 8, 4, 3, OVEROL[2]); c.hline(cx - 2, sy + 8, 4, OVEROL[3])
    } else {
      c.vline(cx, sy, altoT, CAMISA[3]); for (const k of [2, 5, 8]) c.px(cx, sy + k, ROPA.boton || "#e8c76f")
      c.hline(tx, sy + altoT - 2, anchoT, OVEROL[3]); c.px(cx, sy + altoT - 2, "#e8c76f")   // cinturon
    }
    if (opts.manos) { c.line(tx, sy + 2, opts.manos[0], opts.manos[1], CAMISA[1], 3); c.rect(opts.manos[0] - 1, opts.manos[1] - 1, 3, 3, PIEL[1]) }
    else { brazoFrente(c, tx - 3, sy + 1, aI, m, CAMISA, PIEL, -1) }
    if (opts.ambas) { c.line(tx + anchoT - 1, sy + 2, opts.manos[0], opts.manos[1], CAMISA[2], 3); c.rect(opts.manos[0] - 1, opts.manos[1] - 1, 3, 3, PIEL[1]) }
    else brazoFrente(c, tx + anchoT, sy + 1, aD, m, [CAMISA[1], CAMISA[1], CAMISA[2], CAMISA[3]], PIEL, 1)
  }
  if (atras && opts.ambas) { for (const x0 of [tx, tx + anchoT - 1]) c.line(x0, sy + 2, opts.manos[0], opts.manos[1], CAMISA[1], 3) }
  // cuello, cabeza y sombrero que llega un cuadro tarde
  const lista = caderas(m), yAhora = lista[i], yAntes = lista[(i + CICLO - 1) % CICLO]
  const cae = yAhora < yAntes - 0.2 ? 1 : 0
  const hx = cx - 7 + (m === MODO.corre && !atras ? 0 : 0), hyC = sy - 12
  if (!atras) c.rect(cx - 2, sy - 1, 4, 2, PIEL[2])
  if (atras) { cabezaAtras(c, hx, hyC); if (ROPA.sombrero === "paja") sombreroAtras(c, hx, hyC + 1, cae); else peloFrente(c, hx, hyC) }
  else {
    caraFrente(c, hx, hyC, opts.parpadeo); adornoFrente(c, hx, hyC)
    if (ROPA.sombrero === "paja") sombreroFrente(c, hx, hyC + 1 + cae); else peloFrente(c, hx, hyC)
  }
}

// ---------- reposo: respiracion muy suave y un parpadeo ----------
// k = 0 pecho abajo, 1 pecho arriba, 2 parpadeo
function reposo(c, dir, k) {
  const m = { ...MODO.camina, muslo: 0, adelante: 0, rodilla: 0, alzada: 0, brazo: 0, codo: 8, codoVaiven: 0, inclina: 1, balanceo: 0 }
  const o = { parpadeo: k === 2, respira: k === 1 ? 1 : 0 }
  if (dir === "izq") lado(c, 0, m, null, o)
  else frente(c, 0, m, dir === "arriba", o)
}

const O = { w: 30, h: 46, outline: "K" }
const CARPETAS = { Izquierda: "izq", Arriba: "arriba", Abajo: "abajo" }
const dibuja = (c, d, i, m) => { if (d === "izq") lado(c, i, m); else frente(c, i, m, d === "arriba") }
for (let i = 0; i < CICLO; i++) {
  for (const [n, d] of Object.entries(CARPETAS)) {
    sprite(`PedroN_${n}${i + 1}`, O, (c) => dibuja(c, d, i, MODO.camina))
    sprite(`PedroN_Correr${n}${i + 1}`, O, (c) => dibuja(c, d, i, MODO.corre))
  }
  sprite(`PedroN_Derecha${i + 1}`, { ...O, flip: "x" }, (c) => lado(c, i, MODO.camina))
  sprite(`PedroN_CorrerDerecha${i + 1}`, { ...O, flip: "x" }, (c) => lado(c, i, MODO.corre))
}
for (const [n, d] of Object.entries(CARPETAS)) for (let k = 0; k < 3; k++) sprite(`PedroN_Quieto${n}${k + 1}`, O, (c) => reposo(c, d, k))
for (let k = 0; k < 3; k++) sprite(`PedroN_QuietoDerecha${k + 1}`, { ...O, flip: "x" }, (c) => reposo(c, "izq", k))

// ---------- golpe con espada: preparar, cortar, terminar ----------
function espada(c, x0, y0, x1, y1) {
  c.line(x0, y0, x1, y1, "#c8d2d8", 2); c.line(x0, y0 + 1, x1, y1 + 1, "#7f8c98"); c.px(x1, y1, "#ffffff")
  c.rect(x0 - 1, y0 - 1, 3, 3, "#a56a3c"); c.px(x0, y0, "#e8c76f")
}
function arco(c, cx, cy, r, a, b) {
  for (let t = a; t <= b; t += 3) {
    const q = t * RAD
    c.px(R(cx + Math.cos(q) * r), R(cy + Math.sin(q) * r), "#fff8e8")
    if (t > a + 12 && t < b - 12) c.px(R(cx + Math.cos(q) * (r - 1)), R(cy + Math.sin(q) * (r - 1)), "#f4e7c8")
  }
}
const FIRME = { ...MODO.camina, muslo: 9, adelante: 2, rodilla: 5, alzada: 0, brazo: 0, codo: 10, codoVaiven: 0, inclina: 3, balanceo: 0 }
const H = (d, f, fn, extra = {}) => sprite(`PedroN_Ataque${d}${f}`, { ...O, ...extra }, fn)
H("Abajo", 1, (c) => { espada(c, 4, 25, 0, 16); frente(c, 0, FIRME, false, { manos: [4, 25] }) })
H("Abajo", 2, (c) => { frente(c, 0, FIRME, false, { manos: [15, 33] }); arco(c, 15, 28, 14, 35, 145); espada(c, 15, 33, 24, 39) })
H("Abajo", 3, (c) => { frente(c, 0, FIRME, false, { manos: [25, 27] }); espada(c, 25, 27, 29, 19) })
H("Arriba", 1, (c) => { frente(c, 0, FIRME, true); espada(c, 25, 26, 29, 17) })
H("Arriba", 2, (c) => { arco(c, 15, 19, 14, 215, 325); espada(c, 10, 18, 4, 8); frente(c, 0, FIRME, true) })
H("Arriba", 3, (c) => { espada(c, 4, 26, 0, 17); frente(c, 0, FIRME, true) })
for (const [n, fl] of [["Izquierda", {}], ["Derecha", { flip: "x" }]]) {
  H(n, 1, (c) => { espada(c, 22, 22, 28, 14); lado(c, 0, FIRME, null, { mano: [22, 22] }) }, fl)
  H(n, 2, (c) => { arco(c, 14, 27, 13, 130, 230); lado(c, 0, FIRME, null, { mano: [8, 28] }); espada(c, 7, 28, 0, 28) }, fl)
  H(n, 3, (c) => { lado(c, 0, FIRME, null, { mano: [9, 31] }); espada(c, 8, 31, 1, 36) }, fl)
}
sprite("PolvoPaso", { w: 7, h: 5 }, (c) => { c.ellipse(3, 2, 3, 2, "#d9c8a4"); c.px(1, 1, "#efe2c4"); c.px(2, 1, "#efe2c4"); c.px(5, 3, "#b8a688") })

// ---------- HERRAMIENTAS: cada una con su gesto. Lienzo grande para que tengan recorrido ----------
const LX = 15, LY = 14   // desplazamiento de Pedro dentro del lienzo de 60 x 60
const OH = { w: 60, h: 60, outline: "K" }
const MADERA = ["#c79a68", "#9a6d48", "#6f4b35"], HIERRO = ["#e6edf0", "#b3c0c8", "#7c8c98", "#55636f"]

function mango(c, x, y, ang, largo) {
  const q = ang * RAD, fx = x + Math.cos(q) * largo, fy = y + Math.sin(q) * largo
  c.line(R(x), R(y), R(fx), R(fy), MADERA[1], 2); c.line(R(x), R(y), R(fx), R(fy), MADERA[0])
  return [fx, fy, q]
}
function hacha(c, x, y, ang) {   // hoja ancha a un solo lado
  const [fx, fy, q] = mango(c, x, y, ang, 13), nx = -Math.sin(q), ny = Math.cos(q), s = Math.cos(q) >= 0 ? -1 : 1
  for (let k = 0; k < 5; k++) {
    const t = 1 + k, ax = fx - Math.cos(q) * 2 + nx * s * t, ay = fy - Math.sin(q) * 2 + ny * s * t
    const bx = fx + Math.cos(q) * (1 + k * 0.45) + nx * s * t, by = fy + Math.sin(q) * (1 + k * 0.45) + ny * s * t
    c.line(R(ax), R(ay), R(bx), R(by), k > 3 ? HIERRO[0] : k > 1 ? HIERRO[1] : HIERRO[3], 2)
  }
  c.px(R(fx), R(fy), HIERRO[3])
}
function pico(c, x, y, ang) {    // cabeza curva con dos puntas
  const [fx, fy, q] = mango(c, x, y, ang, 13), nx = -Math.sin(q), ny = Math.cos(q)
  for (const s of [-1, 1]) {
    let px_ = fx, py_ = fy
    for (let k = 1; k <= 7; k++) {
      const hx = fx + nx * s * k - Math.cos(q) * (k * k) / 14, hy = fy + ny * s * k - Math.sin(q) * (k * k) / 14
      c.line(R(px_), R(py_), R(hx), R(hy), k > 5 ? HIERRO[0] : HIERRO[2], k > 5 ? 1 : 2)
      px_ = hx; py_ = hy
    }
  }
  c.rect(R(fx) - 1, R(fy) - 1, 3, 3, HIERRO[3])
}
function azadon(c, x, y, ang) {  // mango largo y hoja plana en angulo recto
  const [fx, fy, q] = mango(c, x, y, ang, 17), nx = -Math.sin(q), ny = Math.cos(q), s = Math.cos(q) >= 0 ? 1 : -1
  for (let k = 0; k < 6; k++) {
    const ax = fx + nx * s * k, ay = fy + ny * s * k
    c.line(R(ax), R(ay), R(ax + Math.cos(q) * 2), R(ay + Math.sin(q) * 2), k > 2 ? HIERRO[0] : HIERRO[2], 2)
  }
}
function regadera(c, x, y, incl) { // incl: 0 recta, 1 inclinada echando agua
  const M = ["#d7e4ea", "#a9bcc8", "#7c8fa2", "#566a80"], d = incl
  c.rect(x, y, 8, 7, M[1]); c.vline(x, y, 7, M[0]); c.vline(x + 7, y, 7, M[3]); c.hline(x, y + 6, 8, M[3])
  c.line(x + 5, y - 1, x + 2, y - 4, M[2]); c.line(x + 2, y - 4, x + 1, y - 1, M[2])   // asa
  c.line(x, y + 4, x - 4, y + 1 + d * 3, M[2], 2); c.rect(x - 6, y + d * 3, 3, 2, M[0])  // pico
}
function gotas(c, x, y, f) {
  for (let k = 0; k < 9; k++) {
    const t = (k * 3 + f * 5) % 13, gx = x - (k % 3) * 2 - t * 0.35, gy = y + t
    c.px(R(gx), R(gy), k % 2 ? "#8fd0e8" : "#d6f0f8")
  }
}
function tierraVuela(c, x, y) { for (const [a, b, col] of [[-3, -1, "#96704c"], [-1, -3, "#7d5a41"], [2, -2, "#ab8358"], [4, 0, "#7d5a41"], [0, 0, "#ab8358"]]) c.px(x + a, y + b, col) }
function chispas(c, x, y) { for (const [a, b] of [[-3, -2], [2, -3], [4, 1], [-2, 2]]) { c.px(x + a, y + b, "#fff2a8"); c.px(x + a + 1, y + b, "#f4c64e") } }
function lineasGolpe(c, x, y) { for (const [a, b] of [[-4, -1], [-3, 2], [3, -2]]) c.px(x + a, y + b, "#fff8e8") }

const CUERPO = (inclina, muslo = 9) => ({ ...MODO.camina, muslo, adelante: 2, rodilla: 6, alzada: 0, brazo: 0, codo: 10, codoVaiven: 0, inclina, balanceo: 0 })
// grip: donde agarran las manos, ang: hacia donde apunta el mango. 0 derecha, 90 abajo, 180 izquierda, 270 arriba. "atras": se pinta detras de Pedro
const GESTOS = {
  Hacha: { dib: hacha, efecto: lineasGolpe, lado: [
      { grip: [20, 15], ang: 305, inc: -6, atras: true }, { grip: [13, 8], ang: 245, inc: -3 }, { grip: [6, 14], ang: 195, inc: 8 },
      { grip: [5, 24], ang: 172, inc: 14, efecto: [-9, 24] }, { grip: [9, 28], ang: 150, inc: 8 } ],
    frente: [ { grip: [24, 15], ang: 305, atras: true }, { grip: [15, 7], ang: 270 }, { grip: [15, 18], ang: 90 }, { grip: [15, 28], ang: 90, efecto: [15, 43] }, { grip: [11, 30], ang: 110 } ],
    espalda: [ { grip: [24, 16], ang: 305 }, { grip: [15, 8], ang: 270 }, { grip: [15, 14], ang: 270, atras: true }, { grip: [15, 18], ang: 270, atras: true, efecto: [15, 1] }, { grip: [11, 24], ang: 250, atras: true } ] },
  Pico: { dib: pico, efecto: chispas, lado: [
      { grip: [21, 17], ang: 320, inc: -8, atras: true }, { grip: [16, 6], ang: 280, inc: -5 }, { grip: [6, 11], ang: 215, inc: 9 },
      { grip: [4, 22], ang: 160, inc: 16, efecto: [-10, 29] }, { grip: [9, 27], ang: 145, inc: 9 } ],
    frente: [ { grip: [25, 17], ang: 315, atras: true }, { grip: [15, 6], ang: 270 }, { grip: [15, 16], ang: 90 }, { grip: [15, 27], ang: 90, efecto: [15, 43] }, { grip: [19, 30], ang: 75 } ],
    espalda: [ { grip: [25, 18], ang: 315 }, { grip: [15, 7], ang: 270 }, { grip: [15, 13], ang: 270, atras: true }, { grip: [15, 17], ang: 270, atras: true, efecto: [15, -2] }, { grip: [19, 24], ang: 290, atras: true } ] },
  Azadon: { dib: azadon, efecto: tierraVuela, lado: [
      { grip: [17, 22], ang: 225, inc: 2 }, { grip: [14, 13], ang: 235, inc: -4 }, { grip: [9, 18], ang: 165, inc: 7 },
      { grip: [8, 28], ang: 128, inc: 15, efecto: [-3, 44] }, { grip: [10, 26], ang: 145, inc: 10 } ],
    frente: [ { grip: [20, 24], ang: 250 }, { grip: [15, 12], ang: 270 }, { grip: [15, 22], ang: 90 }, { grip: [15, 29], ang: 90, efecto: [15, 47] }, { grip: [15, 26], ang: 100 } ],
    espalda: [ { grip: [20, 24], ang: 290, atras: true }, { grip: [15, 12], ang: 270 }, { grip: [15, 16], ang: 270, atras: true }, { grip: [15, 19], ang: 270, atras: true, efecto: [15, 3] }, { grip: [15, 22], ang: 270, atras: true } ] },
}
function herramientaLado(c, g, gesto) {
  const dibuja = () => gesto.dib(c, g.grip[0], g.grip[1], g.ang)
  if (g.atras) dibuja()
  lado(c, 0, CUERPO(g.inc, 8), null, { mano: g.grip })
  if (!g.atras) dibuja()
  if (g.efecto) gesto.efecto(c, g.efecto[0], g.efecto[1])
}
function herramientaFrente(c, g, gesto, espalda) {
  const dibuja = () => gesto.dib(c, g.grip[0], g.grip[1], g.ang)
  if (g.atras) dibuja()
  frente(c, 0, CUERPO(0, 7), espalda, { manos: g.grip, ambas: true })
  if (!g.atras) dibuja()
  if (g.efecto) gesto.efecto(c, g.efecto[0], g.efecto[1])
}
const enLienzo = (fn) => layer("p", { x: LX, y: LY }, fn)
for (const [herr, gesto] of Object.entries(GESTOS)) {
  gesto.lado.forEach((g, i) => {
    sprite(`PedroN_${herr}Izquierda${i + 1}`, OH, enLienzo((c) => herramientaLado(c, g, gesto)))
    sprite(`PedroN_${herr}Derecha${i + 1}`, { ...OH, flip: "x" }, enLienzo((c) => herramientaLado(c, g, gesto)))
  })
  gesto.frente.forEach((g, i) => sprite(`PedroN_${herr}Abajo${i + 1}`, OH, enLienzo((c) => herramientaFrente(c, g, gesto, false))))
  gesto.espalda.forEach((g, i) => sprite(`PedroN_${herr}Arriba${i + 1}`, OH, enLienzo((c) => herramientaFrente(c, g, gesto, true))))
}
// Regar: acerca la regadera, la inclina y cae el agua
const REGAR = [{ incl: 0, ag: false, g: [10, 24] }, { incl: 1, ag: true, g: [8, 25] }, { incl: 1, ag: true, g: [8, 25] }, { incl: 1, ag: true, g: [8, 25] }]
REGAR.forEach((r, i) => {
  const lat = (c) => { lado(c, 0, CUERPO(5, 7), null, { mano: r.g }); regadera(c, r.g[0] - 7, r.g[1] - 2, r.incl); if (r.ag) gotas(c, r.g[0] - 13, r.g[1] + 2, i) }
  sprite(`PedroN_RegarIzquierda${i + 1}`, OH, enLienzo(lat))
  sprite(`PedroN_RegarDerecha${i + 1}`, { ...OH, flip: "x" }, enLienzo(lat))
  sprite(`PedroN_RegarAbajo${i + 1}`, OH, enLienzo((c) => { frente(c, 0, CUERPO(0, 7), false, { manos: [15, 27], ambas: true }); regadera(c, 12, 26, r.incl); if (r.ag) gotas(c, 8, 33, i) }))
  sprite(`PedroN_RegarArriba${i + 1}`, OH, enLienzo((c) => { if (r.ag) gotas(c, 12, 3, i); regadera(c, 12, 13, r.incl); frente(c, 0, CUERPO(0, 7), true, { manos: [15, 20], ambas: true }) }))
})
// Pescar: lanzar, esperar y recoger. La caña mide 22 pixeles y el punto "Punta" lleva la linea
function cana(c, x, y, ang, curva = 0) {
  let px_ = x, py_ = y
  for (let k = 1; k <= 22; k++) {
    const q = (ang + curva * k * k * 0.05) * RAD
    const nx = px_ + Math.cos(q), ny = py_ + Math.sin(q)
    c.px(R(nx), R(ny), k < 7 ? "#6f4b35" : k < 15 ? "#b58a55" : "#e3c478")
    if (k < 7) c.px(R(nx), R(ny) + 1, "#9a6d48")
    px_ = nx; py_ = ny
  }
  return [px_, py_]
}
const POSES_CANA = {
  Lanzar: [ { g: [20, 17], ang: 305, inc: -8 }, { g: [11, 14], ang: 250, inc: 0 }, { g: [5, 22], ang: 205, inc: 12 } ],
  Esperar: [ { g: [9, 24], ang: 205, inc: 2 }, { g: [9, 25], ang: 207, inc: 2 } ],
  Tirar: [ { g: [12, 22], ang: 250, inc: -7, curva: 3 }, { g: [13, 21], ang: 262, inc: -9, curva: 4 } ],
}
for (const [nom, poses] of Object.entries(POSES_CANA)) poses.forEach((p, i) => {
  const lat = (c) => { lado(c, 0, CUERPO(p.inc, 7), null, { mano: p.g }); cana(c, p.g[0], p.g[1], p.ang, p.curva || 0) }
  sprite(`PedroN_Pesca${nom}Izquierda${i + 1}`, OH, enLienzo(lat))
  sprite(`PedroN_Pesca${nom}Derecha${i + 1}`, { ...OH, flip: "x" }, enLienzo(lat))
  const ajuste = p.ang > 270 ? 0 : p.ang < 225 ? 40 : 0
  sprite(`PedroN_Pesca${nom}Abajo${i + 1}`, OH, enLienzo((c) => { frente(c, 0, CUERPO(0, 7), false, { manos: [15, 25 - (nom === "Tirar" ? 5 : 0)], ambas: true }); cana(c, 15, 25 - (nom === "Tirar" ? 5 : 0), nom === "Lanzar" ? [270, 280, 80][i] : nom === "Esperar" ? 72 + ajuste * 0 : 285 + i * 8, p.curva || 0) }))
  sprite(`PedroN_Pesca${nom}Arriba${i + 1}`, OH, enLienzo((c) => { cana(c, 15, 14, nom === "Lanzar" ? [80, 270, 280][i] : nom === "Esperar" ? 282 : 262 - i * 6, p.curva || 0); frente(c, 0, CUERPO(0, 7), true, { manos: [15, 20], ambas: true }) }))
})

// ---------- ELENCO DE LA HISTORIA: mismo esqueleto, otra ropa ----------
const T_ = (a, b, c_, d) => [a, b, c_, d]
const ELENCO = {
  Hetol: { piel: ["#ecc4a2", "#d6a180", "#b07c66", "#83594f"], pelo: T_("#9c8a78", "#7a6a5c", "#5a4e46", "#3f3836"), camisa: T_("#7f9a68", "#5f7c52", "#465e42", "#324634"), overol: T_("#8a6e54", "#6a5240", "#4f3c30", "#382a24"),
    peto: false, bigote: T_("#d8d4cc", "#a8a49c", "#7c7a78", "#55535a"), sombrero: "paja", cinta: ["#4c97a0", "#2e6e7c"], ojo: "#2e2622", boton: "#d9b86a" },
  Chuchini: { piel: ["#e6b98d", "#cf9568", "#a96f50", "#7e4e40"], pelo: T_("#4f3a2c", "#3a2a22", "#2a1f1c", "#1c1516"), camisa: T_("#7fa6d0", "#5782b0", "#3f6490", "#2f4a70"), overol: T_("#8a7a5c", "#6a5c46", "#4e4436", "#38322a"),
    peto: false, bigote: T_("#5a4434", "#3f2f26", "#2c211e", "#1c1516"), sombrero: "ninguno", ojo: "#2e2622", boton: "#e6e0d0" },
  ChuchiniSombrero: { piel: ["#e6b98d", "#cf9568", "#a96f50", "#7e4e40"], pelo: T_("#4f3a2c", "#3a2a22", "#2a1f1c", "#1c1516"), camisa: T_("#7fa6d0", "#5782b0", "#3f6490", "#2f4a70"), overol: T_("#8a7a5c", "#6a5c46", "#4e4436", "#38322a"),
    peto: false, bigote: T_("#5a4434", "#3f2f26", "#2c211e", "#1c1516"), sombrero: "paja", ojo: "#2e2622", boton: "#e6e0d0" },
  ChuchiniViejo: { piel: ["#e0b490", "#c89270", "#a3705a", "#78503f"], pelo: T_("#e4e0d8", "#c0bcb4", "#94928e", "#6a6a6c"), camisa: T_("#a0b4c4", "#7c92a6", "#5f7488", "#465868"), overol: T_("#8a7a5c", "#6a5c46", "#4e4436", "#38322a"),
    peto: false, barba: T_("#f2efe6", "#d6d2c8", "#aaa8a4", "#7e7e82"), sombrero: "paja", ojo: "#352b2a", boton: "#e6e0d0" },
  PedroSin: { sombrero: "ninguno" },
  ChuchiniViejoSin: { piel: ["#e0b490", "#c89270", "#a3705a", "#78503f"], pelo: T_("#e4e0d8", "#c0bcb4", "#94928e", "#6a6a6c"), camisa: T_("#a0b4c4", "#7c92a6", "#5f7488", "#465868"), overol: T_("#8a7a5c", "#6a5c46", "#4e4436", "#38322a"),
    peto: false, barba: T_("#f2efe6", "#d6d2c8", "#aaa8a4", "#7e7e82"), sombrero: "ninguno", ojo: "#352b2a", boton: "#e6e0d0" },
  Tomas: { piel: ["#e6b98d", "#cf9568", "#a96f50", "#7e4e40"], pelo: T_("#f2efe6", "#d6d2c8", "#aaa8a4", "#7e7e82"), camisa: T_("#7fb1d2", "#568bb2", "#3f6a90", "#2f4f70"), overol: T_("#8d6b4c", "#6f5240", "#533d32", "#3c2c28"),
    peto: false, barba: T_("#fbf9f2", "#dedbd2", "#b3b1ac", "#858487"), sombrero: "paja", cinta: ["#8b4a42", "#6a3a36"], ojo: "#352b2a", boton: "#d9b86a" },
}
for (const [n, r] of Object.entries(ELENCO)) {
  for (let i = 0; i < CICLO; i++) sprite(`Actor_${n}_Camina${i + 1}`, O, (c) => lado(c, i, MODO.camina, null, { ropa: r }))
  const quieto = { ...MODO.camina, muslo: 0, adelante: 0, rodilla: 0, alzada: 0, brazo: 0, codo: 8, codoVaiven: 0, inclina: 1, balanceo: 0 }
  sprite(`Actor_${n}_Lado1`, O, (c) => lado(c, 0, quieto, null, { ropa: r })); sprite(`Actor_${n}_Lado2`, O, (c) => lado(c, 0, quieto, null, { ropa: r, respira: 1 }))
  sprite(`Actor_${n}_Frente1`, O, (c) => frente(c, 0, quieto, false, { ropa: r })); sprite(`Actor_${n}_Frente2`, O, (c) => frente(c, 0, quieto, false, { ropa: r, respira: 1 }))
}
// Pedro cae rendido: se tambalea, de rodillas, tendido
const CAIDA = (inc, muslo) => ({ ...MODO.camina, muslo, adelante: 8, rodilla: 18, alzada: 0, brazo: 12, codo: 20, codoVaiven: 0, inclina: inc, balanceo: 0, aire: 0 })
sprite("Actor_PedroCae1", O, (c) => lado(c, 1, CAIDA(10, 12), null, { ropa: ELENCO.PedroSin, parpadeo: true }))
sprite("Actor_PedroCae2", O, (c) => lado(c, 2, CAIDA(26, 18), null, { ropa: ELENCO.PedroSin, parpadeo: true }))
sprite("Actor_PedroCae3", { w: 46, h: 30, outline: "K", rot: 90 }, layer("p", { x: 0, y: 0 }, (c) => frente(c, 0, FIRME, false, { ropa: ELENCO.PedroSin, parpadeo: true })))
sprite("Actor_SombreroSuelo", { w: 22, h: 10, outline: "K" }, (c) => { const q = PEDRO.paja; c.ellipse(11, 7, 10, 2, q[1]); c.ellipse(9, 6, 7, 1, q[0]); c.rect(6, 2, 10, 4, q[1]); c.hline(7, 1, 8, q[0]); c.hline(6, 5, 10, PEDRO.cinta[0]); c.vline(15, 2, 3, q[2]) })
sprite("Actor_Sombrero", { w: 24, h: 12, outline: "K" }, (c) => { const q = PEDRO.paja; c.ellipse(12, 9, 11, 2, q[1]); c.ellipse(10, 8, 8, 1, q[0]); c.rect(7, 3, 10, 5, q[1]); c.hline(8, 2, 8, q[0]); c.hline(7, 6, 10, PEDRO.cinta[0]); c.vline(16, 3, 4, q[2]) })
// Farol de Tomas
sprite("Actor_Farol", { w: 7, h: 11, outline: "K" }, (c) => { c.rect(1, 3, 5, 6, "#ffd777"); c.px(2, 4, "#fff4c0"); c.hline(1, 2, 5, "#5c6470"); c.hline(1, 9, 5, "#5c6470"); c.px(3, 0, "#5c6470"); c.px(3, 1, "#5c6470") })
sprite("Actor_Halo", { w: 64, h: 64 }, layer("h", { density: 0.28 }, (c) => c.circ(32, 32, 31, "#ffd777")), layer("h2", { density: 0.32 }, (c) => c.circ(32, 32, 18, "#fff0b0")))
// Zanahoria recien cosechada
sprite("Zanahoria_Icono", { w: 30, h: 30, outline: "K" }, (c) => {
  const V_ = ["#2c5540", "#3a6e45", "#4f8a49", "#6ea552", "#93bf60"], Z = ["#ffc27a", "#f09a3f", "#d0702a", "#9c4f24"]
  c.poly([9, 13, 19, 9, 22, 13, 8, 27, 6, 26], Z[1])
  c.clip((x, y) => x + y < 26, () => c.poly([9, 13, 19, 9, 22, 13, 8, 27, 6, 26], Z[0]))
  c.clip((x, y) => x + y > 33, () => c.poly([9, 13, 19, 9, 22, 13, 8, 27, 6, 26], Z[2]))
  for (const [x, y, l] of [[9, 18, 3], [13, 15, 4], [12, 20, 2], [16, 13, 3]]) for (let k = 0; k < l; k++) c.px(x + k, y + k, Z[3])
  for (const [dx, dy, t] of [[0, -8, 3], [4, -7, 2], [-3, -6, 4], [6, -4, 3], [3, -9, 4]]) { c.line(20, 10, 20 + dx, 10 + dy, V_[t], 2); c.px(20 + dx, 10 + dy, V_[4]) }
})

// ---------- ESPADA LARGA: lienzo mayor para que quepan la hoja y el tajo ----------
const OE = { w: 80, h: 84, outline: "K" }
const enE = (fn) => layer("p", { x: 25, y: 20 }, fn)
function espadaLarga(c, x0, y0, x1, y1) {
  const L_ = Math.hypot(x1 - x0, y1 - y0) || 1, ux = (x1 - x0) / L_, uy = (y1 - y0) / L_, nx = -uy, ny = ux
  c.line(x0 + R(ux * 3), y0 + R(uy * 3), x1, y1, "#c8d2d8", 2)                         // hoja
  c.line(x0 + R(ux * 3) + R(nx), y0 + R(uy * 3) + R(ny), x1 + R(nx), y1 + R(ny), "#7f8c98") // filo en sombra
  c.line(x0 + R(ux * 5), y0 + R(uy * 5), x0 + R(ux * (L_ - 4)), y0 + R(uy * (L_ - 4)), "#eef4f6") // brillo
  c.px(x1, y1, "#ffffff")
  c.line(x0 + R(ux * 2 + nx * 4), y0 + R(uy * 2 + ny * 4), x0 + R(ux * 2 - nx * 4), y0 + R(uy * 2 - ny * 4), "#d9b86a", 2) // guarda
  c.line(x0 - R(ux * 3), y0 - R(uy * 3), x0 + R(ux), y0 + R(uy), "#7a4f30", 2)          // empuñadura
  c.px(x0 - R(ux * 4), y0 - R(uy * 4), "#e8c76f")
}
function tajoLargo(c, cx, cy, r, a, b) {
  const m = (a + b) / 2, medio = (b - a) / 2
  for (let t = a; t <= b; t += 2) {
    const q = t * RAD, ancho = 1 + R(2.6 * (1 - Math.abs(t - m) / medio))
    for (let k = 0; k < ancho; k++) c.px(R(cx + Math.cos(q) * (r - k)), R(cy + Math.sin(q) * (r - k)), k === 0 ? "#fffdf0" : "#f4e7c8")
  }
}
const E_ = (d, f, fn, extra = {}) => sprite(`PedroN_Espada${d}${f}`, { ...OE, ...extra }, enE(fn))
E_("Abajo", 1, (c) => { espadaLarga(c, 4, 25, -8, 5); frente(c, 0, FIRME, false, { manos: [4, 25] }) })
E_("Abajo", 2, (c) => { frente(c, 0, FIRME, false, { manos: [15, 33] }); tajoLargo(c, 15, 28, 29, 28, 152); espadaLarga(c, 15, 33, 29, 56) })
E_("Abajo", 3, (c) => { frente(c, 0, FIRME, false, { manos: [25, 27] }); espadaLarga(c, 25, 27, 38, 6) })
E_("Arriba", 1, (c) => { frente(c, 0, FIRME, true); espadaLarga(c, 25, 26, 38, 5) })
E_("Arriba", 2, (c) => { tajoLargo(c, 15, 22, 29, 208, 332); espadaLarga(c, 10, 18, -2, -12); frente(c, 0, FIRME, true) })
E_("Arriba", 3, (c) => { espadaLarga(c, 4, 26, -9, 6); frente(c, 0, FIRME, true) })
for (const [n, fl] of [["Izquierda", {}], ["Derecha", { flip: "x" }]]) {
  E_(n, 1, (c) => { espadaLarga(c, 22, 22, 36, 1); lado(c, 0, FIRME, null, { mano: [22, 22] }) }, fl)
  E_(n, 2, (c) => { tajoLargo(c, 12, 27, 31, 122, 238); lado(c, 0, FIRME, null, { mano: [7, 28] }); espadaLarga(c, 7, 28, -21, 28) }, fl)
  E_(n, 3, (c) => { lado(c, 0, FIRME, null, { mano: [9, 31] }); espadaLarga(c, 8, 31, -16, 44) }, fl)
}
