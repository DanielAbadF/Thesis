import os
import cv2
import numpy as np
from multiprocessing import Pool

def rotate_image(args):
    img_path, output_dir, rotation_step = args
    file_name = os.path.basename(img_path)
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)

    if img is None:
        print(f"Error: Cannot identify image file {img_path}")
        return

    h, w = img.shape[:2]
    center = (w // 2, h // 2)

    for angle in range(0, 360, rotation_step):
        new_file_name = f"{os.path.splitext(file_name)[0]}_rot{angle}.jpg"  # Save as JPEG
        output_path = os.path.join(output_dir, new_file_name)

        if os.path.exists(output_path):
            print(f"Skipping rotation for {file_name} at {angle} degrees, already exists.")
            continue

        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated_img = cv2.warpAffine(img, M, (w, h), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
        rotated_img = crop_to_original_size(rotated_img, M, w, h)

        # Guardar con compresión (JPEG)
        cv2.imwrite(output_path, rotated_img, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
        print(f"Processed {file_name} at {angle} degrees")

def crop_to_original_size(rotated_img, M, w, h):
    M_inv = cv2.invertAffineTransform(M)
    corners = np.array([[0, 0], [w, 0], [0, h], [w, h]])
    transformed_corners = cv2.transform(np.array([corners]), M_inv)[0]

    min_x = max(0, np.min(transformed_corners[:, 0]))
    max_x = min(w, np.max(transformed_corners[:, 0]))
    min_y = max(0, np.min(transformed_corners[:, 1]))
    max_y = min(h, np.max(transformed_corners[:, 1]))

    cropped_img = rotated_img[int(min_y):int(max_y), int(min_x):int(max_x)]
    return cropped_img

def augment_dataset_parallel(original_dir, augmented_dir, rotation_step=10, num_workers=4):
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
                args_list.append((img_path, new_subdir, rotation_step))
    
    with Pool(num_workers) as pool:
        pool.map(rotate_image, args_list)

if __name__ == '__main__':
    original_dataset_dir = "C:/Thesis/Dataset4Classes2/train/esc"
    augmented_dataset_dir = "C:/Tesis/Dataset4Classes2/augesc"

    augment_dataset_parallel(original_dataset_dir, augmented_dataset_dir, rotation_step=90, num_workers=16)
