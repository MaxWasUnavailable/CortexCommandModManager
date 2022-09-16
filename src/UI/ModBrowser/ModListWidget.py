from PySide6 import QtWidgets, QtCore
from src.ModManager.ModManager import ModManager
from UI.utils.GenericThread import GenericThread
from src.UI.ModBrowser.ModListItem import ModListItem
from src.UI.ModBrowser.IconFetchTask import IconFetchTask
from src.utils.logger import get_logger
from modio.mod import Mod
import time


class ModListWidget(QtWidgets.QListWidget):
    """
    A QListWidget which lists mods from mod.io.
    """
    def __init__(self, parent=None, mod_manager: ModManager = None):
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Setting up mod list widget...")

        self.mod_manager = mod_manager
        self.mods = []
        self.refresher_thread = GenericThread(self, self.refresh_start)

        self.refresher_thread.finished.connect(self.refresh_end)

        self.icons_enabled = True

        self.refreshing_list = False

        self.setup_ui()
        self.logger.info("Mod list widget setup complete.")

    def setup_ui(self):
        """
        Sets up the UI.
        """
        self.setSortingEnabled(True)

        self.refresher_thread.start()

    def refresh_start(self):
        """
        Called when the list refresh has started.
        """
        self.parent().set_button_enabled(False)
        self.parent().set_button_loading(True)
        self.refresh_mods()

    def refresh_end(self):
        """
        Called when the list refresh has ended.
        """
        self.parent().set_button_enabled(True)
        self.parent().set_button_loading(False)
        self.refresh_list()

    def refresh_mods(self):
        """
        Refreshes the cached mod list.
        """
        self.mods = self.mod_manager.get_mods()

        if self.icons_enabled:
            for mod in self.mods:
                QtCore.QThreadPool.globalInstance().start(IconFetchTask(mod))

            QtCore.QThreadPool.globalInstance().waitForDone()

    def apply_filters(self, search: str = None, tags: list = None):
        """
        Applies a search to the list.
        :param search: The search to apply.
        :param tags: The tags to apply.
        """
        self.mods = self.mod_manager.filter_mods(name_filter=search, tag_filters=tags)

    def refresh_list(self):
        """
        Refreshes the list.
        """
        if self.refreshing_list:
            self.logger.debug("List refresh already in progress, skipping.")
            return
        self.refreshing_list = True

        self.clear()
        for mod in self.mods:
            self.add_item(mod)

        self.refreshing_list = False

    def add_item(self, mod: Mod) -> None:
        """
        Adds an item to the list, and then sets that item to display the given ModListItem widget.
        :param mod: The mod to list.
        """
        item = QtWidgets.QListWidgetItem()
        mod_widget = ModListItem(mod=mod, parent=self)
        item.setSizeHint(mod_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, mod_widget)
