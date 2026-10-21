// Puestos del pueblo, panel de la tienda e iconos de mejoras. Paleta DB32 + madera de la interfaz.
pal({
  k: "#000000", n: "#222034", p: "#45283c", b: "#663931", c: "#8f563b", o: "#df7126",
  t: "#d9a066", T: "#eec39a", y: "#fbf236", L: "#99e550", g: "#6abe30", G: "#37946e", d: "#4b692f",
  e: "#323c39", s: "#9badb7", S: "#cbdbfc", w: "#ffffff", r: "#696a6a", R: "#847e87", m: "#595652",
  a: "#8a6f30", x: "#ac3232", X: "#d95763", u: "#3f3f74",
  // madera de la interfaz
  K: "#24150d", D: "#4a2a17", M: "#6e4024", N: "#8f5a32", W: "#dcb57c", Z: "#c99a5e", P: "#2a1a10", Q: "#3b2616",
  h: "#d6ff6a", H: "#4f9a1f",
})
ramps("kpbcotT", "kerRw", "kdgL")

// ---------- PUESTO DEL MERCADO (64x56): toldo a rayas, mostrador y cajones con papas y zanahorias ----------
sprite("PuestoMercado", { w: 64, h: 56, outline: "k" }, (c) => {
  // postes
  c.rect(3, 12, 3, 42, "b"); c.rect(58, 12, 3, 42, "b"); c.vline(3, 12, 42, "c"); c.vline(58, 12, 42, "c")
  // toldo a rayas con borde ondulado
  for (let x = 0; x < 64; x++) {
    const col = Math.floor(x / 8) % 2 ? "w" : "g"
    c.vline(x, 4, 10, col)
    if (x % 8 < 4) c.px(x, 14, col)
  }
  c.hline(0, 4, 64, "d"); c.hline(0, 3, 64, "k")
  // letrero
  c.rect(17, 0, 30, 8, "c"); c.hline(17, 0, 30, "t"); c.text(19, 2, "MERCADO", "T")
  // mostrador
  c.rect(4, 34, 56, 14, "c"); c.hline(4, 34, 56, "t"); c.hline(4, 47, 56, "b")
  for (const x of [18, 32, 46]) c.vline(x, 35, 12, "b")
  // cajones con papas, zanahorias y papas radiactivas sobre el mostrador
  function cajon(x, contenido) {
    c.rect(x, 26, 14, 9, "b"); c.rect(x + 1, 27, 12, 7, "c"); c.hline(x + 1, 30, 12, "b")
    contenido(x)
  }
  cajon(7, (x) => { for (const [dx, dy] of [[2, 24], [6, 23], [10, 24], [4, 25], [8, 25]]) { c.rect(x + dx, dy, 3, 2, "t"); c.px(x + dx, dy, "T") } })
  cajon(25, (x) => { for (const dx of [2, 5, 8, 11]) { c.vline(x + dx, 23, 4, "o"); c.px(x + dx, 22, "g") } })
  cajon(43, (x) => { for (const [dx, dy] of [[2, 24], [6, 23], [10, 24], [6, 25]]) { c.rect(x + dx, dy, 3, 2, "t"); c.px(x + dx + 1, dy, "L") } })
  // saco de semillas en el suelo
  c.poly([22, 55, 21, 50, 25, 48, 29, 50, 28, 55], "T"); c.hline(23, 50, 4, "a")
})

// ---------- HERRERIA (64x48): yunque, fragua con fuego y letrero ----------
anim("Herreria", { w: 64, h: 48, fps: 6, outline: "k" },
  (c) => {
    // fragua de piedra
    c.rect(34, 14, 28, 32, "r"); c.ellipse(48, 14, 14, 6, "r"); c.ellipse(47, 12, 10, 4, "R")
    for (let y = 18; y < 44; y += 5) for (let x = (y % 2 ? 36 : 39); x < 60; x += 7) c.hline(x, y, 4, "m")
    c.rect(40, 26, 16, 14, "k"); c.rect(41, 27, 14, 13, "p")
    c.rect(44, 2, 8, 9, "m"); c.rect(45, 2, 6, 1, "e")
    // yunque
    c.rect(6, 30, 22, 6, "e"); c.poly([2, 30, 6, 30, 6, 33], "e"); c.hline(6, 30, 22, "R")
    c.rect(12, 36, 10, 4, "m"); c.rect(9, 40, 16, 5, "e"); c.hline(9, 40, 16, "r")
    // letrero colgante
    c.rect(4, 6, 26, 9, "c"); c.hline(4, 6, 26, "t"); c.vline(9, 2, 4, "b"); c.vline(25, 2, 4, "b"); c.text(6, 8, "FORJA", "T")
  },
  frame(rect(43, 33, 10, 7, "o"), rect(45, 31, 6, 9, "y"), px(46, 30, "o")),
  frame(rect(43, 32, 10, 8, "o"), rect(44, 33, 7, 7, "y"), px(50, 30, "o")))

// ---------- panel de la tienda (380x246): titulo, fila de ofertas, mochila y caja de informacion ----------
function tablas(c, x0, y0, w, h, alto, seed) {
  const r = c.rng(seed)
  for (let y = y0; y < y0 + h; y += alto) {
    const hh = Math.min(alto, y0 + h - y)
    c.rect(x0, y, w, hh, "Z"); c.hline(x0, y, w, "W"); if (y + hh < y0 + h) c.hline(x0, y + hh - 1, w, "c")
    for (let k = 0; k < w / 14; k++) c.hline(x0 + Math.floor(r() * (w - 10)), y + 2 + Math.floor(r() * Math.max(1, hh - 4)), 3 + Math.floor(r() * 6), "c")
  }
}
sprite("PanelTienda", { w: 380, h: 246 }, (c) => {
  c.rect(0, 0, 380, 246, "K"); c.rect(1, 1, 378, 244, "M"); c.hline(1, 1, 378, "N"); c.vline(1, 1, 244, "N")
  c.hline(1, 244, 378, "D"); c.vline(378, 1, 244, "D")
  c.box(9, 9, 362, 228, "K")
  tablas(c, 10, 10, 360, 226, 15, 51)
  // separador entre ofertas y mochila
  c.rect(14, 73, 352, 2, "D"); c.hline(14, 75, 352, "W")
  // caja de informacion
  c.rect(14, 190, 352, 42, "K"); c.rect(15, 191, 350, 40, "P"); c.hline(15, 192, 350, "Q")
  for (const [x, len] of [[30, 3], [90, 5], [160, 2], [250, 4], [330, 3]]) { c.vline(x, 10, len, "g"); c.vline(x + 1, 10, len - 1, "H"); c.px(x, 10 + len, "h") }
})

// ---------- iconos de mejoras ----------
sprite("EspadaCobre", { w: 30, h: 30, outline: "k" },
  line(6, 23, 22, 7, "o", 3), line(7, 22, 21, 8, "T"), line(4, 19, 10, 25, "c", 2), line(3, 26, 6, 23, "b", 2), px(23, 6, "T"))
sprite("EspadaHierro", { w: 30, h: 30, outline: "k" },
  line(6, 23, 22, 7, "s", 3), line(7, 22, 21, 8, "w"), line(4, 19, 10, 25, "u", 2), line(3, 26, 6, 23, "b", 2), px(23, 6, "w"))

sheet("pueblo", ["PuestoMercado", "Herreria", "EspadaCobre", "EspadaHierro"], { pad: 2 })
