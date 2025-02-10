import os
import shutil

# Rutas de las carpetas
total_folder = "C:/Thesis/images/squamous_cell_carcinoma"
test_folder = "C:/Tesis/DatasetBinario/test/No Melanoma"
#valid_folder = "C:/Thesis/Dataset4Classes2/valid/melanoma"
train_folder = "C:/Thesis/Dataset4Classes2/train/scc"
new_test_folder = "C:/Thesis/Dataset4Classes2/test/scc"

# Crear la carpeta de train si no existe
if not os.path.exists(train_folder):
    os.makedirs(train_folder)

# Obtener nombres de archivos en test y valid
test_files = set(os.listdir(test_folder))
#valid_files = set(os.listdir(valid_folder))

# Iterar por los archivos de la carpeta total
for file_name in os.listdir(total_folder):
    if file_name not in test_files and file_name:
        # Copiar a la carpeta de train
        shutil.copy(
            os.path.join(total_folder, file_name),
            os.path.join(train_folder, file_name)
        )
    else:
         shutil.copy(
            os.path.join(total_folder, file_name),
            os.path.join(new_test_folder, file_name)
        )
        

print("Proceso completado. Las imágenes se han distribuido correctamente.")
