import os
import shutil

def copiar_archivos_comunes(path1, path2, path3):
    """
    Copia todos los archivos que existan tanto en path1 como en path2,
    guardándolos en path3.
    """
    
    # Verificar que las rutas existan
    if not os.path.isdir(path1):
        print(f"La ruta {path1} no existe o no es una carpeta.")
        return
    if not os.path.isdir(path2):
        print(f"La ruta {path2} no existe o no es una carpeta.")
        return
    
    # Crear la carpeta de destino si no existe
    os.makedirs(path3, exist_ok=True)
    
    # Listar los archivos de cada carpeta
    archivos_path1 = set(os.listdir(path1))
    archivos_path2 = set(os.listdir(path2))
    
    # Determinar la intersección de archivos
    archivos_comunes = archivos_path1.intersection(archivos_path2)
    
    # Filtrar para asegurarnos de que en ambos lugares sean archivos (no carpetas)
    archivos_comunes = [
        nombre for nombre in archivos_comunes
        if os.path.isfile(os.path.join(path1, nombre))
        and os.path.isfile(os.path.join(path2, nombre))
    ]
    
    # Copiar archivos comunes a la carpeta destino
    for archivo in archivos_comunes:
        origen = os.path.join(path1, archivo)
        destino = os.path.join(path3, archivo)
        shutil.copy2(origen, destino)  # copy2 preserva metadatos
    
    print(f"Se han copiado {len(archivos_comunes)} archivo(s) a la carpeta '{path3}'.")


# Rutas definidas directamente en el código
# Cambia estas rutas según tu sistema
path1 = "C:/Thesis/escamosos"
path2 = "C:/Thesis/Dataset4Classes2/train/esc/scc"
path3 = "C:/Thesis/escamososEntr"

# Llamar a la función
copiar_archivos_comunes(path1, path2, path3)
