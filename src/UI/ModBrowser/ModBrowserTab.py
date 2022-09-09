from PySide6 import QtWidgets
from src.ModManager.ModManager import ModManager
from UI.ModBrowser.ModListWidget import ModListWidget
from src.utils.logger import get_logger


class ModBrowserView(QtWidgets.QWidget):
    """
    Mod Browser view widget.

    Holds all widgets related to the mod browser.
    """

    def __init__(self, parent=None, mod_manager: ModManager = None):
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Setting up mod browser view...")

        self.mod_manager = mod_manager

        self.mod_view = None
        self.mod_list_container = None
        self.layout = None
        self.search_bar = None
        self.tags_bar = None
        self.mod_list = None
        self.refresh_button = None

        self.setup_ui()
        self.logger.info("Mod browser view setup complete.")

    def setup_ui(self):
        """
        Sets up the UI.
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.layout.addWidget(self.search_bar)

        self.tags_bar = QtWidgets.QLineEdit()
        self.tags_bar.setPlaceholderText("Tags...")
        self.layout.addWidget(self.tags_bar)

        self.mod_list = ModListWidget(self, self.mod_manager)
        self.layout.addWidget(self.mod_list)

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.layout.addWidget(self.refresh_button)

        self.refresh_button.clicked.connect(self.mod_list.refresher_thread.start)
