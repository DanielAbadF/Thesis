import os
from PIL import Image, UnidentifiedImageError
from multiprocessing import Pool

def flip_image(args):
    img_path, output_dir = args
    file_name = os.path.basename(img_path)

    try:
        img = Image.open(img_path)
    except UnidentifiedImageError:
        print(f"Error: Cannot identify image file {img_path}. Skipping.")
        return

    # Archivos de salida
    flip_x_file_name = f"{os.path.splitext(file_name)[0]}_flip_x.jpg"
    flip_y_file_name = f"{os.path.splitext(file_name)[0]}_flip_y.jpg"
    _90degfp_name = f"{os.path.splitext(file_name)[0]}_flip_90.jpg"
    _180degfp_name = f"{os.path.splitext(file_name)[0]}_flip_180.jpg"
    _270degfp_name = f"{os.path.splitext(file_name)[0]}_flip_270.jpg"
    flip_x_path = os.path.join(output_dir, flip_x_file_name)
    flip_y_path = os.path.join(output_dir, flip_y_file_name)

    # Verificar si las imágenes ya han sido procesadas
    if os.path.exists(flip_x_path) and os.path.exists(flip_y_path):
        print(f"Skipping {file_name} - already processed.")
        return

    # Flip horizontal (sobre el eje X)
    flip_x = img.transpose(Image.FLIP_LEFT_RIGHT)
    flip_x.save(flip_x_path, "JPEG", quality=85)

    # Flip vertical (sobre el eje Y)
    flip_y = img.transpose(Image.FLIP_TOP_BOTTOM)
    flip_y.save(flip_y_path, "JPEG", quality=85)
    
    

    print(f"Processed {file_name} in {output_dir}")

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
            if file_name.endswith(".png"):
                img_path = os.path.join(subdir, file_name)
                args_list.append((img_path, new_subdir))
    
    with Pool(num_workers) as pool:
        pool.map(flip_image, args_list)

if __name__ == '__main__':
    # Ruta del dataset original
    original_dataset_dir = "C:/Thesis/Dataset4Classes2/train/mel"
    # Ruta para guardar el dataset aumentado
    augmented_dataset_dir = "C:/Thesis/AugMelEntr"

    augment_dataset_with_flip_parallel(original_dataset_dir, augmented_dataset_dir, num_workers=16)

