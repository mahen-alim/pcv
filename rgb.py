import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QLabel, QVBoxLayout, 
QHBoxLayout, QPushButton, QFileDialog, QWidget)
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Aplikasi Filter Fuzzy HE RGB")
        self.setGeometry(100, 100, 800, 400)

        # Layout utama
        layout = QHBoxLayout()

        # Label untuk gambar asli
        self.labelGambar1 = QLabel(self)
        self.labelGambar1.setStyleSheet("background-color: white;")
        self.labelGambar1.setFixedSize(350, 350)
        self.labelGambar1.setAlignment(Qt.AlignCenter)

        # Label untuk gambar edit
        self.labelGambar2 = QLabel(self)
        self.labelGambar2.setStyleSheet("background-color: white;")
        self.labelGambar2.setFixedSize(350, 350)
        self.labelGambar2.setAlignment(Qt.AlignCenter)

        # Tombol buka file
        self.btnBukaFile = QPushButton("Buka File", self)
        self.btnBukaFile.clicked.connect(self.bukaFile)

        # Tombol terapkan filter Fuzzy HE RGB
        self.btnTerapkanFilter = QPushButton("Terapkan Fuzzy HE RGB", self)
        self.btnTerapkanFilter.clicked.connect(self.fuzzy_he_rgb)

        # Layout tombol
        tombolLayout = QVBoxLayout()
        tombolLayout.addWidget(self.btnBukaFile)
        tombolLayout.addWidget(self.btnTerapkanFilter)

        # Tambahkan label dan tombol ke layout utama
        layout.addWidget(self.labelGambar1)
        layout.addWidget(self.labelGambar2)
        layout.addLayout(tombolLayout)

        # Buat widget utama
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Variabel untuk menyimpan gambar
        self.pixmapGambar1 = None

    def bukaFile(self):
        # Buka file dialog untuk memilih gambar
        filePath, _ = QFileDialog.getOpenFileName(self, "Buka File Gambar", "", "Image Files (*.png *.jpg *.bmp)")
        if filePath:
            self.pixmapGambar1 = QPixmap(filePath)
            self.labelGambar1.setPixmap(self.pixmapGambar1.scaled(self.labelGambar1.size(), Qt.KeepAspectRatio))

    def fuzzy_he_rgb(self):
        if self.pixmapGambar1 is not None:
            # Konversi gambar dari QPixmap ke QImage
            input_image = self.pixmapGambar1.toImage()
            width = input_image.width()
            height = input_image.height()

            # Buat QImage untuk output
            output_image = QImage(width, height, QImage.Format_RGB32)

            # Proses setiap piksel secara manual
            for y in range(height):
                for x in range(width):
                    pixel_color = input_image.pixel(x, y)
                    color = QColor(pixel_color)
                    
                    # Ambil nilai R, G, B
                    r = color.red()
                    g = color.green()
                    b = color.blue()

                    # Terapkan Fuzzy HE RGB untuk masing-masing channel
                    r = self.apply_fuzzy_he_rgb(r)
                    g = self.apply_fuzzy_he_rgb(g)
                    b = self.apply_fuzzy_he_rgb(b)

                    # Set piksel hasil ke gambar output
                    output_image.setPixel(x, y, QColor(r, g, b).rgb())

            # Tampilkan gambar hasil edit di label kedua
            self.labelGambar2.setPixmap(QPixmap.fromImage(output_image).scaled(self.labelGambar2.size(), Qt.KeepAspectRatio))

    def apply_fuzzy_he_rgb(self, value):
        """
        Terapkan rumus Fuzzy HE RGB:
        - Jika value < 128: 2 * (value^2) / 255
        - Jika value >= 128: 255 - 2 * (255 - value)^2 / 255
        """
        if value < 128:
            return int(2 * (value ** 2) / 255.0)
        else:
            return int(255 - 2 * ((255 - value) ** 2) / 255.0)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())