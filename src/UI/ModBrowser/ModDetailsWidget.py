from PySide6 import QtWidgets, QtCore, QtGui
from src.ModManager.ModManager import ModManager
from UI.utils.GenericThread import GenericThread
from src.UI.ModBrowser.ModListItem import ModListItem
from src.UI.ModBrowser.Tasks.ImagesFetchTask import ImagesFetchTask
from src.utils.logger import get_logger
from modio.mod import Mod


class ModDetailsWidget(QtWidgets.QWidget):
    """
    A widget which displays the details of a mod.
    """
    def __init__(self, parent=None, mod_manager: ModManager = None):
        super().__init__(parent)
        self.logger = get_logger()
        self.logger.info("Setting up mod details widget...")

        self.mod_manager = mod_manager

        self.mod: Mod = None

        self.layout = None

        self.image_label: QtWidgets.QLabel = None
        self.name_label: QtWidgets.QLabel = None
        self.description_text: QtWidgets.QTextEdit = None
        self.download_button: QtWidgets.QPushButton = None
        self.close_button: QtWidgets.QPushButton = None

        self.setup_ui()
        self.logger.info("Mod details widget setup complete.")

    def setup_ui(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        self.image_label = QtWidgets.QLabel()
        self.layout.addWidget(self.image_label)

        self.name_label = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setPixelSize(20)
        self.name_label.setFont(font)
        self.layout.addWidget(self.name_label)

        self.description_text = QtWidgets.QTextBrowser()
        self.description_text.setReadOnly(True)
        self.description_text.setAcceptRichText(True)
        self.description_text.setOpenExternalLinks(True)
        self.layout.addWidget(self.description_text)

        self.download_button = QtWidgets.QPushButton("Download")
        self.layout.addWidget(self.download_button)

        self.close_button = QtWidgets.QPushButton("Close")
        self.layout.addWidget(self.close_button)

        self.close_button.clicked.connect(self.parent().parent().close_details)

        self.setMaximumWidth(400)

    def update_ui(self):
        """
        Update the UI to reflect the current mod.
        """
        # TODO: Clean this up a bit.
        # If self.mod has images_data
        if hasattr(self.mod, "images_data"):
            if self.mod.images_data not in [None, []]:
                images_data = self.mod.images_data[0]
                images_pixmap = QtGui.QPixmap()
                images_pixmap.loadFromData(images_data)

                self.image_label.setPixmap(images_pixmap)
                self.image_label.setMaximumWidth(600)
                self.image_label.setMaximumHeight(200)
                self.image_label.setPixmap(self.image_label.pixmap().scaled(600, 600, QtCore.Qt.KeepAspectRatio))
            else:
                self.image_label.setText("No image available.")
        else:
            self.image_label.setText("No image available.")

        self.name_label.setText(self.mod.name)
        self.description_text.setText(self.mod.description)

    def fetch_mod_images(self):
        """
        Fetch the images for the current mod.
        """
        self.mod.images_data = self.mod_manager.get_mod_images(self.mod.id)
        self.update_ui()

    def set_mod(self, mod: Mod):
        """
        Set the mod to display the details of.
        """
        if mod is None:
            return
        self.mod = mod
        QtCore.QThreadPool.globalInstance().start(ImagesFetchTask(self.mod))
        self.update_ui()
