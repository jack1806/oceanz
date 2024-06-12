from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
from Windows.app_window import OceanZApp
import sys
import os

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'oceanz.lounge.com'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(os.path.join(basedir, 'logo.ico')))
    window = OceanZApp()
    window.show()
    sys.exit(app.exec())
