"""Genera iconos de 16x16 para la barra rapida a partir de los iconos de 32x32 de IconoItem.

Reduce a la mitad eligiendo, en cada bloque de 2x2, el color que mas se repite; si el bloque toca el borde del
dibujo usa el pixel mas oscuro para conservar el contorno. Uso: python3 arte/iconos_mini.py proyecto.json
"""
import json, sys, os
from PIL import Image
from collections import Counter
P = sys.argv[1]
base = os.path.dirname(os.path.abspath(P))
d = json.load(open(P, encoding="utf8"))
res = {r["name"]: r["file"] for r in d["resources"]["resources"]}
ico = next(o for o in d["objects"] if o["name"] == "IconoItem")
def lum(c): return 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]
hechos = []
for a in ico["animations"]:
    if a["name"].endswith("_mini"): continue
    img = Image.open(os.path.join(base, res[a["directions"][0]["sprites"][0]["image"]])).convert("RGBA")
    # recortar al dibujo y llevarlo a un cuadrado de 32 centrado
    bb = img.getbbox(); img = img.crop(bb)
    lado = max(img.size, 32) if isinstance(img.size, int) else max(max(img.size), 32)
    lienzo = Image.new("RGBA", (lado + lado % 2, lado + lado % 2)); lienzo.alpha_composite(img, ((lienzo.width - img.width) // 2, (lienzo.height - img.height) // 2))
    if lienzo.width > 32: lienzo = lienzo.resize((32, 32), Image.NEAREST)
    src = lienzo.load(); out = Image.new("RGBA", (16, 16)); dst = out.load()
    for y in range(16):
        for x in range(16):
            px = [src[2 * x + i, 2 * y + j] for j in (0, 1) for i in (0, 1)]
            op = [p for p in px if p[3] > 100]
            if len(op) < 2: continue
            borde = len(op) < 4
            elegido = min(op, key=lum) if borde else Counter(p[:3] for p in op).most_common(1)[0][0] + (255,)
            dst[x, y] = elegido[:3] + (255,)
    nombre = "Mini/" + a["name"].replace(" ", "_") + ".png"
    out.save(os.path.join(base, nombre)); hechos.append((a["name"], nombre))
json.dump(hechos, open(os.path.join(base, "Mini/lista.json"), "w"), ensure_ascii=False)
print(len(hechos), "iconos")
