"""Personajes de la introduccion y retratos para la caja de dialogo, hechos a partir del sprite de Pedro
(assets/NewSprite13.png) para que tengan las mismas proporciones, contorno y piel.
Salida: Intro/<Nombre>.png (sprite 32x32) y Intro/Retrato<Nombre>.png (retrato 64x64 a escala de juego)."""
from PIL import Image
import os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
base = Image.open(os.path.join(B, "assets/NewSprite13.png")).convert("RGBA")
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
PELO, PELO_OSC, PIEL, MEJ = H("#46200a"), H("#311200"), H("#e3bc9a"), H("#e3775a")
CAM_OSC, CAM, OVER_OSC, OVER, CONT = H("#560505"), H("#ad0a0a"), H("#048288"), H("#07d4de"), H("#3a3434")
def recolor(img, m):
    img = img.copy(); px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y] in m: px[x, y] = m[px[x, y]]
    return img
def dibujar(img, filas, x0, y0, colores):
    px = img.load()
    for y, fila in enumerate(filas):
        for i, ch in enumerate(fila):
            if ch != ".": px[x0 + i, y0 + y] = (0, 0, 0, 0) if ch == "_" else colores[ch]
def bigote(img, color, sombra):
    dibujar(img, [".aaaa.aaaa.", "abbbbabbbba", "abb.....bba"], 11, 14, {"a": CONT, "b": color})
    px = img.load(); px[16, 15] = sombra

# HetolMimiao, 1847: pelo y bigote blancos, sombrero de copa, levita cafe con botones dorados
hetol = recolor(base, {PELO: H("#e8e8ee"), PELO_OSC: H("#b0b0bc"), CAM_OSC: H("#4a2a17"), CAM: H("#6e4024"),
                       OVER_OSC: H("#222034"), OVER: H("#3f3f74")})
dibujar(hetol, ["_______________", "....aaaaaaa....", "....akkkkka.....", "....akkkkka.....", "....akkkkka.....",
                "....arrrrra.....", "..aaakkkkkaaa...", "..akkkkkkkkka..."], 9, 0,
        {"a": CONT, "k": H("#1b1630"), "r": H("#ac3232")})
for y in range(0, 3):
    for x in range(8, 25):
        if y < 1: hetol.load()[x, y] = (0, 0, 0, 0)
bigote(hetol, H("#ffffff"), H("#cbdbfc"))
for (x, y) in [(15, 20), (15, 22), (17, 20), (17, 22)]: hetol.load()[x, y] = H("#fbf236")
hetol.save(os.path.join(B, "Intro/Hetol.png"))

# Chuchini Gutierrez: pelo negro, bigote, gorra verde, camisa amarilla y overol azul
chu = recolor(base, {PELO: H("#1b1630"), PELO_OSC: H("#0d0b18"), CAM_OSC: H("#8a6f30"), CAM: H("#fbf236"),
                     OVER_OSC: H("#306082"), OVER: H("#5b6ee1")})
dibujar(chu, [".....aaaaaaaa.....", "...aaggggggggaa...", "..agggggggggggga..", ".aggggwgggggggggaa", "aaaaaaaaaaaaaaaaaa"], 7, 2,
        {"a": CONT, "g": H("#37946e"), "w": H("#6abe30")})
bigote(chu, H("#1b1630"), H("#45283c"))
chu.save(os.path.join(B, "Intro/Chuchini.png"))
viejo = recolor(chu, {H("#1b1630"): H("#c2c3c7"), H("#0d0b18"): H("#8b8d96"), H("#45283c"): H("#9badb7")})
viejo.save(os.path.join(B, "Intro/ChuchiniViejo.png"))

# Hijos de HetolMimiao (1847): nina con trenzas y nino, ropa de epoca
nina = recolor(base, {PELO: H("#8a6f30"), PELO_OSC: H("#663931"), CAM_OSC: H("#76428a"), CAM: H("#d77bba"),
                      OVER_OSC: H("#76428a"), OVER: H("#d77bba")})
dibujar(nina, ["aa", "bb", "ab", "bb", "aa"], 6, 12, {"a": CONT, "b": H("#8a6f30")})
dibujar(nina, ["aa", "bb", "ba", "bb", "aa"], 25, 12, {"a": CONT, "b": H("#8a6f30")})
nina.save(os.path.join(B, "Intro/Hija.png"))
nino = recolor(base, {PELO: H("#663931"), PELO_OSC: H("#45283c"), CAM_OSC: H("#4b692f"), CAM: H("#8f974a"),
                      OVER_OSC: H("#4a2a17"), OVER: H("#8f563b")})
nino.save(os.path.join(B, "Intro/Hijo.png"))

# Retratos: cara recortada (filas 0-19) ampliada x3 sobre un fondo de color, 64x64 a escala de juego
FONDOS = {"Pedro": ("#5fcde4", "#306082"), "Hetol": ("#d9a066", "#8a6f30"), "Chuchini": ("#99e550", "#4b692f"),
          "ChuchiniViejo": ("#d77bba", "#76428a"), "Rosa": ("#d77bba", "#76428a"), "Fermin": ("#df7126", "#8f563b")}
FUENTES = {"Pedro": base, "Hetol": hetol, "Chuchini": chu, "ChuchiniViejo": viejo,
           "Rosa": Image.open(os.path.join(B, "Pueblo/Rosa1.png")).convert("RGBA"),
           "Fermin": Image.open(os.path.join(B, "Pueblo/Fermin1.png")).convert("RGBA")}
for nombre, img in FUENTES.items():
    claro, oscuro = FONDOS[nombre]
    r = Image.new("RGBA", (64, 64), H(oscuro)); px = r.load()
    for y in range(64):
        for x in range(64):
            if (x - 32) ** 2 + (y - 60) ** 2 < 46 ** 2 and (x + y) % 2 == 0 or (x - 32) ** 2 + (y - 60) ** 2 < 40 ** 2: px[x, y] = H(claro)
    cara = img.crop((6, 0, 27, 21)).resize((63, 63), Image.NEAREST)
    r.alpha_composite(cara, (1, 6))
    r.save(os.path.join(B, "Intro/Retrato%s.png" % nombre))
print("ok")
