import cv2
import numpy as np
from PIL import Image
from PyQt5.QtWidgets import (QLabel, QMessageBox)
from PyQt5.QtCore import Qt, QRect, QSize
from PyQt5.QtGui import QPainter, QImage, QPixmap

def convert_cv_to_pil(image_np):
    # Konversi dari OpenCV (BGR) ke PIL.Image (RGB)
    return Image.fromarray(cv2.cvtColor(image_np, cv2.IMREAD_COLOR))

# Fungsi untuk translasi gambar
def translation(image_np, tx=100, ty=50):
    rows, cols = image_np.shape[:2]
    
    # Matriks translasi (tx, ty) untuk memindahkan gambar
    translation_matrix = np.float32([[1, 0, tx], [0, 1, ty]])
    
    translated_image = cv2.warpAffine(image_np, translation_matrix, (cols, rows))
    return translated_image

# Fungsi untuk rotasi gambar
def rotation(image_np, angle=45):
    rows, cols = image_np.shape[:2]
    
    # Titik tengah untuk rotasi
    center = (cols // 2, rows // 2)
    
    # Matriks rotasi dengan sudut tertentu
    rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1)
    
    rotated_image = cv2.warpAffine(image_np, rotation_matrix, (cols, rows))
    return rotated_image

# Fungsi untuk flipping gambar
def flipping(image_np, flip_code=1):
    # Flip code: 1 = Horizontal, 0 = Vertikal, -1 = Keduanya
    flipped_image = cv2.flip(image_np, flip_code)
    return flipped_image

def display_image_zoom(image, label):
        # Mengatur ukuran label sesuai dengan ukuran gambar
        width, height = image.size
        label.setFixedSize(QSize(width, height))

        # Konversi gambar ke format QImage
        image_np = np.array(image)
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            format = QImage.Format_RGB888
        else:
            format = QImage.Format_Grayscale8

        qimage = QImage(image_np.data, image_np.shape[1], image_np.shape[0], image_np.strides[0], format)
        pixmap = QPixmap.fromImage(qimage)

        # Buat QPixmap yang cukup besar untuk menampung gambar
        label_pixmap = QPixmap(label.size())
        label_pixmap.fill(Qt.white)  # Set background putih

        # Gambar pada label_pixmap dengan posisi tengah
        painter = QPainter(label_pixmap)
        painter.drawPixmap(
            (label_pixmap.width() - pixmap.width()) // 2,  # X posisi
            (label_pixmap.height() - pixmap.height()) // 2, # Y posisi
            pixmap
        )
        painter.end()

        # Set pixmap label
        label.setPixmap(label_pixmap)


class CroppableLabel(QLabel):
    def __init__(self, parent=None):
        super(CroppableLabel, self).__init__(parent)
        self.start_pos = None
        self.end_pos = None
        self.parent_window = parent  # Reference to the MainWindow
        self.cropping_enabled = False  # State for cropping mode

    def enable_cropping(self):
        """Enable cropping mode and change cursor to cross."""
        self.cropping_enabled = True
        self.setCursor(Qt.CrossCursor)  # Set cursor to cross when cropping is enabled

    def disable_cropping(self):
        """Disable cropping mode and change cursor to default."""
        self.cropping_enabled = False
        self.setCursor(Qt.ArrowCursor)  # Set cursor to default when cropping is disabled

    def mousePressEvent(self, event):
        if self.cropping_enabled and event.button() == Qt.LeftButton:
            self.start_pos = event.pos()  # Start dragging
            self.end_pos = None  # Reset end position
            self.update()

    def mouseMoveEvent(self, event):
        if self.cropping_enabled and event.buttons() & Qt.LeftButton:
            self.end_pos = event.pos()  # Update end position during dragging
            self.update()

    def mouseReleaseEvent(self, event):
        if self.cropping_enabled and event.button() == Qt.LeftButton:
            self.end_pos = event.pos()  # End dragging
            if self.start_pos == self.end_pos:
                # If no area was dragged, show a warning message
                QMessageBox.warning(self, "Peringatan", "Anda harus mendrag bagian gambar tertentu untuk melakukan cropping.")
            else:
                self.update()
                self.parent_window.perform_cropping(self.start_pos, self.end_pos)

    def paintEvent(self, event):
        super(CroppableLabel, self).paintEvent(event)
        if self.start_pos and self.end_pos and self.cropping_enabled:
            painter = QPainter(self)
            painter.setPen(Qt.red)
            rect = QRect(self.start_pos, self.end_pos)
            painter.drawRect(rect.normalized())  # Draw rectangle for selection
      