from PySide6.QtWidgets import QApplication
from src.UI.CCMMMainWindow import CCMMMainwindow
import sys


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = CCMMMainwindow()

    main_window.show()

    sys.exit(app.exec())
