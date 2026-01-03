# AGENTS.md

## Alcance
Este archivo aplica a todo el repositorio.

## Resumen del proyecto
`V6_auto.py` es un script de Python que busca fotos duplicadas usando *perceptual hashing* (`imagehash.phash`). Recorre una carpeta origen, agrupa imágenes por hash, elige una “preferida” por **mayor resolución** y, si hay empate, por **fecha EXIF más antigua**. Copia la preferida a una estructura de salida por **año/mes** y mueve los duplicados a una carpeta de descartes. No elimina archivos: **mueve** duplicados a la carpeta de descartadas y **copia** la preferida a la carpeta de limpias.

## Ejecución
- Punto de entrada: `procesar_y_organizar(ruta_origen)` en `V6_auto.py`.
- `ruta_origen` está definido al final del archivo y se usa en `__main__`.
- Salidas por defecto:
  - `Fotos_Limpias/AAAA/MM` (copias)
  - `Fotos_Eliminadas/` (movidos)

## Dependencias
- Python 3
- Paquetes: `Pillow`, `imagehash`, `tqdm`

## Comportamiento y criterios clave
- Formatos soportados: `.jpg`, `.jpeg`, `.png`.
- Agrupación: por `imagehash.phash`.
- Preferencia dentro de un grupo:
  1. Mayor resolución (ancho × alto).
  2. Fecha EXIF más antigua (`DateTimeOriginal`).
- Organización por fecha EXIF:
  - Si hay EXIF: `Fotos_Limpias/<año>/<mes>`.
  - Si no hay EXIF: `Fotos_Limpias/SinFecha/SinFecha`.
- Duplicados se **mueven** con prefijo `grupo<N>_` al nombre.

## Buenas prácticas de edición
- Si se cambia el criterio de selección o agrupación, actualizar este archivo.
- Evitar borrar archivos en el origen sin confirmación explícita.
- Mantener mensajes y comportamiento en español.
