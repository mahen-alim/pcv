import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QFileDialog, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
from linear_contrast import linear_contrast
from linear_saturation import linear_saturation
from PIL import Image, ImageQt
# from PIL.ImageQt import ImageQt


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        # Set up the main window
        self.setWindowTitle("Image Filter Application")
        self.setGeometry(100, 100, 1000, 600)  # Adjusted size for better layout

        # Create a central widget to display the image
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Label to show the image
        self.imageLabel = QLabel(self)
        self.layout.addWidget(self.imageLabel)

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

         # Create additional menu for linear contrast and saturation
        menuAdjustments = menubar.addMenu('Adjustments')

        # Create actions for linear contrast and saturation
        self.actionLinearContrast = QAction('Linear Contrast', self)
        self.actionLinearSaturation = QAction('Linear Saturation', self)

        # Add actions to Adjustments menu
        menuAdjustments.addAction(self.actionLinearContrast)
        menuAdjustments.addAction(self.actionLinearSaturation)

        # Connect the actions to the corresponding methods
        self.actionLinearContrast.triggered.connect(self.apply_linear_contrast)
        self.actionLinearSaturation.triggered.connect(self.apply_linear_saturation)

        # Initialize image variables
        self.originalImage = None
        self.processedImage = None

    def open_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", 
                                                   "Images (*.png *.xpm *.jpg *.jpeg *.bmp);;All Files (*)", options=options)
        if file_name:
            self.originalImage = cv2.imread(file_name)
            self.processedImage = self.originalImage.copy()
            self.display_image(self.originalImage)

    def save_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Image As", "", 
                                                   "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)", options=options)
        if file_name:
            cv2.imwrite(file_name, self.processedImage)

    def display_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        height, width, channel = image_rgb.shape
        bytes_per_line = channel * width
        qt_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qt_image)
        self.imageLabel.setPixmap(pixmap)

    def apply_filter(self, kernel):
        if self.processedImage is not None:
            self.processedImage = cv2.filter2D(self.originalImage, -1, kernel)
            self.display_image(self.processedImage)

    def edge_detection_1(self):
        kernel = np.array([[-1, -1, -1],
                           [-1,  8, -1],
                           [-1, -1, -1]])
        self.apply_filter(kernel)

    def edge_detection_2(self):
        kernel = np.array([[1,  0, -1],
                           [0,  0,  0],
                           [-1, 0,  1]])
        self.apply_filter(kernel)

    def edge_detection_3(self):
        kernel = np.array([[0,  1,  0],
                           [1, -4,  1],
                           [0,  1,  0]])
        self.apply_filter(kernel)

    def gaussian_blur_3x3(self):
        self.processedImage = cv2.GaussianBlur(self.originalImage, (3, 3), 0)
        self.display_image(self.processedImage)

    def gaussian_blur_3x5(self):
        self.processedImage = cv2.GaussianBlur(self.originalImage, (3, 5), 0)
        self.display_image(self.processedImage)

    def identity_filter(self):
        kernel = np.array([[0,  0,  0],
                           [0,  1,  0],
                           [0,  0,  0]])
        self.apply_filter(kernel)

    def sharpen_filter(self):
        kernel = np.array([[ 0, -1,  0],
                           [-1,  5, -1],
                           [ 0, -1,  0]])
        self.apply_filter(kernel)

    def unsharp_masking_filter(self):
        gaussian_blur = cv2.GaussianBlur(self.originalImage, (9, 9), 10.0)
        self.processedImage = cv2.addWeighted(self.originalImage, 1.5, gaussian_blur, -0.5, 0)
        self.display_image(self.processedImage)

    def average_filter(self):
        kernel = np.ones((5, 5), np.float32) / 25
        self.apply_filter(kernel)

    def low_pass_filter(self):
        kernel = np.ones((3, 3), np.float32) / 9
        self.apply_filter(kernel)

    def high_pass_filter(self):
        kernel = np.array([[-1, -1, -1],
                           [-1,  8, -1],
                           [-1, -1, -1]])
        self.apply_filter(kernel)

    def bandstop_filter(self):
        kernel = np.array([[1,  1,  1],
                           [1, -7,  1],
                           [1,  1,  1]])
        self.apply_filter(kernel)

    def apply_linear_contrast(self):
        if self.originalImage is not None:
            contrast_factor = 1.2  # Nilai default, bisa disesuaikan
            self.processedImage = linear_contrast(self.originalImage, contrast_factor)
            self.display_image(self.processedImage)

    def apply_linear_saturation(self):
        if self.processedImage is not None:
            if isinstance(self.processedImage, np.ndarray):  # Pastikan processedImage adalah array NumPy
                try:
                    # Konversi ke gambar PIL
                    pil_image = Image.fromarray(cv2.cvtColor(self.processedImage, cv2.COLOR_BGR2RGB))
                    saturation_factor = 1.5  # Misalnya, tingkat saturasi ditetapkan ke 1.5
                    enhanced_image = linear_saturation(pil_image, saturation_factor)  # Panggil fungsi dengan faktor saturasi
                    self.processedImage = np.array(enhanced_image)  # Konversi kembali ke array NumPy
                    self.display_image(self.processedImage)  # Tampilkan gambar
                except cv2.error as e:
                    print(f"Error in cvtColor: {e}")
            else:
                print("Processed image is not a valid NumPy array.")
        else:
            print("No image loaded to process.")

    def display_image(self, image):
        if isinstance(image, Image.Image):  # Jika image adalah objek PIL
            image_np = np.array(image)  # Konversi ke array NumPy
        else:
            image_np = image  # Jika sudah berupa array NumPy, langsung digunakan
        
        image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGR2RGB)  # Konversi warna
        height, width, _ = image_rgb.shape  # Mendapatkan dimensi gambar
        q_image = QImage(image_rgb.data, width, height, 3 * width, QImage.Format_RGB888)  # Konversi ke QImage
        self.imageLabel.setPixmap(QPixmap.fromImage(q_image))  # Menampilkan gambar



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = Ui_MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
