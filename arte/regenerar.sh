#!/bin/sh
# Vuelve a generar el proyecto desde la copia original aplicando todos los scripts en orden.
set -e
cd "$(dirname "$0")/.."
cp "Legado Radioactivo-Papayork.respaldo-antes-menu.json" "Legado Radioactivo-Papayork.json"
for paso in inventario recursos mundo fabricacion cultivos menu; do
  python3 "arte/generar_$paso.py" "Legado Radioactivo-Papayork.json"
done
