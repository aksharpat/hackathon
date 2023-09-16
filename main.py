class MainWindow(QtWidgets.QMainWindow):
    """
    Main window for the <TODO: COOL NAME>.
    Boots on startup of the executable.
    Entry to all other files and subsidary interfaces.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.init_ui()
        self.load_state()
    
    def init_ui(self):
        """
        Initialize the User Interface.
        """
        pass



def main():
    """
    Entry point for the application.
    """
    app = QtWidgets.QApplication([])
    window = MainWindow()

    window.showMaximized()
    app.exec_()


if __name__ == "__main__":
    main()