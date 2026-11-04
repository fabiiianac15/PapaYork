# Orden de profundidad de PapaYork

GDevelop dibuja primero las capas y, dentro de cada capa, ordena por el valor Z: el número mayor queda delante.

## Capas, de atrás hacia delante
1. `""`: el mundo. La usa toda la tabla de abajo.
2. `Luz Exterior`: la luz del día y la noche.
3. `Interfaz`: barra de vida.
4. `UIHD`: reloj y barra rápida, Z de 40 a 150. Barra de energía, Z 5000. Minijuego de pesca, Z de 6000 a 6002.
5. `Inventario`: mochila, tienda y pausa, Z de 500 a 560.
6. `DialogoHD`: diálogos y fundidos.

## Capa del mundo
| Z | Qué hay |
|---|---|
| -10000 | Pasto de fondo |
| -9000 | Agua |
| -8900 | Orillas |
| -8000 | Caminos de tierra |
| -7900 | Empedrado |
| -7850 y -7800 | Trozos de agua y camino que van encima del empedrado en el Pueblo |
| -7500 | Flores, piedritas y briznas |
| -7400 | Flores y hongos grandes |
| -7000 | Muelle y puente |
| -6800 | Charcos radiactivos |
| -6500 | Tierra arada |
| -6400 | Marca de la casilla elegida |
| -6000 | Colisiones invisibles y teletransportes |
| -5500 | Muros de bosque |
| -5400 | Cercas del mapa |
| Y del pie, de -400 a 1400 | Todo lo que está de pie |
| -6700 | Boya de pesca |
| 80000 | Línea de pesca |
| -9000 | Fondo de las salas en la escena Interior |
| 90000 | Cortes de espada y números de daño |
| 95000 | Signo de que picó |
| 100000 | Avisos y textos flotantes |

## Por qué hay valores como 302 o 400
Los objetos que están de pie no llevan un número fijo: su Z es la coordenada Y del punto donde pisan.
Un árbol que pisa en Y = 302 tiene Z = 302. Si Pedro pisa en Y = 320, queda delante; si pisa en Y = 280, pasa por detrás.
Así el orden se resuelve solo mientras Pedro camina. Esos números no son desorden.

## Dónde se calcula
- Objetos colocados en el mapa: al empezar la escena, en el evento externo `Profundidad`.
- Objetos que se mueven o aparecen durante el juego: en cada cuadro.
- Pedro: `Personaje_jugador.Y() + 3`. Papas: `Papa.Y()`. Cultivos: `Cultivo.Y() + 28`. Vecinos: `NPC.Y() + 29`, en cada cuadro porque ahora caminan.

Al añadir un objeto nuevo: si es plano, va en una franja negativa de la tabla. Si está de pie, va en `Profundidad`.
