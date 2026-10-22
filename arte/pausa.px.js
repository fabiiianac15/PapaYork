// Menu de pausa dentro de la mochila (pestanas Mochila / Opciones / Salir), como en Stardew.
// Mismo estilo que el menu: madera oscura con contorno, interior hundido y baba radiactiva.
pal({
  k: "#24150d",                               // contorno
  D: "#4a2a17", d: "#6e4024", m: "#8f5a32",   // madera del marco (oscuro -> claro)
  s: "#a8763f", w: "#c99a5e", W: "#dcb57c",   // tablas
  i: "#5a3a22", I: "#7a5233", j: "#9a6c43",   // interior hundido de la casilla
  n: "#55555e", N: "#a9a9b4",                 // clavos
  G: "#4f9a1f", g: "#8fdc2e", h: "#d6ff6a",   // baba radiactiva
  L: "#2f6b2a", l: "#4f9a3c", e: "#7cc25a",   // hojas
  p: "#2a1a10", P: "#3b2616",                 // fondo oscuro de la caja de informacion
})
ramps("kDdm", "sWw", "iIj", "nN", "Ggh", "Lle", "pP")

// ---------- utilidades (copiadas de menu_ui.px.js para que cada archivo se lea solo) ----------
function tablas(c, x0, y0, w, h, alto, seed) {
  const r = c.rng(seed)
  for (let y = y0; y < y0 + h; y += alto) {
    const hh = Math.min(alto, y0 + h - y)
    c.rect(x0, y, w, hh, "w")
    c.hline(x0, y, w, "W")
    if (y + hh < y0 + h) c.hline(x0, y + hh - 1, w, "s")
    for (let k = 0; k < w / 14; k++) {
      const vx = x0 + Math.floor(r() * (w - 10)), vy = y + 2 + Math.floor(r() * Math.max(1, hh - 4))
      c.hline(vx, vy, 3 + Math.floor(r() * 6), "s")
    }
    c.vline(x0 + 20 + Math.floor(r() * (w - 40)), y + 1, hh - 2, "s")
  }
}
function marco(c, w, h, t) {
  c.rect(0, 0, w, h, "k")
  c.rect(1, 1, w - 2, h - 2, "d")
  c.rect(1, 1, w - 2, 2, "m"); c.rect(1, 1, 2, h - 2, "m")
  c.rect(1, h - 3, w - 2, 2, "D"); c.rect(w - 3, 1, 2, h - 2, "D")
  const r = c.rng(w * 7 + h)
  for (let k = 0; k < (w + h) / 6; k++) {
    const x = 4 + Math.floor(r() * (w - 14))
    c.hline(x, 4 + Math.floor(r() * (t - 7)), 3 + Math.floor(r() * 5), "D")
    c.hline(x, h - t + 2 + Math.floor(r() * (t - 6)), 3 + Math.floor(r() * 5), "D")
  }
  c.line(1, 1, t - 1, t - 1, "D"); c.line(w - 2, 1, w - t, t - 1, "D")
  c.line(1, h - 2, t - 1, h - t, "D"); c.line(w - 2, h - 2, w - t, h - t, "D")
  c.box(t - 1, t - 1, w - 2 * t + 2, h - 2 * t + 2, "k")
  for (const [cx, cy] of [[t / 2, t / 2], [w - 1 - t / 2, t / 2], [t / 2, h - 1 - t / 2], [w - 1 - t / 2, h - 1 - t / 2]]) {
    const x = Math.round(cx), y = Math.round(cy)
    c.circ(x, y, 2, "k"); c.rect(x - 1, y - 1, 2, 2, "n"); c.px(x - 1, y - 1, "N")
  }
}
function babas(c, x0, y, w, n, seed, maxLen = 7) {
  const r = c.rng(seed)
  for (let k = 0; k < n; k++) {
    const x = x0 + Math.floor(r() * w), len = 2 + Math.floor(r() * maxLen)
    c.rect(x - 1, y, 4, 2, "G"); c.hline(x, y, 2, "g")
    c.vline(x, y, len, "g"); c.vline(x + 1, y, len, "G")
    c.rect(x - 1, y + len, 3, 3, "g"); c.px(x - 1, y + len, "h")
  }
}


// ---------- panel de las pestanas Opciones y Salir: igual que la mochila pero sin casillas ----------
sprite("PanelPausa", { w: 380, h: 200 }, (c) => {
  marco(c, 380, 200, 10)
  tablas(c, 10, 10, 360, 180, 15, 33)
  babas(c, 16, 10, 348, 12, 13)
  c.hline(20, 32, 340, "s"); c.hline(20, 33, 340, "W")            // linea bajo el titulo
}, stamp("_hojaPeq", 1, 1, { flip: "x" }), stamp("_hojaPeq", 372, 1), stamp("_hojaPeq", 1, 192, { flip: "xy" }),
   stamp("_hojaPeq", 372, 192, { flip: "y" }))

sprite("_hojaPeq", { outline: "k" }, `
  ...le
  .llle
  lleel
  lelL.
  lL...`)

// ---------- pestanas 28x24 (la activa es mas clara y sube 3px) ----------
function pestana(c, activa) {
  const y0 = activa ? 0 : 3
  c.rect(0, y0, 28, 24 - y0, "k")
  c.rect(1, y0 + 1, 26, 23 - y0, activa ? "m" : "d")
  c.hline(1, y0 + 1, 26, activa ? "W" : "m"); c.vline(1, y0 + 1, 22 - y0, activa ? "W" : "m")
  c.vline(26, y0 + 1, 22 - y0, "D")
  c.rect(3, y0 + 3, 22, 19 - y0, activa ? "w" : "s")
  c.hline(3, y0 + 3, 22, activa ? "W" : "w")
  if (activa) { c.rect(4, y0 + 1, 3, 2, "g"); c.px(5, y0 + 3, "g"); c.vline(5, y0 + 3, 3, "g"); c.px(5, y0 + 6, "h") }
}
function icoMochila(c, dy) {
  c.rect(8, 8 + dy, 12, 11, "k"); c.rect(9, 9 + dy, 10, 9, "m"); c.rect(9, 9 + dy, 10, 3, "W")
  c.box(11, 5 + dy, 6, 4, "k"); c.rect(11, 13 + dy, 6, 3, "D"); c.px(14, 14 + dy, "N")
}
function icoEngrane(c, dy) {
  const cx = 14, cy = 13 + dy
  for (const [x, y] of [[0, -7], [0, 7], [-7, 0], [7, 0], [-5, -5], [5, -5], [-5, 5], [5, 5]]) { c.rect(cx + x - 2, cy + y - 2, 4, 4, "k"); c.rect(cx + x - 1, cy + y - 1, 2, 2, "N") }
  c.circ(cx, cy, 6, "k"); c.circ(cx, cy, 5, "N"); c.circ(cx + 1, cy + 1, 4, "n"); c.circ(cx, cy, 4, "N"); c.circ(cx, cy, 2, "k")
}
function icoPuerta(c, dy) {
  c.rect(9, 6 + dy, 11, 15, "k"); c.rect(10, 7 + dy, 9, 14, "d"); c.vline(14, 7 + dy, 14, "D")
  c.rect(10, 7 + dy, 9, 2, "m"); c.px(17, 14 + dy, "g"); c.px(16, 14 + dy, "h")
  c.hline(3, 13 + dy, 6, "G"); c.line(3, 13 + dy, 5, 11 + dy, "G"); c.line(3, 13 + dy, 5, 15 + dy, "G"); c.px(4, 13 + dy, "h")
}
for (const [nombre, ico] of [["Mochila", icoMochila], ["Opciones", icoEngrane], ["Salir", icoPuerta]]) {
  sprite("Pestana" + nombre, { w: 28, h: 24 }, (c) => { pestana(c, false); ico(c, 2) })
  sprite("Pestana" + nombre + "Activa", { w: 28, h: 24 }, (c) => { pestana(c, true); ico(c, 0) })
}

// ---------- boton largo 150x24 de tabla, con hover radiactivo ----------
function boton(c, hover) {
  c.rect(0, 0, 150, 24, "k")
  c.rect(1, 1, 148, 22, hover ? "m" : "d")
  c.hline(1, 1, 148, hover ? "W" : "m"); c.hline(1, 22, 148, "D")
  c.rect(3, 3, 144, 18, hover ? "W" : "w"); c.hline(3, 3, 144, hover ? "w" : "W"); c.hline(3, 20, 144, "s")
  const r = c.rng(5); for (let k = 0; k < 9; k++) c.hline(6 + Math.floor(r() * 130), 6 + Math.floor(r() * 12), 4, "s")
  for (const x of [5, 144]) { c.rect(x - 1, 10, 2, 2, "n"); c.px(x - 1, 10, "N") }
  if (hover) { babas(c, 10, 21, 130, 5, 3, 2) }
}
sprite("BotonPausa", { w: 150, h: 26 }, (c) => boton(c, false))
sprite("BotonPausaHover", { w: 150, h: 26 }, (c) => boton(c, true))

// ---------- barra de volumen ----------
sprite("BarraVol", { w: 104, h: 10 }, (c) => { c.rect(0, 0, 104, 10, "k"); c.rect(1, 1, 102, 8, "p"); c.hline(1, 1, 102, "P") })
sprite("BarraVolRelleno", { w: 100, h: 6 }, (c) => { c.rect(0, 0, 100, 6, "G"); c.hline(0, 0, 100, "h"); c.hline(0, 1, 100, "g"); for (let x = 4; x < 100; x += 9) c.px(x, 3, "g") })

sheet("pausa", ["PanelPausa", "Pestana*", "BotonPausa*", "BarraVol*"], { pad: 2 })
