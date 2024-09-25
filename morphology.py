# morphology.py

import numpy as np
import cv2
from PIL import Image

def pros_morphology(original_image, operation, shape, size):
    """Terapkan operasi morfologi berdasarkan input"""
    if original_image is None:
        print("Error: Gambar asli tidak ditemukan.")
        return None

    # Konversi gambar ke format NumPy dengan warna (RGB)
    image = np.array(original_image)

    # Definisikan kernel berdasarkan bentuk dan ukuran
    if shape == 'square':
        kernel = np.ones((size, size), np.uint8)
    elif shape == 'cross':
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (size, size))
    else:
        print("Error: Bentuk kernel tidak valid.")
        return None

    # Pisahkan gambar menjadi 3 channel warna (RGB)
    channels = cv2.split(image)

    # Simpan hasil operasi untuk setiap channel
    result_channels = []

    for channel in channels:
        # Terapkan operasi morfologi yang sesuai pada setiap channel
        if operation == 'erosion':
            result_channel = cv2.erode(channel, kernel, iterations=1)
        elif operation == 'dilation':
            result_channel = cv2.dilate(channel, kernel, iterations=1)
        elif operation == 'opening':
            result_channel = cv2.morphologyEx(channel, cv2.MORPH_OPEN, kernel)
        elif operation == 'closing':
            result_channel = cv2.morphologyEx(channel, cv2.MORPH_CLOSE, kernel)
        else:
            print("Error: Operasi morfologi tidak valid.")
            return None

        result_channels.append(result_channel)

    # Gabungkan kembali hasil dari setiap channel
    result = cv2.merge(result_channels)

    # Kembalikan gambar hasil sebagai objek PIL
    return Image.fromarray(result)
