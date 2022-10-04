from PySide6 import QtWidgets
from src.ModManager.ModManager import ModManager
from UI.utils.GenericThread import GenericThread
from UI.ModBrowser.ModListWidget import ModListWidget, SortingMode
from src.utils.logger import get_logger


class ModBrowserSearch(QtWidgets.QWidget):
    """
    Mod Browser search widget.

    Holds the search, filter & sort UI.
    """
    def __init__(self, parent=None, mod_manager: ModManager = None):
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Setting up mod browser search tab...")

        self.mod_manager = mod_manager

        self.layout = None

        self.v_widget_1 = None
        self.v_widget_1_layout = None
        self.v_widget_2 = None
        self.v_widget_2_layout = None

        self.search_bar: QtWidgets.QLineEdit = None
        self.tags_bar: QtWidgets.QLineEdit = None
        self.sort_by: QtWidgets.QComboBox = None
        self.sort_order: QtWidgets.QComboBox = None

        self.setup_ui()

    def setup_ui(self):
        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        # Set up the first vertical widget
        self.v_widget_1 = QtWidgets.QWidget()
        self.v_widget_1_layout = QtWidgets.QVBoxLayout()

        self.search_bar = QtWidgets.QLineEdit()
        self.search_bar.setPlaceholderText("Search...")
        self.v_widget_1_layout.addWidget(self.search_bar)

        self.tags_bar = QtWidgets.QLineEdit()
        self.tags_bar.setPlaceholderText("Tags...")
        self.v_widget_1_layout.addWidget(self.tags_bar)

        self.v_widget_1.setLayout(self.v_widget_1_layout)

        # Set up the second vertical widget
        self.v_widget_2 = QtWidgets.QWidget()
        self.v_widget_2_layout = QtWidgets.QVBoxLayout()

        self.sort_by = QtWidgets.QComboBox()
        self.sort_by.addItems([SortingMode.NAME.name, SortingMode.DOWNLOADS.name, SortingMode.LIKES.name, SortingMode.LAST_UPDATED.name])
        self.v_widget_2_layout.addWidget(self.sort_by)

        self.sort_order = QtWidgets.QComboBox()
        self.sort_order.addItems(["Ascending", "Descending"])
        self.v_widget_2_layout.addWidget(self.sort_order)

        self.v_widget_2.setLayout(self.v_widget_2_layout)

        # Add the widgets to the main widget's layout
        self.layout.addWidget(self.v_widget_1)
        self.layout.addWidget(self.v_widget_2)

        self.logger.info("Mod browser search tab setup complete.")


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
        self.search_widget: ModBrowserSearch = None
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
        search_term = self.search_widget.search_bar.text()
        tags = self.search_widget.tags_bar.text()

        if search_term == "":
            search_term = None
        else:
            search_term = search_term.lower()

        if tags == "":
            tags = None
        else:
            tags = tags.lower().split(",")

        self.mod_list.apply_filters(search_term, tags)

    def apply_sorting(self):
        """
        Applies the sorting to the mod list.
        """
        sort_by = self.search_widget.sort_by.currentText()
        sort_order = self.search_widget.sort_order.currentText()

        if sort_order == "Ascending":
            sort_order = True
        else:
            sort_order = False

        self.mod_list.apply_sorting(SortingMode.from_name(sort_by), sort_order)

    def setup_ui(self):
        """
        Sets up the UI.
        """
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.search_widget = ModBrowserSearch(self, self.mod_manager)
        self.layout.addWidget(self.search_widget)

        self.mod_list = ModListWidget(self, self.mod_manager)
        self.layout.addWidget(self.mod_list)

        self.refresh_button = QtWidgets.QPushButton("Refresh")
        self.layout.addWidget(self.refresh_button)

        self.refresh_button.clicked.connect(self.mod_list.refresher_thread.start)
        self.search_widget.search_bar.textChanged.connect(self.filter_thread.start)
        self.search_widget.tags_bar.textChanged.connect(self.filter_thread.start)
        self.search_widget.sort_by.currentTextChanged.connect(self.apply_sorting)
        self.search_widget.sort_order.currentTextChanged.connect(self.apply_sorting)

        self.filter_thread.finished.connect(self.mod_list.refresh_list)
