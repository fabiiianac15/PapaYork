// Interfaz del menu principal de Papayork: paneles de madera con baba radiactiva,
// a juego con los letreros de los botones (marco marron, tablas claras, clavos, hojas).
pal({
  k: "#24150d",            // contorno
  D: "#4a2a17", d: "#6e4024", m: "#8f5a32",   // marco de madera (oscuro -> claro)
  s: "#a8763f", w: "#c99a5e", W: "#dcb57c",   // tablas interiores
  n: "#55555e", N: "#a9a9b4",                 // clavos
  G: "#4f9a1f", g: "#8fdc2e", h: "#d6ff6a",   // baba radiactiva
  L: "#2f6b2a", l: "#4f9a3c", e: "#7cc25a",   // hojas
  x: "#000000",
})
ramps("kDdm", "sWw", "nN", "Ggh", "Lle")

// Tablas horizontales con vetas y juntas desplazadas, dentro de un rectangulo.
function tablas(c, x0, y0, w, h, alto, seed) {
  const r = c.rng(seed)
  for (let y = y0; y < y0 + h; y += alto) {
    const hh = Math.min(alto, y0 + h - y)
    c.rect(x0, y, w, hh, "w")
    c.hline(x0, y, w, "W")
    if (y + hh < y0 + h) c.hline(x0, y + hh - 1, w, "s")
    // vetas: trazos cortos siguiendo la tabla
    for (let i = 0; i < w / 14; i++) {
      const vx = x0 + Math.floor(r() * (w - 10)), vy = y + 2 + Math.floor(r() * Math.max(1, hh - 4))
      c.hline(vx, vy, 3 + Math.floor(r() * 6), "s")
    }
    // junta vertical entre tablas
    const jx = x0 + 20 + Math.floor(r() * (w - 40))
    c.vline(jx, y + 1, hh - 2, "s")
  }
}

// Marco de madera grueso: vigas con canto claro, vetas y clavos grandes en las esquinas.
function marco(c, w, h, t) {
  c.rect(0, 0, w, h, "k")
  c.rect(1, 1, w - 2, h - 2, "d")
  // canto iluminado arriba/izquierda, sombra abajo/derecha
  c.rect(1, 1, w - 2, 2, "m"); c.rect(1, 1, 2, h - 2, "m")
  c.rect(1, h - 3, w - 2, 2, "D"); c.rect(w - 3, 1, 2, h - 2, "D")
  const r = c.rng(w * 7 + h)
  for (let i = 0; i < (w + h) / 6; i++) {
    const x = 4 + Math.floor(r() * (w - 14))
    c.hline(x, 4 + Math.floor(r() * (t - 7)), 3 + Math.floor(r() * 5), "D")
    c.hline(x, h - t + 2 + Math.floor(r() * (t - 6)), 3 + Math.floor(r() * 5), "D")
  }
  for (let i = 0; i < (w + h) / 10; i++) {
    const y = t + Math.floor(r() * (h - 2 * t - 6))
    c.vline(3 + Math.floor(r() * (t - 6)), y, 3 + Math.floor(r() * 4), "D")
    c.vline(w - t + 2 + Math.floor(r() * (t - 6)), y, 3 + Math.floor(r() * 4), "D")
  }
  // juntas de las vigas en las esquinas (inglete)
  c.line(1, 1, t - 1, t - 1, "D"); c.line(w - 2, 1, w - t, t - 1, "D")
  c.line(1, h - 2, t - 1, h - t, "D"); c.line(w - 2, h - 2, w - t, h - t, "D")
  c.box(t - 1, t - 1, w - 2 * t + 2, h - 2 * t + 2, "k")
  for (const [cx, cy] of [[t / 2, t / 2], [w - 1 - t / 2, t / 2], [t / 2, h - 1 - t / 2], [w - 1 - t / 2, h - 1 - t / 2]]) {
    const x = Math.round(cx), y = Math.round(cy)
    c.circ(x, y, 3, "k"); c.circ(x, y, 2, "n"); c.px(x - 1, y - 1, "N"); c.px(x, y - 1, "N")
  }
}

// Gotas de baba que cuelgan de un borde horizontal: chorro de 2px con gota al final.
function babas(c, x0, y, w, n, seed, maxLen = 9) {
  const r = c.rng(seed)
  for (let i = 0; i < n; i++) {
    const x = x0 + Math.floor(r() * w), len = 2 + Math.floor(r() * maxLen)
    c.rect(x - 1, y, 4, 2, "G"); c.hline(x, y, 2, "g")
    c.vline(x, y, len, "g"); c.vline(x + 1, y, len, "G")
    c.rect(x - 1, y + len, 3, 3, "g"); c.px(x - 1, y + len, "h"); c.px(x + 1, y + len + 2, "G")
    if (r() < 0.4) { c.px(x, y + len + 5, "g"); c.px(x, y + len + 6, "G") }
  }
}

// Hoja con nervio y contorno (parte reutilizable).
sprite("_hoja", { outline: "k" }, `
  .....le
  ...llle
  ..lleel
  .lleell
  lleelL.
  leelL..
  llLL...
  L......`)

sprite("PanelMadera", { w: 300, h: 240 }, (c) => {
  marco(c, 300, 240, 12)
  tablas(c, 12, 12, 276, 216, 16, 7)
  babas(c, 18, 12, 262, 16, 3)
}, stamp("_hoja", 0, 0, { flip: "x" }), stamp("_hoja", 9, 0), stamp("_hoja", 290, 0),
   stamp("_hoja", 0, 229, { flip: "xy" }), stamp("_hoja", 289, 229, { flip: "y" }))

function tarjeta(c, w, h, borde) {
  c.rect(0, 0, w, h, "k")
  c.rect(1, 1, w - 2, h - 2, borde)
  tablas(c, 3, 3, w - 6, h - 6, 14, w + h)
  c.hline(3, 3, w - 6, "W")
}
sprite("Ranura", { w: 264, h: 46 }, (c) => { tarjeta(c, 264, 46, "d") })
sprite("RanuraHover", { w: 264, h: 46 }, (c) => {
  tarjeta(c, 264, 46, "g"); c.box(1, 1, 262, 44, "h"); c.box(2, 2, 260, 42, "G")
  babas(c, 10, 3, 244, 7, 11, 5)
})

sprite("BotonPeq", { w: 84, h: 22 }, (c) => { tarjeta(c, 84, 22, "d"); c.hline(3, 18, 78, "s") })
sprite("BotonPeqHover", { w: 84, h: 22 }, (c) => {
  tarjeta(c, 84, 22, "g"); c.box(1, 1, 82, 20, "h")
})

// Mas/menos para el volumen.
sprite("BotonMini", { w: 18, h: 18 }, (c) => { tarjeta(c, 18, 18, "d") })
sprite("BotonMiniHover", { w: 18, h: 18 }, (c) => { tarjeta(c, 18, 18, "g"); c.box(1, 1, 16, 16, "h") })

// Espora radiactiva flotante para el ambiente del menu.
sprite("Espora", `
  .G.
  GhG
  .G.`)

sprite("Negro", { w: 8, h: 8 }, rect(0, 0, 8, 8, "x"))
