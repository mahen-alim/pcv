# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1079, 673)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.graphInputGbr = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphInputGbr.setGeometry(QtCore.QRect(10, 10, 411, 391))
        self.graphInputGbr.setObjectName("graphInputGbr")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1079, 31))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        
        # Create actions
        self.actionBuka = QtWidgets.QAction(MainWindow)
        self.actionBuka.setObjectName("actionBuka")
        self.actionSImpan_Sebagai = QtWidgets.QAction(MainWindow)
        self.actionSImpan_Sebagai.setObjectName("actionSImpan_Sebagai")
        self.actionKeluar = QtWidgets.QAction(MainWindow)
        self.actionKeluar.setObjectName("actionKeluar")
        
        # Add actions to menu
        self.menuFile.addAction(self.actionBuka)
        self.menuFile.addAction(self.actionSImpan_Sebagai)
        self.menuFile.addAction(self.actionKeluar)
        self.menubar.addAction(self.menuFile.menuAction())
        
        # Connect actions to slots
        self.actionBuka.triggered.connect(self.openFile)
        self.actionKeluar.triggered.connect(MainWindow.close)
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.actionBuka.setText(_translate("MainWindow", "Buka"))
        self.actionSImpan_Sebagai.setText(_translate("MainWindow", "Simpan Sebagai.."))
        self.actionKeluar.setText(_translate("MainWindow", "Keluar"))

    def openFile(self):
        # Open file dialog
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Open Image File", "", "Images (*.png *.jpg *.bmp)")
        
        if file_path:
            # Load and display image
            pixmap = QtGui.QPixmap(file_path)
            scene = QtWidgets.QGraphicsScene()
            scene.addPixmap(pixmap)
            self.graphInputGbr.setScene(scene)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
