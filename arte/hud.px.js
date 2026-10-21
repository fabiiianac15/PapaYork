// Panel de la esquina (reloj, fecha, estacion, monedas y experiencia) inspirado en el de Stardew,
// con la madera, clavos y baba radiactiva del resto de la interfaz de Papayork.
pal({
  k: "#24150d", D: "#4a2a17", d: "#6e4024", m: "#8f5a32", W: "#dcb57c",
  p: "#2a1a10", P: "#3b2616", n: "#55555e", N: "#a9a9b4",
  G: "#4f9a1f", g: "#8fdc2e", h: "#d6ff6a",
  // cielo del dial
  A: "#0d0b26", a: "#1f2250", b: "#3f3f74", B: "#306082", c: "#639bff", C: "#9fd4ff",
  o: "#df7126", O: "#f2a65e", r: "#d95763", u: "#76428a", y: "#fbf236", Y: "#fff6b0",
  w: "#ffffff", s: "#cbdbfc", e: "#323c39", v: "#37946e", l: "#4b692f", L: "#6abe30",
  x: "#ac3232", t: "#8a6f30", T: "#d9a066", q: "#d77bba",
})
ramps("kDdmW", "pP", "Ggh", "AabBcC", "toyY")

// ---------- panel ----------
function caja(c, x, y, w, h) {   // caja hundida oscura para el texto
  c.rect(x, y, w, h, "k"); c.rect(x + 1, y + 1, w - 2, h - 2, "p"); c.hline(x + 1, y + 1, w - 2, "P")
}
sprite("HudPanel", { w: 150, h: 64 }, (c) => {
  c.rect(0, 0, 150, 60, "k"); c.rect(1, 1, 148, 58, "d")
  c.hline(1, 1, 148, "m"); c.vline(1, 1, 58, "m"); c.hline(1, 58, 148, "D"); c.vline(148, 1, 58, "D")
  const r = c.rng(4)
  for (let i = 0; i < 26; i++) c.hline(40 + Math.floor(r() * 104), 2 + Math.floor(r() * 55), 2 + Math.floor(r() * 4), "D")
  // hueco redondo donde va el dial
  c.circ(21, 21, 18, "k"); c.circ(21, 21, 17, "D")
  caja(c, 41, 4, 78, 16)      // fecha
  caja(c, 121, 4, 25, 16)     // estacion
  caja(c, 41, 22, 105, 16)    // hora
  caja(c, 4, 41, 70, 16)      // monedas
  caja(c, 77, 41, 69, 16)     // nivel y experiencia
  for (const [x, y] of [[3, 3], [146, 3], [3, 56], [146, 56], [38, 39]]) { c.rect(x - 1, y - 1, 2, 2, "n"); c.px(x - 1, y - 1, "N") }
  // baba radiactiva que gotea del borde de abajo
  for (const [x, len] of [[12, 3], [30, 2], [57, 4], [95, 3], [133, 2]]) {
    c.rect(x - 1, 59, 4, 1, "G"); c.vline(x, 59, len + 1, "g"); c.vline(x + 1, 59, len, "G"); c.px(x, 60 + len, "h")
  }
})
// Barra de experiencia: marco (va dentro de la caja de nivel) y relleno que se estira por codigo.
sprite("HudExpMarco", { w: 40, h: 8 }, (c) => { c.rect(0, 0, 40, 8, "k"); c.rect(1, 1, 38, 6, "e"); c.hline(1, 1, 38, "P") })
sprite("HudExpRelleno", { w: 38, h: 6 }, (c) => { c.rect(0, 0, 38, 6, "g"); c.hline(0, 0, 38, "h"); c.hline(0, 5, 38, "G") })

// Moneda de Papayork: oro con una papa grabada.
sprite("HudMoneda", { w: 12, h: 12, outline: "k" }, (c) => {
  c.circ(5, 5, 5, "o"); c.circ(5, 5, 4, "y"); c.ellipse(5, 6, 3, 2, "o"); c.px(5, 3, "L"); c.px(6, 3, "L"); c.px(3, 3, "Y")
})

// ---------- iconos de estacion (12x12) ----------
sprite("Estacion0", { w: 12, h: 12, outline: "k" }, (c) => {   // primavera: flor
  for (const [x, y] of [[5, 1], [5, 7], [2, 4], [8, 4]]) c.circ(x, y + 1, 2, "q")
  c.circ(5, 5, 1, "y"); c.vline(5, 8, 3, "L")
})
sprite("Estacion1", { w: 12, h: 12, outline: "k" }, (c) => {   // verano: sol
  c.circ(5, 5, 3, "y"); c.px(4, 4, "Y")
  for (const [x, y] of [[5, 0], [5, 10], [0, 5], [10, 5], [1, 1], [9, 1], [1, 9], [9, 9]]) c.px(x, y, "o")
})
sprite("Estacion2", { w: 12, h: 12, outline: "k" },             // otono: hoja
  poly([1, 10, 2, 3, 6, 0, 11, 1, 10, 6, 5, 10], "o"), line(2, 9, 8, 3, "t"), px(4, 3, "O"))
sprite("Estacion3", { w: 12, h: 12, outline: "k" }, (c) => {   // invierno: copo
  c.line(5, 0, 5, 10, "s"); c.line(0, 5, 10, 5, "s"); c.line(1, 1, 9, 9, "C"); c.line(9, 1, 1, 9, "C"); c.px(5, 5, "w")
})

// ---------- dial del cielo: 6 momentos del dia, 34x34 con su aro ----------
function dial(cielo, astro) {
  return (c) => {
    c.circ(17, 17, 16, "k")
    c.clip([17, 17, 15], () => {
      c.grad(1, 1, 33, 33, cielo, "v", 0.6)
      astro(c)
      // colinas de la granja y la torre de la planta nuclear al fondo
      c.ellipse(8, 31, 13, 7, "l"); c.ellipse(27, 32, 12, 7, "v")
      c.rect(23, 19, 5, 9, "e"); c.hline(22, 19, 7, "e"); c.px(25, 18, "g")
      c.rect(1, 28, 33, 6, "l"); c.hline(1, 28, 33, "L")
    })
    c.ring(17, 17, 16, "k"); c.ring(17, 17, 15, "m")
    c.px(17, 1, "h"); c.px(16, 1, "g"); c.px(18, 1, "g")   // gotita radiactiva en lo alto del aro
  }
}
const sol = (x, y) => (c) => { c.circ(x, y, 3, "y"); c.circ(x, y, 2, "Y") }
sprite("Dial0", { w: 34, h: 34 }, dial("AAaab", (c) => {      // noche
  c.circ(11, 9, 3, "s"); c.circ(12, 8, 2, "a")
  for (const [x, y] of [[21, 6], [27, 11], [16, 14], [6, 16], [24, 16]]) c.px(x, y, "w")
}))
sprite("Dial1", { w: 34, h: 34 }, dial("buroO", sol(8, 24)))     // amanecer
sprite("Dial2", { w: 34, h: 34 }, dial("BccCC", sol(11, 12)))    // manana
sprite("Dial3", { w: 34, h: 34 }, dial("BBccC", sol(17, 8)))     // mediodia
sprite("Dial4", { w: 34, h: 34 }, dial("cCCOO", sol(23, 13)))    // tarde
sprite("Dial5", { w: 34, h: 34 }, dial("auroo", sol(26, 24)))    // atardecer

sheet("hud", ["HudPanel", "Dial*", "Estacion*", "HudMoneda"], { pad: 2 })
