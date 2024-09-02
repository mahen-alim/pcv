from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # Membuat menubar
        self.menubar = self.menuBar()

        # Membuat menu "File"
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuFile.setTitle("File")
        
        # Menambahkan menu "File" ke menubar
        self.menubar.addMenu(self.menuFile)

        # Membuat aksi untuk "Gambar"
        self.actionGambar = QtWidgets.QAction("Gambar", self)
        self.actionGambar.setObjectName("actionGambar")
        self.actionGambar.triggered.connect(self.openFileDialog)  # Menghubungkan aksi dengan fungsi openFileDialog
        self.menuFile.addAction(self.actionGambar)

        # Membuat aksi untuk "Simpan Sebagai"
        self.actionSimpan_Sebagai = QtWidgets.QAction("Simpan Sebagai", self)
        self.actionSimpan_Sebagai.setObjectName("actionSimpan_Sebagai")
        self.menuFile.addAction(self.actionSimpan_Sebagai)
        
        # Membuat aksi untuk "Keluar"
        self.actionKeluar = QtWidgets.QAction("Keluar", self)
        self.actionKeluar.setObjectName("actionKeluar")
        self.actionKeluar.triggered.connect(self.close)  # Menghubungkan aksi dengan fungsi close (tutup aplikasi)
        self.menuFile.addAction(self.actionKeluar)

    def openFileDialog(self):
        # Membuka dialog pemilihan file
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*);;Image Files (*.png;*.jpg;*.bmp)", options=options)
        if fileName:
            print(f"File yang dipilih: {fileName}")  # Ganti dengan logika yang Anda inginkan setelah memilih file

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
