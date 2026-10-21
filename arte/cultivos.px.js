// Cultivos de papa (normal y mutante), papas cosechadas y el monticulo de donde sale la papa radiactiva.
// Mismo estilo que Etapa1..4 (la zanahoria original): contorno negro, verdes DB32.
pal({
  k: "#000000", p: "#45283c", b: "#663931", c: "#8f563b", t: "#d9a066", T: "#eec39a",
  L: "#99e550", g: "#6abe30", G: "#37946e", d: "#4b692f", v: "#306c06", y: "#fbf236",
  w: "#ffffff", q: "#d77bba", Q: "#76428a", e: "#323c39",
})
ramps("kpbctT", "kvdgL")

// Etapas dibujadas a mano, del tamano de las de la zanahoria original (Etapa1..4).
const SEMILLAS = `
  .tb.....tb..
  ..........tb
  ...tb.......
  .........tb.
  tb...tb.....`
const BROTE = `
  .kk...kk.
  kLgk.kgLk
  kggkkkggk
  .kkgdgkk.
  ...kdk...
  ...kdk...`
const MATA = `
  ......kkk......
  .....kLggk.kk..
  .kk..kgggkkLgk.
  kLgk.kggdkgggk.
  kgggkkgdkLggdk.
  .kggdkdkgggdk..
  ..kkddddddkk...
  .kLgkddddkgLk..
  kgggdkddkdggk..
  .kgddkkkkddk...
  ..kkk....kk....`
const MATA_FLOR = `
  ....kkk..kkk....
  ...kwywkkwywk...
  ...kkwkLgkwkk...
  .kk.kkLgggkkkk..
  kLgk.kgggdkLgk..
  kgggkkggdkgggdk.
  .kggdkgdkLggdk..
  ..kgddkdkgggdk..
  .kkkdddddddkk...
  kLgkkddddkkgLk..
  kgggdkddkdgggk..
  .kgddkttttkddk..
  ..kkkTtttttkk...
  ....kttbtttk....
  .....kkkkkk.....`
sprite("Papa_0", { w: 32, h: 32 }, layer("s", { x: 9, y: 13 }, SEMILLAS))
sprite("Papa_1", { w: 32, h: 32 }, layer("s", { x: 11, y: 16 }, BROTE))
sprite("Papa_2", { w: 32, h: 32 }, layer("s", { x: 8, y: 12 }, MATA))
sprite("Papa_3", { w: 32, h: 32 }, layer("s", { x: 7, y: 8 }, MATA_FLOR))
const MUTA = { g: "L", L: "y", d: "G", w: "q", t: "L", T: "y", b: "g" }
sprite("PapaMutante_0", { base: "Papa_0", swap: { t: "L", b: "g" } })
sprite("PapaMutante_1", { base: "Papa_1", swap: MUTA })
sprite("PapaMutante_2", { base: "Papa_2", swap: MUTA }, glow("y", { r: 2, strength: 0.5, bands: 2 }))
sprite("PapaMutante_3", { base: "Papa_3", swap: MUTA }, glow("yL", { r: 2, strength: 0.5, bands: 2 }))

// ---------- papas cosechadas (iconos) ----------
sprite("Papa", { w: 30, h: 30, outline: "k" }, (c) => {
  c.ellipse(15, 16, 10, 8, "c"); c.ellipse(14, 15, 9, 7, "t"); c.ellipse(12, 13, 4, 3, "T")
  for (const [x, y] of [[18, 12], [9, 17], [16, 19], [21, 17]]) c.px(x, y, "b")
})
sprite("PapaRadiactiva", { w: 30, h: 30, outline: "k" }, (c) => {
  c.ellipse(15, 16, 10, 8, "c"); c.ellipse(14, 15, 9, 7, "t"); c.ellipse(12, 13, 4, 3, "T")
  c.line(7, 15, 12, 17, "g"); c.line(12, 17, 15, 13, "L"); c.line(15, 13, 21, 16, "g"); c.line(15, 13, 16, 20, "g")
  c.px(15, 13, "y")
}, glow("Ly", { r: 3, strength: 0.6, bands: 3 }))

// ---------- monticulo de tierra que tiembla antes de que salga la papa (3 cuadros) ----------
anim("Monticulo", { w: 34, h: 16, fps: 10 },
  (c) => { c.ellipse(17, 11, 15, 4, "b"); c.ellipse(17, 10, 12, 3, "c"); c.ellipse(17, 11, 15, 4, "k", true) },
  frame(line(12, 9, 16, 11, "k"), px(22, 9, "k")),
  frame(line(12, 9, 16, 11, "k"), line(16, 11, 21, 8, "k"), px(17, 10, "L"), px(9, 10, "t")),
  frame(line(10, 10, 16, 11, "k"), line(16, 11, 23, 8, "k"), line(16, 11, 15, 14, "k"), px(17, 10, "L"), px(18, 9, "y"),
        px(5, 7, "c"), px(28, 6, "c"), px(25, 4, "t")))

sheet("cultivos", ["Papa_*", "PapaMutante_*", "Papa", "PapaRadiactiva"], { pad: 2 })
