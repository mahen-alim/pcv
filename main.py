# main.py
import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QFileDialog, QLabel, 
    QVBoxLayout, QWidget, QHBoxLayout, QDesktopWidget, QDialog, 
    QInputDialog, QMessageBox, QSizePolicy, QScrollArea
)
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QImage, QPixmap, QPainter
import numpy as np
import cv2
from PIL import Image
# Import filters from the 'filter' module
from filter import (
    edge_detection_1, edge_detection_2, edge_detection_3,
    gaussian_blur, identity_filter, sharpen_filter,
    unsharp_masking_filter, average_filter, low_pass_filter,
    high_pass_filter, bandstop_filter
)
# Import color adjustments from the 'colors' module
from colors import (
    apply_kuning, apply_orange, apply_cyan, apply_purple,
    apply_grey, apply_coklat, apply_merah, convert_to_average,
    convert_to_lightness, convert_to_luminance, adjust_saturation,
    adjust_contrast, adjust_brightness, apply_bit_depth, apply_invers,
    apply_log_brightness, apply_gamma_correction
)
from img_pross import (
    fuzzy_histogram_equalization, fuzzy_histogram_equalization_rgb, 
    apply_histogram_equalization, convert_to_qimage, display_image
)
from popup_slider import ColorCorrectionDialog 
from histogram import plot_histogram
from transform import translation, rotation, flipping, convert_cv_to_pil, CroppableLabel, display_image_zoom
from about_dialog import about_dialog
from segmentation import (
    region_growing, kmeans_clustering, watershed_segmentation, 
    global_thresholding, adaptive_thresholding, display_images
)
from morphology import pros_morphology
from aritmetical import AritmeticalOperationApp
from fitur_extract import ekstraksi_warna, ekstraksi_tekstur
           
class Ui_MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle("Image Filter Application")
        self.default_width = 1700
        self.default_height = 900
        self.setGeometry(100, 100, self.default_width, self.default_height)
    
        # Center the window on the screen
        self.center()

        # Create a central widget to display the images
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)
        self.layout = QVBoxLayout(self.centralWidget)

        # Create a horizontal layout to place two labels side by side
        self.imageLayout = QHBoxLayout()
        self.layout.addLayout(self.imageLayout)

        # Create a vertical layout for the original image and its text
        self.originalImageLayout = QVBoxLayout()
        self.imageLayout.addLayout(self.originalImageLayout)

        # Label to show the original image
        self.originalImageLabel = CroppableLabel(self)
        self.originalImageLabel.setFixedSize(800, 600)
        self.originalImageLayout.addWidget(self.originalImageLabel)

        # Apply CSS style for border radius
        self.originalImageLabel.setStyleSheet("""
            border: 1px solid black; 
            background-color: white;          
            padding: 10px;      
        """)

        # Create a vertical layout for the processed image and its text
        self.processedImageLayout = QVBoxLayout()
        self.imageLayout.addLayout(self.processedImageLayout)

        # Label to show the processed image
        self.processedImageLabel = QLabel(self)
        self.processedImageLabel.setAlignment(Qt.AlignCenter)
        self.processedImageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Mengatur ukuran default
        default_width = 750  # Ganti dengan lebar default yang diinginkan
        default_height = 800  # Ganti dengan tinggi default yang diinginkan

        # Mengatur ukuran default untuk originalImageLabel
        self.originalImageLabel.setFixedSize(default_width, default_height)

        # Mengatur ukuran default untuk processedImageLabel
        self.processedImageLabel.setFixedSize(default_width, default_height)

        # Membuat QScrollArea untuk processedImageLabel
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidget(self.processedImageLabel)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedSize(default_width, default_height)

        # Menambahkan QScrollArea ke layout
        self.processedImageLayout.addWidget(self.scrollArea)

         # Apply CSS style for border radius
        self.processedImageLabel.setStyleSheet("""
            border: 1px solid black; 
            background-color: white;
            padding: 10px;
        """)

        # Menu bar
        menubar = self.menuBar()
        menuFile = menubar.addMenu('File')

        # Create actions for File menu
        self.actionOpenImage = QAction('Open Image', self)
        self.actionSaveAs = QAction('Save As', self)
        self.actionExit = QAction('Exit', self)

        # Add actions to File menu
        menuFile.addAction(self.actionOpenImage)
        menuFile.addAction(self.actionSaveAs)
        menuFile.addAction(self.actionExit)

        # Create the View menu
        menuView = menubar.addMenu('View')

        # Create submenus for View menu
        menuHistogram = menuView.addMenu('Histogram') 

        # Actions for Submenu Histogram 
        self.actionInput = QAction('Input', self)
        self.actionOutput = QAction('Output', self)
        self.actionInputOuput = QAction('Input Output', self)

        # Add RGB actions to the Histogram submenu
        menuHistogram.addAction(self.actionInput)
        menuHistogram.addAction(self.actionOutput)
        menuHistogram.addAction(self.actionInputOuput)

        # Create the Colors menu
        menuColors = menubar.addMenu('Colors')

        # Create submenus for Colors menu
        menuRgb = menuColors.addMenu('RGB')  # Should be added to Colors menu, not Filter
        menuRgbtg = menuColors.addMenu('RGB to Greyscale')  # Should also be under Colors
        # menuLinear = menuColors.addMenu('Linear')  # Similarly, part of Colors

        # Actions for RGB color manipulations
        self.actionKuning = QAction('Yellow', self)
        self.actionOrange = QAction('Orange', self)
        self.actionCyan = QAction('Cyan', self)
        self.actionPurple = QAction('Purple', self)
        self.actionGrey = QAction('Grey', self)
        self.actionCoklat = QAction('Brown', self)
        self.actionMerah = QAction('Red', self)

        # Add RGB actions to the RGB submenu
        menuRgb.addAction(self.actionKuning)
        menuRgb.addAction(self.actionOrange)
        menuRgb.addAction(self.actionCyan)
        menuRgb.addAction(self.actionPurple)
        menuRgb.addAction(self.actionGrey)
        menuRgb.addAction(self.actionCoklat)
        menuRgb.addAction(self.actionMerah)

        # Actions for RGB to Greyscale
        self.actionAverage = QAction('Average', self)
        self.actionLightness = QAction('Lightness', self)
        self.actionLuminance = QAction('Luminance', self)

        # Add RGB to Greyscale actions to the RGB to Greyscale submenu
        menuRgbtg.addAction(self.actionAverage)
        menuRgbtg.addAction(self.actionLightness)
        menuRgbtg.addAction(self.actionLuminance)

        # Bit Depth submenu and actions
        menuBith = menuColors.addMenu('Bit Depth')
        self.action1bith = QAction('1 Bit', self)
        self.action2bith = QAction('2 Bit', self)
        self.action3bith = QAction('3 Bit', self)
        self.action4bith = QAction('4 Bit', self)
        self.action5bith = QAction('5 Bit', self)
        self.action6bith = QAction('6 Bit', self)
        self.action7bith = QAction('7 Bit', self)

        # Add Bit Depth actions to the Bit Depth submenu
        menuBith.addAction(self.action1bith)
        menuBith.addAction(self.action2bith)
        menuBith.addAction(self.action3bith)
        menuBith.addAction(self.action4bith)
        menuBith.addAction(self.action5bith)
        menuBith.addAction(self.action6bith)
        menuBith.addAction(self.action7bith)

        # Additional color adjustment actions
        self.menuLinear = QAction("Linear", self)
        self.menuInvers = QAction('Invers', self)
        self.menuLog = QAction('Log Brightness', self)
        self.menuGamma = QAction('Gamma Correction', self)

        # Add these actions directly to the Colors menu
        menuColors.addAction(self.menuLinear)
        menuColors.addAction(self.menuInvers)
        menuColors.addAction(self.menuLog)
        menuColors.addAction(self.menuGamma)

        # Create the Image Processing menu
        menuImgPross = menubar.addMenu('Image Processing')

        self.menuHe = QAction('Histogram Equalization', self)
        self.menuFHE = QAction('Fuzy HE', self)
        self.menuFuzzyRGB = QAction('Fuzzy HE RGB', self)

        # Add these actions directly to the Image Processing menu
        menuImgPross.addAction(self.menuHe)
        menuImgPross.addAction(self.menuFHE)
        menuImgPross.addAction(self.menuFuzzyRGB)

        # Create the Transform menu
        menuTransform = menubar.addMenu('Transform')

        self.actionTranslation = QAction('Translation', self)
        self.actionRotation = QAction('Rotation', self)
        self.actionFlipping = QAction('Flipping', self)
        self.actionZooming = QAction('Zooming', self)
        self.actionCropping = QAction('Cropping', self)

        menuTransform.addAction(self.actionTranslation)
        menuTransform.addAction(self.actionRotation)
        menuTransform.addAction(self.actionFlipping)
        menuTransform.addAction(self.actionZooming)
        menuTransform.addAction(self.actionCropping)

        # Create the Segmentation menu
        menuSegment = menubar.addMenu('Segmentation')

        self.actionGrowing = QAction('Region Growing')
        self.actionClustering = QAction('K-Means Clustering')
        self.actionWatershed = QAction('Watershed Segmentation')
        self.actionTGlobal = QAction('Global Thresholding ')
        self.actionTAdaptif = QAction('Adaptif Thresholding ')

        menuSegment.addAction(self.actionGrowing)
        menuSegment.addAction(self.actionClustering)
        menuSegment.addAction(self.actionWatershed)
        menuSegment.addAction(self.actionTGlobal)
        menuSegment.addAction(self.actionTAdaptif)

        # Create the Morfologi menu
        menuMorfologi = menubar.addMenu('Morphology')

        # Submenus under Morfologi
        menuErosion = menuMorfologi.addMenu('Erosi')
        menuDilation = menuMorfologi.addMenu('Dilasi')
        menuOpening = menuMorfologi.addMenu('Opening')
        menuClosing = menuMorfologi.addMenu('Closing')

        # Additional Morphology Menus
        menuHitOrMiss = menuMorfologi.addMenu('Hit-or-Miss')
        menuBoundaryExtraction = menuMorfologi.addMenu('Boundary Extraction')
        menuRegionFilling = menuMorfologi.addMenu('Region Filling')
        menuThinning = menuMorfologi.addMenu('Thinning')
        menuSkeletonization = menuMorfologi.addMenu('Skeletonization')

        # Erosion Actions
        self.actionSquare3 = QAction('Square 3', self)
        self.actionSquare5 = QAction('Square 5', self)
        self.actionCross3 = QAction('Cross 3', self)

        # Dilation Actions
        self.actionDSquare3 = QAction('Square 3', self)
        self.actionDSquare5 = QAction('Square 5', self)
        self.actionDCross3 = QAction('Cross 3', self)

        # Opening and Closing Actions
        self.actionOSquare9 = QAction('Square 9', self)
        self.actionCSquare9 = QAction('Square 9', self)

        # Hit-or-Miss Actions
        self.actionHitSquare3 = QAction('Square 3', self)
        self.actionHitCross3 = QAction('Cross 3', self)

        # Boundary Extraction Actions
        self.actionBoundarySquare3 = QAction('Square 3', self)
        self.actionBoundaryCross3 = QAction('Cross 3', self)

        # Region Filling Actions
        self.actionRegionSquare3 = QAction('Square 3', self)
        self.actionRegionCross3 = QAction('Cross 3', self)

        # Thinning Actions
        self.actionThinningSquare3 = QAction('Square 3', self)
        self.actionThinningCross3 = QAction('Cross 3', self)

        # Skeletonization Actions
        self.actionSkeletonSquare3 = QAction('Square 3', self)
        self.actionSkeletonCross3 = QAction('Cross 3', self)

        # Add Erosion actions
        menuErosion.addAction(self.actionSquare3)
        menuErosion.addAction(self.actionSquare5)
        menuErosion.addAction(self.actionCross3)

        # Add Dilation actions
        menuDilation.addAction(self.actionDSquare3)
        menuDilation.addAction(self.actionDSquare5)
        menuDilation.addAction(self.actionDCross3)

        # Add Opening and Closing actions
        menuOpening.addAction(self.actionOSquare9)
        menuClosing.addAction(self.actionCSquare9)

        # Add Hit-or-Miss actions
        menuHitOrMiss.addAction(self.actionHitSquare3)
        menuHitOrMiss.addAction(self.actionHitCross3)

        # Add Boundary Extraction actions
        menuBoundaryExtraction.addAction(self.actionBoundarySquare3)
        menuBoundaryExtraction.addAction(self.actionBoundaryCross3)

        # Add Region Filling actions
        menuRegionFilling.addAction(self.actionRegionSquare3)
        menuRegionFilling.addAction(self.actionRegionCross3)

        # Add Thinning actions
        menuThinning.addAction(self.actionThinningSquare3)
        menuThinning.addAction(self.actionThinningCross3)

        # Add Skeletonization actions
        menuSkeletonization.addAction(self.actionSkeletonSquare3)
        menuSkeletonization.addAction(self.actionSkeletonCross3)
   
        # Create the "Tentang" action directly in the menubar
        self.aboutAction = QAction('About', self)

        # Add the action directly to the menubar without creating a submenu
        menubar.addAction(self.aboutAction)

        # Create the Aritmetical Operation menu
        self.aritmeticalAction = QAction('Aritmetical Operation')

        # Add the action directly to the menubar without creating a submenu
        menubar.addAction(self.aritmeticalAction)

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

       # Create the Edge Detection menu
        menuEdgeDetection = menubar.addMenu('Edge Detection')

        # Create actions for Edge Detection submenu
        self.actionPrewitt = QAction('Prewitt', self)
        self.actionSobel = QAction('Sobel', self)
        self.actionCanny = QAction('Canny', self)

        # Add actions to Edge Detection submenu
        menuEdgeDetection.addAction(self.actionPrewitt)
        menuEdgeDetection.addAction(self.actionSobel)
        menuEdgeDetection.addAction(self.actionCanny)

        # Create the Ekstraksi Fitur menu
        menuEkstraksiFitur = menubar.addMenu('Ekstraksi Fitur')

        # Create actions for Ekstraksi Fitur submenu
        self.actionWarnaEks = QAction('Ekstraksi Warna', self)
        self.actionTeksturEks = QAction('Ekstraksi Tekstur', self)

        # Add actions to Ekstraksi Fitur submenu
        menuEkstraksiFitur.addAction(self.actionWarnaEks)
        menuEkstraksiFitur.addAction(self.actionTeksturEks)

        # Create the "Clear" action directly in the menubar
        self.clearAction = QAction('Clear', self)

        # Add the action directly to the menubar without creating a submenu
        menubar.addAction(self.clearAction)

        # Connect actions to methods
        self.actionOpenImage.triggered.connect(self.open_image)
        self.actionSaveAs.triggered.connect(self.save_image)
        self.actionExit.triggered.connect(self.close)
        self.aboutAction.triggered.connect(self.dialog_popup_apply)
        self.aritmeticalAction.triggered.connect(self.open_aritmetical_operation)

        # Image Processing Filters
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

        # Color Actions
        self.actionKuning.triggered.connect(self.action_kuning)
        self.actionOrange.triggered.connect(self.action_orange)
        self.actionCyan.triggered.connect(self.action_cyan)
        self.actionPurple.triggered.connect(self.action_purple)
        self.actionGrey.triggered.connect(self.action_grey)
        self.actionCoklat.triggered.connect(self.action_coklat)
        self.actionMerah.triggered.connect(self.action_merah)

        # Color Correction
        self.actionAverage.triggered.connect(self.action_average)
        self.actionLightness.triggered.connect(self.action_lightness)
        self.actionLuminance.triggered.connect(self.action_luminance)
        self.menuLinear.triggered.connect(self.action_color_correction)

        # Bit Depth Actions
        self.action1bith.triggered.connect(self.action_1bith)
        self.action2bith.triggered.connect(self.action_2bith)
        self.action3bith.triggered.connect(self.action_3bith)
        self.action4bith.triggered.connect(self.action_4bith)
        self.action5bith.triggered.connect(self.action_5bith)
        self.action6bith.triggered.connect(self.action_6bith)
        self.action7bith.triggered.connect(self.action_7bith)

        # Histogram and Color Correction
        self.menuInvers.triggered.connect(self.action_invers)
        self.menuLog.triggered.connect(self.action_log_brightness)
        self.menuGamma.triggered.connect(self.action_gamma_correction)

        # Histogram Actions
        self.actionInput.triggered.connect(self.show_input_histogram)
        self.actionOutput.triggered.connect(self.show_output_histogram)
        self.actionInputOuput.triggered.connect(self.show_input_output_histogram)

        # Transformations
        self.actionTranslation.triggered.connect(self.show_transform_translation)
        self.actionFlipping.triggered.connect(self.show_transform_flipping)
        self.actionRotation.triggered.connect(self.show_transform_rotation)
        self.actionZooming.triggered.connect(self.show_transform_zooming)
        self.actionCropping.triggered.connect(self.show_transform_cropping)

        # Image Processing
        self.menuHe.triggered.connect(self.apply_histogram_equalization)
        self.menuFHE.triggered.connect(self.apply_fuzzy_histogram_equalization)
        self.menuFuzzyRGB.triggered.connect(self.apply_fuzzy_he_rgb)

        # Segmentation
        self.actionGrowing.triggered.connect(self.apply_region_growing)
        self.actionClustering.triggered.connect(self.apply_kmeans_clustering)
        self.actionWatershed.triggered.connect(self.apply_watershed_segmentation)
        self.actionTGlobal.triggered.connect(self.apply_global_thresholding)
        self.actionTAdaptif.triggered.connect(self.apply_adaptive_thresholding)

        # Connect actions to triggers (Erosion)
        self.actionSquare3.triggered.connect(lambda: self.apply_morphology('erosion', 'square', 3))
        self.actionSquare5.triggered.connect(lambda: self.apply_morphology('erosion', 'square', 5))
        self.actionCross3.triggered.connect(lambda: self.apply_morphology('erosion', 'cross', 3))

        # Connect actions to triggers (Dilation)
        self.actionDSquare3.triggered.connect(lambda: self.apply_morphology('dilation', 'square', 3))
        self.actionDSquare5.triggered.connect(lambda: self.apply_morphology('dilation', 'square', 5))
        self.actionDCross3.triggered.connect(lambda: self.apply_morphology('dilation', 'cross', 3))

        # Connect actions to triggers (Opening and Closing)
        self.actionOSquare9.triggered.connect(lambda: self.apply_morphology('opening', 'square', 9))
        self.actionCSquare9.triggered.connect(lambda: self.apply_morphology('closing', 'square', 9))

        # Triggers for Hit-or-Miss actions
        self.actionHitSquare3.triggered.connect(lambda: self.apply_morphology('hit-or-miss', 'square', 3))
        self.actionHitCross3.triggered.connect(lambda: self.apply_morphology('hit-or-miss', 'cross', 3))

        # Triggers for Boundary Extraction actions
        self.actionBoundarySquare3.triggered.connect(lambda: self.apply_morphology('boundary-extraction', 'square', 3))
        self.actionBoundaryCross3.triggered.connect(lambda: self.apply_morphology('boundary-extraction', 'cross', 3))

        # Triggers for Region Filling actions
        self.actionRegionSquare3.triggered.connect(lambda: self.apply_morphology('region-filling', 'square', 3))
        self.actionRegionCross3.triggered.connect(lambda: self.apply_morphology('region-filling', 'cross', 3))

        # Triggers for Thinning actions
        self.actionThinningSquare3.triggered.connect(lambda: self.apply_morphology('thinning', 'square', 3))
        self.actionThinningCross3.triggered.connect(lambda: self.apply_morphology('thinning', 'cross', 3))

        # Triggers for Skeletonization actions
        self.actionSkeletonSquare3.triggered.connect(lambda: self.apply_morphology('skeletonization', 'square', 3))
        self.actionSkeletonCross3.triggered.connect(lambda: self.apply_morphology('skeletonization', 'cross', 3))

        # Hubungkan aksi menu dengan fungsi pemrosesan
        self.actionPrewitt.triggered.connect(lambda: self.process_edge_detection('Prewitt'))
        self.actionSobel.triggered.connect(lambda: self.process_edge_detection('Sobel'))
        self.actionCanny.triggered.connect(lambda: self.process_edge_detection('Canny'))

        # Connect actions to respective functions
        self.actionWarnaEks.triggered.connect(self.apply_ekstraksi_warna)
        self.actionTeksturEks.triggered.connect(self.apply_ekstraksi_tekstur)

        # Clear Action
        self.clearAction.triggered.connect(self.clear_image)

        # Initialize image variables
        self.original_image = None
        self.processed_image = None
        # Placeholder for image data
        self.input_image_np = None
        self.output_image_np = None
        # Inisialisasi variabel untuk cropping
        self.start_pos = None
        self.end_pos = None
        self.cropping = False
        self.image = None

    def center(self):
        """
        Center the window on the screen.
        """
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)

    def resize_image(self, image, max_width, max_height):
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_width = int(width * ratio)
        new_height = int(height * ratio)
        return image.resize((new_width, new_height), Image.LANCZOS)
        
    def open_image(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image File', '', 'Images (*.png *.jpg *.bmp);;All Files (*)', options=options)
        
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.originalImageLabel)
            self.processed_image = None
            
            # Simpan jalur file gambar yang dipilih
            self.image_file_path = file_path

    def save_image(self):
        # Buka dialog untuk memilih lokasi penyimpanan gambar
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(self, 'Save Image File', '', 'Images (*.png *.jpg *.bmp);;All Files (*)', options=options)
        
        if file_path:
            try:
                # Simpan gambar yang sudah diproses ke lokasi yang dipilih
                self.processed_image.save(file_path)
                
                # Tampilkan pesan sukses dengan direktori tempat gambar disimpan
                QMessageBox.information(self, 'Success', f'Image has been saved successfully at:\n{file_path}')
            
            except Exception as e:
                # Tampilkan pesan error jika terjadi masalah saat menyimpan gambar
                QMessageBox.warning(self, 'Error', f'Failed to save image: {str(e)}')
    
    def display_image(self, image, label):
        max_width = 750
        max_height = 800
        resized_image = self.resize_image(image, max_width, max_height)
        image_np = np.array(resized_image)

        # Store image data
        if label == self.originalImageLabel:
            self.input_image_np = image_np
        elif label == self.processedImageLabel:
            self.output_image_np = image_np

        # Mengatur ukuran label sesuai dengan ukuran gambar
        width, height = resized_image.size
        label.setFixedSize(QSize(width, height))

        # Konversi gambar ke format QImage
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

        # Jika label lebih besar dari gambar, pastikan background tetap terlihat
        label.setScaledContents(True)  # Mengatur agar pixmap disesuaikan dengan label

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

    def action_kuning(self):
        if self.original_image:
            self.processed_image = apply_kuning(self.original_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_orange(self):
        if self.original_image:
            self.processed_image = apply_orange(self.original_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_cyan(self):
        if self.original_image:
            self.processed_image = apply_cyan(self.original_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_purple(self):
        if self.original_image:
            self.processed_image = apply_purple(self.original_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_grey(self):
        if self.original_image:
            self.processed_image = apply_grey(self.original_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_coklat(self):
        if self.original_image:
            self.processed_image = apply_coklat(self.original_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_merah(self):
        if self.original_image:
            self.processed_image = apply_merah(self.original_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_average(self):
        if self.original_image:
            # Terapkan filter average grayscale
            self.processed_image = convert_to_average(self.original_image)
            # Tampilkan gambar hasil
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_lightness(self):
        if self.original_image:
            # Terapkan filter lightness grayscale
            self.processed_image = convert_to_lightness(self.original_image)
            # Tampilkan gambar hasil
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_luminance(self):
        if self.original_image:
            # Terapkan filter luminance grayscale
            self.processed_image = convert_to_luminance(self.original_image)
            # Tampilkan gambar hasil
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_color_correction(self):
        # Buat instance dialog koreksi warna
        dialog = ColorCorrectionDialog(self)

        # Jalankan dialog, jika user menekan "OK", maka terapkan koreksi warna
        if dialog.exec_() == QDialog.Accepted:
            saturation, contrast, brightness = dialog.get_values()

            # Terapkan perubahan pada gambar yang sedang diproses
            self.processed_image = self.apply_image_corrections(self.original_image, saturation, contrast, brightness)
            self.display_image(self.processed_image, self.processedImageLabel)

    def apply_image_corrections(self, image, saturation, contrast, brightness):
        """
        Menerapkan koreksi gambar berdasarkan nilai saturasi, kontras, dan kecerahan.
        :param image: Gambar asli dalam format PIL
        :param saturation: Faktor saturasi
        :param contrast: Faktor kontras
        :param brightness: Faktor kecerahan
        :return: Gambar yang telah dikoreksi
        """
        # Terapkan koreksi saturasi
        image = adjust_saturation(image, saturation)

        # Terapkan koreksi kontras
        image = adjust_contrast(image, contrast)

        # Terapkan koreksi kecerahan
        image = adjust_brightness(image, brightness)

        return image

    def action_1bith(self):
        if self.processed_image:
            processed_image = apply_bit_depth(self.processed_image, 1)
            self.display_image(processed_image, self.processedImageLabel)

    def action_2bith(self):
        if self.processed_image:
            processed_image = apply_bit_depth(self.processed_image, 2)
            self.display_image(processed_image, self.processedImageLabel)

    def action_3bith(self):
        if self.processed_image:
            processed_image = apply_bit_depth(self.processed_image, 3)
            self.display_image(processed_image, self.processedImageLabel)

    def action_4bith(self):
        if self.processed_image:
            processed_image = apply_bit_depth(self.processed_image, 4)
            self.display_image(processed_image, self.processedImageLabel)

    def action_5bith(self):
        if self.processed_image:
            processed_image = apply_bit_depth(self.processed_image, 5)
            self.display_image(processed_image, self.processedImageLabel)

    def action_6bith(self):
        if self.processed_image:
            processed_image = apply_bit_depth(self.processed_image, 6)
            self.display_image(processed_image, self.processedImageLabel)

    def action_7bith(self):
        if self.processed_image:
            processed_image = apply_bit_depth(self.processed_image, 7)
            self.display_image(processed_image, self.processedImageLabel)

    def action_invers(self):
        if self.processed_image:
            self.processed_image = apply_invers(self.processed_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_log_brightness(self):
        if self.processed_image:
            self.processed_image = apply_log_brightness(self.processed_image)
            self.display_image(self.processed_image, self.processedImageLabel)

    def action_gamma_correction(self):
        if self.processed_image:
            gamma_value = 1.2  # Nilai gamma, bisa ditentukan sesuai kebutuhan
            self.processed_image = apply_gamma_correction(self.processed_image, gamma_value)
            self.display_image(self.processed_image, self.processedImageLabel)

    def apply_histogram_equalization(main_window):
        """
        Aplikasi histogram equalization pada gambar yang ada di QLabel.
        """
        # Pastikan gambar di QLabel original ada (tidak None)
        if main_window.originalImageLabel.pixmap() is not None:
            # Konversi gambar dari QPixmap di originalImageLabel ke QImage
            input_pixmap = main_window.originalImageLabel.pixmap()
            input_image = input_pixmap.toImage()

            # Konversi QImage menjadi numpy array
            buffer = input_image.bits().asstring(input_image.width() * input_image.height() * 4)
            image_np = np.frombuffer(buffer, dtype=np.uint8).reshape((input_image.height(), input_image.width(), 4))

            # Konversi gambar ke format RGB
            image_rgb = cv2.cvtColor(image_np, cv2.COLOR_BGRA2RGB)

            # Terapkan histogram equalization
            equalized_image = apply_histogram_equalization(image_rgb)

            # Konversi kembali ke QImage untuk ditampilkan
            qimage_result = convert_to_qimage(equalized_image)

            # Tampilkan gambar hasil pada processedImageLabel
            main_window.processedImageLabel.setPixmap(QPixmap.fromImage(qimage_result).scaled(
                main_window.processedImageLabel.size(), Qt.KeepAspectRatio))

    def apply_fuzzy_histogram_equalization(self):
        """
        Menerapkan Fuzzy Histogram Equalization pada gambar yang telah dibuka.
        """
        if self.original_image is None:
            QMessageBox.warning(self, "Warning", "Tidak ada gambar yang dibuka. Silakan buka gambar terlebih dahulu.")
            return
        
        try:
            # Konversi gambar dari PIL Image ke NumPy array (RGB format)
            original_image_np = np.array(self.original_image.convert('RGB'))
            
            # Menerapkan fuzzy histogram equalization pada gambar RGB
            equalized_image_np = fuzzy_histogram_equalization(original_image_np)
            
            # Konversi kembali hasil dari NumPy ke PIL Image untuk penyimpanan
            equalized_image_pil = Image.fromarray(equalized_image_np)
            
            # Tampilkan hasilnya di QLabel processedImageLabel
            display_image(equalized_image_pil, self.processedImageLabel)
            
            # Simpan gambar yang telah diproses untuk digunakan oleh fungsi save_image
            self.processed_image = equalized_image_pil
        
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to apply histogram equalization: {str(e)}")

    def apply_fuzzy_he_rgb(self):
        """
        Menerapkan Fuzzy Histogram Equalization pada gambar RGB yang telah dibuka.
        """
        if self.original_image is None:
            QMessageBox.warning(self, "Warning", "Tidak ada gambar yang dibuka. Silakan buka gambar terlebih dahulu.")
            return

        try:
            # Mengonversi gambar PIL ke format numpy array (RGB)
            original_image_rgb = np.array(self.original_image)

            # Memastikan gambar memiliki 3 channel (RGB)
            if original_image_rgb is None or len(original_image_rgb.shape) != 3 or original_image_rgb.shape[2] != 3:
                raise ValueError("Gambar bukan gambar RGB.")

            # Menampilkan gambar asli di QLabel pertama (originalImageLabel)
            display_image(original_image_rgb, self.originalImageLabel)

            # Menerapkan fuzzy histogram equalization pada gambar RGB
            fuzzy_histogram_equalization_rgb(self)  # Mengirimkan instance dari self

            # Simpan gambar yang diproses untuk keperluan save
            self.processed_image = Image.fromarray(original_image_rgb)

        except ValueError as e:
            # Menampilkan pesan kesalahan jika terjadi error
            QMessageBox.critical(self, "Error", str(e))

    def get_image_np_from_label(self, label):
        pixmap = label.pixmap()
        if pixmap is None:
            return None

        # Convert QPixmap to QImage
        qimage = pixmap.toImage()
        qimage = qimage.convertToFormat(QImage.Format_RGB888)  # Ensure RGB format

        # Convert QImage to numpy array
        width = qimage.width()
        height = qimage.height()
        image_np = np.array(qimage.bits().asarray(width * height * 3)).reshape((height, width, 3))
        
        # If the image is RGB, it will have 3 channels
        if image_np.ndim == 3 and image_np.shape[2] == 3:
            image_np = np.dot(image_np[...,:3], [0.2989, 0.5870, 0.1140])  # Convert to grayscale

        return image_np

    def show_input_histogram(self):
        image_np = self.get_image_np_from_label(self.originalImageLabel)
        if image_np is None:
            print("Error: Failed to get image from label")
            return

        plot_histogram(image_np, title="Input Image Histogram")

    def show_output_histogram(self):
        image_np = self.get_image_np_from_label(self.processedImageLabel)
        if image_np is None:
            print("Error: Failed to get image from label")
            return
    
        plot_histogram(image_np, title="Output Image Histogram")

    def show_input_output_histogram(self):
        input_image_np = self.get_image_np_from_label(self.originalImageLabel)
        output_image_np = self.get_image_np_from_label(self.processedImageLabel)
        if input_image_np is not None:
            plot_histogram(input_image_np, title="Input Image Histogram")
        if output_image_np is not None:
            plot_histogram(output_image_np, title="Output Image Histogram")

    def show_transform_translation(self):
        image_np = self.input_image_np
        tx, ok = QInputDialog.getDouble(self, "Input Translation X", "Masukkan nilai translasi x:", 100)
        if ok:
            ty, ok = QInputDialog.getDouble(self, "Input Translation Y", "Masukkan nilai translasi y:", 50)
            if ok:
                translated_image = translation(image_np, tx, ty)
            self.display_image(convert_cv_to_pil(translated_image), self.processedImageLabel)

    def show_transform_rotation(self):
        image_np = self.input_image_np
        angle, ok = QInputDialog.getDouble(self, "Input Rotation Angle", "Masukkan sudut rotasi:", 45)
        if ok:
            rotated_image = rotation(image_np, angle)
            self.display_image(convert_cv_to_pil(rotated_image), self.processedImageLabel)

    def show_transform_flipping(self):
        image_np = self.input_image_np
        flip_code, ok = QInputDialog.getItem(self, "Select Flip Type", "Pilih jenis flipping:", ["Horizontal", "Vertical", "Keduanya"], 0, False)
        if ok:
            flip_code_dict = {"Horizontal": 1, "Vertical": 0, "Keduanya": -1}
            flipped_image = flipping(image_np, flip_code_dict[flip_code])
            self.display_image(convert_cv_to_pil(flipped_image), self.processedImageLabel)
            
    def apply_zoom(self, scale_percent):
        # Menghitung faktor zoom berdasarkan persentase
        factor = scale_percent / 100.0
        print(f"Zoom Factor: {factor}")
        
        if not self.original_image:
            return
        
        # Mengubah ukuran gambar
        if factor != 1.0:
            original_size = self.original_image.size
            new_size = (int(original_size[0] * factor), int(original_size[1] * factor))
            print(f"Original Size: {original_size}")
            print(f"New Size: {new_size}")
            resized_image = self.original_image.resize(new_size, Image.LANCZOS)
        else:
            # Jika faktor zoom adalah 1, tidak perlu resize
            resized_image = self.original_image
        
        # Menampilkan gambar yang sudah di-zoom di processedImageLabel
        display_image_zoom(resized_image, self.processedImageLabel)

    def show_transform_zooming(self):
        # Menampilkan dialog input untuk skala zoom
        scale, ok = QInputDialog.getDouble(self, 'Input Zoom Scale', 'Enter zoom scale (0-100):', 100, 0, 100, 1)
        if ok:
            print(f"Input Zoom Scale: {scale}")
            # Memanggil fungsi untuk menerapkan zoom
            self.apply_zoom(scale)

    def perform_cropping(self, start_pos, end_pos):
        """Perform cropping based on drag coordinates and update processed image label."""
        if self.original_image and start_pos and end_pos:
            label_width = self.originalImageLabel.width()
            label_height = self.originalImageLabel.height()
            image_width, image_height = self.original_image.size

            # Calculate scaling factor between QLabel and original image
            x_scale = image_width / label_width
            y_scale = image_height / label_height

            # Calculate crop area in image coordinates
            x1 = int(start_pos.x() * x_scale)
            y1 = int(start_pos.y() * y_scale)
            x2 = int(end_pos.x() * x_scale)
            y2 = int(end_pos.y() * y_scale)

            # Ensure the crop box is correctly formed (top-left to bottom-right)
            crop_box = (min(x1, x2), min(y1, y2), max(x1, x2), max(y1, y2))

            # Perform cropping
            self.processed_image = self.original_image.crop(crop_box)

            # Display the cropped image in processedImageLabel
            self.display_image(self.processed_image, self.processedImageLabel)

    def show_transform_cropping(self):
        # Aktifkan mode cropping
        self.originalImageLabel.setCursor(Qt.CrossCursor)
        self.originalImageLabel.enable_cropping()

    def dialog_popup_apply(self):
        about_dialog()

    def open_aritmetical_operation(self):
        """Open the Aritmetical Operation application."""
        self.aritmetical_operation_app = AritmeticalOperationApp()
        self.aritmetical_operation_app.show()  # Show the Aritmetical Operation App

    def apply_region_growing(self):
        if self.original_image is not None:
            # Mengonversi gambar PIL ke NumPy array
            image_np = np.array(self.original_image)

            # Jika gambar berwarna, ubah menjadi grayscale
            if len(image_np.shape) == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

            # Definisikan seed point dan threshold
            seed = (10, 10)  # Contoh seed point
            threshold_value = 20  # Threshold

            # Segmentasi dengan region growing
            segmented_image = region_growing(image_np, seed, threshold_value)

            # Tampilkan hasil
            display_images(image_np, segmented_image, "Region Growing")
        else:
            print("No image loaded!")

    def apply_kmeans_clustering(self):
        if self.original_image is not None:
            image_np = np.array(self.original_image)

            # Ubah menjadi grayscale jika gambar berwarna
            if len(image_np.shape) == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

            # Segmentasi dengan k-means
            segmented_image = kmeans_clustering(image_np, 2)

            # Tampilkan hasil
            display_images(image_np, segmented_image, "k-Means Clustering")
        else:
            print("No image loaded!")

    def apply_watershed_segmentation(self):
        if self.original_image is not None:
            image_np = np.array(self.original_image)

            # Ubah menjadi grayscale jika gambar berwarna
            if len(image_np.shape) == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

            # Segmentasi dengan watershed
            segmented_image = watershed_segmentation(image_np)

            # Tampilkan hasil
            display_images(image_np, segmented_image, "Watershed Segmentation")
        else:
            print("No image loaded!")

    def apply_global_thresholding(self):
        if self.original_image is not None:
            image_np = np.array(self.original_image)

            # Ubah menjadi grayscale jika gambar berwarna
            if len(image_np.shape) == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

            # Segmentasi dengan global thresholding
            segmented_image = global_thresholding(image_np, 100)

            # Tampilkan hasil
            display_images(image_np, segmented_image, "Global Thresholding")
        else:
            print("No image loaded!")

    def apply_adaptive_thresholding(self):
        if self.original_image is not None:
            image_np = np.array(self.original_image)

            # Ubah menjadi grayscale jika gambar berwarna
            if len(image_np.shape) == 3:
                image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)

            # Segmentasi dengan adaptive thresholding
            adaptive_thresh_mean, adaptive_thresh_gaussian = adaptive_thresholding(image_np)

            # Tampilkan hasil
            display_images(image_np, adaptive_thresh_mean, "Adaptive Thresholding (Mean)")
            display_images(image_np, adaptive_thresh_gaussian, "Adaptive Thresholding (Gaussian)")
        else:
            print("No image loaded!")

    def apply_morphology(self, operation, shape, size):
        # Panggil fungsi apply_morphology
        processed_image = pros_morphology(self.original_image, operation, shape, size)

        if processed_image is not None:
            self.processed_image = processed_image
            self.display_image(self.processed_image, self.processedImageLabel)

    def process_edge_detection(self, method):
        """Proses deteksi tepi menggunakan metode yang dipilih."""
        if self.original_image is None:
            print("Error: Gambar asli tidak ditemukan.")
            return

        # Konversi gambar ke format NumPy
        image = np.array(self.original_image)

        if method == 'Prewitt':
            # Definisikan kernel Prewitt
            kernel_x = np.array([[1, 0, -1], [1, 0, -1], [1, 0, -1]], dtype=np.float32)
            kernel_y = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=np.float32)
            
            # Terapkan filter Prewitt
            gradient_x = cv2.filter2D(image.astype(np.float32), -1, kernel_x)
            gradient_y = cv2.filter2D(image.astype(np.float32), -1, kernel_y)
            
            # Hitung magnitude dan konversi kembali ke uint8
            result = cv2.sqrt(gradient_x**2 + gradient_y**2)
            result = np.uint8(np.clip(result, 0, 255))  # Memastikan hasil berada dalam rentang 0-255

        elif method == 'Sobel':
            # Terapkan filter Sobel
            gradient_x = cv2.Sobel(image.astype(np.float32), cv2.CV_64F, 1, 0, ksize=5)
            gradient_y = cv2.Sobel(image.astype(np.float32), cv2.CV_64F, 0, 1, ksize=5)
            result = cv2.magnitude(gradient_x, gradient_y)
            result = np.uint8(np.clip(result, 0, 255))  # Memastikan hasil berada dalam rentang 0-255

        elif method == 'Canny':
            # Terapkan deteksi tepi Canny
            # Anda dapat menyesuaikan nilai threshold1 dan threshold2 sesuai kebutuhan
            threshold1 = 100  # Threshold untuk deteksi tepi
            threshold2 = 200  # Threshold untuk deteksi tepi
            result = cv2.Canny(image.astype(np.uint8), threshold1, threshold2)

        else:
            print("Error: Metode deteksi tepi tidak valid.")
            return

        # Kembalikan gambar hasil sebagai objek PIL
        self.processed_image = Image.fromarray(result)
        self.display_image(self.processed_image, self.processedImageLabel)

    def apply_ekstraksi_warna(self):
        if self.image_file_path:
            try:
                # Jalankan fungsi ekstraksi warna
                ekstraksi_warna(self.image_file_path)
                
                # Tampilkan pesan sukses
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Ekstraksi Warna Berhasil")
                msg.setText(f"Ekstraksi warna selesai untuk {self.image_file_path}. Hasil disimpan di 'D:/ekstraksi_fitur/ekstraksi_warna.xlsx'.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()  # Menampilkan popup
                
            except Exception as e:
                # Tampilkan pesan error jika ada kesalahan
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText(f"Terjadi kesalahan: {str(e)}")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()  # Menampilkan popup error

    def apply_ekstraksi_tekstur(self):
        if hasattr(self, 'image_file_path'):  # Pastikan gambar telah dipilih
            try:
                # Jalankan fungsi ekstraksi tekstur
                ekstraksi_tekstur(self.image_file_path)
                
                # Tampilkan pesan sukses menggunakan QMessageBox
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setWindowTitle("Ekstraksi Tekstur Berhasil")
                msg.setText(f"Ekstraksi tekstur selesai untuk {self.image_file_path}. Hasil disimpan di 'D:/ekstraksi_fitur/ekstraksi_tekstur.xlsx'.")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()  # Menampilkan popup sukses

            except Exception as e:
                # Jika terjadi kesalahan, tampilkan pesan error
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Error")
                msg.setText(f"Terjadi kesalahan: {str(e)}")
                msg.setStandardButtons(QMessageBox.Ok)
                msg.exec_()  # Menampilkan popup error
        else:
            # Jika gambar belum dipilih, tampilkan pesan peringatan
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setWindowTitle("Gambar Belum Dipilih")
            msg.setText("Silakan pilih gambar terlebih dahulu.")
            msg.setStandardButtons(QMessageBox.Ok)
            msg.exec_()  # Menampilkan popup peringatan

    def clear_image(self):
        # Clear the pixmap from both labels
        self.originalImageLabel.clear()  # Clears the original image
        self.processedImageLabel.clear()  # Clears the processed image
        self.originalImageLabel.disable_cropping()
        
        # Mengembalikan ukuran label ke ukuran semula
        default_label_width = 750
        default_label_height = 800
        
        self.originalImageLabel.setFixedSize(default_label_width, default_label_height)
        self.processedImageLabel.setFixedSize(default_label_width, default_label_height)
        
        # Mengatur ukuran dan posisi jendela ke ukuran default
        screen_geometry = QDesktopWidget().availableGeometry()  # Mendapatkan ukuran layar
        x = (screen_geometry.width() - self.default_width) // 2  # Menghitung posisi X tengah
        y = (screen_geometry.height() - self.default_height) // 2  # Menghitung posisi Y tengah

        self.setGeometry(x, y, self.default_width, self.default_height)

        print("Images cleared from both labels and window size reset to default")
    
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Ui_MainWindow()
    window.show()
    sys.exit(app.exec_())