from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
)


class MainWindow(QtWidgets.QMainWindow):
    """
    Main window for the Circuit Analyzer.
    Boots on startup of the executable.
    Entry to all other files and subsidiary interfaces.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWindowTitle("Circuit Analyzer")
        self.init_ui()

    def init_ui(self):
        """
        Initialize the User Interface.
        """

        # Central widget and layout
        central_widget = QtWidgets.QWidget(self)
        layout = QVBoxLayout()

        # Combobox for selecting breadboard size
        self.combo = QComboBox()
        self.combo.addItems(
            ["Small Breadboard", "Medium Breadboard", "Large Breadboard"]
        )
        layout.addWidget(self.combo)

        # Button for uploading image
        self.upload_btn = QPushButton("Upload Image")
        self.upload_btn.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_btn)

        # Label for displaying image
        self.image_label = QLabel(self)
        default_image = QtGui.QPixmap("default_breadboard.jpg")
        self.image_label.setPixmap(default_image)
        self.image_label.setScaledContents(True)
        self.image_label.setFixedSize(800, 800)
        layout.addWidget(self.image_label)

        # Analyze Circuit Button
        self.analyze_btn = QPushButton("Analyze Circuit")
        self.analyze_btn.setEnabled(False)  # Disabled by default
        self.analyze_btn.clicked.connect(self.analyze_circuit)
        layout.addWidget(self.analyze_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.xpm *.jpg)", options=options
        )

        if file_name:
            pixmap = QtGui.QPixmap(file_name)
            self.image_label.setPixmap(
                pixmap.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio)
            )
            self.analyze_btn.setEnabled(True)  # Enable the analyze button

    def analyze_circuit(self):
        # TODO: Implement the actual analysis
        QMessageBox.information(
            self, "Analysis", "Circuit analysis will be implemented here!"
        )

    def resizeEvent(self, event):
        if hasattr(self, "image_label"):
            pixmap = self.image_label.pixmap()
            self.image_label.setPixmap(
                pixmap.scaled(self.image_label.size(), QtCore.Qt.KeepAspectRatio)
            )


def main():
    """
    Entry point for the application.
    """
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
