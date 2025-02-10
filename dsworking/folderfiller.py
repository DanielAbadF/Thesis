import os
from PIL import Image, UnidentifiedImageError
from multiprocessing import Pool

def augment_image_in_place(img_path):
    try:
        img = Image.open(img_path)
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file {img_path}. Skipping.")
        return

    base_name, ext = os.path.splitext(img_path)
    ext = ext.lower() if ext.lower() in ['.jpg', '.jpeg', '.png'] else '.jpg'

    # Flip horizontal (sobre el eje X)
    flip_x_file_name = f"{base_name}_flip_x{ext}"
    if not os.path.exists(flip_x_file_name):
        flip_x = img.transpose(Image.FLIP_LEFT_RIGHT)
        flip_x.save(flip_x_file_name, quality=85)

    # Flip vertical (sobre el eje Y)
    flip_y_file_name = f"{base_name}_flip_y{ext}"
    if not os.path.exists(flip_y_file_name):
        flip_y = img.transpose(Image.FLIP_TOP_BOTTOM)
        flip_y.save(flip_y_file_name, quality=85)

    # Rotaciones
    for angle in [90, 180, 270]:
        rotated_file_name = f"{base_name}_rot_{angle}{ext}"
        if not os.path.exists(rotated_file_name):
            rotated = img.rotate(angle, expand=True)
            rotated.save(rotated_file_name, quality=85)

    print(f"Processed: {img_path}")

def augment_dataset_in_place(original_dir, target_count, num_workers=16):
    # Obtener todas las imágenes en el dataset
    all_files = []
    for subdir, _, files in os.walk(original_dir):
        for file_name in files:
            if file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                all_files.append(os.path.join(subdir, file_name))

    # Paso 1: Realizar aumentación en paralelo
    print("Starting augmentation in place...")
    with Pool(num_workers) as pool:
        pool.map(augment_image_in_place, all_files)

    # Paso 2: Contar imágenes generadas
    current_image_count = sum(len(files) for _, _, files in os.walk(original_dir))

    # Paso 3: Repetir aumentación si es necesario
    while current_image_count < target_count:
        print(f"Insufficient images ({current_image_count}). Augmenting further...")
        additional_files = [file for file in all_files if "_flip" in file or "_rot" in file]
        with Pool(num_workers) as pool:
            pool.map(augment_image_in_place, additional_files)
        current_image_count = sum(len(files) for _, _, files in os.walk(original_dir))

    print(f"Augmentation completed. Total images: {current_image_count}")

if __name__ == '__main__':
    # Ruta del dataset original
    original_dataset_dir = "C:/Tesis/images"
    # Número objetivo de imágenes
    target_image_count = 15000

    augment_dataset_in_place(original_dataset_dir, target_image_count, num_workers=16)
