import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
from PIL import Image

def fuzzy_membership_function(x, mean, stddev):
    return np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

def fuzzy_histogram_equalization(image, block_size=16):
    """
    Menerapkan fuzzy histogram equalization pada gambar.
    """
    if len(image.shape) == 3:
        # Jika gambar dalam format RGB, konversi ke grayscale
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = image.shape
    equalized_image = np.zeros_like(image, dtype=np.uint8)

    # Ukuran blok
    block_height = block_size
    block_width = block_size

    for y in range(0, height, block_height):
        for x in range(0, width, block_width):
            # Tentukan batas blok
            y_end = min(y + block_height, height)
            x_end = min(x + block_width, width)
            block = image[y:y_end, x:x_end]

            if block.size == 0:
                continue

            # Hitung histogram lokal
            hist, bins = np.histogram(block.flatten(), bins=256, range=[0, 256])
            cdf = hist.cumsum()
            cdf_normalized = cdf * 255 / cdf[-1]  # Normalisasi CDF ke rentang 0-255

            # Equalisasi blok menggunakan CDF
            equalized_block = np.interp(block.flatten(), bins[:-1], cdf_normalized).reshape(block.shape)

            # Hitung keanggotaan fuzzy
            mean = np.mean(equalized_block)
            stddev = np.std(equalized_block)
            membership = fuzzy_membership_function(equalized_block, mean, stddev)

            # Normalisasi membership ke rentang [0, 1]
            membership_normalized = (membership - np.min(membership)) / (np.max(membership) - np.min(membership))

            # Terapkan penyesuaian kontras fuzzy
            adjusted_block = np.clip(equalized_block * membership_normalized, 0, 255).astype(np.uint8)

            # Tempel hasil blok yang sudah diproses ke gambar hasil akhir
            equalized_image[y:y_end, x:x_end] = adjusted_block

    return equalized_image

def apply_fuzzy_he_rgb(value):
    """
    Terapkan rumus Fuzzy HE RGB:
    - Jika value < 128: 2 * (value^2) / 255
    - Jika value >= 128: 255 - 2 * (255 - value)^2 / 255
    """
    if value < 128:
        return int(2 * (value ** 2) / 255.0)
    else:
        return int(255 - 2 * ((255 - value) ** 2) / 255.0)
  
def fuzzy_histogram_equalization_rgb(main_window):
    """
    Fungsi ini menerima instance dari main_window untuk mengakses originalImageLabel dan processedImageLabel.
    """
    # Pastikan gambar di QLabel original ada (tidak None)
    if main_window.originalImageLabel.pixmap() is not None:
        # Konversi gambar dari QPixmap di originalImageLabel ke QImage
        input_image = main_window.originalImageLabel.pixmap().toImage()
        width = input_image.width()
        height = input_image.height()

        # Buat QImage untuk output
        output_image = QImage(width, height, QImage.Format_RGB32)

        # Proses setiap piksel secara manual
        for y in range(height):
            for x in range(width):
                # Ambil piksel dari input_image
                pixel_color = input_image.pixel(x, y)
                color = QColor(pixel_color)

                # Ambil nilai R, G, B
                r = apply_fuzzy_he_rgb(color.red())
                g = apply_fuzzy_he_rgb(color.green())
                b = apply_fuzzy_he_rgb(color.blue())

                # Set piksel hasil ke output_image
                output_image.setPixel(x, y, QColor(r, g, b).rgb())

        # Tampilkan gambar hasil edit di label processedImageLabel
        main_window.processedImageLabel.setPixmap(QPixmap.fromImage(output_image).scaled(
        main_window.processedImageLabel.size(), Qt.KeepAspectRatio))
  
def display_image(image, label):
    """
    Fungsi untuk menampilkan gambar di QLabel dengan memastikan gambar berada di tengah.
    
    :param image: Gambar dalam format PIL Image, NumPy array, atau QImage.
    :param label: QLabel tempat gambar akan ditampilkan.
    """
    # Jika gambar dalam format PIL Image, konversi ke array NumPy
    if isinstance(image, Image.Image):
        image = np.array(image)
    
    # Jika gambar dalam format NumPy array, konversi ke QImage
    if isinstance(image, np.ndarray):
        if len(image.shape) == 3 and image.shape[2] == 3:
            # Format RGB
            format = QImage.Format_RGB888
        elif len(image.shape) == 2:
            # Format Grayscale
            format = QImage.Format_Grayscale8
        else:
            raise ValueError("Format gambar tidak didukung.")
        
        qimage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], format)
    elif isinstance(image, QImage):
        # Jika gambar sudah dalam format QImage, langsung gunakan
        qimage = image
    else:
        raise TypeError("Tipe gambar tidak dikenali. Harus berupa PIL Image, NumPy array, atau QImage.")
    
    # Buat QPixmap dari QImage
    pixmap = QPixmap.fromImage(qimage)
    
    # Resize gambar jika lebih besar dari ukuran label
    max_width = 820
    max_height = 800
    pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    # Buat QPixmap dengan ukuran label
    label_pixmap = QPixmap(label.size())
    label_pixmap.fill(Qt.white)  # Set background putih jika diperlukan
    
    # Gambar gambar pada QPixmap label_pixmap dengan posisi tengah
    painter = QPainter(label_pixmap)
    painter.drawPixmap(
        (label_pixmap.width() - pixmap.width()) // 2,  # X posisi
        (label_pixmap.height() - pixmap.height()) // 2, # Y posisi
        pixmap
    )
    painter.end()
    
    # Set pixmap label
    label.setPixmap(label_pixmap)
    label.adjustSize()
    
def resize_image(image, max_width, max_height):
    """
    Fungsi untuk meresize gambar.
    """
    if isinstance(image, np.ndarray):
        image = Image.fromarray(image)
    width, height = image.size
    ratio = min(max_width / width, max_height / height)
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    return image.resize((new_width, new_height), Image.LANCZOSf)