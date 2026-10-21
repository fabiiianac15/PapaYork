"""Arregla el reloj: una hora pasa cuando los minutos llegan a 60 (no a 10) y suma 1 (no 10).
Ademas el tiempo corre como en Stardew: 10 minutos del juego cada 7 segundos reales."""
import json, sys
P = sys.argv[1]
d = json.load(open(P, encoding="utf8"))
reloj = next(e for e in d["externalEvents"] if e["name"] == "RelojProg")
def recorrer(evs):
    for e in evs:
        yield e
        yield from recorrer(e.get("events") or [])
hechos = 0
for e in recorrer(reloj["events"]):
    for c in e.get("conditions") or []:
        if c["type"]["value"] == "NumberVariable" and c["parameters"][0] == "Reloj.Minuto" and c["parameters"][1] == ">=" \
                and any(a["type"]["value"] == "SetNumberVariable" and a["parameters"][0] == "Reloj.Hora" for a in e["actions"]):
            c["parameters"][2] = "60"
            for a in e["actions"]:
                if a["type"]["value"] == "SetNumberVariable" and a["parameters"][0] == "Reloj.Hora": a["parameters"][1:] = ["+", "1"]
            hechos += 1
        if c["type"]["value"] == "CompareTimer" and c["parameters"][1] == '"PasoTiempo"':
            c["parameters"][3] = "7"
            hechos += 1
assert hechos == 2, hechos
json.dump(d, open(P, "w", encoding="utf8"), ensure_ascii=False, indent=2)
print("ok: reloj arreglado")
