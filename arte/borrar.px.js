// Boton de papelera para borrar una partida guardada (18x18, normal y con el mouse encima).
pal({ k: "#24150d", d: "#6e4024", m: "#8f5a32", D: "#4a2a17", w: "#c99a5e", W: "#dcb57c",
      x: "#ac3232", X: "#d95763", g: "#8fdc2e", h: "#d6ff6a", G: "#4f9a1f", n: "#55555e", N: "#a9a9b4" })
function papelera(c, cuerpo, tapa) {
  c.rect(5, 4, 8, 2, tapa); c.rect(7, 3, 4, 1, tapa)
  c.rect(6, 6, 6, 8, cuerpo); for (const x of [7, 9, 11]) c.vline(x, 7, 6, "k")
}
sprite("BorrarNormal", { w: 18, h: 18 }, (c) => {
  c.rect(0, 0, 18, 18, "k"); c.rect(1, 1, 16, 16, "d"); c.hline(1, 1, 16, "m"); c.box(2, 2, 14, 14, "k"); c.rect(3, 3, 12, 12, "w")
  papelera(c, "N", "n")
})
sprite("BorrarHover", { w: 18, h: 18 }, (c) => {
  c.rect(0, 0, 18, 18, "k"); c.rect(1, 1, 16, 16, "x"); c.box(1, 1, 16, 16, "X"); c.box(2, 2, 14, 14, "k"); c.rect(3, 3, 12, 12, "W")
  papelera(c, "X", "x")
})
