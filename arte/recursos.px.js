// Recursos de Papayork: iconos 32x32 para la mochila y objetos del mundo (vetas, hierba).
// Paleta DB32, la misma que usan los sprites originales hechos en Aseprite.
pal({
  k: "#000000", n: "#222034", p: "#45283c", b: "#663931", c: "#8f563b", o: "#df7126",
  t: "#d9a066", T: "#eec39a", y: "#fbf236", L: "#99e550", g: "#6abe30", G: "#37946e",
  d: "#4b692f", v: "#306c06", e: "#323c39", u: "#3f3f74", B: "#306082", s: "#9badb7",
  S: "#cbdbfc", w: "#ffffff", r: "#696a6a", R: "#847e87", m: "#595652", a: "#8a6f30",
  x: "#ac3232", q: "#76428a", C: "#5fcde4", z: "#8b6136",
})
ramps("kndvgL", "kpbcotT", "kerRw", "kuBCS", "kaoy", "kpqL")

// Centra una parte (ya con contorno) en un icono de 32x32, apoyada un poco abajo como los originales.
function icono(nombre, parte, w, h, dy = 1) {
  sprite(nombre, { w: 32, h: 32 }, stamp(parte, Math.floor((32 - w) / 2), Math.floor((32 - h) / 2) + dy))
}

// ---------- FIBRA: manojo de hierba atado con una cinta ----------
sprite("_fibra", { outline: "k" }, `
  ..g....g...g..
  .gL...gL..gL..
  .gL..gL...gL.g
  ..gL.gL..gL.gL
  ..gLgL..gL.gL.
  ...gLgL.gLgL..
  ...gLLgLgLL...
  ....gLLLLL....
  ....tTTTTt....
  ....cttttc....
  ....gLLLLg....
  ...gLgLLgLg...
  ..gL.gLLg.Lg..
  .gL..gLLg..Lg.
  .g...gddg...g.
  .....dvvd.....`)
icono("Fibra", "_fibra", 16, 18)

// ---------- RESINA: gota de savia ambar con brillo ----------
sprite("_resina", { outline: "k" }, `
  .....o.....
  .....o.....
  ....oyo....
  ....oyo....
  ...ooyoo...
  ...oyyoo...
  ..ooyooao..
  ..oyyoooa..
  .ooyoooooa.
  .oyooooooa.
  .oyooooooa.
  .oooooooaa.
  ..oooooaa..
  ...aaaaa...`)
sprite("_astilla", { outline: "k" }, `
  ttcccc
  .ccbbb`)
sprite("Resina", { w: 32, h: 32 }, stamp("_astilla", 9, 22), stamp("_resina", 10, 6), px(14, 10, "w"), px(14, 11, "w"))

// ---------- CARBON: tres terrones oscuros con destellos ----------
sprite("Carbon", { w: 30, h: 30, outline: "k" },
  ellipse(11, 19, 6, 5, "e"), ellipse(20, 18, 7, 6, "n"), ellipse(15, 13, 6, 5, "e"),
  ellipse(13, 12, 3, 2, "m"), ellipse(18, 16, 3, 2, "m"), ellipse(9, 18, 2, 2, "m"),
  px(13, 11, "w"), px(19, 15, "w"), px(8, 17, "S"))

// ---------- MINERALES: roca con pepitas ----------
function rocaMineral(c, claro, medio, oscuro) {
  c.ellipse(15, 17, 11, 8, "r"); c.ellipse(13, 15, 7, 5, "R")
  c.hline(9, 12, 4, "w"); c.px(8, 13, "w")
  for (const [x, y] of [[10, 17], [17, 13], [19, 19], [14, 21]]) {
    c.rect(x, y, 3, 3, medio); c.px(x, y, claro); c.px(x + 2, y + 2, oscuro); c.px(x + 2, y, medio)
  }
}
sprite("Cobre", { w: 30, h: 30, outline: "k" }, (c) => rocaMineral(c, "T", "o", "c"))
sprite("Hierro", { w: 30, h: 30, outline: "k" }, (c) => rocaMineral(c, "w", "s", "u"))

// ---------- CRISTAL RADIACTIVO: racimo de puntas verdes que brillan ----------
sprite("_cristal", { w: 24, h: 23, outline: "k" },
  poly([4, 20, 7, 6, 10, 20], "g"), poly([9, 21, 13, 1, 17, 21], "g"), poly([15, 20, 19, 8, 22, 20], "G"),
  line(12, 4, 11, 19, "L"), line(7, 8, 6, 18, "L"), line(19, 11, 18, 18, "g"),
  px(12, 5, "y"), px(7, 9, "y"), rect(3, 19, 21, 3, "G"), hline(4, 19, 19, "d"))
sprite("Cristal", { w: 32, h: 32 }, stamp("_cristal", 4, 4), glow("Ly", { r: 4, strength: 0.6, bands: 3 }))

// ---------- NUCLEO DE URANIO: esfera de metal con el corazon verde y el simbolo radiactivo ----------
sprite("Nucleo", { w: 30, h: 30, outline: "k" }, (c) => {
  c.circ(15, 15, 11, "e"); c.ring(15, 15, 11, "m"); c.circ(15, 15, 8, "G"); c.circ(15, 15, 7, "g"); c.circ(14, 14, 4, "L")
  // trebol radiactivo (3 aspas y centro)
  c.circ(15, 15, 1, "k")
  c.poly([13, 12, 15, 9, 17, 12], "k"); c.poly([10, 17, 12, 14, 14, 18], "k"); c.poly([16, 18, 18, 14, 20, 17], "k")
  c.px(9, 8, "w"); c.px(10, 7, "w"); c.px(8, 9, "S")
  for (const [x, y] of [[15, 3], [3, 15], [27, 15], [15, 27]]) c.rect(x - 1, y - 1, 3, 3, "R")
}, glow("gL", { r: 3, strength: 0.4, bands: 2 }))

// ---------- TIERRA FERTIL: monticulo de tierra oscura con un brote ----------
sprite("TierraFertil", { w: 30, h: 30, outline: "k" },
  clip([0, 0, 30, 25], ellipse(15, 25, 12, 10, "b")), clip([0, 0, 30, 25], ellipse(13, 24, 8, 6, "c")),
  rect(3, 24, 25, 2, "p"),
  px(9, 19, "t"), px(18, 21, "t"), px(21, 17, "p"), px(12, 22, "p"), px(15, 18, "T"),
  vline(15, 9, 7, "g"), line(15, 11, 11, 8, "g"), line(15, 10, 19, 7, "L"), px(10, 7, "L"), px(20, 6, "L"))

// ---------- SOBRES DE SEMILLAS (misma forma que el sobre de zanahoria original) ----------
// Sobre: borde x (rojo oscuro) / cuerpo / pliegue sombreado. "_papa" se pinta encima.
const SOBRE = `
  ..xxxxxxxxxxxxxxxxx..
  .xbbbbbbbbbbbbbbbbbx.
  xbxbbbbbbbbbbbbbbbxzx
  xbbxbbbbbbbbbbbbbxzzx
  xbbbxbbbbbbbbbbbxzbzx
  xbbbbxbbbbbbbbbxzbbzx
  xbbbbbxbbbbbbbxzbbbzx
  xbbbbbbxbbbbbxzbbbbzx
  xbbbbbbbxbbbxzbbbbbzx
  xbbbbbbbbxxxzbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbbzx
  xbbbbbbbbbbbbbbbbbzzx
  .xbbbbbbbbbbbbbbbzzx.
  ..xxxxxxxxxxxxxxxxx..`
sprite("_papa", `
  ......gL......
  .....gLg......
  ...cccccccc...
  ..cttTTttttc..
  .cttTTtttbttc.
  cttTttttttttc.
  ctttttbtttttc.
  cttttttttbttc.
  cttbtttttttc..
  .ctttttbtttc..
  ..cccccccccc..`)
sprite("_papaMutante", `
  ......gL......
  .....gLg......
  ...cccccccc...
  ..ctLtttLttc..
  .cttLttLtbttc.
  ctttLLLLtttLc.
  ctLtttLtttLtc.
  cLtttttLLLttc.
  cttLtttLtttc..
  .ctLttLtLttc..
  ..cccccccccc..`)
sprite("Semillas de Papa", { w: 32, h: 32 },
  layer("sobre", { x: 6, y: 2 }, SOBRE), recolor({ b: "C", z: "B", x: "u" }, [6, 2, 21, 26]),
  stamp("_papa", 9, 12))
sprite("Semillas de Papa Mutante", { w: 32, h: 32 },
  layer("sobre", { x: 6, y: 2 }, SOBRE), recolor({ b: "p", z: "n", x: "q" }, [6, 2, 21, 26]),
  stamp("_papaMutante", 9, 12), glow("L", { where: [9, 12, 14, 11], r: 2, strength: 0.5 }))

// ---------- MUNDO: vetas de mineral (misma roca que Roca1) ----------
const ROCA = `
  .....kkkkk..............
  ...kkkwwwkk.............
  ..kkrrrrrrkk............
  .kkwrrrrrrwk............
  .kwrrrrrrrrrk...........
  kkrrrrrrrrrrkkkkkkkk....
  kwrrrrrrrrrrrrrrRRRkk...
  kwrrrrrrrrrrrrrrrrRRkk..
  kwrrrrrrwwwwwrrrrrrRRk..
  kwrrrrrwwrrrwwrrrrrRRk..
  kwrrrrwwrrrrrwwrrrRRRk..
  kwrrrrrrrrrrrrrrrRRRRk..
  kkwrrrrrrrrrrrrrRRRRkk..
  .kkwrrrrrrrrrrrRRRRkk...
  ..kkrrrrRRRRRRRRRRkk....
  ...kkkkkkkkkRRRRRkk.....
  ...........kkkkkkk......`
function pepitas(claro, medio, oscuro, lugares) {
  return (c) => { for (const [x, y] of lugares) { c.rect(x, y, 3, 2, medio); c.px(x, y, claro); c.px(x + 2, y + 1, oscuro); c.px(x - 1, y + 1, "k") } }
}
sprite("VetaCobre", { w: 32, h: 32 }, layer("roca", { x: 4, y: 7 }, ROCA),
  pepitas("T", "o", "c", [[9, 14], [16, 17], [21, 14], [12, 19], [19, 20]]))
sprite("VetaHierro", { w: 32, h: 32 }, layer("roca", { x: 4, y: 7 }, ROCA),
  pepitas("w", "s", "u", [[9, 14], [16, 17], [21, 14], [12, 19], [19, 20]]), recolor({ r: "m", R: "r" }, [4, 7, 24, 17]))
sprite("_puntas", { w: 19, h: 19, outline: "k" },
  poly([0, 18, 3, 4, 6, 18], "g"), poly([5, 17, 9, 0, 13, 17], "g"), poly([11, 18, 15, 6, 18, 18], "G"),
  line(8, 3, 7, 16, "L"), line(3, 7, 2, 16, "L"), line(15, 9, 14, 16, "g"), px(8, 4, "y"), px(3, 8, "y"))
sprite("VetaCristal", { w: 32, h: 32 }, layer("roca", { x: 4, y: 11 }, ROCA), recolor({ r: "e", R: "m", w: "R" }, [4, 11, 24, 17]),
  stamp("_puntas", 6, 0), glow("Ly", { r: 4, strength: 0.5, bands: 3 }))

// ---------- MUNDO: hierba alta que se corta y suelta fibra (estilo de los arbustos de DecoBosque) ----------
// Hierbajos: matitas bajas de hojas (contorno azul oscuro como los arbustos de DecoBosque).
const MATA1 = `
  ......n.....n..........
  .....nLn...nLn...n.....
  ..n.nLgLn.nLgLn.nLn....
  .nLnLgggLnLgggLnLgLn...
  nLgLgggggLgggggLgggLn..
  nggggLgggggLgggggggggn.
  ngGgggggGgggggGgggggGn.
  nGGgGgggGGggGgGGgggGGn.
  .nGGGGGGGGGGGGGGGGGGn..
  ..nnnnnnnnnnnnnnnnnn...`
const MATA2 = `
  .....n.......n....
  ....nLn.....nLn...
  ....nLn..n..nLn...
  .n..nLgnnLnnLgn.n.
  nLn.nLgLLgLLggnnLn
  nLgnLggggggggLnLgn
  ngggLgggGgggggLggn
  nGggggGgggGggggGgn
  nGGgGGGgGGGGgGGGGn
  .nGGGGGGGGGGGGGGn.
  ..nnnnnnnnnnnnnn..`
const MATA3 = `
  ...........y........
  ....n.....ywy...n...
  ...nLn.n...y...nLn..
  ..nLgLnLn.nLn.nLgLn.
  .nLgggLgLnLgLnLgggLn
  nLgggggggLgggggggggn
  ngggGgggggggGggggggn
  nGgGGggGgggGGgggGgGn
  .nGGGGGGGGGGGGGGGGn.
  ..nnnnnnnnnnnnnnnn..`
sprite("Hierba1", { w: 30, h: 30 }, layer("mata", { x: 4, y: 19 }, MATA1))
sprite("Hierba2", { w: 30, h: 30 }, layer("mata", { x: 6, y: 18 }, MATA2))
sprite("Hierba3", { w: 30, h: 30 }, layer("mata", { x: 5, y: 19 }, MATA3))

sheet("iconos_recursos", ["Fibra", "Resina", "Carbon", "Cobre", "Hierro", "Cristal", "Nucleo", "TierraFertil",
  "Semillas de Papa", "Semillas de Papa Mutante"], { pad: 2 })
sheet("mundo_recursos", ["VetaCobre", "VetaHierro", "VetaCristal", "Hierba1", "Hierba2", "Hierba3"], { pad: 2 })
