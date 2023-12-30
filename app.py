import sys
from PyQt5.QtWidgets import QApplication

from PyQt5.QtCore import QTimer

from Splash import SplashScreen

from login import Login   


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    splash = SplashScreen()
    splash.show()
    QTimer.singleShot(3000, splash.close)
    login = Login()
    
    sys.exit(app.exec_())
