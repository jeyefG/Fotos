# -*- coding: utf-8 -*-
"""
Created on Thu Jul 24 19:53:49 2025

@author: jfcog
Programa que identifica fotos repetidas
Crea carpeta con Fotos limpias y otra con Fotos a Eliminar (no elimina)
"""

import os
import shutil
import imagehash
from PIL import Image
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

def procesar_y_organizar(path_base, carpeta_salida='Fotos_Limpias', carpeta_descartadas='Fotos_Eliminadas'):
    hash_dict = defaultdict(list)

    # 1. Recorrer todas las imágenes primero para saber cuántas son
    print("\n🔍 Escaneando imágenes...")
    lista_imagenes = []
    for root, _, files in os.walk(path_base):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                lista_imagenes.append(os.path.join(root, file))

    print(f"📸 Total de imágenes encontradas: {len(lista_imagenes)}\n")

    # 2. Procesar imágenes con barra de progreso
    for ruta in tqdm(lista_imagenes, desc="Procesando imágenes", unit="img"):
        try:
            img = Image.open(ruta)
            hash_img = str(imagehash.phash(img))
            fecha = obtener_fecha_exif(img)
            ancho, alto = img.size
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

    # 3. Crear carpetas destino
    os.makedirs(carpeta_salida, exist_ok=True)
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

        # Determinar destino por fecha EXIF
        fecha = preferida['fecha']
        if fecha:
            year = str(fecha.year)
            month = f"{fecha.month:02}"
        else:
            year = "SinFecha"
            month = "SinFecha"

        carpeta_final = os.path.join(carpeta_salida, year, month)
        os.makedirs(carpeta_final, exist_ok=True)

        # Copiar imagen preferida a carpeta final
        destino = os.path.join(carpeta_final, preferida['nombre'])
        if not os.path.exists(destino):  # Evita sobreescribir
            shutil.copy2(preferida['ruta'], destino)

        # Mover duplicados
        for img in imagenes:
            if img != preferida:
                try:
                    nombre = os.path.basename(img['ruta'])
                    destino_descartado = os.path.join(carpeta_descartadas, f"grupo{grupo_id}_{nombre}")
                    shutil.move(img['ruta'], destino_descartado)
                except Exception as e:
                    print(f"\n⚠️ Error al mover duplicado {img['ruta']}: {e}")

    print("\n🎉 Proceso completado.")

# Ruta de origen
ruta_origen = 'D:'

if __name__ == '__main__':
    procesar_y_organizar(ruta_origen)
