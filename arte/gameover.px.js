// Pantalla de "te desmayaste": la granja de noche, con niebla radiactiva y papas mutantes mirando desde el campo.
// Paleta DB32 como el resto del juego.
pal({
  k: "#000000", n: "#222034", p: "#45283c", b: "#663931", c: "#8f563b", t: "#d9a066", T: "#eec39a",
  y: "#fbf236", Y: "#fff6b0", L: "#99e550", g: "#6abe30", G: "#37946e", d: "#4b692f", v: "#306c06", e: "#323c39",
  u: "#3f3f74", B: "#306082", a: "#8a6f30", x: "#ac3232", X: "#d95763", q: "#76428a", w: "#ffffff", W: "#cbdbfc",
  m: "#595652", r: "#696a6a", z: "#14101e", Z: "#1a2620",
})
ramps("znuq", "ZevdGgLY", "kpbct")

scene("FondoGameOver", { w: 480, h: 270, bg: "z" },
  layer("cielo", (c) => {
    c.grad(0, 0, 480, 170, "znnuq", "v", 0.8)
    const r = c.rng(11); for (let i = 0; i < 70; i++) c.px(Math.floor(r() * 480), Math.floor(r() * 120), r() < 0.2 ? "W" : "u")
    // luna enferma con halo verde
    c.circ(428, 46, 30, "Z"); c.circ(428, 46, 25, "d"); c.circ(428, 46, 21, "g"); c.circ(424, 42, 18, "L")
    c.circ(420, 38, 4, "g"); c.circ(436, 52, 5, "g"); c.circ(430, 34, 2, "g"); c.px(418, 49, "G"); c.px(439, 40, "G")
  }),
  layer("montes", (c) => {
    c.poly([0, 140, 60, 96, 120, 128, 190, 86, 260, 130, 330, 98, 400, 132, 450, 104, 480, 118, 480, 170, 0, 170], "n")
    c.poly([0, 160, 80, 128, 170, 150, 250, 124, 340, 152, 420, 130, 480, 146, 480, 180, 0, 180], "Z")
  }),
  layer("casa", (c) => {
    // silueta de la casa de la granja, con una ventana encendida
    c.poly([60, 138, 96, 112, 132, 138], "z"); c.rect(66, 138, 60, 32, "z"); c.rect(112, 116, 6, 12, "z")
    c.rect(78, 146, 12, 10, "a"); c.rect(79, 147, 10, 8, "y"); c.vline(84, 147, 8, "a"); c.hline(79, 151, 10, "a")
    c.rect(98, 150, 12, 20, "e")
    for (let x = 0; x < 200; x += 12) { c.rect(x, 160, 2, 12, "e") } c.hline(0, 163, 200, "e"); c.hline(0, 168, 200, "e")
    // arbol seco a la derecha
    c.rect(438, 120, 4, 52, "z"); c.line(440, 132, 456, 116, "z", 2); c.line(440, 142, 424, 126, "z", 2); c.line(450, 122, 452, 110, "z")
  }),
  layer("campo", (c) => {
    c.rect(0, 170, 480, 100, "Z")
    for (let f = 0; f < 8; f++) {
      const y = 176 + f * 12
      c.rect(0, y, 480, 6, "e"); c.hline(0, y, 480, "v")
      const r = c.rng(f + 3)
      for (let x = 4 + (f % 2) * 10; x < 480; x += 20) { const h = 2 + Math.floor(r() * 3); c.rect(x, y - h, 3, h, "d"); c.px(x + 1, y - h - 1, "G") }
    }
  }),
  layer("papas", (c) => {
    // papas mutantes asomadas entre los surcos: solo se ven la silueta y los ojos
    for (const [x, y, s] of [[40, 182, 1], [170, 176, 0.8], [300, 184, 1.1], [420, 178, 0.9], [235, 194, 1.2], [110, 200, 1]]) {
      c.ellipse(x, y, Math.round(11 * s), Math.round(8 * s), "z")
      c.line(x, y - Math.round(8 * s), x - 3, y - Math.round(13 * s), "z"); c.line(x, y - Math.round(8 * s), x + 4, y - Math.round(12 * s), "z")
      c.rect(x - Math.round(5 * s), y - 3, 2, 2, "L"); c.px(x - Math.round(5 * s), y - 3, "Y")
      c.rect(x + Math.round(3 * s), y - 3, 2, 2, "L"); c.px(x + Math.round(3 * s), y - 3, "Y")
    }
  }),
)

// Titulo con la fuente 3x5 de pxl a escala 4 y baba radiactiva escurriendo.
sprite("TituloGameOver", { w: 236, h: 40, outline: "k" }, (c) => {
  c.text(118, 4, "TE DESMAYASTE", "x", { scale: 4, align: "c" })   // sombra roja oscura
  c.text(118, 1, "TE DESMAYASTE", "X", { scale: 4, align: "c" })
  const r = c.rng(4)
  for (let i = 0; i < 9; i++) { const x = 6 + Math.floor(r() * 222), l = 3 + Math.floor(r() * 10); if (c.get(x, 21) && c.get(x, 21) !== ".") { c.vline(x, 21, l, "g"); c.px(x, 21 + l, "L") } }
})

// Estrellita que gira sobre la cabeza de Pedro
sprite("Estrellita", { w: 7, h: 7, outline: "k" }, `
  ...y...
  ..yYy..
  yyYYYyy
  ..yYy..
  .y...y.`)

sheet("gameover", ["FondoGameOver", "TituloGameOver", "Estrellita"], { pad: 2 })
