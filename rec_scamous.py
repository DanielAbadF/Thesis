import os
import shutil

# Rutas
carpeta_origen = "C:/Thesis/Dataset4classes/test/scc"  # Cambia a la carpeta donde están los datos
carpeta_destino = "C:/Thesis/escamosos"  # Cambia a la carpeta donde copiar los datos

# Crear la carpeta destino si no existe
os.makedirs(carpeta_destino, exist_ok=True)

# Filtrar y copiar archivos
for archivo in os.listdir(carpeta_origen):
    if not any(substring in archivo for substring in ["trans", "flip", "rot"]):
        origen = os.path.join(carpeta_origen, archivo)
        destino = os.path.join(carpeta_destino, archivo)
        shutil.copy2(origen, destino)  # Copia con metadatos
        print(f"Copiado: {archivo}")

print("Proceso completado.")
