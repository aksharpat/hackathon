import cv2 as cv
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QComboBox,
    QPushButton,
    QFileDialog,
    QMessageBox,
    QScrollArea,
    QLineEdit,
    QHBoxLayout,
)
from components import ElectronicComponent


class LabelSceneWindow(QtWidgets.QDialog):
    def __init__(self, components: list[ElectronicComponent], parent=None):
        super().__init__(parent)
        self.init_ui(components)

    def init_ui(self, components):
        self.setWindowTitle("Component Labeler")

        main_layout = QHBoxLayout()

        # Left panel
        left_layout = QVBoxLayout()
        scroll = QScrollArea(self)
        scroll_widget = QtWidgets.QWidget()
        scroll.setWidget(scroll_widget)
        scroll.setWidgetResizable(True)
        scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        scroll_layout = QVBoxLayout(scroll_widget)

        left_layout.addWidget(QtWidgets.QLabel("Name | Value"))

        self.inputs = []
        for component in components:
            label = QLabel(component.name)
            input = QLineEdit(self)
            self.inputs.append(input)

            h_layout = QHBoxLayout()
            h_layout.addWidget(label)
            h_layout.addWidget(input)

            scroll_layout.addLayout(h_layout)

        generate_button = QPushButton("Generate schematic", self)
        generate_button.clicked.connect(self.generate_schematic)

        left_layout.addWidget(scroll)
        left_layout.addWidget(generate_button)

        # Right panel
        right_layout = QVBoxLayout()
        self.image_label = QLabel("Labeled Image Display")

        # Load the image from 'temp' folder
        pixmap = QtGui.QPixmap("temp/analyzed_image.jpg")
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        right_layout.addWidget(self.image_label)

        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        self.setLayout(main_layout)

    def generate_schematic(self):
        # Check if all inputs are filled
        if any([input.text() == "" for input in self.inputs]):
            QMessageBox.warning(
                self, "Warning", "You must fill out all component values"
            )
        else:
            # Implement the rest of the functionality here
            pass


def main():
    components = [
        ElectronicComponent("R1", "Resistor"),
        ElectronicComponent("R2", "Resistor"),
        ElectronicComponent("R3", "Resistor"),
        ElectronicComponent("R4", "Resistor"),
        ElectronicComponent("R5", "Resistor"),
        ElectronicComponent("R6", "Resistor"),
        ElectronicComponent("R7", "Resistor"),
        ElectronicComponent("R8", "Resistor"),
        ElectronicComponent("R9", "Resistor"),
        ElectronicComponent("R10", "Resistor"),
        ElectronicComponent("L1", "Inductor"),
        ElectronicComponent("L2", "Inductor"),
        ElectronicComponent("L3", "Inductor"),
        ElectronicComponent("L4", "Inductor"),
        ElectronicComponent("L5", "Inductor"),
        ElectronicComponent("L6", "Inductor"),
        ElectronicComponent("C1", "Capacitor"),
        ElectronicComponent("C2", "Capacitor"),
        ElectronicComponent("C3", "Capacitor"),
        ElectronicComponent("C4", "Capacitor"),
        ElectronicComponent("C5", "Capacitor"),
        ElectronicComponent("C6", "Capacitor"),
        ElectronicComponent("C7", "Capacitor"),
        ElectronicComponent("C8", "Capacitor"),
        ElectronicComponent("Q1", "Transistor"),
        ElectronicComponent("Q2", "Transistor"),
        ElectronicComponent("Q3", "Transistor"),
        ElectronicComponent("D1", "Diode"),
        ElectronicComponent("D2", "Diode"),
        ElectronicComponent("D3", "Diode"),
        ElectronicComponent("IC1", "Integrated Circuit"),
        ElectronicComponent("IC2", "Integrated Circuit"),
        ElectronicComponent("IC3", "Integrated Circuit"),
        ElectronicComponent("SW1", "Switch"),
        ElectronicComponent("SW2", "Switch"),
        ElectronicComponent("M1", "Motor"),
        ElectronicComponent("M2", "Motor"),
        ElectronicComponent("LED1", "LED"),
        ElectronicComponent("LED2", "LED"),
        ElectronicComponent("LED3", "LED"),
    ]

    app = QtWidgets.QApplication([])
    window = LabelSceneWindow(components)
    window.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()
