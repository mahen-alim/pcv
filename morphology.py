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
        elif operation == 'hit-or-miss':
            # Hit-or-miss transform
            result_channel = cv2.morphologyEx(channel, cv2.MORPH_HITMISS, kernel)
        elif operation == 'boundary-extraction':
            # Boundary extraction: Original - Erosion
            eroded = cv2.erode(channel, kernel, iterations=1)
            result_channel = cv2.subtract(channel, eroded)
        elif operation == 'region-filling':
            # Region filling: Dilasi dan AND dengan mask
            result_channel = region_filling(channel, kernel)
        elif operation == 'thinning':
            # Thinning (penipisan) menggunakan cv2.ximgproc.thinning
            result_channel = cv2.ximgproc.thinning(channel)
        elif operation == 'skeletonization':
            # Skeletonization
            result_channel = skeletonization(channel)
        else:
            print("Error: Operasi morfologi tidak valid.")
            return None

        result_channels.append(result_channel)

    # Gabungkan kembali hasil dari setiap channel
    result = cv2.merge(result_channels)

    # Kembalikan gambar hasil sebagai objek PIL
    return Image.fromarray(result)

def region_filling(image, kernel):
    """Region Filling menggunakan dilasi berulang"""
    inverted_image = cv2.bitwise_not(image)
    filled_image = np.zeros_like(image)
    prev_filled_image = filled_image.copy()

    # Iterasi hingga gambar yang diisi berhenti berubah
    while True:
        filled_image = cv2.dilate(filled_image, kernel, iterations=1)
        filled_image = cv2.bitwise_and(filled_image, inverted_image)

        if np.array_equal(filled_image, prev_filled_image):
            break
        prev_filled_image = filled_image.copy()

    return cv2.bitwise_not(filled_image)

def skeletonization(image):
    """Skeletonization menggunakan iterasi dilasi dan erosi"""
    skeleton = np.zeros_like(image)
    eroded = np.copy(image)
    temp = np.zeros_like(image)

    while True:
        eroded = cv2.erode(eroded, cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)))
        temp = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3)))
        temp = cv2.subtract(image, temp)
        skeleton = cv2.bitwise_or(skeleton, temp)
        image = eroded.copy()

        if cv2.countNonZero(image) == 0:
            break

    return skeleton
