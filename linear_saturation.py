# image_processing.py
from PIL import Image
import numpy as np

def linear_saturation(input_image, saturation_factor):
    # Memastikan input image adalah objek PIL.Image
    if not isinstance(input_image, Image.Image):
        raise TypeError("input_image harus berupa objek PIL.Image")

    # Mengubah gambar ke ruang warna HSV
    img_hsv = input_image.convert('HSV')
    img_hsv_np = np.array(img_hsv, dtype=np.float32)

    # Meningkatkan komponen saturasi (channel ke-1)
    img_hsv_np[..., 1] *= saturation_factor

    # Memastikan nilai piksel tetap dalam rentang [0, 255]
    img_hsv_np[..., 1] = np.clip(img_hsv_np[..., 1], 0, 255)

    # Mengubah array kembali ke gambar HSV
    img_hsv = Image.fromarray(img_hsv_np.astype(np.uint8), 'HSV')

    # Mengubah gambar HSV kembali ke RGB
    img_out = img_hsv.convert('RGB')

    return img_out

# # Contoh Penggunaan
# input_image_path = os.path.join('img', 'klambi.jpg')
# output_image_path = os.path.join('img', 'klambi_output.jpg')
# linear_saturation(input_image_path, output_image_path, 1.5)
