from PySide6.QtWidgets import QTabWidget
from src.ModManager.ModManager import ModManager
from UI.ModBrowser.ModBrowserTab import ModBrowserView
from src.utils.logger import get_logger


class TabWidget(QTabWidget):
    """
    Main Tabwidget for the application.
    """
    def __init__(self, parent=None, mod_manager: ModManager = None):
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Setting up tab widget...")

        self.mod_manager = mod_manager
        self.tabs = dict()

        self.setup_ui()
        self.setup_tabs()
        self.logger.info("Main tab widget setup complete.")

    def setup_ui(self):
        """
        Sets up the UI.
        """
        self.setTabsClosable(False)
        self.setMovable(True)
        self.setDocumentMode(True)
        self.setTabPosition(QTabWidget.North)

    def setup_tabs(self):
        """
        Sets up the tabs.
        """
        self.add_tab("Mod Browser", ModBrowserView(self, self.mod_manager))

    def add_tab(self, tab_name, tab_widget):
        """
        Adds a tab to the tabwidget.
        :param tab_name: Name of the tab.
        :param tab_widget: Tab widget to add.
        """
        self.tabs[tab_name] = tab_widget
        self.addTab(tab_widget, tab_name)

    def get_tab(self, tab_name):
        """
        Returns the tab with the given name.
        :param tab_name: Name of the tab.
        :return: Tab widget.
        """
        return self.tabs[tab_name]
