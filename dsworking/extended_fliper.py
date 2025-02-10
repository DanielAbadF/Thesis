import os
from PIL import Image, UnidentifiedImageError
from multiprocessing import Pool

def augment_image(args):
    img_path, output_dir = args
    file_name = os.path.basename(img_path)

    try:
        img = Image.open(img_path)
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file {img_path}. Skipping.")
        return

    # Lista de transformaciones: nombre y la función que la realiza sobre la imagen.
    # Nota: para las rotaciones, usamos rotate(angulo, expand=True) para evitar el recorte.
    transformations = [
        ("flip_x",  lambda x: x.transpose(Image.FLIP_LEFT_RIGHT)),
        ("flip_y",  lambda x: x.transpose(Image.FLIP_TOP_BOTTOM)),
        ("rot_90",  lambda x: x.rotate(90, expand=True)),
        ("rot_180", lambda x: x.rotate(180, expand=True)),
        ("rot_270", lambda x: x.rotate(270, expand=True))
    ]

    for transform_name, transform_func in transformations:
        # Construimos el nombre de salida según la transformación
        out_file_name = f"{os.path.splitext(file_name)[0]}_{transform_name}.jpg"
        out_path = os.path.join(output_dir, out_file_name)

        # Verifica si ya existe para evitar reprocesarlo
        if os.path.exists(out_path):
            print(f"Skipping {file_name} - {transform_name} already processed.")
            continue

        # Aplica la transformación y guarda el resultado
        transformed_img = transform_func(img)
        transformed_img.save(out_path, "JPEG", quality=85)
        print(f"Processed {file_name} -> {transform_name} in {output_dir}")

def augment_dataset_with_flip_parallel(original_dir, augmented_dir, num_workers=16):
    if not os.path.exists(augmented_dir):
        os.makedirs(augmented_dir)

    args_list = []
    for subdir, _, files in os.walk(original_dir):
        subdir_name = os.path.relpath(subdir, original_dir)
        new_subdir = os.path.join(augmented_dir, subdir_name)
        if not os.path.exists(new_subdir):
            os.makedirs(new_subdir)

        for file_name in files:
            # Ajusta la extensión según tu dataset (PNG, JPG, etc.)
            if file_name.lower().endswith(".png"):
                img_path = os.path.join(subdir, file_name)
                args_list.append((img_path, new_subdir))
    
    with Pool(num_workers) as pool:
        pool.map(augment_image, args_list)

if __name__ == '__main__':
    # Ruta del dataset original
    original_dataset_dir = "C:/Thesis/Dataset4Classes2/esc"
    # Ruta para guardar el dataset aumentado
    augmented_dataset_dir = "C:/Tesis/Dataset4Classes2/augscc"

    augment_dataset_with_flip_parallel(original_dataset_dir, augmented_dataset_dir, num_workers=16)
