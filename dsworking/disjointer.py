import os

# Rutas de las carpetas principales
train_folder = "C:/Tesis/DatasetBinario/train/Melanoma"
test_folder = "C:/Thesis/Dataset4Classes2/test/mel"

# Obtener nombres de las imágenes en test
test_files = set(os.listdir(test_folder))

# Iterar por los archivos de train
for item in os.listdir(train_folder):
    train_item_path = os.path.join(train_folder, item)
    
    # Verificar si es un archivo y está en test
    if os.path.isfile(train_item_path) and item in test_files:
        print(f"Eliminando imagen: {train_item_path}")
        os.remove(train_item_path)

print("Proceso completado. Todas las imágenes comunes entre train y test han sido eliminadas.")
