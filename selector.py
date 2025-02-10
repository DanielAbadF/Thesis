import os
import shutil
import random

# Rutas de las carpetas
total_folder = "C:/Thesis/images/squamous_cell_carcinoma"
test_folder = "C:/Thesis/Dataset4Classes2/test/scc"
train_folder = "C:/Thesis/Dataset4Classes2/train/scc"
other_train_folder = "C:/Tesis/DatasetBinario/train/No Melanoma"

# Crear las carpetas de train y test si no existen
os.makedirs(test_folder, exist_ok=True)
os.makedirs(train_folder, exist_ok=True)

# Obtener nombres de archivos en test y train del otro modelo
test_files = set(os.listdir(test_folder))
other_train_files = set(os.listdir(other_train_folder))

# Filtrar archivos en total que no estén en test ni en el train del otro modelo
eligible_for_test = [
    file_name for file_name in os.listdir(total_folder)
    if file_name not in test_files and file_name not in other_train_files
]

# Seleccionar aleatoriamente 204 imágenes para test
if len(eligible_for_test) >= 64:
    selected_for_test = random.sample(eligible_for_test, 64)
else:
    raise ValueError("No hay suficientes imágenes elegibles para mover al test.")

# Mover las imágenes seleccionadas a la carpeta de test
for file_name in selected_for_test:
    shutil.move(
        os.path.join(total_folder, file_name),
        os.path.join(test_folder, file_name)
    )

# Mover todas las imágenes restantes a la carpeta de train
for file_name in os.listdir(total_folder):
    if file_name not in selected_for_test:
        shutil.move(
            os.path.join(total_folder, file_name),
            os.path.join(train_folder, file_name)
        )

print(f"Proceso completado.")
print(f"204 imágenes movidas a {test_folder}.")
print(f"El resto de las imágenes movidas a {train_folder}.")
