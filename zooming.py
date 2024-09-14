import numpy as np
import cv2

# Fungsi untuk zoom gambar
def zooming(image, scale):
    """
    Fungsi untuk melakukan zoom in atau zoom out pada gambar dengan skala tertentu.

    Parameters:
    - image: Gambar input dalam format numpy array (RGB atau grayscale).
    - scale: Faktor skala zoom (harus > 0). Skala > 1 untuk zoom in, skala < 1 untuk zoom out.

    Returns:
    - zoomed_image: Gambar hasil zoom.
    """
    # Validasi input gambar
    if image is None or not isinstance(image, np.ndarray):
        raise ValueError("Gambar input tidak valid. Harus berupa array numpy.")
    
    if scale <= 0:
        raise ValueError("Skala harus lebih besar dari 0.")

    # Menghitung ukuran baru gambar berdasarkan skala
    height, width = image.shape[:2]
    new_height = int(height * scale)
    new_width = int(width * scale)

    # Pastikan ukuran baru tidak terlalu kecil
    if new_height < 1 or new_width < 1:
        raise ValueError("Ukuran gambar hasil terlalu kecil dengan skala ini.")

    # Mengubah ukuran gambar menggunakan OpenCV dengan interpolasi linier
    zoomed_image = cv2.resize(image, (new_width, new_height), interpolation=cv2.INTER_LINEAR)
    
    return zoomed_image

# Membaca gambar
image = cv2.imread('img/klambi.jpg')

# Zoom in (misalnya dengan skala 2x)
zoomed_in_image = zooming(image, 2)

# Zoom out (misalnya dengan skala 0.5x)
zoomed_out_image = zooming(image, 0.5)

# Menampilkan gambar hasil zoom
cv2.imshow("Zoomed In", zoomed_in_image)
cv2.imshow("Zoomed Out", zoomed_out_image)
cv2.waitKey(0)
cv2.destroyAllWindows()