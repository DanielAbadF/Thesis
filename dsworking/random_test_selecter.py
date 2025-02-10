import os
import shutil
import random

# Rutas de las carpetas
train_folder = "C:/Thesis/Dataset4classes2/train/scc"
test_folder = "C:/Thesis/Dataset4classes2/test/scc"
other_train_folder = "C:/Tesis/DatasetBinario/train/No Melanoma"

# Crear la carpeta de test si no existe
if not os.path.exists(test_folder):
    os.makedirs(test_folder)

# Obtener nombres de archivos en la carpeta de train del otro conjunto
other_train_files = set(os.listdir(other_train_folder))

# Filtrar archivos de train que no estén en la carpeta de otro conjunto
eligible_files = [
    file_name for file_name in os.listdir(train_folder)
    if file_name not in other_train_files 
]

# Asegurarse de que hay suficientes archivos para mover
if len(eligible_files) < 64:
    raise ValueError("No hay suficientes imágenes en train que no estén en el otro conjunto.")

# Seleccionar aleatoriamente 214 imágenes
selected_files = random.sample(eligible_files, 64)

# Mover las imágenes seleccionadas a la carpeta de test
for file_name in selected_files:
    shutil.copy(
        os.path.join(train_folder, file_name),
        os.path.join(test_folder, file_name)
    )

print(f"Proceso completado. Se movieron 214 imágenes de {train_folder} a {test_folder}.")
