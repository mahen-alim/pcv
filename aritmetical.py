import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QAction, QMenu, QFileDialog, QHBoxLayout, QDesktopWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class AritmeticalOperationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set the main window properties
        self.setWindowTitle("Aritmetical Operation with Images")
        self.default_width = 1300
        self.default_height = 600
        self.setGeometry(100, 100, self.default_width, self.default_height)

        # Center the window on the screen
        self.center()

        # Set up the central widget and layout
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Use a horizontal layout to arrange the image labels side by side
        self.layout = QHBoxLayout(self.central_widget)

        # Label to show the original image (Image 1)
        self.originalImageLabel = QLabel(self)
        self.originalImageLabel.setFixedSize(600, 600)
        self.originalImageLabel.setStyleSheet("border: 1px solid black; background-color: white;")
        self.layout.addWidget(self.originalImageLabel)

        # Label to show the processed image (Image 2)
        self.processedImageLabel = QLabel(self)
        self.processedImageLabel.setFixedSize(600, 600)
        self.processedImageLabel.setStyleSheet("border: 1px solid black; background-color: white;")
        self.layout.addWidget(self.processedImageLabel)

        # Variables to hold the images
        self.image1 = None
        self.image2 = None
        self.result_image = None

        # Setup the menubar
        menubar = self.menuBar()

        # Create the Aritmetical Operation menu
        menuAritmetical = menubar.addMenu('Aritmetical Operation')

        # Create File Menu
        fileMenu = QMenu('File', self)
        menuAritmetical.addMenu(fileMenu)

        openFile1Action = QAction('Open File 1', self)
        openFile1Action.triggered.connect(self.open_file1)
        fileMenu.addAction(openFile1Action)

        openFile2Action = QAction('Open File 2', self)
        openFile2Action.triggered.connect(self.open_file2)
        fileMenu.addAction(openFile2Action)

        clearAction = QAction('Clear', self)
        clearAction.triggered.connect(self.clear_images)
        fileMenu.addAction(clearAction)

        exitAction = QAction('Exit', self)
        exitAction.triggered.connect(self.close)
        fileMenu.addAction(exitAction)

        # Create Calculation Menu
        calculationMenu = QMenu('Calculation', self)
        menuAritmetical.addMenu(calculationMenu)

        # Connect each action to the same function with the operation type
        addAction = QAction('Penjumlahan', self)
        addAction.triggered.connect(lambda: self.aritmetical_apply('add'))
        calculationMenu.addAction(addAction)

        subtractAction = QAction('Pengurangan', self)
        subtractAction.triggered.connect(lambda: self.aritmetical_apply('subtract'))
        calculationMenu.addAction(subtractAction)

        multiplyAction = QAction('Perkalian', self)
        multiplyAction.triggered.connect(lambda: self.aritmetical_apply('multiply'))
        calculationMenu.addAction(multiplyAction)

        divideAction = QAction('Pembagian', self)
        divideAction.triggered.connect(lambda: self.aritmetical_apply('divide'))
        calculationMenu.addAction(divideAction)

        orAction = QAction('Operasi OR', self)
        orAction.triggered.connect(lambda: self.aritmetical_apply('or'))
        calculationMenu.addAction(orAction)

        andAction = QAction('Operasi AND', self)
        andAction.triggered.connect(lambda: self.aritmetical_apply('and'))
        calculationMenu.addAction(andAction)

        xorAction = QAction('Operasi XOR', self)
        xorAction.triggered.connect(lambda: self.aritmetical_apply('xor'))
        calculationMenu.addAction(xorAction)

    def center(self):
        """
        Center the window on the screen.
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def open_file1(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.bmp);;All Files (*)')
        if file_path:
            self.image1 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.display_image_on_label(self.image1, self.originalImageLabel)

    def open_file2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.bmp);;All Files (*)')
        if file_path:
            self.image2 = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
            self.display_image_on_label(self.image2, self.processedImageLabel)

    def clear_images(self):
        self.image1 = None
        self.image2 = None
        self.result_image = None
        self.originalImageLabel.clear()
        self.processedImageLabel.clear()

    def resize_images(self):
        """Resize images to match each other's dimensions."""
        if self.image1 is not None and self.image2 is not None:
            height1, width1 = self.image1.shape
            height2, width2 = self.image2.shape
            if (height1, width1) != (height2, width2):
                if height1 > height2 or width1 > width2:
                    self.image2 = cv2.resize(self.image2, (width1, height1))
                else:
                    self.image1 = cv2.resize(self.image1, (width2, height2))

    def aritmetical_apply(self, operation):
        if self.image1 is not None and self.image2 is not None:
            # Resize images if their dimensions do not match
            self.resize_images()

            if operation == 'add':
                self.result_image = cv2.add(self.image1, self.image2)
            elif operation == 'subtract':
                self.result_image = cv2.subtract(self.image1, self.image2)
            elif operation == 'multiply':
                self.result_image = cv2.multiply(self.image1, self.image2)
            elif operation == 'divide':
                with np.errstate(divide='ignore', invalid='ignore'):
                    self.result_image = cv2.divide(self.image1.astype('float'), self.image2.astype('float'))
                    self.result_image = np.nan_to_num(self.result_image).astype('uint8')
            elif operation == 'or':
                self.result_image = cv2.bitwise_or(self.image1, self.image2)
            elif operation == 'and':
                self.result_image = cv2.bitwise_and(self.image1, self.image2)
            elif operation == 'xor':
                self.result_image = cv2.bitwise_xor(self.image1, self.image2)

            self.display_images()

    def display_images(self):
        """Display the result image using matplotlib."""
        if self.result_image is not None:
            plt.figure()
            plt.imshow(self.result_image, cmap='gray')
            plt.title('Result Image')
            plt.axis('off')
            plt.show()

    def display_image_on_label(self, image, label):
        """Display a grayscale image on a QLabel."""
        height, width = image.shape
        q_image = QImage(image.data, width, height, width, QImage.Format_Grayscale8)
        pixmap = QPixmap.fromImage(q_image)
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))
