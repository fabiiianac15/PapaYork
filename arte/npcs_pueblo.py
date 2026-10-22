"""Vecinos nuevos del pueblo (desde el sprite de Pedro) con su retrato para la caja de dialogo.
Salida: Pueblo/<Nombre>1.png, Pueblo/<Nombre>2.png (parpadeo) e Intro/Retrato<Nombre>HD.png (128x128)."""
from PIL import Image
import os
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
base = Image.open(os.path.join(B, "assets/NewSprite13.png")).convert("RGBA")
H = lambda s: tuple(int(s[i:i + 2], 16) for i in (1, 3, 5)) + (255,)
PELO, PELO_OSC, PIEL = H("#46200a"), H("#311200"), H("#e3bc9a")
CAM_OSC, CAM, OVER_OSC, OVER, CONT = H("#560505"), H("#ad0a0a"), H("#048288"), H("#07d4de"), H("#3a3434")
def recolor(img, m):
    img = img.copy(); px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            if px[x, y] in m: px[x, y] = m[px[x, y]]
    return img
def dibujar(img, filas, x0, y0, col):
    px = img.load()
    for y, fila in enumerate(filas):
        for i, ch in enumerate(fila):
            if ch != ".": px[x0 + i, y0 + y] = (0, 0, 0, 0) if ch == "_" else col[ch]
def parpadeo(img):
    img = img.copy(); px = img.load()
    for x in (12, 13, 19, 20):
        px[x, 12] = PIEL
        if px[x, 14] == CONT: px[x, 14] = PIEL
    for x in (11, 12, 13, 19, 20, 21): px[x, 13] = CONT
    return img
def retrato(img, claro, oscuro, nombre):
    r = Image.new("RGBA", (64, 64), H(oscuro)); px = r.load()
    for y in range(64):
        for x in range(64):
            if (x - 32) ** 2 + (y - 60) ** 2 < 40 ** 2 or ((x - 32) ** 2 + (y - 60) ** 2 < 46 ** 2 and (x + y) % 2 == 0): px[x, y] = H(claro)
    r.alpha_composite(img.crop((6, 0, 27, 21)).resize((63, 63), Image.NEAREST), (1, 6))
    r.resize((128, 128), Image.NEAREST).save(os.path.join(B, "Intro/Retrato%sHD.png" % nombre))
def guardar(nombre, img, claro, oscuro):
    img.save(os.path.join(B, "Pueblo/%s1.png" % nombre)); parpadeo(img).save(os.path.join(B, "Pueblo/%s2.png" % nombre))
    retrato(img, claro, oscuro, nombre)

# Alcalde Ramiro: pelo gris peinado, bigote, traje azul oscuro con banda tricolor
ram = recolor(base, {PELO: H("#9badb7"), PELO_OSC: H("#696a6a"), CAM_OSC: H("#222034"), CAM: H("#3f3f74"), OVER_OSC: H("#222034"), OVER: H("#3f3f74")})
dibujar(ram, [".aaaa.aaaa.", "abbbbabbbba"], 11, 14, {"a": CONT, "b": H("#696a6a")})
for i, col in enumerate(("#fbf236", "#5b6ee1", "#ac3232")):
    for k in range(5): ram.load()[11 + k + i, 18 + k] = H(col)
guardar("Ramiro", ram, "#9badb7", "#3f3f74")

# Lupita: trenzas negras, vestido amarillo
lup = recolor(base, {PELO: H("#222034"), PELO_OSC: H("#000000"), CAM_OSC: H("#8a6f30"), CAM: H("#fbf236"), OVER_OSC: H("#df7126"), OVER: H("#fbf236")})
dibujar(lup, ["aa", "bb", "ab", "bb", "aa", "xx"], 6, 12, {"a": CONT, "b": H("#222034"), "x": H("#d95763")})
dibujar(lup, ["aa", "bb", "ba", "bb", "aa", "xx"], 25, 12, {"a": CONT, "b": H("#222034"), "x": H("#d95763")})
guardar("Lupita", lup, "#fbf236", "#df7126")

# Abuelo Tomas: sombrero de paja, barba blanca corta, camisa azul de pescador
tom = recolor(base, {PELO: H("#e8e8ee"), PELO_OSC: H("#b0b0bc"), CAM_OSC: H("#306082"), CAM: H("#639bff"), OVER_OSC: H("#4a2a17"), OVER: H("#8f563b")})
dibujar(tom, ["....aaaaaaaaaa....", "...aTTTTTTTTTTa...", "..aTTTTTTTTTTTTa..", "aaaTTTtTTTTtTTTTaaa", "aTTTTTTTTTTTTTTTTTa", "aaaaaaaaaaaaaaaaaaa"], 7, 0,
        {"a": CONT, "T": H("#eec39a"), "t": H("#d9a066")})
dibujar(tom, [".aaaaaaa.", "awwwwwwwa", ".awwwwwa."], 12, 15, {"a": CONT, "w": H("#ffffff")})
guardar("Tomas", tom, "#5fcde4", "#306082")
print("ok")
