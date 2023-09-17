import cv2 as cv
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
)
from components import ElectronicComponent


class LabelSceneWindow(QtWidgets.QDialog):
    """
    Handles the dialog for loading batches and jobs.
    """

    def __init__(self, components: list[ElectronicComponent], parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        """
        Initialize the User Interface.
        """
        # Initialize private variables

        # Set window title
        self.setWindowTitle("Component Labeler")

        # Set up layout
        self.splitter = QtWidgets.QSplitter()
        self.setCentralWidget(self.splitter)

        # Initialize left and right panels
        self.init_left_panel()
        self.init_right_panel()


def main():
    """
    Entry for testing purposes.
    Not used in the full app.
    """
    app = QtWidgets.QApplication([])
    window = LabelSceneWindow()

    window.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()
