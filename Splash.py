from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QSplashScreen

class SplashScreen(QSplashScreen):
    def __init__(self):
        super().__init__(QPixmap("splash.png"))
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.showMessage("Loading...")
