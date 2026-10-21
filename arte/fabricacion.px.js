// Fabricacion: mesa de trabajo, objetos que se colocan en el mundo y materiales nuevos.
// Paleta DB32 y contorno negro, como los sprites originales.
pal({
  k: "#000000", n: "#222034", p: "#45283c", b: "#663931", c: "#8f563b", o: "#df7126",
  t: "#d9a066", T: "#eec39a", y: "#fbf236", L: "#99e550", g: "#6abe30", G: "#37946e",
  d: "#4b692f", e: "#323c39", s: "#9badb7", S: "#cbdbfc", w: "#ffffff", r: "#696a6a",
  R: "#847e87", m: "#595652", a: "#8a6f30", x: "#ac3232", X: "#d95763", u: "#3f3f74",
})
ramps("kpbcotT", "kerRw", "kaoy", "kdgL", "kusS")

// ---------- MESA DE TRABAJO (40x32): tablero con herramientas y un frasco radiactivo ----------
sprite("MesaTrabajo", { w: 40, h: 32, outline: "k" }, (c) => {
  // patas
  c.rect(3, 18, 3, 12, "b"); c.rect(33, 18, 3, 12, "b"); c.rect(4, 18, 1, 12, "c"); c.rect(34, 18, 1, 12, "c")
  c.rect(5, 24, 29, 2, "b")
  // tablero
  c.rect(0, 12, 40, 7, "c"); c.hline(0, 12, 40, "t"); c.hline(0, 18, 40, "b")
  for (const x of [9, 21, 31]) c.vline(x, 13, 5, "b")
  // sierra
  c.rect(4, 8, 13, 4, "s"); c.hline(4, 11, 13, "R"); for (let x = 4; x < 17; x += 2) c.px(x, 12, "R")
  c.rect(16, 7, 4, 5, "b"); c.px(17, 8, "c")
  // martillo
  c.line(23, 11, 29, 5, "c"); c.rect(27, 2, 5, 3, "r"); c.px(28, 2, "R")
  // frasco con baba radiactiva
  c.rect(33, 4, 5, 8, "S"); c.rect(34, 7, 3, 5, "g"); c.px(34, 7, "L"); c.rect(33, 3, 5, 1, "c")
})

// ---------- ANTORCHA (16x32, 3 cuadros de fuego) ----------
anim("Antorcha", { w: 16, h: 32, fps: 8, outline: "k" },
  rect(7, 12, 3, 18, "c"), vline(7, 12, 18, "t"), rect(6, 11, 5, 3, "b"),
  frame(poly([5, 11, 8, 2, 11, 11], "o"), poly([7, 11, 8, 5, 10, 11], "y")),
  frame(poly([5, 11, 7, 3, 11, 11], "o"), poly([6, 11, 8, 6, 9, 11], "y"), px(10, 4, "o")),
  frame(poly([5, 11, 9, 1, 11, 11], "o"), poly([7, 11, 9, 4, 10, 11], "y"), px(6, 5, "o")))

// ---------- ESPANTAPAPAS (32x40): espantapajaros con cabeza de papa y el simbolo radiactivo ----------
sprite("Espantapapas", { w: 32, h: 40, outline: "k" }, (c) => {
  c.rect(15, 14, 3, 25, "b"); c.vline(15, 14, 25, "c")                  // palo
  c.rect(3, 17, 26, 3, "b"); c.hline(3, 17, 26, "c")                      // brazos
  c.poly([9, 18, 23, 18, 21, 31, 11, 31], "x"); c.hline(10, 19, 12, "X")  // camisa
  c.rect(11, 24, 10, 2, "a"); c.px(15, 24, "y")                           // cinturon
  for (const [x, y] of [[3, 20], [4, 21], [28, 20], [27, 21], [12, 31], [19, 31]]) c.px(x, y, "y")   // paja
  c.ellipse(16, 9, 8, 7, "t"); c.ellipse(15, 8, 6, 5, "T")                // cabeza de papa
  c.px(12, 11, "c"); c.px(20, 7, "c"); c.px(18, 12, "c")
  c.rect(12, 8, 2, 2, "k"); c.rect(18, 8, 2, 2, "k"); c.hline(13, 12, 6, "b")
  c.poly([6, 4, 16, -1, 26, 4], "a"); c.hline(5, 4, 23, "o")              // sombrero de paja
  c.circ(16, 22, 2, "y"); c.px(16, 22, "k"); c.px(15, 20, "k"); c.px(17, 20, "k"); c.px(14, 23, "k"); c.px(18, 23, "k")
})

// ---------- HORNO (32x36, fuego de 2 cuadros) ----------
anim("Horno", { w: 32, h: 36, fps: 6, outline: "k" },
  (c) => {
    c.rect(2, 10, 28, 26, "r"); c.ellipse(16, 10, 14, 8, "r"); c.ellipse(15, 8, 10, 5, "R")
    for (let y = 14; y < 34; y += 5) for (let x = (y % 2 ? 4 : 7); x < 28; x += 7) c.hline(x, y, 4, "m")
    c.rect(12, 0, 8, 5, "m"); c.rect(13, 0, 6, 1, "e")                 // chimenea
    c.rect(9, 20, 14, 12, "k"); c.rect(10, 21, 12, 11, "p")             // boca del horno
  },
  frame(rect(11, 26, 10, 6, "o"), rect(13, 24, 6, 8, "y"), px(14, 23, "o")),
  frame(rect(11, 25, 10, 7, "o"), rect(12, 26, 7, 6, "y"), px(18, 23, "o")))

// ---------- ABONO: saco de tela con tierra fertil asomando ----------
sprite("Abono", { w: 30, h: 30, outline: "k" }, (c) => {
  c.poly([6, 28, 4, 12, 9, 7, 21, 7, 26, 12, 24, 28], "T"); c.poly([6, 28, 5, 14, 15, 12, 24, 14, 24, 28], "t")
  c.ellipse(15, 8, 6, 3, "b"); c.ellipse(15, 7, 4, 2, "c")
  c.px(13, 6, "g"); c.px(16, 5, "L"); c.px(17, 6, "g")
  c.line(9, 9, 21, 9, "a")
  c.rect(10, 17, 10, 6, "c"); c.px(12, 19, "g"); c.px(15, 20, "g"); c.px(17, 19, "g"); c.hline(12, 21, 6, "d")
})

// ---------- LINGOTES ----------
function lingote(claro, medio, oscuro) {
  return (c) => {
    c.poly([3, 18, 9, 10, 27, 10, 21, 18], claro); c.poly([3, 18, 21, 18, 21, 24, 3, 24], medio)
    c.poly([21, 18, 27, 10, 27, 16, 21, 24], oscuro); c.line(11, 12, 23, 12, "w")
  }
}
sprite("LingoteCobre", { w: 30, h: 30, outline: "k" }, lingote("T", "o", "c"))
sprite("LingoteHierro", { w: 30, h: 30, outline: "k" }, lingote("S", "s", "u"))

// ---------- suelo abonado: puntitos de abono sobre la tierra arada (se pinta encima de SueloPreparado) ----------
sprite("AbonoSuelo", { w: 32, h: 32 }, (c) => {
  const r = c.rng(5)
  for (let i = 0; i < 26; i++) { const x = 5 + Math.floor(r() * 22), y = 5 + Math.floor(r() * 22); c.px(x, y, i % 3 ? "b" : "p") }
  for (const [x, y] of [[9, 10], [20, 16], [13, 22]]) c.px(x, y, "g")
})

sheet("fabricacion", ["MesaTrabajo", "Antorcha", "Espantapapas", "Horno", "Abono", "Lingote*"], { pad: 2 })
