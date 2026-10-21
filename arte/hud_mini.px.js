// Version compacta del panel de la esquina y de la barra rapida (tamano parecido al de Stardew en pantalla).
pal({
  k: "#24150d", D: "#4a2a17", d: "#6e4024", m: "#8f5a32", W: "#dcb57c",
  p: "#2a1a10", P: "#3b2616", n: "#55555e", N: "#a9a9b4",
  G: "#4f9a1f", g: "#8fdc2e", h: "#d6ff6a",
  A: "#0d0b26", a: "#1f2250", b: "#3f3f74", B: "#306082", c: "#639bff", C: "#9fd4ff",
  o: "#df7126", O: "#f2a65e", r: "#d95763", u: "#76428a", y: "#fbf236", Y: "#fff6b0",
  w: "#ffffff", s: "#cbdbfc", e: "#323c39", v: "#37946e", l: "#4b692f", L: "#6abe30",
  t: "#8a6f30", q: "#d77bba", I: "#5a3a22", i: "#7a5233", j: "#9a6c43",
})

function caja(c, x, y, w, h) { c.rect(x, y, w, h, "k"); c.rect(x + 1, y + 1, w - 2, h - 2, "p"); c.hline(x + 1, y + 1, w - 2, "P") }

// ---------- panel 98x44: dial, fecha + estacion, hora, monedas, nivel ----------
sprite("HudPanelMini", { w: 98, h: 46 }, (c) => {
  c.rect(0, 0, 98, 43, "k"); c.rect(1, 1, 96, 41, "d")
  c.hline(1, 1, 96, "m"); c.vline(1, 1, 41, "m"); c.hline(1, 41, 96, "D"); c.vline(96, 1, 41, "D")
  c.circ(15, 15, 13, "k"); c.circ(15, 15, 12, "D")
  caja(c, 30, 2, 54, 12)      // fecha
  caja(c, 85, 2, 11, 12)      // estacion
  caja(c, 30, 15, 66, 12)     // hora
  caja(c, 2, 29, 44, 12)      // monedas
  caja(c, 48, 29, 48, 12)     // nivel + experiencia
  for (const [x, len] of [[8, 2], [33, 1], [70, 2], [90, 1]]) { c.vline(x, 42, len + 1, "g"); c.px(x, 43 + len, "h") }
})
sprite("HudExpMarcoMini", { w: 26, h: 5 }, (c) => { c.rect(0, 0, 26, 5, "k"); c.rect(1, 1, 24, 3, "e") })
sprite("HudExpRellenoMini", { w: 24, h: 3 }, (c) => { c.rect(0, 0, 24, 3, "g"); c.hline(0, 0, 24, "h") })
sprite("HudMonedaMini", { w: 7, h: 7, outline: "k" }, (c) => { c.circ(3, 3, 3, "y"); c.px(2, 2, "Y"); c.px(4, 4, "o"); c.px(3, 3, "o") })

// estaciones 8x8
sprite("EstacionMini0", { w: 8, h: 8, outline: "k" }, (c) => { for (const [x, y] of [[3, 1], [3, 5], [1, 3], [5, 3]]) c.rect(x, y, 2, 2, "q"); c.rect(3, 3, 2, 2, "y") })
sprite("EstacionMini1", { w: 8, h: 8, outline: "k" }, (c) => { c.circ(3, 3, 2, "y"); c.px(3, 3, "Y"); for (const [x, y] of [[3, 0], [3, 7], [0, 3], [7, 3]]) c.px(x, y, "o") })
sprite("EstacionMini2", { w: 8, h: 8, outline: "k" }, poly([0, 7, 1, 2, 4, 0, 8, 1, 7, 5, 3, 7], "o"), line(1, 6, 5, 2, "t"))
sprite("EstacionMini3", { w: 8, h: 8, outline: "k" }, line(3, 0, 3, 7, "s"), line(0, 3, 7, 3, "s"), line(1, 1, 6, 6, "C"), line(6, 1, 1, 6, "C"))

// dial 26x26
function dial(cielo, astro) {
  return (c) => {
    c.circ(13, 13, 12, "k")
    c.clip([13, 13, 11], () => {
      c.grad(1, 1, 25, 25, cielo, "v", 0.6); astro(c)
      c.ellipse(6, 24, 10, 5, "l"); c.ellipse(21, 25, 9, 5, "v")
      c.rect(18, 15, 4, 7, "e"); c.px(19, 14, "g")
      c.rect(1, 22, 25, 4, "l"); c.hline(1, 22, 25, "L")
    })
    c.ring(13, 13, 12, "k"); c.ring(13, 13, 11, "m"); c.px(13, 1, "h")
  }
}
const sol = (x, y) => (c) => { c.circ(x, y, 2, "y"); c.px(x, y, "Y") }
sprite("DialMini0", { w: 26, h: 26 }, dial("AAaab", (c) => { c.circ(9, 8, 2, "s"); c.px(10, 7, "a"); c.px(10, 8, "a"); for (const [x, y] of [[17, 5], [21, 9], [13, 11], [5, 12]]) c.px(x, y, "w") }))
sprite("DialMini1", { w: 26, h: 26 }, dial("buroO", sol(6, 19)))
sprite("DialMini2", { w: 26, h: 26 }, dial("BccCC", sol(9, 9)))
sprite("DialMini3", { w: 26, h: 26 }, dial("BBccC", sol(13, 6)))
sprite("DialMini4", { w: 26, h: 26 }, dial("cCCOO", sol(18, 10)))
sprite("DialMini5", { w: 26, h: 26 }, dial("auroo", sol(20, 19)))

// ---------- barra rapida compacta: 10 casillas de 20px ----------
function casilla(c, borde, luz, sombra) {
  c.rect(0, 0, 20, 20, "k"); c.rect(1, 1, 18, 18, borde)
  c.hline(1, 1, 18, luz); c.vline(1, 1, 18, luz); c.hline(1, 18, 18, sombra); c.vline(18, 1, 18, sombra)
  c.box(2, 2, 16, 16, "k"); c.rect(3, 3, 14, 14, "i"); c.hline(3, 3, 14, "I"); c.vline(3, 3, 14, "I"); c.hline(3, 16, 14, "j")
}
sprite("CasillaMini", { w: 20, h: 20 }, (c) => casilla(c, "d", "m", "D"))
sprite("CasillaMiniHover", { w: 20, h: 20 }, (c) => { casilla(c, "m", "W", "d"); c.rect(4, 4, 13, 12, "j") })
sprite("CasillaMiniSeleccionada", { w: 20, h: 20 }, (c) => {
  casilla(c, "G", "h", "G"); c.box(1, 1, 18, 18, "g")
  for (const [x, y] of [[0, 0], [17, 0], [0, 17], [17, 17]]) { c.rect(x, y, 3, 3, "h"); c.px(x + 1, y + 1, "g") }
})
sprite("BarraRapidaMini", { w: 208, h: 26 }, (c) => {
  c.rect(0, 0, 208, 26, "k"); c.rect(1, 1, 206, 24, "d"); c.hline(1, 1, 206, "m"); c.hline(1, 24, 206, "D")
  const r = c.rng(3); for (let i = 0; i < 30; i++) c.hline(2 + Math.floor(r() * 200), 2 + Math.floor(r() * 21), 3, "D")
  for (const x of [20, 60, 120, 180]) { c.vline(x, 25, 2, "g") }
})
sprite("EtiquetaItemMini", { w: 90, h: 12 }, (c) => { c.rect(0, 0, 90, 12, "k"); c.rect(1, 1, 88, 10, "p"); c.px(0, 0, "_"); c.px(89, 0, "_"); c.px(0, 11, "_"); c.px(89, 11, "_") })

sheet("hud_mini", ["HudPanelMini", "DialMini*", "EstacionMini*", "HudMonedaMini", "BarraRapidaMini", "CasillaMini*"], { pad: 2 })
