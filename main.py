from PyQt5.QtWidgets import QApplication
from core.window import MainWindow
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())