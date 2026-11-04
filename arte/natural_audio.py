"""Musica y sonidos originales de PapaYork, sintetizados aqui mismo (sin muestras externas).
Salida: Natural/Audio/*.ogg (via ffmpeg). Uso: python3 arte/natural_audio.py"""
import math, os, random, struct, subprocess, tempfile, wave
B = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."); OUT = os.path.join(B, "Natural/Audio"); os.makedirs(OUT, exist_ok=True)
SR = 22050
NOTA = {n: i for i, n in enumerate("C C# D D# E F F# G G# A A# B".split())}
def f(n):
    return 440 * 2 ** ((NOTA[n[:-1]] + 12 * (int(n[-1]) + 1) - 69) / 12)
def voz(buf, t0, dur, hz, vol, forma):
    a, n = int(t0 * SR), int(dur * SR)
    for i in range(n):
        if a + i >= len(buf): break
        t = i / SR; env = min(1, t / .012) * math.exp(-t * forma["caida"])
        s = sum(g * math.sin(2 * math.pi * hz * m * t) for m, g in forma["arm"])
        buf[a + i] += s * env * vol
PLUCK = {"caida": 3.2, "arm": [(1, .8), (2, .25), (3, .08)]}
FLAUTA = {"caida": 1.0, "arm": [(1, .9), (2, .12)]}
BAJO = {"caida": 1.6, "arm": [(1, 1), (2, .2)]}
ACORDE = {"caida": .55, "arm": [(1, .7), (2, .1)]}
def pieza(nombre, bpm, acordes, melodia, sem, flauta=True):
    r = random.Random(sem); beat = 60 / bpm; total = len(acordes) * 4 * beat
    buf = [0.0] * int((total + 1) * SR)
    for k, ac in enumerate(acordes):
        t = k * 4 * beat
        voz(buf, t, 4 * beat, f(ac[0]), .16, BAJO); voz(buf, t + 2 * beat, 2 * beat, f(ac[0]), .1, BAJO)
        for n in ac[1:]: voz(buf, t, 4 * beat, f(n), .055, ACORDE)
        for b in range(8):
            voz(buf, t + b * beat / 2, beat * 1.2, f(ac[1 + b % (len(ac) - 1)]), .05 if b % 2 else .075, PLUCK)
    for ini, n, d in melodia:
        voz(buf, ini * beat, d * beat * 1.15, f(n), .17, FLAUTA if flauta else PLUCK)
        if not flauta: voz(buf, ini * beat, d * beat, f(n) * 2, .03, PLUCK)
    # Eco suave para dar espacio; lo que sobra al final vuelve al principio y el bucle no se nota
    eco = int(beat * .75 * SR)
    for i in range(eco, len(buf)): buf[i] += buf[i - eco] * .22
    n = int(total * SR); sal = buf[:n]
    for i in range(n, len(buf)): sal[i - n] += buf[i]
    pico = max(abs(x) for x in sal) or 1
    guardar(nombre, [x / pico * .8 for x in sal])
def guardar(nombre, m):
    tmp = tempfile.mktemp(suffix=".wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(b"".join(struct.pack("<h", int(max(-1, min(1, x)) * 32000)) for x in m))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-c:a", "libvorbis", "-q:a", "4", os.path.join(OUT, nombre + ".ogg")], check=True)
    os.remove(tmp)
def frase(ini, notas, paso=1):
    o = []; t = ini
    for n in notas:
        if isinstance(n, tuple): nn, d = n
        else: nn, d = n, paso
        if nn != "-": o.append((t, nn, d))
        t += d
    return o
# Tema del menu: La menor, nostalgico; la tierra que se perdio
am, fa, do, sol = ["A2", "A3", "C4", "E4"], ["F2", "F3", "A3", "C4"], ["C3", "G3", "C4", "E4"], ["G2", "G3", "B3", "D4"]
pieza("TemaPapayork", 76, [am, fa, do, sol, am, fa, sol, am],
      frase(0, [("E5", 2), "D5", "C5", ("A4", 3), "C5", ("C5", 2), "A4", "G4", ("A4", 3), "-", ("E4", 1), "G4", "A4", "C5", ("D5", 2), ("C5", 2), ("B4", 2), "A4", "G4", ("A4", 3), "-"])
      + frase(16, [("E5", 2), "G5", "E5", ("D5", 3), "C5", ("C5", 2), "D5", "E5", ("G4", 3), "-", ("A4", 2), "C5", "D5", ("E5", 2), ("D5", 2), ("C5", 2), "B4", "G4", ("A4", 4)]), 1)
# Granja: Sol mayor, manana tranquila
G, C, Em, D = ["G2", "G3", "B3", "D4"], ["C3", "G3", "C4", "E4"], ["E2", "G3", "B3", "E4"], ["D3", "F#3", "A3", "D4"]
pieza("MananaEnLaGranja", 92, [G, C, G, D, Em, C, D, G],
      frase(0, ["G4", "B4", "D5", ("E5", 2), "D5", "B4", "-", "C5", "E5", "G5", ("E5", 2), "D5", "C5", "-", "B4", "D5", "G5", ("F#5", 2), "E5", "D5", "-", "A4", "C5", "D5", ("A5", 2), "G5", "F#5", "-"])
      + frase(16, ["E5", "G5", "E5", ("B4", 2), "D5", "E5", "-", "C5", "E5", "G5", ("A5", 2), "G5", "E5", "-", ("F#5", 2), "D5", "A4", ("C5", 2), "B4", "A4", ("G4", 4), "-"]), 2)
# Bosque: Mi menor, misterio; radiacion entre los arboles
Em2, Cm, Am2, B7 = ["E2", "E3", "G3", "B3"], ["C3", "G3", "C4", "E4"], ["A2", "A3", "C4", "E4"], ["B2", "F#3", "A3", "D#4"]
pieza("BosqueContaminado", 66, [Em2, Cm, Am2, B7, Em2, Am2, B7, Em2],
      frase(2, [("B4", 2), "A4", "G4", ("E4", 4), "-", ("G4", 2), "A4", ("B4", 3), ("C5", 2), ("B4", 4), "-", ("D#5", 2), "C5", ("B4", 4), "-", ("E5", 2), "D5", "B4", ("G4", 2), ("A4", 2), ("F#4", 2), ("E4", 4)]), 3)
# Pueblo: Fa mayor, plaza alegre, sin flauta
F, Bb, C7, Dm = ["F2", "F3", "A3", "C4"], ["A#2", "F3", "A#3", "D4"], ["C3", "E3", "A#3", "C4"], ["D3", "F3", "A3", "D4"]
pieza("PlazaDelPueblo", 108, [F, Bb, C7, F, Dm, Bb, C7, F],
      frase(0, ["A4", "C5", "F5", "C5", "D5", "F5", "A#5", "F5", "G5", "E5", "C5", "E5", "F5", "A4", ("C5", 2), "D5", "F5", "A5", "F5", "A#5", "G5", "F5", "D5", "C5", "E5", "G5", "E5", ("F5", 3), "-"], .5)
      + frase(16, ["A4", "C5", "F5", "C5", "D5", "F5", "A#5", "F5", "G5", "E5", "C5", "E5", "F5", "A4", ("C5", 2), "D5", "F5", "A5", "F5", "A#5", "G5", "F5", "D5", "C5", "E5", "G5", "E5", ("F5", 3), "-"], .5), 4, flauta=False)
# Mina: Re menor, hueca y con eco; golpes lejanos de pico
Dm2, Bb2, Gm2, A7 = ["D2", "D3", "F3", "A3"], ["A#1", "F3", "A#3", "D4"], ["G2", "G3", "A#3", "D4"], ["A2", "E3", "G3", "C#4"]
pieza("Profundidades", 58, [Dm2, Dm2, Bb2, A7, Dm2, Gm2, A7, Dm2],
      frase(4, [("A4", 3), "F4", ("D4", 4), "-", ("C#4", 2), "E4", ("A3", 5), "-", ("F4", 3), "G4", ("A4", 2), ("A#4", 2), ("A4", 4), "-", ("G4", 2), "E4", ("D4", 6)]), 6)
# Efectos
r = random.Random(9)
def efecto(nombre, dur, fn):
    guardar(nombre, [fn(i / SR, i / (dur * SR)) for i in range(int(dur * SR))])
ult = [0.0]
def filtrado(a):
    def g(t, p):
        ult[0] += (r.uniform(-1, 1) - ult[0]) * a(p); return ult[0]
    return g
ef = filtrado(lambda p: .12 + .7 * math.sin(math.pi * p) ** 2)
efecto("Espada", .22, lambda t, p: ef(t, p) * 1.3 * math.sin(math.pi * p) ** 1.5)
ag = filtrado(lambda p: .3)
efecto("Regar", .5, lambda t, p: (ag(t, p) * .55 + .12 * math.sin(2 * math.pi * (900 + 500 * math.sin(t * 50)) * t) * (r.random() < .25)) * min(1, p * 8) * (1 - p))
efecto("Comer", .25, lambda t, p: r.uniform(-1, 1) * .35 * (1 - p) * (1 if math.sin(t * 90) > 0 else .15))
print("ok")
