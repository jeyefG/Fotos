# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 19:53:49 2025

@author: jfcog
Programa que identifica fotos repetidas
Crea carpeta con Fotos a Eliminar (no elimina)
"""

import os
import shutil
import imagehash
from PIL import Image, ImageOps
from PIL.ExifTags import TAGS
from collections import defaultdict
from datetime import datetime
from tqdm import tqdm  # Barra de progreso

def obtener_fecha_exif(imagen):
    try:
        exif_data = imagen._getexif()
        if not exif_data:
            return None
        for tag, value in exif_data.items():
            nombre = TAGS.get(tag, tag)
            if nombre == 'DateTimeOriginal':
                return datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
    except Exception:
        return None
    return None

def procesar_y_organizar(path_base, carpeta_descartadas='Fotos_a_Eliminar'):
    hash_dict = defaultdict(list)
    carpeta_descartadas = os.path.join(path_base, carpeta_descartadas)

    # 1. Recorrer todas las imágenes primero para saber cuántas son
    print("\n🔍 Escaneando imágenes...")
    lista_imagenes = []
    nombre_descartadas = os.path.basename(carpeta_descartadas)
    for root, dirs, files in os.walk(path_base):
        if nombre_descartadas in dirs:
            dirs.remove(nombre_descartadas)
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                lista_imagenes.append(os.path.join(root, file))

    print(f"📸 Total de imágenes encontradas: {len(lista_imagenes)}\n")

    # 2. Procesar imágenes con barra de progreso
    for ruta in tqdm(lista_imagenes, desc="Procesando imágenes", unit="img"):
        try:
            img = Image.open(ruta)
            img = ImageOps.exif_transpose(img)
            img_rgb = img.convert("RGB")
            hash_img = (
                str(imagehash.phash(img_rgb, hash_size=16)),
                str(imagehash.colorhash(img_rgb))
            )
            fecha = obtener_fecha_exif(img)
            ancho, alto = img_rgb.size
            resolucion = ancho * alto
            hash_dict[hash_img].append({
                'ruta': ruta,
                'fecha': fecha,
                'ancho': ancho,
                'alto': alto,
                'resolucion': resolucion,
                'nombre': os.path.basename(ruta)
            })
        except Exception as e:
            print(f"\n❌ Error procesando {ruta}: {e}")

    # 3. Crear carpeta destino para duplicados
    os.makedirs(carpeta_descartadas, exist_ok=True)

    # 4. Procesar duplicados con barra de progreso
    print("\n🔄 Organizando imágenes por grupos de duplicados...")
    for grupo_id, (hash_val, imagenes) in enumerate(tqdm(hash_dict.items(), desc="Organizando", unit="grupo"), start=1):
        if len(imagenes) == 1:
            preferida = imagenes[0]
        else:
            # Preferir mayor resolución, luego fecha más antigua
            preferida = sorted(
                imagenes,
                key=lambda x: (-x['resolucion'], x['fecha'] or datetime.max)
            )[0]

        # Mover duplicados a ruta espejo dentro de Fotos_a_Eliminar
        for img in imagenes:
            if img != preferida:
                try:
                    ruta_relativa = os.path.relpath(img['ruta'], path_base)
                    carpeta_destino = os.path.join(carpeta_descartadas, os.path.dirname(ruta_relativa))
                    os.makedirs(carpeta_destino, exist_ok=True)
                    nombre = os.path.basename(img['ruta'])
                    destino_descartado = os.path.join(carpeta_destino, f"grupo{grupo_id}_{nombre}")
                    shutil.move(img['ruta'], destino_descartado)
                except Exception as e:
                    print(f"\n⚠️ Error al mover duplicado {img['ruta']}: {e}")

    print("\n🎉 Proceso completado.")

# Ruta de origen
ruta_origen = 'D:'

if __name__ == '__main__':
    procesar_y_organizar(ruta_origen)
