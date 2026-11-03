"""Prueba temporal: la tecla Z cambia el zoom de las capas del mundo entre 2 y 1.

Solo afecta a Nivel 01, Nivel 02 y Pueblo, y solo a las capas "" y "Luz Exterior".
El zoom elegido no se guarda en la partida: al abrir el juego vuelve a ser 2.
Para quitar la prueba, restaurar Legado Radioactivo-Papayork.respaldo-antes-12.json
si no hubo cambios después, o borrar el enlace "PruebaZoom" de cada escena.
"""
import json, sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from gdutil import *

P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))

if any(e["name"] == "PruebaZoom" for e in d["externalEvents"]):
    sys.exit("La prueba de zoom ya está aplicada; no se cambió nada.")

set_global_var(d, var("ZoomMundoPrueba", "number", 2))

external_events(d, "PruebaZoom", [
    COM("PRUEBA TEMPORAL DE ZOOM. La tecla Z cambia el mundo entre zoom 2 y zoom 1. "
        "La interfaz no cambia. Se quitara cuando se decida el zoom definitivo."),
    EV([key_released("z")], [nv("ZoomMundoPrueba", "3 - ZoomMundoPrueba")]),
    EV([], [A("ZoomCamera", "", "ZoomMundoPrueba", q(""), "0"),
            A("ZoomCamera", "", "ZoomMundoPrueba", q("Luz Exterior"), "0")]),
])

# Va justo antes de Personaje: así la cámara se centra y se limita ya con el zoom nuevo.
for nombre in ("Nivel 01", "Nivel 02", "Pueblo"):
    escena = next(l for l in d["layouts"] if l["name"] == nombre)
    i = next(k for k, e in enumerate(escena["events"]) if e.get("target") == "Personaje")
    escena["events"].insert(i, LINK("PruebaZoom"))

with open(P, "w", encoding="utf8") as f:
    json.dump(d, f, ensure_ascii=False, indent=2)
    f.write("\n")
print("ok")
