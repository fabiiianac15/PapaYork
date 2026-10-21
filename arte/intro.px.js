// Fondos y efectos de la introduccion (480x270, misma escala de pixel que el juego).
// Paleta DB32. Los fondos se derivan del valle de 1847 con cambios de color (swap).
pal({
  k: "#000000", n: "#222034", p: "#45283c", b: "#663931", c: "#8f563b", o: "#df7126", t: "#d9a066", T: "#eec39a",
  y: "#fbf236", Y: "#fff6b0", L: "#99e550", g: "#6abe30", G: "#37946e", d: "#4b692f", v: "#306c06", e: "#323c39",
  u: "#3f3f74", B: "#306082", s: "#5b6ee1",
  C: "#639bff", S: "#5fcde4", w: "#ffffff", W: "#cbdbfc", r: "#696a6a", R: "#847e87", m: "#595652",
  a: "#8a6f30", f: "#fbf236", F: "#fff6b0", x: "#ac3232", X: "#d95763", q: "#76428a", Q: "#d77bba", h: "#9badb7", O: "#8f974a",
})

// ---------- piezas ----------
function cielo(c, bandas) { c.grad(0, 0, 480, 150, bandas, "v", 0.7) }
function nube(c, x, y, s) { for (const [dx, dy, r] of [[0, 0, 6], [8, -3, 8], [17, 0, 6], [8, 2, 6]]) c.circ(x + dx * s, y + dy * s, r * s, "w"); c.hline(x - 5 * s, y + 5 * s, 28 * s, "W") }
function montes(c) {
  c.poly([0, 120, 50, 78, 95, 105, 150, 62, 215, 108, 270, 72, 330, 104, 395, 66, 450, 96, 480, 84, 480, 140, 0, 140], "u")
  c.poly([150, 62, 162, 72, 147, 70], "W"); c.poly([395, 66, 406, 75, 391, 74], "W"); c.poly([270, 72, 280, 80, 266, 80], "W")
}
function colinas(c, claro, oscuro) {
  c.ellipse(90, 150, 170, 40, oscuro); c.ellipse(380, 155, 190, 45, oscuro)
  c.ellipse(240, 170, 300, 45, claro); c.rect(0, 165, 480, 105, claro)
}
function arbol(c, x, y, copa, sombra) {
  c.rect(x - 2, y, 5, 14, "b"); c.vline(x - 2, y, 14, "c")
  c.circ(x, y - 6, 10, sombra); c.circ(x - 1, y - 8, 9, copa); c.circ(x - 4, y - 11, 3, "L")
}
function surcos(c, y0, filas) {   // tierra dorada con matas de papa en flor
  for (let f = 0; f < filas; f++) {
    const y = y0 + f * 12
    c.rect(0, y + 6, 480, 5, "a"); c.hline(0, y + 6, 480, "t"); c.hline(0, y + 10, 480, "b")
    for (let x = 6 + (f % 2) * 8; x < 480; x += 16) {
      c.circ(x, y + 4, 4, "G"); c.circ(x - 1, y + 3, 3, "g"); c.px(x - 2, y + 1, "L")
      if ((x + f * 7) % 3 === 0) { c.px(x, y - 1, "f"); c.px(x + 1, y, "F") }
    }
  }
}
function casa(c, x, y) {   // granja de madera con techo rojo
  c.rect(x, y + 22, 64, 36, "c"); for (let yy = y + 26; yy < y + 58; yy += 5) c.hline(x, yy, 64, "b")
  c.poly([x - 6, y + 24, x + 32, y, x + 70, y + 24], "x"); c.poly([x + 2, y + 22, x + 32, y + 4, x + 62, y + 22], "X")
  c.rect(x + 26, y + 36, 12, 22, "p"); c.rect(x + 8, y + 32, 10, 9, "S"); c.rect(x + 46, y + 32, 10, 9, "S")
  c.box(x + 8, y + 32, 10, 9, "b"); c.box(x + 46, y + 32, 10, 9, "b"); c.rect(x + 48, y + 2, 6, 12, "m")
}
function cerca(c, x0, x1, y) { for (let x = x0; x < x1; x += 10) c.rect(x, y - 10, 3, 12, "c"); c.hline(x0, y - 7, x1 - x0, "c"); c.hline(x0, y - 3, x1 - x0, "c") }

// ---------- VALLE 1847: dorado y prospero ----------
sprite("Valle", { w: 480, h: 270 },
  (c) => {
    cielo(c, "SSCC"); c.circ(400, 34, 16, "Y"); c.circ(400, 34, 13, "y")
    nube(c, 70, 34, 1.3); nube(c, 250, 22, 1); nube(c, 330, 50, 0.8)
    montes(c); colinas(c, "g", "d")
    for (const [x, y] of [[30, 150], [62, 156], [440, 152], [462, 160], [410, 150]]) arbol(c, x, y, "g", "G")
    casa(c, 70, 100); cerca(c, 0, 160, 166)
    surcos(c, 176, 8)          // campos dorados de papas
    c.rect(0, 172, 480, 4, "c")
  })

// Reactor (torre de enfriamiento) que se ve al fondo del valle
sprite("Reactor", { w: 44, h: 52, outline: "e" }, (c) => {
  c.poly([6, 52, 10, 26, 6, 0, 38, 0, 34, 26, 38, 52], "R"); c.poly([10, 52, 13, 26, 10, 0, 22, 0, 22, 52], "h")
  c.ellipse(22, 1, 16, 2, "m"); for (let y = 10; y < 50; y += 12) c.hline(9, y, 26, "r")
  c.circ(22, 32, 5, "y"); c.px(22, 32, "k"); c.px(20, 30, "k"); c.px(24, 30, "k"); c.px(22, 35, "k")
})

// ---------- VALLE RADIACTIVO: todo se vuelve verde enfermo y gris ----------
sprite("ValleRadiactivo", { w: 480, h: 270, base: "Valle", swap: { S: "O", C: "L", y: "L", Y: "y", g: "O", G: "e", L: "O", d: "e", u: "e", a: "e", t: "G", f: "L", F: "L", w: "h", W: "R", X: "R", x: "m" } },
  (c) => {
    for (let i = 0; i < 40; i++) {    // grietas que brillan
      const x = (i * 97) % 470, y = 180 + (i * 53) % 85
      c.line(x, y, x + 6, y + 3, "L"); c.px(x + 3, y + 1, "y")
    }
  }, glow("Ly", { r: 4, strength: 0.4, bands: 2 }))

// ---------- VALLE RECUPERADO (anos despues): verde y normal ----------
sprite("ValleVerde", { w: 480, h: 270, base: "Valle", swap: { a: "b", t: "c", f: "w", F: "W" } })
// ---------- ATARDECER ----------
sprite("Atardecer", { w: 480, h: 270, base: "ValleVerde", swap: { S: "Q", C: "o", Y: "f", y: "o", W: "T", w: "T", u: "q", d: "G" } })
// ---------- GRANJA DE NOCHE: el brillo verde volvio ----------
sprite("GranjaNoche", { w: 480, h: 270, base: "ValleVerde", swap: { S: "n", C: "u", Y: "W", y: "W", w: "u", W: "s", u: "n", g: "G", L: "G", d: "v", c: "b", t: "b", X: "q", x: "p" } },
  (c) => {
    for (let i = 0; i < 50; i++) c.px((i * 131) % 480, (i * 37) % 70, "w")
    for (let i = 0; i < 30; i++) {
      const x = (i * 83 + 20) % 470, y = 182 + (i * 41) % 80
      c.line(x, y, x + 5, y + 2, "L"); c.px(x + 2, y + 1, "y")
    }
  }, glow("Ly", { r: 5, strength: 0.6, bands: 3 }))

// ---------- explosion: hongo radiactivo (8 cuadros) ----------
anim("Explosion", { w: 120, h: 130, frames: 8, fps: 8, loop: false }, (c) => {
  const f = c.frame, k = Math.min(1, (f + 1) / 6)
  const alto = Math.round(20 + 85 * k), copa = Math.round(10 + 34 * k)
  c.rect(60 - Math.round(6 + 6 * k), 130 - alto, Math.round(12 + 12 * k), alto, "y")
  c.rect(60 - Math.round(3 + 4 * k), 130 - alto, Math.round(6 + 8 * k), alto, "Y")
  c.circ(60, 130 - alto, copa, "L"); c.circ(60, 128 - alto, Math.round(copa * 0.8), "y"); c.circ(56, 124 - alto, Math.round(copa * 0.4), "Y")
  c.ellipse(60, 128, Math.round(20 + 40 * k), 6, "L")
  if (f >= 6) { c.recolor({ Y: "y", y: "L", L: "G" }) }
})

// ---------- carreta de la huida ----------
sprite("Carreta", { w: 64, h: 40, outline: "k" }, (c) => {
  c.ellipse(32, 12, 26, 12, "T"); c.rect(6, 12, 52, 12, "T"); for (const x of [14, 26, 38, 50]) c.vline(x, 2, 22, "t")
  c.rect(4, 22, 56, 8, "c"); c.hline(4, 22, 56, "t")
  for (const x of [14, 48]) { c.circ(x, 32, 7, "b"); c.ring(x, 32, 7, "k"); c.px(x, 32, "t") }
})

// ---------- caja de dialogo (escala de juego; se amplia x2 para la capa HD) ----------
function marco(c, w, h) {
  c.rect(0, 0, w, h, "e"); c.rect(1, 1, w - 2, h - 2, "c"); c.hline(1, 1, w - 2, "t"); c.vline(1, 1, h - 2, "t")
  c.hline(1, h - 2, w - 2, "b"); c.vline(w - 2, 1, h - 2, "b")
  c.box(4, 4, w - 8, h - 8, "e"); c.rect(5, 5, w - 10, h - 10, "T"); c.hline(5, 5, w - 10, "Y")
  for (const [x, y] of [[2, 2], [w - 4, 2], [2, h - 4], [w - 4, h - 4]]) c.rect(x, y, 2, 2, "R")
  for (const [x, l] of [[20, 3], [60, 5], [w - 40, 4]]) { c.vline(x, h - 1, l, "g"); c.px(x, h - 1 + l, "L") }
}
sprite("CajaTexto", { w: 330, h: 80 }, (c) => marco(c, 330, 74))
sprite("CajaRetrato", { w: 104, h: 94 }, (c) => { marco(c, 104, 88); c.rect(18, 8, 68, 68, "e"); c.rect(10, 74, 84, 10, "c"); c.box(10, 74, 84, 10, "b") })
sprite("Flecha", { w: 9, h: 6, outline: "e" }, poly([0, 0, 9, 0, 4.5, 5], "x"))

sheet("intro", ["Valle", "ValleRadiactivo", "ValleVerde", "Atardecer", "GranjaNoche"], { cols: 2, pad: 2 })
