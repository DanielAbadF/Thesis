import os
import cv2
import numpy as np
from multiprocessing import Pool
import random

def translate_image(args):
    img_path, output_dir, num_translations = args
    file_name = os.path.basename(img_path)
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        print(f"Error: Cannot identify image file {img_path}")
        return

    h, w = img.shape[:2]

    for i in range(num_translations):
        # Generate random translation values for x and y within the range [-15, 15]
        tx = random.randint(-30, 30)
        ty = random.randint(-30, 30)
        new_file_name = f"{os.path.splitext(file_name)[0]}_trans{tx}_{ty}.jpg"  # Save as JPEG
        output_path = os.path.join(output_dir, new_file_name)

        if os.path.exists(output_path):
            print(f"Skipping translation for {file_name} at (tx: {tx}, ty: {ty}), already exists.")
            continue

        # Create the translation matrix and apply the translation
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        translated_img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)

        # Guardar con compresión (JPEG)
        cv2.imwrite(output_path, translated_img, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        print(f"Processed {file_name} with translation (tx: {tx}, ty: {ty})")

def augment_dataset_parallel(original_dir, augmented_dir, num_translations=10, num_workers=4):
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
                args_list.append((img_path, new_subdir, num_translations))
    
    with Pool(num_workers) as pool:
        pool.map(translate_image, args_list)

if __name__ == '__main__':
    original_dir = "C:/Thesis/escamososEntr"
    augmented_dir = "C:/Thesis/TransScc"

    augment_dataset_parallel(original_dir, augmented_dir, num_translations=4, num_workers=16)
