from PySide6 import QtWidgets
from src.ModManager.ModManager import ModManager
from UI.utils.GenericThread import GenericThread
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
        self.search_bar: QtWidgets.QLineEdit = None
        self.tags_bar: QtWidgets.QLineEdit = None
        self.mod_list: ModListWidget = None
        self.refresh_button: QtWidgets.QPushButton = None

        self.filter_thread = GenericThread(self, self.apply_filters)

        self.setup_ui()

        self.logger.info("Mod browser view setup complete.")

    def set_button_enabled(self, enabled: bool):
        """
        Sets the refresh button to enabled or disabled.
        :param enabled: Whether the button should be enabled.
        """
        self.refresh_button.setEnabled(enabled)

    def set_button_loading(self, loading: bool):
        """
        Sets the refresh button to loading or not loading.
        :param loading: Whether the button should be loading.
        """
        if loading:
            self.refresh_button.setText("Loading...")
        else:
            self.refresh_button.setText("Refresh")

    def apply_filters(self):
        """
        Applies the filters to the mod list.
        """
        search_term = self.search_bar.text()
        tags = self.tags_bar.text()

        if search_term == "":
            search_term = None
        else:
            search_term = search_term.lower()

        if tags == "":
            tags = None
        else:
            tags = tags.lower().split(",")

        self.mod_list.apply_filters(search_term, tags)

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
        self.search_bar.textChanged.connect(self.filter_thread.start)
        self.tags_bar.textChanged.connect(self.filter_thread.start)

        self.filter_thread.finished.connect(self.mod_list.refresh_list)
