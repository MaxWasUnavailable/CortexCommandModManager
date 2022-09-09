from src.ModManager.ModManager import ModManager
from src.UI.ManagerTabWidget import TabWidget
from UI.utils.UIPopup import UIPopup
from src.utils.logger import get_logger
from src.Config.Config import Config
from PySide6 import QtWidgets


class CCMMMainwindow(QtWidgets.QMainWindow):
    """
    Cortex Command Mod Manager Main Window

    Main GUI window.
    Holds all widgets.
    """
    def __init__(self, parent=None, config: Config = None):
        """
        Initialises the window.
        :param parent: Parent widget. Optional since this is the main window.
        :param config: Config object to use as config. Optional.
        """
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Setting up main window...")

        self.central_widget = None
        self.popups = []

        self.config = config or Config.default()
        self.mod_manager = ModManager(config)

        self.setup_window()
        self.logger.info("Main window setup complete.")

    def closeEvent(self, QCloseEvent) -> None:
        """
        Called when the window closes.
        Close all remaining popups when the window is closed.
        """
        for popup in self.popups:
            popup.close()

    def popup(self, message: str) -> None:
        """
        Create and show a popup dialogue.
        :param message: The message to display.
        """
        self.popups.append(UIPopup(message))

    def setup_window(self) -> None:
        """
        Sets up the window.
        Initialises the necessary widgets.
        """
        self.setWindowTitle("Cortex Command Mod Manager")

        self.setMinimumSize(*[1200, 800])

        self.central_widget = TabWidget(parent=self, mod_manager=self.mod_manager)
        self.setCentralWidget(self.central_widget)
