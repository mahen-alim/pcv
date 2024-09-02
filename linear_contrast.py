from PIL import Image
import numpy as np

def linear_contrast(input_image, contrast_factor):
    img_np = np.array(input_image, dtype=np.float32)
    img_np = img_np * contrast_factor
    img_np = np.clip(img_np, 0, 255).astype(np.uint8)
    return Image.fromarray(img_np)

# def show_images(input_image_path, output_image_path):
#     # Membuka gambar input dan output
#     input_img = Image.open(input_image_path)
#     output_img = Image.open(output_image_path)
    
#     # Membuat plot untuk menampilkan gambar
#     fig, axes = plt.subplots(1, 2, figsize=(12, 6))
#     axes[0].imshow(input_img)
#     axes[0].set_title("Input Image")
#     axes[0].axis('off')

#     axes[1].imshow(output_img)
#     axes[1].set_title("Output Image")
#     axes[1].axis('off')

#     plt.show()

# # Contoh penggunaan
# input_image_path = os.path.join('img', 'klambi.jpg')
# output_image_path = os.path.join('img', 'klambi_output.jpg')
# linear_contrast(input_image_path, output_image_path, 1.2)
