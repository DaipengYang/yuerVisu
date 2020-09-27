import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from MainWin import MainWindow

__appname__ = "Yuer Visualization"
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationDisplayName(__appname__)
    app.setWindowIcon(QIcon('icons/app.png'))
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())