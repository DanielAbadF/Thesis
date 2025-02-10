import os
import shutil
import sys

def move_images(folder_a, folder_b, folder_c):
    # Verifica que la carpeta A exista
    if not os.path.exists(folder_a):
        print(f"La carpeta {folder_a} no existe.")
        return
    # Verifica que la carpeta B exista
    if not os.path.exists(folder_b):
        print(f"La carpeta {folder_b} no existe.")
        return
    # Crea la carpeta C si no existe
    if not os.path.exists(folder_c):
        print(f"La carpeta {folder_c} no existe, se creará.")
        os.makedirs(folder_c)
    
    # Conjunto de extensiones de imagen permitidas
    allowed_exts = {'.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff'}

    # Recorre todos los archivos en la carpeta A
    for filename in os.listdir(folder_a):
        # Obtiene la extensión en minúsculas
        ext = os.path.splitext(filename)[1].lower()
        if ext in allowed_exts:
            # Comprueba si el archivo existe en la carpeta B
            file_in_b = os.path.join(folder_b, filename)
            if not os.path.exists(file_in_b):
                # Si no existe en B, mueve el archivo de A a C
                src = os.path.join(folder_a, filename)
                dest = os.path.join(folder_c, filename)
                print(f"Moviendo {src} a {dest}")
                shutil.copy(src, dest)

if __name__ == "__main__":
    
    folder_a = "C:/Thesis/melanoma"
    folder_b = "C:/Tesis/DatasetBinario/train/Melanoma"
    folder_c = "C:/Tesis/DatasetBinario/test/Melanoma"
    move_images(folder_a, folder_b, folder_c)
