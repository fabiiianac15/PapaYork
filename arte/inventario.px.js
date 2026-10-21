// Inventario de Papayork: casillas, barra rapida, mochila y caja de informacion.
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

// ---------- casillas 34x34 ----------
// Marco de madera de 3px y fondo hundido: sombra arriba/izquierda, luz abajo/derecha.
function casilla(c, borde, luz, sombra) {
  c.rect(0, 0, 34, 34, "k")
  c.rect(1, 1, 32, 32, borde)
  c.hline(1, 1, 32, luz); c.vline(1, 1, 32, luz)
  c.hline(1, 32, 32, sombra); c.vline(32, 1, 32, sombra)
  c.box(3, 3, 28, 28, "k")
  c.rect(4, 4, 26, 26, "I")
  c.hline(4, 4, 26, "i"); c.vline(4, 4, 26, "i")      // borde interior en sombra
  c.hline(5, 5, 25, "i")
  c.hline(4, 29, 26, "j"); c.vline(29, 5, 25, "j")    // reflejo abajo/derecha
}
sprite("Casilla", { w: 34, h: 34 }, (c) => casilla(c, "d", "m", "D"))
sprite("CasillaHover", { w: 34, h: 34 }, (c) => {
  casilla(c, "m", "W", "d"); c.rect(5, 6, 24, 23, "j"); c.hline(5, 6, 24, "I")
})
// Seleccionada: el marco se vuelve baba radiactiva y brilla en las esquinas.
sprite("CasillaSeleccionada", { w: 34, h: 34 }, (c) => {
  casilla(c, "G", "h", "G")
  c.box(2, 2, 30, 30, "g")
  for (const [x, y] of [[0, 0], [29, 0], [0, 29], [29, 29]]) {
    c.rect(x, y, 5, 5, "h"); c.box(x, y, 5, 5, "k"); c.px(x + 2, y + 2, "g")
  }
})

// ---------- fondo de la barra rapida: tabla larga detras de las 10 casillas ----------
sprite("BarraRapida", { w: 352, h: 42 }, (c) => {
  marco(c, 352, 42, 4)
  tablas(c, 4, 4, 344, 34, 17, 21)
  babas(c, 12, 4, 330, 9, 8, 3)
}, stamp("_hojaPeq", 0, 0, { flip: "x" }), stamp("_hojaPeq", 343, 0))

sprite("_hojaPeq", { outline: "k" }, `
  ...le
  .llle
  lleel
  lelL.
  lL...`)

// ---------- mochila: 3 filas de 10 casillas + caja de informacion ----------
// Interior: titulo (y 12..28), casillas desde y 30 (3 x 36 = 108), info desde y 144.
sprite("PanelMochila", { w: 380, h: 200 }, (c) => {
  marco(c, 380, 200, 10)
  tablas(c, 10, 10, 360, 180, 15, 33)
  babas(c, 16, 10, 348, 12, 13)
  // caja de informacion hundida al fondo del panel
  c.rect(14, 146, 352, 42, "k")
  c.rect(15, 147, 350, 40, "p")
  c.hline(15, 147, 350, "k"); c.hline(15, 148, 350, "P")
  c.hline(15, 186, 350, "P")
}, stamp("_hojaPeq", 1, 1, { flip: "x" }), stamp("_hojaPeq", 372, 1), stamp("_hojaPeq", 1, 192, { flip: "xy" }),
   stamp("_hojaPeq", 372, 192, { flip: "y" }))

// Etiqueta flotante con el nombre del objeto en la mano (aparece sobre la barra al cambiar).
sprite("EtiquetaItem", { w: 120, h: 16 }, (c) => {
  c.rect(0, 0, 120, 16, "k"); c.rect(1, 1, 118, 14, "p"); c.hline(1, 1, 118, "P")
  c.px(0, 0, "_"); c.px(119, 0, "_"); c.px(0, 15, "_"); c.px(119, 15, "_")
})
