from PIL import Image, ImageOps
import numpy as np
import cv2

def apply_rgb_filter(image, r_factor, g_factor, b_factor):
    image_np = np.array(image)
    image_np[..., 0] = image_np[..., 0] * r_factor  # Red channel
    image_np[..., 1] = image_np[..., 1] * g_factor  # Green channel
    image_np[..., 2] = image_np[..., 2] * b_factor  # Blue channel
    return Image.fromarray(image_np)

def apply_kuning(image):
    return apply_rgb_filter(image, 1.0, 1.0, 0.0)

def apply_orange(image):
    return apply_rgb_filter(image, 1.0, 0.5, 0.0)

def apply_cyan(image):
    return apply_rgb_filter(image, 0.0, 1.0, 1.0)

def apply_purple(image):
    return apply_rgb_filter(image, 0.5, 0.0, 0.5)

def apply_grey(image):
    return apply_rgb_filter(image, 0.5, 0.5, 0.5)

def apply_coklat(image):
    return apply_rgb_filter(image, 0.6, 0.4, 0.2)

def apply_merah(image):
    return apply_rgb_filter(image, 1.0, 0.0, 0.0)

def convert_to_average(image):
    image_np = np.array(image)
    # Rata-rata dari tiga channel warna
    average = np.mean(image_np, axis=2).astype(np.uint8)
    return Image.fromarray(average)

def convert_to_lightness(image):
    image_np = np.array(image)
    # Lightness: rata-rata nilai min dan max dari R, G, B
    lightness = (np.max(image_np, axis=2) + np.min(image_np, axis=2)) / 2
    return Image.fromarray(lightness.astype(np.uint8))

def convert_to_luminance(image):
    image_np = np.array(image)
    # Luminance: menggunakan rumus perceptual weighting
    luminance = (0.299 * image_np[..., 0] + 0.587 * image_np[..., 1] + 0.114 * image_np[..., 2]).astype(np.uint8)
    return Image.fromarray(luminance)

def adjust_saturation(image, saturation_factor):
    """
    Mengubah saturasi gambar.
    :param image: Gambar dalam format PIL
    :param saturation_factor: Nilai faktor saturasi
    :return: Gambar yang telah diubah saturasinya
    """
    image_np = np.array(image)
    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    hsv[..., 1] = hsv[..., 1] * saturation_factor
    enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return Image.fromarray(enhanced)

def adjust_contrast(image, contrast_factor):
    """
    Mengubah kontras gambar.
    :param image: Gambar dalam format PIL
    :param contrast_factor: Nilai faktor kontras
    :return: Gambar yang telah diubah kontrasnya
    """
    image_np = np.array(image)
    enhanced = cv2.convertScaleAbs(image_np, alpha=contrast_factor, beta=0)
    return Image.fromarray(enhanced)

def adjust_brightness(image, brightness_factor):
    """
    Mengubah kecerahan gambar.
    :param image: Gambar dalam format PIL
    :param brightness_factor: Nilai faktor kecerahan
    :return: Gambar yang telah diubah kecerahannya
    """
    image_np = np.array(image)
    enhanced = cv2.convertScaleAbs(image_np, alpha=1, beta=brightness_factor)
    return Image.fromarray(enhanced)

def apply_bit_depth(image, bit_depth):
    # Ubah gambar PIL ke array NumPy
    image_np = np.array(image)
    
    # Normalisasi nilai pixel gambar ke rentang [0, 1]
    image_normalized = image_np / 255.0
    
    # Hitung jumlah level berdasarkan bit depth
    num_levels = 2 ** bit_depth
    
    # Skala nilai pixel gambar ke rentang [0, num_levels - 1]
    image_scaled = np.floor(image_normalized * (num_levels - 1))
    
    # Skala kembali nilai pixel gambar ke rentang [0, 255]
    image_quantized = (image_scaled / (num_levels - 1) * 255).astype(np.uint8)
    
    return Image.fromarray(image_quantized)

def apply_invers(image):
    # Aplikasi inversi gambar
    image_np = np.array(image)
    inversed_image = ImageOps.invert(image)
    return inversed_image

def apply_log_brightness(image):
    # Aplikasi log brightness
    image_np = np.array(image)
    image_np = np.float32(image_np)  # Convert to float32 for log operation
    image_np = np.log1p(image_np)  # Apply log transformation
    image_np = cv2.normalize(image_np, None, 0, 255, cv2.NORM_MINMAX)  # Normalize back to [0, 255]
    image_np = np.uint8(image_np)
    return Image.fromarray(image_np)

def apply_gamma_correction(image, gamma=1.0):
    # Aplikasi gamma correction
    image_np = np.array(image)
    inv_gamma = 1.0 / gamma
    image_np = np.float32(image_np)  # Convert to float32 for gamma correction
    image_np = np.power(image_np / 255.0, inv_gamma) * 255.0
    image_np = np.uint8(image_np)
    return Image.fromarray(image_np)