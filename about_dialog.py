import sys
from PyQt5.QtWidgets import QApplication, QMessageBox

def about_dialog():
    # Membuat objek QMessageBox
    dialog = QMessageBox()

    # Menentukan judul pop-up
    dialog.setWindowTitle("About")

    # Menentukan ikon pesan (informasi)
    dialog.setIcon(QMessageBox.Information)

    # Menentukan teks utama (pesan yang ditampilkan), dengan beberapa baris
    dialog.setText("Tugas Citra Vision\n"
                   "Author: C3 Group\n"
                   "Class: C\n"
                   "Study: Informatics Technology")

    # Menambahkan keterangan tambahan jika diperlukan
    dialog.setInformativeText("Aplikasi ini dikembangkan untuk tugas mata kuliah 'Pengolahan Citra & Vision'.")

    # Menambahkan tombol OK
    dialog.setStandardButtons(QMessageBox.Ok)

    # Menampilkan pop-up
    dialog.exec_()

if __name__ == "__main__":
    # Inisialisasi aplikasi PyQt
    app = QApplication(sys.argv)
    
    # Menampilkan pop-up about dialog
    about_dialog()

    # Menutup aplikasi dengan aman
    sys.exit(app.exec_())
