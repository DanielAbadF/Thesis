import os
import shutil
import random

# Rutas
dataset_origen = "ruta/a/dataset_origen"  # Ruta al dataset con varias carpetas
carpeta_exclusion = "ruta/a/carpeta_exclusion"  # Ruta de la carpeta cuyas imágenes no deben incluirse
carpeta_destino = "ruta/a/carpeta_destino"  # Ruta donde copiar las imágenes

# Crear la carpeta destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Obtener nombres de los archivos en la carpeta de exclusión
archivos_excluidos = set(os.listdir(carpeta_exclusion))

# Lista para almacenar rutas de las imágenes elegibles
imagenes = []

# Recorrer todas las carpetas en el dataset
for carpeta in os.listdir(dataset_origen):
    carpeta_path = os.path.join(dataset_origen, carpeta)
    
    # Verificar que sea una carpeta
    if not os.path.isdir(carpeta_path):
        continue
    
    # Agregar imágenes que no estén en los archivos excluidos
    for archivo in os.listdir(carpeta_path):
        if archivo.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')) and archivo not in archivos_excluidos:
            imagenes.append(os.path.join(carpeta_path, archivo))

# Seleccionar 300 imágenes aleatorias (o menos si hay menos imágenes elegibles)
imagenes_seleccionadas = random.sample(imagenes, min(300, len(imagenes)))

# Copiar las imágenes seleccionadas a la carpeta destino
for imagen in imagenes_seleccionadas:
    nombre_archivo = os.path.basename(imagen)  # Obtener el nombre del archivo
    destino = os.path.join(carpeta_destino, nombre_archivo)
    shutil.copy2(imagen, destino)  # Copia con metadatos
    print(f"Copiada: {nombre_archivo}")

print(f"Proceso completado. Se copiaron {len(imagenes_seleccionadas)} imágenes.")
