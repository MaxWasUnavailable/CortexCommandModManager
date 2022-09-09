from PySide6 import QtWidgets
from src.ModManager.ModManager import ModManager
from UI.utils.GenericThread import GenericThread
from src.UI.ModBrowser.ModListItem import ModListItem
from src.utils.logger import get_logger
from modio.mod import Mod
import requests
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
        self.refresher_thread = GenericThread(self, self.refresh_mods)
        self.refresher_thread.finished.connect(self.refresh_list)

        self.setup_ui()
        self.logger.info("Mod list widget setup complete.")

    def setup_ui(self):
        """
        Sets up the UI.
        """
        self.setSortingEnabled(True)

        self.refresher_thread.start()

    def refresh_mods(self):
        """
        Refreshes the cached mod list.
        """
        # TODO: Remove the slice
        self.mods = self.mod_manager.get_mods()[10:20]

        # Workaround for loading of icons blocking the UI thread if handled during list population.
        for mod in self.mods:
            start_time = time.time()
            mod.icon_data = requests.get(mod.logo.small).content
            self.logger.debug(f"Icon for mod {mod.name} loaded in {time.time() - start_time} seconds.")

    def refresh_list(self):
        """
        Refreshes the list.
        """
        self.clear()
        for mod in self.mods:
            self.add_item(mod)

    def add_item(self, mod: Mod) -> None:
        """
        Adds an item to the list, and then sets that item to display the given ModEntry widget.
        :param mod: The mod to list.
        """
        item = QtWidgets.QListWidgetItem()
        mod_widget = ModListItem(mod=mod, parent=self)
        item.setSizeHint(mod_widget.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, mod_widget)
