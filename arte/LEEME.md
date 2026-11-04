# Carpeta arte

- `*.px.js`: dibujos en pxl. `menu_ui.px.js` tiene los paneles del menú, `inventario.px.js` las casillas, la barra y la mochila,
  `recursos.px.js` los íconos de los recursos, las vetas y la hierba, `hud.px.js` el panel de hora, fecha y monedas, `fabricacion.px.js` la mesa y las construcciones,
  y `cultivos.px.js` las plantas de papa y el montículo de la papa radiactiva.
  Para compilarlos: `node ~/.claude/skills/pxl-pixel-art/bin/pxl.js build inventario.px.js`. Las imágenes salen en `out/sprites/`
  y se copian a `../Menu/`, `../Inventario/`, `../Recursos/`, `../HUD/`, `../Fabricacion/` o `../Cultivos/`.
- `generar_*.py`: scripts que escriben las escenas y los eventos dentro de `Legado Radioactivo-Papayork.json`.
  Siempre se aplican sobre la copia original, en este orden:

```
cp "Legado Radioactivo-Papayork.respaldo-antes-menu.json" "Legado Radioactivo-Papayork.json"
python3 arte/generar_inventario.py "Legado Radioactivo-Papayork.json"
python3 arte/generar_recursos.py "Legado Radioactivo-Papayork.json"
python3 arte/generar_mundo.py "Legado Radioactivo-Papayork.json"
python3 arte/generar_fabricacion.py "Legado Radioactivo-Papayork.json"
python3 arte/generar_cultivos.py "Legado Radioactivo-Papayork.json"
python3 arte/generar_menu.py "Legado Radioactivo-Papayork.json"
```

Si cambias algo a mano en GDevelop, no vuelvas a ejecutar los scripts: sobrescribirían tus cambios.

## Desde el 21/10/2026 por la tarde: cambios puntuales

El proyecto ya se edita en GDevelop, así que **ya no se usa `regenerar.sh`** (borraría lo que cambies a mano).
Los cambios nuevos están en `arte/cambios/` y se aplican una sola vez sobre el proyecto actual, en orden:

- `01_reloj.py`: arregla el reloj (1 hora cada 60 minutos; 10 minutos de juego cada 7 segundos reales).
- `02_hud_compacto.py`: panel de la esquina y barra rápida pequeños (íconos de 16px en `Mini/`, generados con `arte/iconos_mini.py`).
- `03_pueblo.py`: mercado de Doña Rosa y herrería de Don Fermín (`arte/npcs.py` crea los NPC desde el sprite de Pedro).
- `04_tienda_dinero.py`: ubicación del dinero en el panel de la tienda.
- `05_ui_hd.py` y `06_centro_capas.py`: el juego se dibuja a 960x540; todas las capas llevan zoom 2 menos `UIHD`
  (barra rápida y reloj nítidos con íconos de 32px).
- `07_borrar_partida.py` y `09_papelera_fix.py`: papelera para borrar partidas (pide confirmación).
- `08_dialogo_intro.py`: caja de diálogo estilo Stardew (eventos externos `Dialogo`, capa `DialogoHD`) y la escena `Intro`
  con la historia de HetolMimiao, Chuchini Gutiérrez y Pedro. Arte en `arte/intro.px.js` y `arte/personajes_intro.py`.
- `10_escenarios.py`: rediseño de la Granja (48x32 casillas: casa con puerta para dormir, granero, buzón, huerto cercado,
  estanque, estatua de HetolMimiao, zona contaminada con charcos que quitan vida), del Bosque (56x40: río con puente,
  cantera, cabaña en ruinas, cueva sellada, hongos y la Papa Gigante) y del Pueblo (Ramiro, Lupita, Tomás y el tablón).
  Eventos externos `Mundo2`. Arte en `arte/escenarios.px.js` y `arte/npcs_pueblo.py`. Este script sí se puede volver a ejecutar.
- `11_pausa_gameover.py`: la música suena siempre en el canal 0 y solo cambia si la canción es otra (ya no se reinicia
  al cambiar de zona). Pestañas Mochila / Opciones / Salir en la mochila (eventos externos `Pausa`; volumen general,
  volumen de música, pantalla completa, guardar e ir al menú, cerrar el juego). Nueva escena `GameOver` ("Te desmayaste":
  pierdes el 10% de las monedas, máximo 100, y despiertas en casa). Arte en `arte/pausa.px.js` y `arte/gameover.px.js`.
- `12_prueba_zoom.py`: prueba temporal. La tecla Z cambia el mundo entre zoom 2 y zoom 1 en Granja, Bosque y Pueblo
  (eventos externos `PruebaZoom`, variable global `ZoomMundoPrueba`). No se guarda en la partida. Se quita al decidir el zoom.

Antes de cada cambio se guarda una copia del proyecto (`Legado Radioactivo-Papayork.respaldo-*.json`).
- `13_arte_natural.py`: arte nuevo en `Natural/` (terreno, agua con orillas, árboles, personajes de 32x48, retratos, papas, cultivos,
  casa, granero, madera), música y efectos propios y zoom 1 por defecto. Los sonidos de terceros salen de la lista de recursos.
  Se regenera con `python3 arte/natural_terreno.py`, `pxl build arte/personajes_natural.px.js`, `python3 arte/natural_instalar.py` y `python3 arte/natural_audio.py`.
  Estos generadores no escriben en el `.json`: se pueden repetir sin riesgo.
- `14_dias_energia_riego.py`: evento externo `NuevoDia`. El día cambia al dormir, desmayo a las 2 AM, energía, comida, cultivos por días,
  estaciones, riego y regadera. Luz de día y noche más suave. Corrige las pestañas de pausa que salían durante los diálogos.
- `15_retoques_madera.py`: corrige las piezas de cerca, el muelle y las orillas sueltas del script 13.
- `16_pedro_y_profundidad.py`: Pedro con esqueleto (`arte/pedro.px.js`), sombrero, correr por defecto y Shift para caminar. Orden de profundidad único: `arte/ORDEN_PROFUNDIDAD.md`.
- `17_fermin_visible.py`: Don Fermín pasa a estar junto a su yunque.
- `18_herramientas_caminos.py`: animación propia para hacha, pico, azadón, regadera y caña (lienzo de 62x62, origen 31.5, 57). Árboles y muro de bosque fuera de los caminos del Pueblo.
- `19_inventario_propio.py`: interfaz de madera y lino (`arte/natural_ui.py`), pestaña Vecinos y una casilla más de oferta.
- `20_pesca.py`: evento externo `Pesca`, 8 peces propios en `Peces`, caña en el Mercado.
- `21_amistad.py`: evento externo `Amistad`, corazones, regalos con F, premios y diálogos según la amistad.
- `22_intro_y_desmayo.py`: introducción por capas con más historia (fondos en `arte/natural_intro.py` y `natural_intro2.py`, elenco en `arte/pedro.px.js`), pantalla de desmayo nueva e ícono de la zanahoria.
- `23_rutinas_eventos.py`: eventos externos `Rutinas` (cada vecino camina según la hora; la tienda cierra fuera de horario) y `Eventos` (lector de escenas con condiciones; se guardan en `EventosVistos`).
- `24_casas_pueblo_diario.py`: escena `Interior` con 8 salas, casas de `arte/natural_casas.py`, puertas con clic, barrio este, Inés y Beto, tienda dentro de cada casa, vecinos que entran y salen, y seis páginas del diario.
- `25_arboles_calles_este.py`: quita los árboles que tapaban las calles nuevas del Pueblo.
- `26_barra_energia_alcance.py`: la barra rápida sube cuando Pedro está abajo, herramientas gastan menos energía y la espada alcanza más lejos.
- `27_mina.py`: escena `Mina` con pisos generados al azar, 3 zonas, descansos cada 5 pisos y 6 enemigos que persiguen a Pedro (arte en `arte/natural_mina.py`).
- `28_menu_espada_mina.py`: menú nuevo (papa zombie en la oscuridad, Pedro la vence, valle con aves, logo que baja y opciones con el estilo del inventario; arte en `arte/natural_menu.py`), espada más larga, papas con menos vida y mina en un claro del Bosque.
- `29_retroceso_y_vida.py`: las papas retroceden al recibir un golpe y no hacen daño mientras retroceden; panel de vida nuevo en la capa UIHD con retrato, gestos, colores y números propios (arte en `arte/natural_vida.py`).

Colores y reglas de luz: `arte/paleta.md`. Autores y licencias: `CREDITOS.md`.
