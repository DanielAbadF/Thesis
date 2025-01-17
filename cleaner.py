import os
from PIL import Image, UnidentifiedImageError

def remove_corrupt_images(folder_path):
    """
    Revisa todas las imágenes PNG en la carpeta especificada y sus subcarpetas, eliminando las que están corruptas.

    Args:
        folder_path (str): Ruta de la carpeta a revisar.
    """
    if not os.path.exists(folder_path):
        print(f"La ruta especificada no existe: {folder_path}")
        return

    total_files = 0
    corrupt_files = 0

    for root, _, files in os.walk(folder_path):
        for filename in files:
            filepath = os.path.join(root, filename)

            # Verifica si es un archivo PNG
            if filename.lower().endswith('.png'):
                total_files += 1
                try:
                    # Intenta abrir la imagen
                    with Image.open(filepath) as img:
                        img.verify()  # Verifica la integridad del archivo
                except (UnidentifiedImageError, IOError):
                    corrupt_files += 1
                    print(f"Imagen corrupta encontrada y eliminada: {filepath}")
                    os.remove(filepath)  # Elimina la imagen corrupta

    print(f"Revisión completa. Total de imágenes: {total_files}, Imágenes corruptas eliminadas: {corrupt_files}")

# Ruta de la carpeta
folder_path = r"C:/Thesis/Dataset8clases"

# Ejecutar la función
remove_corrupt_images(folder_path)
