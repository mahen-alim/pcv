from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QSlider, QDesktopWidget
from PyQt5.QtCore import Qt, QRect

class ColorCorrectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Linear Adjustment')
        self.setGeometry(100, 100, 400, 200)

        # Initialize sliders
        self.slider_saturation = QSlider(Qt.Horizontal, self)
        self.slider_contrast = QSlider(Qt.Horizontal, self)
        self.slider_brightness = QSlider(Qt.Horizontal, self)

        # Set default values for sliders
        self.slider_saturation.setMinimum(0)
        self.slider_saturation.setMaximum(200)
        self.slider_saturation.setValue(100)
        self.slider_saturation.setTickInterval(10)
        self.slider_saturation.setTickPosition(QSlider.TicksBelow)

        self.slider_contrast.setMinimum(0)
        self.slider_contrast.setMaximum(200)
        self.slider_contrast.setValue(100)
        self.slider_contrast.setTickInterval(10)
        self.slider_contrast.setTickPosition(QSlider.TicksBelow)

        self.slider_brightness.setMinimum(-100)
        self.slider_brightness.setMaximum(100)
        self.slider_brightness.setValue(0)
        self.slider_brightness.setTickInterval(10)
        self.slider_brightness.setTickPosition(QSlider.TicksBelow)

        # Create labels for sliders
        self.label_saturation = QLabel('Saturation: 1.0')
        self.label_contrast = QLabel('Contrast: 1.0')
        self.label_brightness = QLabel('Brightness: 0')

        # Create OK button
        self.ok_button = QPushButton('OK', self)

        # Layout for sliders and button
        layout = QVBoxLayout()
        layout.addWidget(self.label_saturation)
        layout.addWidget(self.slider_saturation)
        layout.addWidget(self.label_contrast)
        layout.addWidget(self.slider_contrast)
        layout.addWidget(self.label_brightness)
        layout.addWidget(self.slider_brightness)
        layout.addWidget(self.ok_button)
        self.setLayout(layout)

        # Connect sliders to update functions
        self.slider_saturation.valueChanged.connect(self.update_labels)
        self.slider_contrast.valueChanged.connect(self.update_labels)
        self.slider_brightness.valueChanged.connect(self.update_labels)

        # Close dialog on OK button click
        self.ok_button.clicked.connect(self.accept)

        # Center the dialog
        self.center()

    def center(self):
        # Center the dialog on the screen
        frame_geom = self.frameGeometry()
        screen = QDesktopWidget().screenGeometry()
        frame_geom.moveCenter(screen.center())
        self.move(frame_geom.topLeft())

    def update_labels(self):
        # Update labels based on slider values
        self.label_saturation.setText(f'Saturation: {self.slider_saturation.value() / 100:.2f}')
        self.label_contrast.setText(f'Contrast: {self.slider_contrast.value() / 100:.2f}')
        self.label_brightness.setText(f'Brightness: {self.slider_brightness.value()}')

    def get_values(self):
        # Return the current values of sliders
        saturation = self.slider_saturation.value() / 100
        contrast = self.slider_contrast.value() / 100
        brightness = self.slider_brightness.value()
        return saturation, contrast, brightness
