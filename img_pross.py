import cv2
import numpy as np
from PyQt5.QtGui import QImage, QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt
from PIL import Image

def apply_histogram_equalization(image):
    """
    Menerapkan histogram equalization pada gambar grayscale.
    """
    # Konversi ke grayscale jika gambar dalam format RGB
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Equalisasi histogram
    equalized_image = cv2.equalizeHist(image)

    return equalized_image

def convert_to_qimage(image):
    """
    Mengonversi array numpy menjadi QImage untuk menampilkannya di QLabel.
    """
    if image.ndim == 2:  # Grayscale
        qimage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
    elif image.ndim == 3:  # RGB
        qimage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888)
    return qimage

def fuzzy_membership_function(x, mean, stddev):
    return np.exp(-((x - mean) ** 2) / (2 * (stddev ** 2)))

def fuzzy_histogram_equalization(image, block_size=3336):
    """
    Menerapkan fuzzy histogram equalization pada gambar grayscale.
    """
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    height, width = image.shape
    equalized_image = np.zeros_like(image, dtype=np.uint8)

    block_height = block_size
    block_width = block_size

    for y in range(0, height, block_height):
        for x in range(0, width, block_width):
            y_end = min(y + block_height, height)
            x_end = min(x + block_width, width)
            block = image[y:y_end, x:x_end]

            if block.size == 0:
                continue

            hist, bins = np.histogram(block.flatten(), bins=256, range=[0, 256])
            cdf = hist.cumsum()
            cdf_normalized = cdf * 255 / cdf[-1]

            equalized_block = np.interp(block.flatten(), bins[:-1], cdf_normalized).reshape(block.shape)

            mean = np.mean(equalized_block)
            stddev = np.std(equalized_block)
            membership = fuzzy_membership_function(equalized_block, mean, stddev)

            membership_normalized = (membership - np.min(membership)) / (np.max(membership) - np.min(membership))

            adjusted_block = np.clip(equalized_block * membership_normalized, 0, 255).astype(np.uint8)

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
    if main_window.originalImageLabel.pixmap() is not None:
        input_image = main_window.originalImageLabel.pixmap().toImage()
        width = input_image.width()
        height = input_image.height()

        output_image = QImage(width, height, QImage.Format_RGB32)

        for y in range(height):
            for x in range(width):
                pixel_color = input_image.pixel(x, y)
                color = QColor(pixel_color)

                r = apply_fuzzy_he_rgb(color.red())
                g = apply_fuzzy_he_rgb(color.green())
                b = apply_fuzzy_he_rgb(color.blue())

                output_image.setPixel(x, y, QColor(r, g, b).rgb())

        main_window.processedImageLabel.setPixmap(QPixmap.fromImage(output_image).scaled(
            main_window.processedImageLabel.size(), Qt.KeepAspectRatio))

def display_image(image, label):
    """
    Fungsi untuk menampilkan gambar di QLabel dengan memastikan gambar berada di tengah.
    """
    if isinstance(image, Image.Image):
        image = np.array(image)

    if isinstance(image, np.ndarray):
        if len(image.shape) == 3 and image.shape[2] == 3:
            format = QImage.Format_RGB888
        elif len(image.shape) == 2:
            format = QImage.Format_Grayscale8
        else:
            raise ValueError("Format gambar tidak didukung.")
        
        qimage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], format)
    elif isinstance(image, QImage):
        qimage = image
    else:
        raise TypeError("Tipe gambar tidak dikenali. Harus berupa PIL Image, NumPy array, atau QImage.")
    
    pixmap = QPixmap.fromImage(qimage)
    
    max_width = 820
    max_height = 800
    pixmap = pixmap.scaled(max_width, max_height, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    
    label_pixmap = QPixmap(label.size())
    label_pixmap.fill(Qt.white)
    
    painter = QPainter(label_pixmap)
    painter.drawPixmap(
        (label_pixmap.width() - pixmap.width()) // 2,
        (label_pixmap.height() - pixmap.height()) // 2,
        pixmap
    )
    painter.end()
    
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
    return image.resize((new_width, new_height), Image.LANCZOS)
