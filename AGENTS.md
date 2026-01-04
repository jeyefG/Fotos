# AGENTS.md

## Alcance
Este archivo aplica a todo el repositorio.

## Resumen del proyecto
`V6_auto.py` es un script de Python que busca fotos duplicadas usando *perceptual hashing* (combinación de `imagehash.phash` y `imagehash.colorhash`). Recorre una carpeta origen, agrupa imágenes por hash, elige una “preferida” por **mayor resolución** y, si hay empate, por **fecha EXIF más antigua**. No elimina archivos: **mueve** duplicados a una carpeta de descartes con ruta espejo a la original.

## Ejecución
- Punto de entrada: `procesar_y_organizar(ruta_origen)` en `V6_auto.py`.
- `ruta_origen` está definido al final del archivo y se usa en `__main__`.
- Salida por defecto:
  - `Fotos_a_Eliminar/` (movidos con ruta espejo dentro de `ruta_origen`)

## Dependencias
- Python 3
- Paquetes: `Pillow`, `imagehash`, `tqdm`

## Comportamiento y criterios clave
- Formatos soportados: `.jpg`, `.jpeg`, `.png`.
- Agrupación: por combinación de `imagehash.phash` (hash_size=16) y `imagehash.colorhash`.
- Preferencia dentro de un grupo:
  1. Mayor resolución (ancho × alto).
  2. Fecha EXIF más antigua (`DateTimeOriginal`).
- Duplicados se **mueven** con prefijo `grupo<N>_` al nombre, manteniendo la ruta espejo bajo `Fotos_a_Eliminar/`.
- Antes de renombrar, se limpia cualquier prefijo `grupo<N>_` existente para evitar concatenaciones en ejecuciones repetidas.
- Se genera `Fotos_a_Eliminar/reporte_duplicados.csv` con la ruta preferida y la ruta destino de cada duplicado.

## Buenas prácticas de edición
- Si se cambia el criterio de selección o agrupación, actualizar este archivo.
- Evitar borrar archivos en el origen sin confirmación explícita.
- Mantener mensajes y comportamiento en español.
