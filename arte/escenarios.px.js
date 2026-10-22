// Objetos para los escenarios redisenados. Paleta DB32 y contorno negro, como los sprites originales.
pal({
  k: "#000000", n: "#222034", p: "#45283c", b: "#663931", c: "#8f563b", o: "#df7126", t: "#d9a066", T: "#eec39a",
  y: "#fbf236", L: "#99e550", g: "#6abe30", G: "#37946e", d: "#4b692f", e: "#323c39", u: "#3f3f74",
  S: "#5fcde4", C: "#639bff", w: "#ffffff", W: "#cbdbfc", h: "#9badb7", r: "#696a6a", R: "#847e87", m: "#595652",
  a: "#8a6f30", x: "#ac3232", X: "#d95763", q: "#76428a", Q: "#d77bba", O: "#8f974a",
})
ramps("kpbcotT", "kerRhw", "kdgL", "kpxX")

// ---------- GRANERO (128x112): madera roja, techo oscuro, puerta grande en cruz ----------
sprite("Granero", { w: 128, h: 112, outline: "k" }, (c) => {
  c.poly([4, 40, 64, 2, 124, 40], "p"); c.poly([10, 40, 64, 8, 118, 40], "e"); c.hline(4, 40, 120, "k")
  for (let x = 14; x < 118; x += 8) c.line(x, 40, 64, 8 + Math.abs(64 - x) * 0.1, "p")
  c.rect(8, 40, 112, 70, "x"); for (let x = 8; x < 120; x += 8) c.vline(x, 41, 69, "p")
  c.rect(8, 40, 112, 4, "X")
  c.rect(42, 62, 44, 48, "b"); c.box(42, 62, 44, 48, "T"); c.line(42, 62, 86, 109, "T"); c.line(86, 62, 42, 109, "T"); c.vline(64, 62, 48, "T")
  c.rect(56, 20, 16, 14, "b"); c.box(56, 20, 16, 14, "T"); c.line(56, 20, 72, 33, "T"); c.line(72, 20, 56, 33, "T")
  c.rect(16, 74, 14, 12, "S"); c.box(16, 74, 14, 12, "T"); c.rect(98, 74, 14, 12, "S"); c.box(98, 74, 14, 12, "T")
  c.rect(4, 104, 120, 6, "m")
})

// ---------- ESTATUA DE HETOLMIMIAO (48x72): sombrero de copa, bigote y una papa enorme en alto ----------
sprite("Estatua", { w: 48, h: 72, outline: "k" }, (c) => {
  c.rect(6, 56, 36, 16, "r"); c.rect(4, 54, 40, 4, "R"); c.rect(10, 60, 28, 8, "m"); c.hline(12, 63, 24, "R"); c.hline(12, 65, 20, "R")
  c.rect(16, 30, 16, 24, "h"); c.rect(14, 38, 20, 6, "R")              // cuerpo con levita
  c.circ(24, 22, 8, "R"); c.circ(23, 21, 6, "h")                         // cabeza
  c.rect(17, 7, 14, 10, "m"); c.rect(14, 15, 20, 3, "m")                 // sombrero de copa
  c.hline(18, 25, 12, "W"); c.px(17, 26, "W"); c.px(30, 26, "W")         // bigote
  c.line(31, 34, 38, 22, "h", 2); c.ellipse(40, 16, 7, 6, "R"); c.ellipse(39, 15, 5, 4, "h")   // brazo y papa en alto
  c.px(42, 14, "m"); c.px(38, 18, "m")
  c.px(20, 20, "m"); c.px(26, 20, "m")
  for (const [x, y] of [[8, 70], [40, 70], [6, 62]]) c.px(x, y, "g")    // musgo
})

// ---------- BUZON (20x30) ----------
sprite("Buzon", { w: 20, h: 30, outline: "k" }, (c) => {
  c.rect(8, 14, 4, 16, "b"); c.vline(8, 14, 16, "c")
  c.rect(1, 3, 18, 12, "C"); c.ellipse(10, 3, 9, 3, "C"); c.rect(2, 6, 16, 2, "u"); c.vline(18, 2, 12, "u")
  c.rect(14, 0, 2, 6, "x"); c.rect(16, 0, 3, 3, "x")
})

// ---------- BARRILES RADIACTIVOS (2 variantes, 22x28) ----------
function barril(c, color, sombra) {
  c.rect(2, 4, 18, 23, color); c.ellipse(11, 4, 9, 3, sombra); c.ellipse(11, 4, 7, 2, "e")
  c.hline(2, 9, 18, sombra); c.hline(2, 21, 18, sombra); c.vline(17, 5, 21, sombra)
  c.circ(10, 15, 4, "y"); c.px(10, 15, "k"); c.px(8, 13, "k"); c.px(12, 13, "k"); c.px(10, 18, "k")
  for (const [x, y] of [[4, 12], [5, 24], [15, 7], [16, 18]]) c.px(x, y, "o")   // oxido
}
sprite("Barril1", { w: 22, h: 28, outline: "k" }, (c) => { barril(c, "a", "b"); c.vline(6, 27, 1, "L"); c.ellipse(11, 27, 5, 1, "L") })
sprite("Barril2", { w: 22, h: 28, outline: "k" }, (c) => { barril(c, "r", "m"); c.line(3, 6, 8, 2, "L"); c.px(4, 8, "L") })

// ---------- CHARCO RADIACTIVO (32x16, brilla) ----------
anim("Charco", { w: 32, h: 16, fps: 3 },
  (c) => { c.ellipse(16, 8, 14, 6, "G"); c.ellipse(15, 7, 11, 4, "g"); c.ellipse(13, 6, 5, 2, "L") },
  frame(px(20, 7, "y"), px(9, 9, "L")), frame(px(11, 6, "y"), px(22, 9, "L"), px(16, 4, "y")))

// ---------- PUENTE de madera (64x48) para cruzar el rio ----------
sprite("Puente", { w: 64, h: 48, outline: "k" }, (c) => {
  for (let x = 2; x < 62; x += 6) { c.rect(x, 6, 5, 36, "c"); c.vline(x, 6, 36, "t"); c.vline(x + 4, 6, 36, "b") }
  c.rect(0, 2, 64, 4, "b"); c.rect(0, 42, 64, 4, "b"); c.hline(0, 2, 64, "c"); c.hline(0, 42, 64, "c")
  for (const x of [0, 30, 60]) { c.rect(x, 0, 4, 8, "b"); c.rect(x, 40, 4, 8, "b") }
})

// ---------- CABANA EN RUINAS (112x96): la vieja casa de los tiempos de HetolMimiao ----------
sprite("CabanaRuina", { w: 112, h: 96, outline: "k" }, (c) => {
  c.rect(8, 40, 96, 54, "c"); for (let y = 44; y < 94; y += 6) c.hline(8, y, 96, "b")
  c.poly([2, 42, 40, 10, 56, 22, 70, 14, 110, 42], "b"); c.poly([10, 40, 40, 16, 54, 28, 70, 20, 102, 40], "p")
  c.poly([56, 22, 62, 30, 70, 20], "k")                                  // agujero en el techo
  c.rect(46, 60, 20, 34, "e"); c.line(46, 60, 66, 94, "c"); c.line(46, 72, 58, 94, "b")   // puerta rota
  c.rect(18, 56, 16, 14, "e"); c.line(18, 56, 34, 70, "c"); c.rect(80, 56, 16, 14, "e"); c.line(96, 56, 80, 70, "c")
  for (const [x, y, l] of [[10, 50, 8], [100, 60, 10], [30, 44, 6], [86, 46, 7]]) { c.vline(x, y, l, "g"); c.px(x + 1, y + 2, "L") }   // enredaderas
  c.rect(0, 88, 22, 8, "R"); c.rect(90, 86, 22, 10, "r")                 // escombros
})

// ---------- ENTRADA DE CUEVA bloqueada (96x72) ----------
sprite("Cueva", { w: 96, h: 72, outline: "k" }, (c) => {
  c.poly([0, 72, 8, 20, 30, 4, 66, 2, 88, 18, 96, 72], "r"); c.poly([6, 72, 14, 24, 34, 10, 62, 8, 82, 22, 90, 72], "R")
  c.poly([24, 72, 30, 36, 48, 24, 66, 36, 72, 72], "k")
  for (const [x, y, r] of [[34, 62, 8], [50, 58, 10], [64, 64, 7], [42, 50, 6], [58, 46, 5]]) { c.circ(x, y, r, "m"); c.circ(x - 1, y - 1, r - 2, "r") }
  c.rect(40, 30, 18, 4, "c"); c.text(41, 31, "NO", "T")
  for (const [x, y] of [[14, 30], [80, 34], [20, 50]]) { c.px(x, y, "L"); c.px(x + 1, y, "g") }
})

// ---------- TABLON DE ANUNCIOS (48x44) ----------
sprite("Tablon", { w: 48, h: 44, outline: "k" }, (c) => {
  c.rect(4, 22, 4, 22, "b"); c.rect(40, 22, 4, 22, "b")
  c.rect(0, 2, 48, 26, "c"); c.box(0, 2, 48, 26, "b"); c.hline(0, 2, 48, "t")
  c.rect(5, 6, 12, 14, "T"); c.rect(20, 5, 10, 12, "w"); c.rect(33, 7, 11, 15, "T")
  for (const [x, y] of [[7, 9], [7, 12], [22, 8], [22, 11], [35, 10], [35, 13]]) c.hline(x, y, 7, "m")
  c.px(10, 5, "x"); c.px(25, 4, "x"); c.px(38, 6, "x")
})

// ---------- CARTEL de madera (32x32) ----------
sprite("Cartel", { w: 30, h: 30, outline: "k" }, (c) => {
  c.rect(13, 14, 4, 16, "b"); c.rect(1, 2, 28, 14, "c"); c.box(1, 2, 28, 14, "b"); c.hline(1, 2, 28, "t")
  c.hline(5, 7, 20, "b"); c.hline(5, 10, 14, "b")
})

// ---------- HONGO silvestre (objeto que se recoge) ----------
sprite("Hongo", { w: 30, h: 30, outline: "k" }, (c) => {
  c.rect(12, 16, 6, 10, "T"); c.vline(12, 16, 10, "t")
  c.ellipse(15, 14, 11, 7, "x"); c.ellipse(14, 12, 9, 5, "X")
  for (const [x, y] of [[9, 11], [18, 9], [21, 14], [13, 15]]) { c.px(x, y, "w"); c.px(x + 1, y, "w") }
  c.ellipse(15, 27, 9, 2, "g")
})

sheet("escenarios", ["Granero", "Estatua", "Buzon", "Barril*", "Charco", "Puente", "CabanaRuina", "Cueva", "Tablon", "Cartel", "Hongo"], { pad: 2 })
