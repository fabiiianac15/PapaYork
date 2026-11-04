// Personajes de PapaYork: cuerpos y retratos propios, cada uno con su complexion y su ropa.
// Luz desde arriba a la izquierda. Compilar: node ~/.claude/skills/pxl-pixel-art/bin/pxl.js build personajes_natural.px.js
pal({ K: "#2a1d2b" })

const PIEL = {
  clara: ["#f6d3ae", "#e8b48c", "#c98a6c", "#9c6152"],
  media: ["#e6b98d", "#cf9568", "#a96f50", "#7e4e40"],
  morena: ["#c98f62", "#a86f49", "#80523a", "#5c3a30"],
  mayor: ["#ecc4a2", "#d6a180", "#b07c66", "#83594f"],
}
const T = (a, b, c, d) => [a, b, c, d]   // tela: luz, medio, sombra, hondo

const PERSONAJES = {
  Pedro: {
    piel: PIEL.clara, pelo: T("#8a5a34", "#6b4026", "#4e2c1f", "#35201c"), peinado: "revuelto", bajo: 6,
    ancho: 13, torso: 13, ropa: T("#d65a4a", "#b23c3c", "#842c37", "#5e2230"), brazo: "corto",
    pierna: T("#5aa6ad", "#3d8390", "#2e6476", "#23495c"), zapato: T("#8d6345", "#6c4733", "#4f3329", "#3a2622"),
    peto: T("#5aa6ad", "#3d8390", "#2e6476", "#23495c"), ojos: "#3f2a22",
  },
  PedroSin: { sinSombrero: true,
    piel: PIEL.clara, pelo: T("#8a5a34", "#6b4026", "#4e2c1f", "#35201c"), peinado: "revuelto", bajo: 6,
    ancho: 13, torso: 13, ropa: T("#d65a4a", "#b23c3c", "#842c37", "#5e2230"), brazo: "corto",
    pierna: T("#5aa6ad", "#3d8390", "#2e6476", "#23495c"), zapato: T("#8d6345", "#6c4733", "#4f3329", "#3a2622"),
    peto: T("#5aa6ad", "#3d8390", "#2e6476", "#23495c"), ojos: "#3f2a22",
  },
  Hetol: { soloRetrato: true, fondo: ["#c9b97a", "#a8965c"],
    piel: PIEL.mayor, pelo: T("#9c8a78", "#7a6a5c", "#5a4e46", "#3f3836"), peinado: "paja", bajo: 2,
    paja: T("#f7e3a4", "#e3c478", "#bd9a58", "#8d7044"),
    ancho: 13, torso: 13, ropa: T("#7f9a68", "#5f7c52", "#465e42", "#324634"), brazo: "largo",
    pierna: T("#8a6e54", "#6a5240", "#4f3c30", "#382a24"), zapato: T("#6c4733", "#4f3329", "#3a2622", "#2a1f22"),
    bigote: T("#d8d4cc", "#a8a49c", "#7c7a78", "#55535a"), ojos: "#2e2622", arrugas: true,
  },
  Chuchini: { soloRetrato: true,
    piel: PIEL.media, pelo: T("#4f3a2c", "#3a2a22", "#2a1f1c", "#1c1516"), peinado: "peinado", bajo: 2,
    ancho: 13, torso: 13, ropa: T("#7fa6d0", "#5782b0", "#3f6490", "#2f4a70"), brazo: "largo",
    pierna: T("#8a7a5c", "#6a5c46", "#4e4436", "#38322a"), zapato: T("#6c4733", "#4f3329", "#3a2622", "#2a1f22"),
    bigote: T("#5a4434", "#3f2f26", "#2c211e", "#1c1516"), ojos: "#2e2622",
  },
  ChuchiniViejo: { soloRetrato: true,
    piel: PIEL.media, pelo: T("#e4e0d8", "#c0bcb4", "#94928e", "#6a6a6c"), peinado: "paja", bajo: 2,
    paja: T("#f7e3a4", "#e3c478", "#bd9a58", "#8d7044"),
    ancho: 13, torso: 13, ropa: T("#a0b4c4", "#7c92a6", "#5f7488", "#465868"), brazo: "largo",
    pierna: T("#8a7a5c", "#6a5c46", "#4e4436", "#38322a"), zapato: T("#6c4733", "#4f3329", "#3a2622", "#2a1f22"),
    barba: T("#f2efe6", "#d6d2c8", "#aaa8a4", "#858487"), barbaForma: "completa", ojos: "#352b2a", arrugas: true,
  },
  Ines: {
    piel: PIEL.morena, pelo: T("#3f3048", "#2a2034", "#1c1626", "#120e1a"), peinado: "mono", bajo: 3,
    ancho: 11, torso: 15, ropa: T("#8fa88a", "#6a8a68", "#4f6c52", "#3a5040"), brazo: "largo",
    falda: T("#6a5a7a", "#4f4260", "#3a3048", "#2a2236"), zapato: T("#5c4436", "#43322b", "#312523", "#231b1d"),
    ojos: "#2c2230", lentes: true,
  },
  Beto: {
    piel: PIEL.clara, pelo: T("#b0683a", "#8a4e2c", "#663822", "#4a2a1c"), peinado: "peinado", bajo: 5,
    ancho: 17, torso: 13, ropa: T("#efe2c4", "#d4c4a4", "#a89a80", "#7c7060"), brazo: "remangado",
    pierna: T("#5a4a44", "#43362f", "#312824", "#231c1a"), zapato: T("#5c4436", "#43322b", "#312523", "#231b1d"),
    delantal: T("#d8d0b8", "#b8ae94", "#8e8670", "#6a6452"), bigote: T("#c07a44", "#9a5a30", "#744222", "#54301a"), ojos: "#2e2622",
  },
  Rosa: {
    piel: PIEL.mayor, pelo: T("#d9d4cc", "#b4aea8", "#8b8688", "#64606a"), peinado: "mono", bajo: 6,
    ancho: 16, torso: 12, ropa: T("#b98bb0", "#94648f", "#6f4a75", "#50365a"), brazo: "largo",
    falda: T("#a6655f", "#854a4e", "#633840", "#482b35"), zapato: T("#6b4a3d", "#4f3630", "#3a2828", "#2a1f22"),
    delantal: T("#b9cf8b", "#8fae68", "#6b8a55", "#4f6a48"), ojos: "#4a3530", arrugas: true, chal: T("#e39ab0", "#c5728e", "#9a5574", "#73425f"),
  },
  Fermin: {
    piel: PIEL.morena, pelo: T("#8d8a86", "#6b6968", "#4c4b50", "#34343c"), peinado: "gorra", bajo: 4,
    gorra: T("#8c7355", "#6d573f", "#514131", "#3a2f27"),
    ancho: 18, torso: 14, ropa: T("#c7b8a0", "#a39279", "#7c6d5e", "#5a5048"), brazo: "remangado",
    pierna: T("#6a5c58", "#4f4545", "#3b3438", "#2a262c"), zapato: T("#5c4436", "#43322b", "#312523", "#231b1d"),
    mandil: T("#8a5a3a", "#6a4230", "#4e3028", "#382322"), barba: T("#a8a5a0", "#807d7c", "#5c5a60", "#403f48"), barbaForma: "completa", ojos: "#2e2622",
  },
  Ramiro: {
    piel: PIEL.clara, pelo: T("#c3c8cc", "#979da4", "#6f7581", "#505564"), peinado: "peinado", bajo: 1,
    ancho: 10, torso: 16, ropa: T("#5a6494", "#3f4775", "#2d3358", "#20243f"), brazo: "largo",
    pierna: T("#4c5684", "#363e66", "#272c4c", "#1c2038"), zapato: T("#4a3535", "#332526", "#241b1e", "#191316"),
    banda: true, bigote: T("#a7acb2", "#7d828c", "#5a5e6c", "#404452"), ojos: "#32323c", lentes: true, arrugas: true,
  },
  Lupita: {
    piel: PIEL.media, pelo: T("#4a3f58", "#2f2940", "#211c30", "#161322"), peinado: "trenzas", bajo: 13,
    ancho: 10, torso: 9, ropa: T("#f4d36a", "#e0ad3e", "#b37f2f", "#855a2a"), brazo: "corto",
    falda: T("#f4d36a", "#e0ad3e", "#b37f2f", "#855a2a"), piernaDesnuda: true, zapato: T("#d0605e", "#a54350", "#7c3344", "#5c2838"),
    moño: "#d85a68", ojos: "#2c2230", pecas: true,
  },
  Tomas: {
    piel: PIEL.media, pelo: T("#f2efe6", "#d6d2c8", "#aaa8a4", "#7e7e82"), peinado: "paja", bajo: 7, encorvado: true,
    paja: T("#f0d893", "#d6b367", "#aa8549", "#7c5f3a"),
    ancho: 13, torso: 12, ropa: T("#7fb1d2", "#568bb2", "#3f6a90", "#2f4f70"), brazo: "largo",
    pierna: T("#8d6b4c", "#6f5240", "#533d32", "#3c2c28"), zapato: T("#5f4638", "#46332b", "#332624", "#25191b"),
    barba: T("#fbf9f2", "#dedbd2", "#b3b1ac", "#858487"), barbaForma: "larga", ojos: "#352b2a", arrugas: true, baston: true,
  },
}

// ---------- utilidades ----------
function vol(c, x, y, w, h, r) {           // bloque con volumen
  c.rect(x, y, w, h, r[1])
  c.vline(x, y, h, r[0]); c.hline(x, y, w, r[0])
  c.vline(x + w - 1, y, h, r[2]); c.hline(x, y + h - 1, w, r[2])
}
function rect(c, x, y, w, h, col) { c.rect(x, y, w, h, col) }

// ---------- pierna / falda ----------
function piernas(c, P, cx, sup, dir, f) {
  const fin = 45, r = P.pierna || P.piel, z = P.zapato
  if (P.falda) {
    const alto = fin - 3 - sup - (P.piernaDesnuda ? 4 : 0), a = P.ancho + (P.piernaDesnuda ? 2 : 4)
    if (P.piernaDesnuda) {
      const p = f === 1 ? -1 : 0, q = f === 3 ? -1 : 0
      rect(c, cx - 4, sup + alto - 1, 3, fin - sup - alto + 1 + p, P.piel[1]); c.vline(cx - 4, sup + alto - 1, fin - sup - alto + 1 + p, P.piel[0])
      rect(c, cx + 1, sup + alto - 1, 3, fin - sup - alto + 1 + q, P.piel[2])
      vol(c, cx - 5, fin - 2 + p, 5, 3, z); vol(c, cx, fin - 2 + q, 5, 3, z)
    } else {
      const p = f === 1 ? -1 : 0, q = f === 3 ? -1 : 0
      vol(c, cx - 5, fin - 2 + p, 5, 3, z); vol(c, cx, fin - 2 + q, 5, 3, z)
    }
    // falda acampanada con pliegues que siguen la caida
    for (let i = 0; i <= alto; i++) {
      const med = Math.round(P.ancho / 2 + (a - P.ancho) / 2 * i / alto)
      c.hline(cx - med, sup + i, med * 2, P.falda[1])
      c.px(cx - med, sup + i, P.falda[0]); c.px(cx + med - 1, sup + i, P.falda[2]); c.px(cx + med - 2, sup + i, P.falda[2])
    }
    for (const dx of [-3, 2]) c.vline(cx + dx, sup + 2, alto - 2, P.falda[2])
    c.hline(cx - Math.round(a / 2), sup + alto, a, P.falda[2])
    return
  }
  const anchoP = P.ancho >= 16 ? 6 : 5, sep = dir === "izq" ? 0 : Math.round(P.ancho / 2) - anchoP
  if (dir === "izq") {          // de lado: las piernas se cruzan al andar
    const paso = f === 1 ? 3 : f === 3 ? -3 : 0
    for (const [dx, tela] of [[-paso, [r[2], r[2], r[3], r[3]]], [paso, r]]) {
      const xx = cx - 3 + dx
      vol(c, xx, sup, 6, fin - sup - 2, tela)
      vol(c, xx - 1, fin - 3, 7, 4, z)
    }
    return
  }
  const izqAlto = f === 1 ? 2 : 0, derAlto = f === 3 ? 2 : 0
  vol(c, cx - sep - anchoP, sup, anchoP, fin - sup - 2 - izqAlto, r)
  vol(c, cx + sep, sup, anchoP, fin - sup - 2 - derAlto, [r[1], r[1], r[2], r[3]])
  vol(c, cx - sep - anchoP - 1, fin - 3 - izqAlto, anchoP + 1, 4, z)
  vol(c, cx + sep, fin - 3 - derAlto, anchoP + 1, 4, z)
}

// ---------- torso y brazos ----------
function torso(c, P, cx, y, dir, f) {
  const w = dir === "izq" ? Math.max(8, P.ancho - 3) : P.ancho, x = cx - Math.floor(w / 2), h = P.torso, r = P.ropa
  vol(c, x, y, w, h, r)
  c.vline(x + w - 2, y + 1, h - 1, r[2])
  const brazo = (bx, by, largo, tela) => {
    c.rect(bx, by, 3, largo, tela[1]); c.vline(bx, by, largo, tela[0]); c.vline(bx + 2, by, largo, tela[2])
    if (P.brazo === "remangado") { c.rect(bx, by + 4, 3, largo - 4, P.piel[1]); c.vline(bx, by + 4, largo - 4, P.piel[0]); c.vline(bx + 2, by + 4, largo - 4, P.piel[2]) }
    if (P.brazo === "corto") { c.rect(bx, by + 5, 3, largo - 5, P.piel[1]); c.vline(bx + 2, by + 5, largo - 5, P.piel[2]) }
    c.rect(bx, by + largo, 3, 2, P.piel[1]); c.px(bx + 2, by + largo + 1, P.piel[2])
  }
  const largo = Math.max(7, h - 3), sw = f === 1 ? 1 : f === 3 ? -1 : 0
  if (dir === "izq") {
    brazo(cx - 1 + sw * 2, y + 1, largo, r)
  } else {
    brazo(x - 3, y + 1 + sw, largo, r); brazo(x + w, y + 1 - sw, largo, [r[1], r[1], r[2], r[3]])
  }
  if (dir === "arriba" && P.peto) {   // tirantes cruzados por la espalda
    c.line(x + 2, y, x + w - 3, y + 6, P.peto[2]); c.line(x + w - 3, y, x + 2, y + 6, P.peto[2]); c.rect(x + 1, y + 7, w - 2, h - 7, P.peto[1])
  }
  if (dir === "abajo") {
    if (P.peto) {                     // overol
      c.rect(x + 2, y + 5, w - 4, h - 5, P.peto[1]); c.hline(x + 2, y + 5, w - 4, P.peto[0]); c.vline(x + w - 3, y + 5, h - 5, P.peto[2])
      c.vline(x + 2, y, 5, P.peto[1]); c.vline(x + w - 3, y, 5, P.peto[2]); c.px(x + 3, y + 6, "#e8c76f"); c.px(x + w - 4, y + 6, "#e8c76f")
      c.rect(cx - 2, y + 8, 4, 3, P.peto[2])
    }
    if (P.delantal) {                 // delantal de mercado
      c.rect(x + 2, y + 3, w - 4, h - 3, P.delantal[1]); c.hline(x + 2, y + 3, w - 4, P.delantal[0]); c.vline(x + w - 3, y + 3, h - 3, P.delantal[2])
      c.hline(x, y + 7, w, P.delantal[2])
    }
    if (P.mandil) {                   // mandil de cuero de herrero
      c.rect(x + 3, y + 3, w - 6, h - 3, P.mandil[1]); c.hline(x + 3, y + 3, w - 6, P.mandil[0]); c.vline(x + w - 4, y + 3, h - 3, P.mandil[2])
      c.line(x + 3, y + 3, x + 1, y, P.mandil[2]); c.line(x + w - 4, y + 3, x + w - 2, y, P.mandil[2])
      c.rect(cx - 3, y + 8, 6, 2, P.mandil[2]); c.px(cx - 4, y + 12, "#c8b28a")
    }
    if (P.banda) {                    // banda de alcalde
      for (let i = 0; i < 9; i++) { c.px(x + 1 + i, y + 2 + i, "#e0c060"); c.px(x + 2 + i, y + 2 + i, "#4f7ec9"); c.px(x + 3 + i, y + 2 + i, "#c04a4a") }
      c.px(cx, y + 2, "#f2efe6"); c.px(cx, y + 3, "#f2efe6")
    }
    if (P.chal) {                     // chal de Rosa
      c.rect(x, y, w, 4, P.chal[1]); c.hline(x, y, w, P.chal[0]); c.poly([x + 2, y + 4, x + w - 2, y + 4, cx, y + 8], P.chal[1]); c.hline(x, y + 3, w, P.chal[2])
    }
  }
  if (P.baston && dir !== "arriba") { c.vline(dir === "izq" ? cx - 7 : x - 5, y + 2, 45 - y - 2, "#8a6242"); c.vline(dir === "izq" ? cx - 6 : x - 4, y + 2, 45 - y - 2, "#5e4232"); c.hline(dir === "izq" ? cx - 7 : x - 5, y + 2, 3, "#a67b52") }
}

// ---------- cabeza ----------
function cabeza(c, P, cx, y, dir, parp) {
  const s = P.piel, w = 14, x = cx - 7, h = 13, lado = dir === "izq"
  const ox = P.encorvado ? (lado ? -2 : 0) : 0, xx = x + ox + (lado ? -1 : 0)
  c.rect(xx, y, w, h, s[1]); c.vline(xx, y, h, s[0]); c.hline(xx + 1, y, w - 2, s[0])
  c.rect(xx + w - 3, y + 1, 3, h - 2, s[2]); c.hline(xx + 1, y + h - 1, w - 2, s[2]); c.hline(xx + 3, y + h - 2, w - 6, s[1])
  for (const [a, b] of [[xx, y], [xx + w - 1, y], [xx, y + h - 1], [xx + w - 1, y + h - 1]]) c.px(a, b, "_")
  if (dir === "arriba") return { x: xx, w, y, h }
  const ey = y + 7, ojo = (ex) => {
    if (parp) { c.hline(ex, ey + 1, 2, s[3]); return }
    c.rect(ex, ey, 2, 2, "#fbf5ea"); c.vline(ex + (lado ? 0 : 1), ey, 2, P.ojos); c.px(ex + (lado ? 0 : 1), ey, "#1a1320")
  }
  if (lado) {
    ojo(xx + 2)
    c.px(xx - 1, ey + 2, s[1]); c.px(xx, ey + 3, s[2]); c.hline(xx + 1, ey + 4, 2, s[3]); c.px(xx + 5, ey + 3, "#e29a88")
    c.hline(xx + 1, ey - 2, 3, P.peinado === "gorra" ? s[3] : P.pelo[2])
  } else {
    ojo(xx + 3); ojo(xx + 9)
    c.hline(xx + 2, ey - 2, 3, P.pelo[2]); c.hline(xx + 9, ey - 2, 3, P.pelo[2])
    c.px(xx + 6, ey + 2, s[2]); c.px(xx + 7, ey + 2, s[2])
    c.hline(xx + 5, ey + 4, 4, s[3])
    c.px(xx + 2, ey + 2, "#e29a88"); c.px(xx + 11, ey + 2, "#d38778")
    if (P.pecas) { c.px(xx + 4, ey + 2, s[2]); c.px(xx + 9, ey + 2, s[2]) }
    if (P.arrugas) { c.px(xx + 2, ey - 1, s[2]); c.px(xx + 11, ey - 1, s[3]); c.px(xx + 5, ey + 3, s[2]); c.px(xx + 8, ey + 3, s[2]) }
    if (P.lentes) { c.hline(xx + 2, ey + 2, 4, "#6b6f7a"); c.hline(xx + 8, ey + 2, 4, "#6b6f7a"); c.hline(xx + 6, ey, 2, "#6b6f7a"); c.vline(xx + 2, ey - 1, 3, "#6b6f7a"); c.vline(xx + 5, ey - 1, 3, "#6b6f7a"); c.vline(xx + 8, ey - 1, 3, "#6b6f7a"); c.vline(xx + 11, ey - 1, 3, "#6b6f7a") }
    if (P.bigote) { c.rect(xx + 3, ey + 3, 8, 2, P.bigote[1]); c.hline(xx + 3, ey + 3, 4, P.bigote[0]); c.px(xx + 2, ey + 4, P.bigote[2]); c.px(xx + 11, ey + 4, P.bigote[2]) }
  }
  return { x: xx, w, y, h }
}

function barba(c, P, b, dir) {
  if (!P.barba || dir === "arriba") return
  const r = P.barba, lado = dir === "izq", larga = P.barbaForma === "larga"
  const x = b.x + (lado ? 0 : 1), w = lado ? 7 : b.w - 2, y = b.y + 9
  c.rect(x, y, w, 4, r[1]); c.hline(x, y, w, r[0])
  c.rect(x + 1, y + 4, w - 2, larga ? 5 : 3, r[1]); c.vline(x + w - 2, y + 4, larga ? 5 : 3, r[2])
  if (larga) { c.rect(x + 3, y + 9, w - 6, 2, r[1]); for (let i = 0; i < 3; i++) c.vline(x + 3 + i * 3, y + 3, 6, r[2]) }
  if (!lado) { c.hline(x + 3, y + 1, w - 6, P.piel[3]); c.hline(x + 1, y, w - 2, r[0]) }
}

function pelo(c, P, b, dir) {
  const r = P.pelo, { x, y, w } = b, lado = dir === "izq", atras = dir === "arriba"
  const casco = (filas) => {
    for (let i = 0; i < filas; i++) {
      const m = i === 0 ? 2 : 0
      c.hline(x + m, y - 1 + i, w - m * 2, i < 2 ? r[0] : r[1])
    }
    c.vline(x + w - 1, y, filas, r[2]); c.vline(x + w - 2, y, filas, r[2])
  }
  switch (P.peinado) {
    case "revuelto":
      casco(atras ? 11 : 6)
      c.px(x + 3, y - 2, r[1]); c.px(x + 4, y - 2, r[0]); c.px(x + 8, y - 2, r[1]); c.px(x + 11, y - 2, r[2])
      if (atras) { for (const a of [1, 4, 7, 10, 12]) c.vline(x + a, y + 8, 3, r[2]); break }
      if (lado) { c.rect(x + 6, y + 3, w - 6, 8, r[1]); c.vline(x + w - 1, y + 3, 8, r[2]); for (const a of [7, 10]) c.vline(x + a, y + 9, 3, r[2]); c.px(x, y + 5, r[1]); c.px(x + 1, y + 5, r[2]); break }
      for (const [a, l, t] of [[0, 8, 1], [1, 6, 1], [3, 7, 2], [6, 5, 1], [9, 7, 2], [12, 8, 2], [13, 8, 3]]) c.vline(x + a, y + 3, l - 2, r[t])
      break
    case "mono":
      casco(atras ? 10 : 5)
      c.ellipse(x + 7, y - 3, 4, 3, r[1]); c.px(x + 5, y - 5, r[0]); c.px(x + 6, y - 5, r[0]); c.px(x + 9, y - 2, r[2]); c.hline(x + 4, y - 1, 7, r[2])
      if (!atras) { c.vline(x, y + 3, 5, r[1]); c.vline(x + w - 1, y + 3, 5, r[2]); if (lado) c.rect(x + 7, y + 3, w - 7, 6, r[1]) }
      break
    case "peinado":
      casco(atras ? 9 : 4)
      if (!atras && !lado) { c.line(x + 4, y - 1, x + 10, y + 3, r[3]); c.vline(x, y + 3, 4, r[1]); c.vline(x + w - 1, y + 3, 4, r[2]) }
      if (lado) { c.rect(x + 6, y + 3, w - 6, 6, r[1]); c.vline(x + w - 1, y + 3, 6, r[2]) }
      break
    case "trenzas":
      casco(atras ? 9 : 5)
      if (!atras && !lado) { c.hline(x + 2, y + 4, 10, r[1]); for (const a of [2, 5, 8, 11]) c.px(x + a, y + 5, r[1]) }
      for (const [bx, on] of [[x - 3, !lado], [x + w, true]]) {
        if (!on) continue
        for (let i = 0; i < 9; i++) c.hline(bx, y + 5 + i, 3, i % 2 ? r[2] : r[1])
        c.hline(bx, y + 14, 3, P.moño); c.px(bx + 1, y + 15, P.moño)
      }
      c.px(x + 1, y + 2, P.moño); c.px(x + 2, y + 1, P.moño)
      break
    case "gorra": {
      const g = P.gorra
      if (!atras) { c.vline(x, y + 4, 4, r[1]); c.vline(x + w - 1, y + 4, 4, r[2]) }
      c.rect(x - 1, y - 2, w + 2, 6, g[1]); c.hline(x, y - 3, w, g[0]); c.hline(x - 1, y - 2, w + 2, g[0]); c.vline(x + w, y - 2, 6, g[2]); c.vline(x + w - 1, y - 2, 6, g[2])
      if (!atras) { c.rect(lado ? x - 3 : x, y + 3, lado ? 6 : w, 2, g[3]); c.hline(lado ? x - 3 : x, y + 3, lado ? 6 : w, g[2]) }
      else c.rect(x, y + 4, w, 5, r[1])
      break
    }
    case "paja": {
      const q = P.paja
      if (!atras) { c.vline(x, y + 4, 3, r[0]); c.vline(x + w - 1, y + 4, 3, r[1]) } else c.rect(x + 1, y + 4, w - 2, 6, r[1])
      c.rect(x + 1, y - 3, w - 2, 6, q[1]); c.hline(x + 2, y - 4, w - 4, q[0]); c.vline(x + 1, y - 3, 6, q[0]); c.vline(x + w - 2, y - 3, 6, q[2]); c.hline(x + 1, y + 1, w - 2, "#8b4a42")
      c.rect(x - 4, y + 2, w + 8, 2, q[1]); c.hline(x - 4, y + 2, w + 4, q[0]); c.hline(x - 4, y + 3, w + 8, q[2]); c.px(x - 5, y + 3, q[1]); c.px(x + w + 4, y + 3, q[2])
      for (const a of [2, 5, 8, 11]) c.px(x + a, y - 1, q[2])
      for (const a of [-3, 0, 3, 6, 9, 12, 15]) c.px(x + a, y + 3, q[3])
      break
    }
  }
}

function figura(c, P, dir, f, parp) {
  const cx = 15, bajo = P.bajo || 0, boba = f === 1 || f === 3 ? -1 : 0
  const yCab = 3 + bajo + boba, yTorso = yCab + 12
  const sup = yTorso + P.torso - 1
  if (P.peinado === "trenzas" && dir === "arriba") { /* las trenzas van detras: se pintan en pelo */ }
  piernas(c, P, cx, sup, dir, f)
  torso(c, P, cx, yTorso, dir, f)
  if (dir !== "arriba") c.rect(cx - 2, yTorso - 1, 4, 2, P.piel[2])
  const b = cabeza(c, P, cx, yCab, dir, parp)
  barba(c, P, b, dir)
  pelo(c, P, b, dir)
  return { cx, yTorso, yCab, b }
}

// ---------- Pedro: andar 4 direcciones y ataque con espada ----------
function espada(c, x0, y0, x1, y1) {
  c.line(x0, y0, x1, y1, "#d5dde0", 2); c.line(x0, y0 + 1, x1, y1 + 1, "#7f8c98")
  c.px(x1, y1, "#ffffff")
  c.rect(x0 - 1, y0 - 1, 3, 3, "#a56a3c"); c.px(x0, y0, "#e8c76f")
}
function tajo(c, puntos) { for (const [x, y] of puntos) c.px(x, y, "#fff8e8") }

const P = PERSONAJES.Pedro
const O = { w: 30, h: 46, outline: "K" }
const DIRS = { Abajo: "abajo", Arriba: "arriba", Izquierda: "izq" }
for (const [nom, d] of Object.entries(DIRS)) for (let f = 0; f < 4; f++) sprite(`Pedro_${nom}${f + 1}`, O, (c) => { figura(c, P, d, f) })
for (let f = 0; f < 4; f++) sprite(`Pedro_Derecha${f + 1}`, { ...O, flip: "x" }, (c) => { figura(c, P, "izq", f) })

const ARCO = (cx, cy, r, a, b) => { const o = []; for (let t = a; t <= b; t += 4) { const q = t * Math.PI / 180; o.push([Math.round(cx + Math.cos(q) * r), Math.round(cy + Math.sin(q) * r)]); o.push([Math.round(cx + Math.cos(q) * (r - 1)), Math.round(cy + Math.sin(q) * (r - 1))]) } return o }
sprite("Pedro_AtaqueAbajo1", O, (c) => { espada(c, 5, 25, 0, 16); figura(c, P, "abajo", 0) })
sprite("Pedro_AtaqueAbajo2", O, (c) => { figura(c, P, "abajo", 0); tajo(c, ARCO(15, 28, 14, 35, 145)); espada(c, 19, 30, 27, 36) })
sprite("Pedro_AtaqueAbajo3", O, (c) => { figura(c, P, "abajo", 0); espada(c, 24, 26, 29, 18) })
sprite("Pedro_AtaqueArriba1", O, (c) => { figura(c, P, "arriba", 0); espada(c, 24, 26, 29, 17) })
sprite("Pedro_AtaqueArriba2", O, (c) => { tajo(c, ARCO(15, 18, 14, 215, 325)); espada(c, 11, 18, 4, 8); figura(c, P, "arriba", 0) })
sprite("Pedro_AtaqueArriba3", O, (c) => { espada(c, 5, 25, 0, 16); figura(c, P, "arriba", 0) })
for (const [nom, fl] of [["Izquierda", {}], ["Derecha", { flip: "x" }]]) {
  sprite(`Pedro_Ataque${nom}1`, { ...O, ...fl }, (c) => { espada(c, 21, 24, 28, 16); figura(c, P, "izq", 0) })
  sprite(`Pedro_Ataque${nom}2`, { ...O, ...fl }, (c) => { tajo(c, ARCO(14, 27, 13, 130, 230)); figura(c, P, "izq", 0); espada(c, 8, 27, 0, 28) })
  sprite(`Pedro_Ataque${nom}3`, { ...O, ...fl }, (c) => { figura(c, P, "izq", 0); espada(c, 8, 28, 1, 33) })
}

// ---------- Vecinos: de pie y con parpadeo ----------
for (const n of ["Rosa", "Fermin", "Ramiro", "Lupita", "Tomas", "Ines", "Beto"]) {
  sprite(`${n}1`, O, (c) => { figura(c, PERSONAJES[n], "abajo", 0, false) })
  sprite(`${n}2`, O, (c) => { figura(c, PERSONAJES[n], "abajo", 0, true) })
}

// ---------- Retratos 64 x 64 (el juego los muestra a 128 x 128) ----------
const FONDO = { Ines: ["#a8b8a0", "#88a080"], Beto: ["#d8a868", "#b88850"], PedroSin: ["#7da98f", "#5f8f7a"], Hetol: ["#d9c98a", "#b8a468"], Chuchini: ["#8fb8c0", "#6f98a4"], ChuchiniViejo: ["#d8a07a", "#b87f60"], Pedro: ["#7da98f", "#5f8f7a"], Rosa: ["#d6a8b4", "#b98498"], Fermin: ["#b5835c", "#8f6246"], Ramiro: ["#8a93b8", "#6b7498"], Lupita: ["#f0c97a", "#d9a85a"], Tomas: ["#88c0cf", "#649fb2"] }
function retrato(nom, P) {
  sprite(`Retrato${nom}`, { w: 64, h: 64 }, (c) => {
    const fondo = FONDO[nom], s = P.piel, r = P.pelo, cx = 32
    c.rect(0, 0, 64, 64, fondo[1]); c.ellipse(26, 22, 32, 28, fondo[0])
    // hombros
    const anchoH = Math.round(P.ancho * 1.6) + 6, rp = P.ropa
    c.ellipse(cx, 66, anchoH, 22, rp[1]); c.ellipse(cx - 5, 67, anchoH - 8, 20, rp[0]); c.ellipse(cx + 8, 68, anchoH - 9, 19, rp[1])
    c.clip((x) => x > cx + anchoH - 9, () => c.ellipse(cx, 66, anchoH, 22, rp[2]))
    if (P.peto) { c.rect(cx - 15, 49, 5, 15, P.peto[1]); c.rect(cx + 10, 49, 5, 15, P.peto[2]); c.rect(cx - 12, 58, 24, 6, P.peto[1]); c.hline(cx - 12, 58, 24, P.peto[0]); c.rect(cx - 13, 51, 3, 3, "#e8c76f"); c.rect(cx + 11, 51, 3, 3, "#e8c76f") }
    if (P.delantal) { c.rect(cx - 15, 56, 30, 8, P.delantal[1]); c.hline(cx - 15, 56, 30, P.delantal[0]) }
    if (P.chal) { c.ellipse(cx, 56, 26, 8, P.chal[1]); c.ellipse(cx - 4, 55, 18, 5, P.chal[0]); c.poly([cx - 5, 58, cx + 5, 58, cx, 64], P.chal[2]) }
    if (P.mandil) { c.rect(cx - 14, 54, 28, 10, P.mandil[1]); c.hline(cx - 14, 54, 28, P.mandil[0]); c.line(cx - 14, 54, cx - 20, 46, P.mandil[2], 2); c.line(cx + 14, 54, cx + 20, 46, P.mandil[2], 2) }
    if (P.banda) { for (let i = 0; i < 24; i++) { c.vline(cx - 18 + i, 46 + i * 0.7, 2, "#e0c060"); c.vline(cx - 18 + i, 48 + i * 0.7, 2, "#4f7ec9"); c.vline(cx - 18 + i, 50 + i * 0.7, 2, "#c04a4a") } c.rect(cx - 3, 47, 7, 7, "#f2efe6"); c.rect(cx - 2, 48, 2, 5, "#2d3358") }
    // cuello
    c.rect(cx - 6, 40, 12, 10, s[2]); c.rect(cx - 6, 40, 5, 9, s[1])
    // cabeza con volumen
    const hx = cx, hy = 26, rx = 16, ry = 18
    c.ellipse(hx, hy, rx, ry, s[1])
    c.clip((x, y) => (x - hx) + (y - hy) * 0.7 < -6, () => { c.ellipse(hx, hy, rx, ry, s[0]) })
    c.clip((x, y) => (x - hx) * 0.9 + (y - hy) * 0.5 > 9, () => { c.ellipse(hx, hy, rx, ry, s[2]) })
    c.clip((x, y) => (x - hx) * 0.9 + (y - hy) * 0.5 > 14, () => { c.ellipse(hx, hy, rx, ry, s[3]) })
    // orejas
    c.ellipse(hx - rx, hy + 3, 2, 4, s[1]); c.ellipse(hx + rx, hy + 3, 2, 4, s[2]); c.px(hx - rx, hy + 3, s[2]); c.px(hx + rx, hy + 3, s[3])
    // ojos
    for (const [ex, tono] of [[hx - 9, s[3]], [hx + 3, s[3]]]) {
      c.rect(ex, hy + 1, 6, 5, "#fbf5ea"); c.hline(ex, hy, 6, "#3a2730"); c.hline(ex + 1, hy - 1, 4, "#3a2730")
      c.rect(ex + 2, hy + 1, 3, 4, P.ojos); c.px(ex + 2, hy + 1, "#ffffff"); c.px(ex + 3, hy + 4, "#000000")
      c.hline(ex, hy + 6, 6, tono)
    }
    // cejas, nariz, boca, rubor
    const ceja = P.barba ? P.barba[1] : P.bigote ? P.bigote[1] : r[2]
    c.rect(hx - 10, hy - 5, 8, 2, ceja); c.rect(hx + 3, hy - 5, 8, 2, ceja)
    c.px(hx, hy + 6, s[2]); c.vline(hx + 1, hy + 3, 5, s[2]); c.hline(hx - 1, hy + 8, 3, s[3]); c.px(hx - 1, hy + 7, s[0])
    c.hline(hx - 4, hy + 12, 9, "#7a3a3e"); c.hline(hx - 2, hy + 13, 5, "#c8716a")
    c.rect(hx - 13, hy + 7, 5, 2, "#e49c8a"); c.rect(hx + 8, hy + 7, 5, 2, "#d6877c")
    if (P.pecas) for (const [a, b] of [[-11, 6], [-8, 7], [-10, 8], [9, 6], [11, 7], [9, 8]]) c.px(hx + a, hy + b, s[3])
    if (P.arrugas) { c.hline(hx - 7, hy - 8, 12, s[2]); c.line(hx - 6, hy + 8, hx - 8, hy + 12, s[3]); c.line(hx + 7, hy + 8, hx + 9, hy + 12, s[3]); c.px(hx - 12, hy + 1, s[3]); c.px(hx + 11, hy + 1, s[3]) }
    if (P.lentes) { c.ring(hx - 6, hy + 3, 5, "#59606e"); c.ring(hx + 6, hy + 3, 5, "#59606e"); c.hline(hx - 1, hy + 2, 2, "#59606e"); c.px(hx - 9, hy, "#ffffff"); c.px(hx + 3, hy, "#ffffff") }
    if (P.bigote) { c.rect(hx - 9, hy + 9, 18, 3, P.bigote[1]); c.hline(hx - 8, hy + 9, 9, P.bigote[0]); c.hline(hx, hy + 11, 9, P.bigote[2]); c.rect(hx - 11, hy + 11, 3, 2, P.bigote[1]); c.rect(hx + 8, hy + 11, 3, 2, P.bigote[2]); c.hline(hx - 3, hy + 13, 6, "#7a3a3e") }
    if (P.barba) {
      const b = P.barba, larga = P.barbaForma === "larga", fin = larga ? 62 : 54
      const bajoCara = (x, y) => y > hy + 8
      c.clip(bajoCara, () => c.ellipse(hx, hy + 17, rx - 1, larga ? 19 : 12, b[1]))
      c.clip((x, y) => bajoCara(x, y) && x < hx - 2, () => c.ellipse(hx, hy + 17, rx - 1, larga ? 19 : 12, b[0]))
      c.clip((x, y) => bajoCara(x, y) && x > hx + 7, () => c.ellipse(hx, hy + 17, rx - 1, larga ? 19 : 12, b[2]))
      for (let i = -10; i <= 10; i += 4) c.line(hx + i, hy + 16, hx + i * 0.8, fin - 2, b[2])
      c.rect(hx - 8, hy + 9, 17, 3, b[0]); c.hline(hx - 3, hy + 12, 7, "#7a3a3e")
    }
    // peinados
    const melena = () => {
      c.clip((x, y) => y < hy - 7 || x < hx - rx + 2 || x > hx + rx - 2, () => c.ellipse(hx, hy - 1, rx + 2, ry + 1, r[1]))
    }
    switch (P.peinado) {
      case "revuelto":
        melena()
        for (const [x, y, l, t] of [[hx - 18, 22, 12, 1], [hx - 14, 18, 8, 0], [hx - 10, 18, 7, 1], [hx - 5, 17, 6, 2], [hx, 17, 8, 1], [hx + 5, 17, 6, 2], [hx + 10, 18, 9, 2], [hx + 14, 19, 11, 3]]) { c.rect(x, y - 2, 4, l, r[t]) }
        c.ellipse(hx - 4, 11, 11, 4, r[0]); c.ellipse(hx - 7, 9, 5, 2, "#a97745")
        // Sombrero de paja de Pedro: copa baja, ala caida y cinta azul
        if (!P.sinSombrero) { const q = ["#f7e3a4", "#e3c478", "#bd9a58", "#8d7044"]
          c.ellipse(hx, 11, 14, 9, q[1]); c.ellipse(hx - 4, 7, 8, 4, q[0]); c.clip((x) => x > hx + 7, () => c.ellipse(hx, 11, 14, 9, q[2]))
          c.rect(hx - 14, 13, 28, 3, "#2e6e7c"); c.hline(hx - 14, 13, 28, "#4c97a0")
          c.ellipse(hx, 19, 27, 5, q[1]); c.ellipse(hx - 6, 17, 20, 3, q[0]); c.hline(hx - 26, 21, 52, q[2]); c.hline(hx - 22, 23, 44, q[3])
          for (let x = hx - 24; x < hx + 24; x += 5) c.line(x, 15, x + 1, 21, q[2])
          for (let x = hx - 10; x < hx + 11; x += 4) c.line(x, 5, x, 11, q[2]) }
        break
      case "mono":
        melena(); c.ellipse(hx, 5, 9, 6, r[1]); c.ellipse(hx - 2, 3, 6, 3, r[0]); c.hline(hx - 7, 9, 15, r[2])
        for (const x of [-11, -6, 0, 6, 11]) c.line(hx + x * 0.3, 10, hx + x, 18, r[2])
        break
      case "peinado":
        melena(); c.ellipse(hx - 3, 10, 13, 5, r[0]); c.line(hx + 6, 8, hx + 12, 18, r[3], 2); c.rect(hx - 18, 22, 3, 12, r[1]); c.rect(hx + 15, 22, 3, 12, r[2])
        break
      case "trenzas":
        melena(); c.ellipse(hx - 3, 11, 12, 4, r[0]); c.vline(hx, 8, 12, r[3])
        for (const [bx, t] of [[hx - 24, 1], [hx + 18, 2]]) { for (let i = 0; i < 26; i += 4) { c.ellipse(bx + 3, 22 + i, 4, 2, r[t]); c.hline(bx, 23 + i, 7, r[3]) } c.rect(bx, 47, 7, 4, P.moño); c.px(bx + 1, 48, "#ffffff") }
        c.rect(hx - 20, 13, 6, 5, P.moño); c.rect(hx + 14, 13, 6, 5, P.moño); c.px(hx - 18, 14, "#ffffff")
        break
      case "gorra": {
        const g = P.gorra
        c.rect(hx - 18, 22, 3, 8, r[1]); c.rect(hx + 15, 22, 3, 8, r[2])
        c.ellipse(hx, 12, rx + 3, 10, g[1]); c.ellipse(hx - 4, 9, 12, 5, g[0]); c.clip((x) => x > hx + 8, () => c.ellipse(hx, 12, rx + 3, 10, g[2]))
        c.rect(hx - 19, 15, 38, 5, g[2]); c.hline(hx - 19, 15, 38, g[1]); c.hline(hx - 19, 19, 38, g[3])
        break
      }
      case "paja": {
        const q = P.paja
        c.rect(hx - 17, 21, 3, 8, r[0]); c.rect(hx + 14, 21, 3, 8, r[1])
        c.ellipse(hx, 13, 15, 10, q[1]); c.ellipse(hx - 4, 9, 9, 5, q[0]); c.rect(hx - 15, 15, 30, 3, "#8b4a42")
        c.ellipse(hx, 19, 28, 5, q[1]); c.ellipse(hx - 6, 18, 20, 3, q[0]); c.hline(hx - 27, 22, 54, q[2])
        for (let x = hx - 24; x < hx + 24; x += 5) c.line(x, 16, x + 1, 21, q[2])
        for (let x = hx - 11; x < hx + 11; x += 4) c.line(x, 6, x, 13, q[2])
        break
      }
    }
  })
}
for (const [n, p] of Object.entries(PERSONAJES)) retrato(n, p)

// ---------- Papa radiactiva: enemiga con grietas verdes que brillan ----------
const PAP = ["#e0b98a", "#c49565", "#99704e", "#6e4d3e", "#4b3430"]
const NUC = ["#e7ff9c", "#a8ec4a", "#5aa83c"]
function papa(c, dir, f) {
  const bob = f === 1 || f === 3 ? -1 : 0, cy = 16 + bob, pata = (x, up) => { c.rect(x, 25 - up, 5, 3 + up - (up ? 1 : 0), PAP[3]); c.hline(x, 27 - (up ? 1 : 0), 5, PAP[4]) }
  pata(7, f === 1 ? 2 : 0); pata(18, f === 3 ? 2 : 0)
  c.ellipse(15, cy, 13, 11, PAP[2])
  c.clip((x, y) => (x - 15) * 0.7 + (y - cy) < 2, () => c.ellipse(15, cy, 13, 11, PAP[1]))
  c.clip((x, y) => (x - 15) * 0.7 + (y - cy) < -7, () => c.ellipse(15, cy, 13, 11, PAP[0]))
  c.clip((x, y) => (x - 15) * 0.7 + (y - cy) > 8, () => c.ellipse(15, cy, 13, 11, PAP[3]))
  for (const [x, y] of [[6, cy - 3], [23, cy - 4], [21, cy + 6], [8, cy + 6]]) { c.rect(x, y, 3, 2, PAP[3]); c.hline(x, y + 2, 3, PAP[1]) }
  // grietas de radiacion
  c.line(9, cy - 9, 13, cy - 5, NUC[2]); c.line(13, cy - 5, 12, cy - 2, NUC[1]); c.px(12, cy - 5, NUC[0])
  c.vline(14, cy - 13, 3, "#5a8a3c"); c.px(13, cy - 13, "#7fb04a"); c.px(15, cy - 14, "#a8d05a"); c.px(16, cy - 13, "#7fb04a")
  if (dir === "arriba") { c.line(18, cy - 4, 21, cy + 2, NUC[2]); c.px(20, cy, NUC[1]); return }
  const ojo = (x) => { c.rect(x, cy - 1, 4, 4, "#fff8d0"); c.rect(x + 1, cy, 2, 3, "#22202a"); c.px(x + 1, cy, NUC[0]); c.line(x - 1, cy - 2, x + 4, cy - 1, PAP[4]) }
  if (dir === "izq") { ojo(6); c.hline(5, cy + 6, 7, PAP[4]); c.px(6, cy + 5, "#fff8d0"); c.px(9, cy + 5, "#fff8d0") }
  else { ojo(9); ojo(17); c.hline(11, cy + 6, 9, PAP[4]); for (const x of [12, 15, 18]) c.px(x, cy + 5, "#fff8d0") }
}
const OP = { w: 30, h: 30, outline: "K" }
for (let f = 0; f < 4; f++) {
  sprite(`Papa_Abajo${f + 1}`, OP, (c) => papa(c, "abajo", f))
  sprite(`Papa_Arriba${f + 1}`, OP, (c) => papa(c, "arriba", f))
  sprite(`Papa_Izquierda${f + 1}`, OP, (c) => papa(c, "izq", f))
  sprite(`Papa_Derecha${f + 1}`, { ...OP, flip: "x" }, (c) => papa(c, "izq", f))
}

// ---------- Cultivos en 4 etapas (32 x 32): brote, joven, crecido, maduro ----------
const V = ["#2c5540", "#3a6e45", "#4f8a49", "#6ea552", "#93bf60"]
function hojas(c, cx, base, alto, abre, tonos = V) {
  for (let i = 0; i < alto; i++) c.px(cx, base - i, tonos[1])
  for (let k = 1; k <= abre; k++) {
    const y = base - Math.round(alto * k / (abre + 1))
    for (const s of [-1, 1]) {
      const l = 2 + (abre - k)
      for (let j = 1; j <= l; j++) { c.px(cx + s * j, y - Math.floor(j / 2), j === l ? tonos[3] : tonos[2]); c.px(cx + s * j, y - Math.floor(j / 2) + 1, tonos[s > 0 ? 0 : 1]) }
    }
  }
  c.px(cx, base - alto, tonos[4])
}
const OC = { w: 30, h: 30, outline: "#1f2e30" }
const MUT = ["#2a4f3a", "#3e7a42", "#71b444", "#b4e65a", "#e7ff9c"]
function monticulo(c, cx, b) { c.ellipse(cx, b, 5, 2, "#5e4438"); c.hline(cx - 3, b - 1, 5, "#7a5a45") }
sprite("Zanahoria_0", OC, (c) => { monticulo(c, 15, 26); hojas(c, 15, 25, 4, 1) })
sprite("Zanahoria_1", OC, (c) => { monticulo(c, 15, 26); for (const d of [-2, 2]) hojas(c, 15 + d, 25, 7, 2); hojas(c, 15, 25, 9, 2) })
sprite("Zanahoria_2", OC, (c) => { monticulo(c, 15, 26); for (const d of [-5, -2, 2, 5]) hojas(c, 15 + d, 25, 11 - Math.abs(d), 2); hojas(c, 15, 25, 14, 3) })
sprite("Zanahoria_3", OC, (c) => {
  monticulo(c, 15, 27); for (const d of [-6, -3, 3, 6]) hojas(c, 15 + d, 21, 13 - Math.abs(d), 3); hojas(c, 15, 21, 15, 3)
  c.rect(11, 20, 9, 5, "#e0883f"); c.hline(11, 20, 9, "#f4ae62"); c.vline(19, 20, 5, "#b9602f"); c.hline(13, 25, 5, "#b9602f"); c.px(14, 22, "#b9602f"); c.px(16, 23, "#b9602f")
})
function planta(c, tonos, etapa, fruto) {
  monticulo(c, 15, 26)
  if (etapa === 0) { hojas(c, 15, 25, 4, 1, tonos); return }
  if (etapa === 1) { hojas(c, 12, 25, 6, 2, tonos); hojas(c, 18, 25, 6, 2, tonos); hojas(c, 15, 25, 9, 2, tonos); return }
  c.ellipse(15, 16, 11, 9, tonos[1])
  c.clip((x, y) => (x - 15) + (y - 16) < 2, () => c.ellipse(15, 16, 11, 9, tonos[2]))
  c.clip((x, y) => (x - 15) + (y - 16) < -7, () => c.ellipse(15, 16, 11, 9, tonos[3]))
  for (const [x, y] of [[8, 12], [14, 8], [20, 12], [11, 18], [18, 18], [15, 14]]) { c.rect(x, y, 3, 2, tonos[3]); c.px(x, y, tonos[4]); c.hline(x, y + 2, 3, tonos[0]) }
  for (const x of [11, 15, 19]) c.vline(x, 24, 2, tonos[1])
  if (etapa === 3) for (const [x, y] of fruto) { c.rect(x, y, 4, 3, "#c49565"); c.hline(x, y, 4, "#e0b98a"); c.hline(x, y + 2, 4, "#7a5a45") }
}
const FR = [[6, 22], [13, 23], [20, 22]]
for (let i = 0; i < 4; i++) {
  sprite(`Papa_${i}`, OC, (c) => planta(c, V, i, FR))
  sprite(`PapaMutante_${i}`, OC, (c) => {
    planta(c, MUT, i, FR)
    if (i >= 2) for (const [x, y] of [[9, 10], [20, 14], [14, 18]]) { c.px(x, y, "#f7ffc4"); c.px(x + 1, y, MUT[3]); c.px(x, y + 1, MUT[3]) }
    if (i === 3) for (const [x, y] of FR) { c.px(x + 1, y + 1, NUC[1]); c.px(x + 2, y + 1, NUC[0]) }
  })
}

// ---------- Casa de campo (128 x 128): tejas en hileras, muro con vigas, zocalo de piedra ----------
const TEJA = ["#d9775a", "#b85a4a", "#93433f", "#6e3236"], MURO = ["#efe2c4", "#d9c8a4", "#b8a688", "#8f7f6c"]
const VIGA = ["#7c5a44", "#5e4336", "#452f2b"], PIEDRA = ["#a39b8b", "#847e72", "#62605a"]
function tejado(c, x0, y0, w, h) {
  for (let y = 0; y < h; y++) {
    const fila = Math.floor(y / 6), ox = fila % 2 ? 4 : 0
    for (let x = 0; x < w; x++) {
      const p = (x + ox) % 8, q = y % 6
      let k = q === 5 ? 3 : q === 4 ? 2 : p === 7 ? 2 : q === 0 ? 0 : 1
      const luz = x / w
      if (luz > 0.72 && k < 3) k++
      if (luz < 0.18 && k > 0 && q !== 5) k--
      c.px(x0 + x, y0 + y, TEJA[k])
    }
  }
}
function casita(c) {
  // tejado
  tejado(c, 8, 16, 110, 46)
  c.hline(8, 16, 110, TEJA[0]); c.hline(8, 62, 110, TEJA[3]); c.hline(8, 63, 110, "#3f2a2c")
  // chimenea
  c.rect(92, 8, 13, 12, PIEDRA[1]); c.vline(92, 8, 12, PIEDRA[0]); c.vline(104, 8, 12, PIEDRA[2]); c.hline(90, 8, 17, PIEDRA[0]); c.hline(90, 9, 17, PIEDRA[2])
  for (const [x, y] of [[95, 12], [99, 15]]) c.hline(x, y, 5, PIEDRA[2])
  // muro
  c.rect(12, 64, 102, 30, MURO[1]); c.vline(12, 64, 30, MURO[0]); c.rect(106, 64, 8, 30, MURO[2]); c.hline(12, 64, 102, MURO[3]); c.hline(12, 65, 102, MURO[3])
  for (const [x, y, l] of [[20, 74, 6], [72, 72, 8], [96, 84, 5], [66, 86, 4]]) c.hline(x, y, l, MURO[2])
  for (const x of [12, 36, 66, 110]) { c.rect(x, 64, 4, 30, VIGA[1]); c.vline(x, 64, 30, VIGA[0]); c.vline(x + 3, 64, 30, VIGA[2]) }
  c.rect(12, 92, 102, 2, VIGA[2])
  // zocalo de piedra
  c.rect(10, 94, 106, 12, PIEDRA[1]); c.hline(10, 94, 106, PIEDRA[0]); c.hline(10, 105, 106, PIEDRA[2])
  for (let f = 0; f < 3; f++) for (let x = 10 + (f % 2) * 5; x < 112; x += 11) { c.vline(x, 95 + f * 3, 3, PIEDRA[2]); c.hline(x, 97 + f * 3, Math.min(10, 115 - x), PIEDRA[2]); c.px(x + 1, 95 + f * 3, PIEDRA[0]) }
  for (const [x, y] of [[14, 104], [58, 104], [112, 104]]) { c.hline(x, y, 4, "#5e7046"); c.px(x + 1, y - 1, "#7d9458") }
  // puerta (misma zona que la casa vieja)
  c.rect(42, 70, 20, 36, VIGA[2]); c.rect(44, 72, 16, 34, "#7a4a34"); c.vline(44, 72, 34, "#9a6243"); c.vline(52, 72, 34, "#5c3729"); c.vline(59, 72, 34, "#5c3729")
  c.hline(44, 80, 16, "#5c3729"); c.hline(44, 96, 16, "#5c3729"); c.rect(56, 88, 2, 3, "#e8c76f")
  c.rect(38, 66, 28, 4, TEJA[1]); c.hline(38, 66, 28, TEJA[0]); c.hline(38, 69, 28, TEJA[3])
  // ventana con jardinera
  c.rect(76, 70, 22, 16, VIGA[2]); c.rect(78, 72, 18, 12, "#6fa8b0"); c.poly([78, 72, 88, 72, 78, 82], "#a8d3cf"); c.px(81, 74, "#e8f4e8"); c.vline(87, 72, 12, VIGA[1]); c.hline(78, 78, 18, VIGA[1])
  c.rect(74, 86, 26, 4, VIGA[1]); c.hline(74, 86, 26, VIGA[0])
  for (const [x, col] of [[76, "#e88fa8"], [80, "#f0d268"], [84, "#e88fa8"], [88, "#fff4d2"], [92, "#f0d268"], [96, "#e88fa8"]]) { c.px(x, 84, "#4f8a49"); c.px(x + 1, 85, "#3a6e45"); c.px(x, 83, col); c.px(x + 1, 84, col) }
  c.rect(16, 74, 14, 14, VIGA[2]); c.rect(18, 76, 10, 10, "#6fa8b0"); c.poly([18, 76, 24, 76, 18, 82], "#a8d3cf"); c.vline(22, 76, 10, VIGA[1])
}
sprite("Casa", { w: 126, h: 126, outline: "K" }, casita)

// ---------- Granero (128 x 112): madera vertical con vetas, tejado oscuro, puerta en cruz ----------
const TABLA = ["#c0564c", "#a33f40", "#7f3036", "#5d262d"], BLANCO = ["#f2e9d6", "#d4c9b4", "#a89e8e"], PIZARRA = ["#6a6a78", "#4f4f60", "#3a3a4c", "#2a2a3a"]
sprite("Granero", { w: 128, h: 112, outline: "K" }, (c) => {
  c.poly([2, 42, 64, 1, 126, 42], PIZARRA[1])
  c.clip((x, y) => x < 64, () => c.poly([2, 42, 64, 1, 126, 42], PIZARRA[0]))
  for (let y = 7; y < 42; y += 5) { c.hline(0, y, 128, ".");
    const m = Math.round((y - 1) * 62 / 41)
    c.hline(64 - m, y, m * 2, PIZARRA[2])
  }
  c.line(2, 42, 64, 1, PIZARRA[3]); c.line(64, 1, 126, 42, PIZARRA[3])
  c.rect(8, 42, 112, 62, TABLA[1])
  for (let x = 8; x < 120; x += 7) { c.vline(x, 42, 62, TABLA[3]); c.vline(x + 1, 42, 62, TABLA[0]); c.vline(x + 5, 42, 62, TABLA[2]) ; c.px(x + 3, 50 + (x * 7) % 40, TABLA[2]); c.vline(x + 2, 60 + (x * 3) % 30, 4, TABLA[2]) }
  c.rect(96, 42, 24, 62, TABLA[2]); for (let x = 99; x < 120; x += 7) c.vline(x, 42, 62, TABLA[3])
  c.hline(8, 42, 112, TABLA[3]); c.hline(8, 43, 112, TABLA[3])
  // puerta
  c.rect(40, 58, 48, 46, BLANCO[1]); c.rect(44, 62, 19, 42, TABLA[1]); c.rect(65, 62, 19, 42, TABLA[2])
  for (const x of [44, 65]) { c.line(x, 62, x + 18, 103, BLANCO[1], 2); c.line(x + 18, 62, x, 103, BLANCO[1], 2) }
  c.vline(40, 58, 46, BLANCO[0]); c.hline(40, 58, 48, BLANCO[0]); c.vline(87, 58, 46, BLANCO[2]); c.vline(63, 62, 42, BLANCO[2]); c.vline(64, 62, 42, BLANCO[1])
  // ventanas y heno arriba
  for (const x of [14, 100]) { c.rect(x, 68, 16, 14, BLANCO[1]); c.rect(x + 2, 70, 12, 10, "#6fa8b0"); c.poly([x + 2, 70, x + 9, 70, x + 2, 77], "#a8d3cf"); c.vline(x + 8, 70, 10, BLANCO[1]) }
  c.rect(54, 20, 20, 18, BLANCO[1]); c.rect(56, 22, 16, 16, "#3f2a2c"); c.rect(56, 32, 16, 6, "#d6b367"); c.hline(56, 32, 16, "#f0d893"); for (const x of [58, 62, 67]) c.vline(x, 30, 3, "#d6b367")
  // zocalo
  c.rect(4, 104, 120, 8, PIEDRA[1]); c.hline(4, 104, 120, PIEDRA[0]); c.hline(4, 111, 120, PIEDRA[2])
  for (let x = 8; x < 124; x += 12) c.vline(x, 105, 6, PIEDRA[2])
})

// ---------- Regadera (icono 32 x 32) y barra de energia ----------
sprite("Regadera", { w: 30, h: 30, outline: "K" }, (c) => {
  const M = ["#d7e4ea", "#a9bcc8", "#7c8fa2", "#566a80"]
  c.ellipse(9, 7, 6, 5, ".", true); c.ellipse(9, 7, 6, 5, M[2], true); c.ellipse(9, 7, 5, 4, M[3], true)
  c.rect(6, 12, 16, 14, M[1]); c.vline(6, 12, 14, M[0]); c.vline(7, 12, 14, M[0]); c.rect(19, 12, 3, 14, M[3]); c.hline(6, 12, 16, M[0]); c.hline(6, 25, 16, M[3]); c.hline(6, 18, 16, M[2])
  c.line(22, 20, 28, 12, M[2], 2); c.rect(26, 9, 4, 3, M[0]); c.hline(26, 11, 4, M[3])
  for (const [x, y] of [[28, 15], [26, 18], [29, 20]]) c.px(x, y, "#7fd0e0")
})
sprite("EnergiaMarco", { w: 18, h: 106, outline: "K" }, (c) => {
  const W = ["#c79a68", "#9a6d48", "#6f4b35"]
  c.rect(0, 0, 18, 106, W[1]); c.vline(0, 0, 106, W[0]); c.hline(0, 0, 18, W[0]); c.vline(17, 0, 106, W[2]); c.hline(0, 105, 18, W[2]); c.rect(3, 3, 12, 88, "#3a2830")
  c.rect(3, 93, 12, 11, W[2]); c.poly([10, 94, 5, 99, 8, 99, 7, 103, 13, 97, 10, 97], "#f4d36a")
})
sprite("EnergiaRelleno", { w: 12, h: 88 }, (c) => { c.rect(0, 0, 12, 88, "#ffffff"); c.vline(0, 0, 88, "#ffffff"); c.rect(9, 0, 3, 88, "#c9c9c9"); c.hline(0, 0, 12, "#ffffff") })

// ---------- Niños de la historia, de pie ----------
const NINOS = {
  Hija: { piel: PIEL.clara, pelo: T("#b8824a", "#946636", "#6f4a2a", "#4e3320"), peinado: "trenzas", bajo: 13, ancho: 10, torso: 9, ropa: T("#e88fa8", "#c5688a", "#9a4f70", "#73405a"), brazo: "corto",
    falda: T("#e88fa8", "#c5688a", "#9a4f70", "#73405a"), piernaDesnuda: true, zapato: T("#8d6345", "#6c4733", "#4f3329", "#3a2622"), moño: "#fff4d2", ojos: "#2c2230", pecas: true },
  Hijo: { piel: PIEL.clara, pelo: T("#8a5a34", "#6b4026", "#4e2c1f", "#35201c"), peinado: "revuelto", sinSombrero: true, bajo: 15, ancho: 11, torso: 9, ropa: T("#8fb8d0", "#6a94b0", "#4f7690", "#3a5a70"), brazo: "corto",
    pierna: T("#8a6e54", "#6a5240", "#4f3c30", "#382a24"), zapato: T("#6c4733", "#4f3329", "#3a2622", "#2a1f22"), ojos: "#2c2230" },
  PedroNino: { piel: PIEL.clara, pelo: T("#8a5a34", "#6b4026", "#4e2c1f", "#35201c"), peinado: "revuelto", sinSombrero: true, bajo: 15, ancho: 11, torso: 9, ropa: T("#d65a4a", "#b23c3c", "#842c37", "#5e2230"), brazo: "corto",
    pierna: T("#5aa6ad", "#3d8390", "#2e6476", "#23495c"), zapato: T("#8d6345", "#6c4733", "#4f3329", "#3a2622"), ojos: "#3f2a22" },
}
for (const [n, p] of Object.entries(NINOS)) { sprite(`Actor_${n}_Frente1`, O, (c) => { figura(c, p, "abajo", 0, false) }); sprite(`Actor_${n}_Frente2`, O, (c) => { figura(c, p, "abajo", 0, true) }) }

// ---------- Vecinos caminando para sus rutinas ----------
for (const n of ["Rosa", "Fermin", "Ramiro", "Lupita", "Tomas", "Ines", "Beto"]) for (let f = 0; f < 4; f++) {
  const P_ = PERSONAJES[n]
  sprite(`Vecino_${n}_Abajo${f + 1}`, O, (c) => { figura(c, P_, "abajo", f) })
  sprite(`Vecino_${n}_Arriba${f + 1}`, O, (c) => { figura(c, P_, "arriba", f) })
  sprite(`Vecino_${n}_Izquierda${f + 1}`, O, (c) => { figura(c, P_, "izq", f) })
  sprite(`Vecino_${n}_Derecha${f + 1}`, { ...O, flip: "x" }, (c) => { figura(c, P_, "izq", f) })
}
