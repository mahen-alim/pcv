# main.py
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
from PIL import Image
from filter import (
    edge_detection_1, edge_detection_2, edge_detection_3,
    gaussian_blur, identity_filter, sharpen_filter,
    unsharp_masking_filter, average_filter, low_pass_filter,
    high_pass_filter, bandstop_filter
)

# Fungsi-fungsi filter yang digunakan
def linear_contrast(image, contrast_factor):
    # Konversi image PIL ke array NumPy
    image_np = np.array(image)
    # Aplikasi kontrast
    contrasted = cv2.convertScaleAbs(image_np, alpha=contrast_factor, beta=0)
    return contrasted

def linear_saturation(image, saturation_factor):
    # Aplikasi saturasi
    image_np = np.array(image)
    hsv = cv2.cvtColor(image_np, cv2.COLOR_RGB2HSV)
    hsv[..., 1] = hsv[..., 1] * saturation_factor
    enhanced = cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB)
    return Image.fromarray(enhanced)

def resize_image(image, max_width, max_height):
    width, height = image.size
    ratio = min(max_width / width, max_height / height)
    new_width = int(width * ratio)
    new_height = int(height * ratio)
    return image.resize((new_width, new_height), Image.LANCZOS)

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Set up the main window
        self.setWindowTitle("Image Filter Application")
        self.setGeometry(100, 100, 1200, 600)  # Adjusted size for better layout

        # Create a central widget to display the images
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Create a horizontal layout to place two labels side by side
        self.imageLayout = QHBoxLayout()
        self.layout.addLayout(self.imageLayout)

        # Label to show the original image
        self.originalImageLabel = QLabel(self)
        self.imageLayout.addWidget(self.originalImageLabel)

        # Label to show the processed image
        self.processedImageLabel = QLabel(self)
        self.imageLayout.addWidget(self.processedImageLabel)

        # Create the menu bar
        menubar = self.menuBar()

        # Create the File menu
        menuFile = menubar.addMenu('File')

        # Create actions for File menu
        self.actionOpenImage = QAction('Open Image', self)
        self.actionSaveAs = QAction('Save As', self)
        self.actionExit = QAction('Exit', self)

        # Add actions to File menu
        menuFile.addAction(self.actionOpenImage)
        menuFile.addAction(self.actionSaveAs)
        menuFile.addAction(self.actionExit)

        # Create the Filter menu
        menuFilter = menubar.addMenu('Filter')
        menuEdgeDetection = menuFilter.addMenu('Edge Detection')
        menuGaussianBlur = menuFilter.addMenu('Gaussian Blur')

        # Create actions for Edge Detection submenu
        self.actionEdgeDetection1 = QAction('Edge Detection 1', self)
        self.actionEdgeDetection2 = QAction('Edge Detection 2', self)
        self.actionEdgeDetection3 = QAction('Edge Detection 3', self)

        # Add actions to Edge Detection submenu
        menuEdgeDetection.addAction(self.actionEdgeDetection1)
        menuEdgeDetection.addAction(self.actionEdgeDetection2)
        menuEdgeDetection.addAction(self.actionEdgeDetection3)

        # Create actions for Gaussian Blur submenu
        self.actionGaussianBlur3x3 = QAction('Gaussian Blur 3x3', self)
        self.actionGaussianBlur3x5 = QAction('Gaussian Blur 3x5', self)

        # Add actions to Gaussian Blur submenu
        menuGaussianBlur.addAction(self.actionGaussianBlur3x3)
        menuGaussianBlur.addAction(self.actionGaussianBlur3x5)

        # Create additional filter actions
        self.actionIdentity = QAction('Identity', self)
        self.actionSharpen = QAction('Sharpen', self)
        self.actionUnsharpMasking = QAction('Unsharp Masking', self)
        self.actionAverageFilter = QAction('Average Filter', self)
        self.actionLowPassFilter = QAction('Low Pass Filter', self)
        self.actionHighPassFilter = QAction('High Pass Filter', self)
        self.actionBandstopFilter = QAction('Bandstop Filter', self)

        # Add additional filter actions to Filter menu
        menuFilter.addAction(self.actionIdentity)
        menuFilter.addAction(self.actionSharpen)
        menuFilter.addAction(self.actionUnsharpMasking)
        menuFilter.addAction(self.actionAverageFilter)
        menuFilter.addAction(self.actionLowPassFilter)
        menuFilter.addAction(self.actionHighPassFilter)
        menuFilter.addAction(self.actionBandstopFilter)

        # Create additional menu for linear contrast and saturation
        menuAdjustments = menubar.addMenu('Adjustments')

        # Create actions for linear contrast and saturation
        self.actionLinearContrast = QAction('Linear Contrast', self)
        self.actionLinearSaturation = QAction('Linear Saturation', self)

        # Add actions to Adjustments menu
        menuAdjustments.addAction(self.actionLinearContrast)
        menuAdjustments.addAction(self.actionLinearSaturation)

        # Connect actions to methods
        self.actionOpenImage.triggered.connect(self.open_image)
        self.actionSaveAs.triggered.connect(self.save_image)
        self.actionExit.triggered.connect(self.close)

        self.actionEdgeDetection1.triggered.connect(self.edge_detection_1)
        self.actionEdgeDetection2.triggered.connect(self.edge_detection_2)
        self.actionEdgeDetection3.triggered.connect(self.edge_detection_3)
        self.actionGaussianBlur3x3.triggered.connect(self.gaussian_blur_3x3)
        self.actionGaussianBlur3x5.triggered.connect(self.gaussian_blur_3x5)
        self.actionIdentity.triggered.connect(self.identity_filter)
        self.actionSharpen.triggered.connect(self.sharpen_filter)
        self.actionUnsharpMasking.triggered.connect(self.unsharp_masking_filter)
        self.actionAverageFilter.triggered.connect(self.average_filter)
        self.actionLowPassFilter.triggered.connect(self.low_pass_filter)
        self.actionHighPassFilter.triggered.connect(self.high_pass_filter)
        self.actionBandstopFilter.triggered.connect(self.bandstop_filter)
        self.actionLinearContrast.triggered.connect(self.linear_contrast_filter)
        self.actionLinearSaturation.triggered.connect(self.linear_saturation_filter)

        # Initialize image variables
        self.original_image = None
        self.processed_image = None

    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.bmp);;All Files (*)', options=options)
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.originalImageLabel)
            self.processed_image = None

    def save_image(self):
        if self.processed_image:
            options = QFileDialog.Options()
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save Image As', '', 'Images (*.png *.jpg *.bmp);;All Files (*)', options=options)
            if file_path:
                self.processed_image.save(file_path)
        else:
            QMessageBox.warning(self, 'No Image', 'No processed image to save.')

    def display_image(self, image, label):
        # Ukuran default
        max_width = 800
        max_height = 600

        # Ubah ukuran gambar jika melebihi ukuran maksimum
        resized_image = resize_image(image, max_width, max_height)

        # Konversi gambar PIL ke array NumPy
        image_np = np.array(resized_image)
        
        # Cek format gambar dan tentukan format QImage yang sesuai
        if len(image_np.shape) == 3 and image_np.shape[2] == 3:
            format = QImage.Format_RGB888
        else:
            format = QImage.Format_Grayscale8

        # Konversi array NumPy ke QImage
        qimage = QImage(image_np.data, image_np.shape[1], image_np.shape[0], image_np.strides[0], format)
        
        # Konversi QImage ke QPixmap
        pixmap = QPixmap.fromImage(qimage)
        
        # Tampilkan pixmap di label
        label.setPixmap(pixmap)


    def edge_detection_1(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = edge_detection_1(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def edge_detection_2(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = edge_detection_2(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def edge_detection_3(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = edge_detection_3(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def gaussian_blur_3x3(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = gaussian_blur(image_np, (3, 3))
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def gaussian_blur_3x5(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = gaussian_blur(image_np, (5, 5))
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def identity_filter(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = identity_filter(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def sharpen_filter(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = sharpen_filter(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def unsharp_masking_filter(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = unsharp_masking_filter(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def average_filter(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = average_filter(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def low_pass_filter(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = low_pass_filter(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def high_pass_filter(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = high_pass_filter(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def bandstop_filter(self):
        if self.original_image:
            image_np = np.array(self.original_image)
            processed_np = bandstop_filter(image_np)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def linear_contrast_filter(self):
        if self.original_image:
            contrast_factor = 1.5  # Example contrast factor
            image_np = np.array(self.original_image)
            processed_np = linear_contrast(self.original_image, contrast_factor)
            self.processed_image = Image.fromarray(processed_np)
            self.display_image(self.processed_image, self.processedImageLabel)

    def linear_saturation_filter(self):
        if self.original_image:
            saturation_factor = 1.5  # Example saturation factor
            processed_image = linear_saturation(self.original_image, saturation_factor)
            self.processed_image = processed_image
            self.display_image(self.processed_image, self.processedImageLabel)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())
