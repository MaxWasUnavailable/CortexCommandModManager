from PySide6 import QtCore, QtGui, QtWidgets
from modio.mod import Mod
import requests


class ModListItem(QtWidgets.QWidget):
    """
    A QWidget which represents a mod.
    """
    def __init__(self, parent, mod: Mod):
        super().__init__(parent)

        self.mod = mod

        self.mod_icon = None
        self.mod_name_label = None
        self.mod_tags_label = None

        self.layout = None

        self.setup_ui()

    def setup_ui(self):
        """
        Sets up the UI.
        """
        # If self.mod has icon_data
        if hasattr(self.mod, "icon_data"):
            icon_data = self.mod.icon_data
            icon_pixmap = QtGui.QPixmap()
            icon_pixmap.loadFromData(icon_data)

            self.mod_icon = QtWidgets.QLabel()
            self.mod_icon.setPixmap(icon_pixmap)
            self.mod_icon.setScaledContents(True)
            self.mod_icon.setFixedSize(48, 32)

        self.mod_name_label = QtWidgets.QLabel(self.mod.name)
        font = self.mod_name_label.font()
        font.setBold(True)
        self.mod_name_label.setFont(font)

        self.mod_tags_label = QtWidgets.QLabel(", ".join(self.mod.tags))
        font = self.mod_tags_label.font()
        font.setItalic(True)
        self.mod_tags_label.setFont(font)

        self.layout = QtWidgets.QHBoxLayout()
        if self.mod_icon is not None:
            self.layout.addWidget(self.mod_icon)
        self.layout.addWidget(self.mod_name_label)
        self.layout.addWidget(self.mod_tags_label)
        self.setLayout(self.layout)

    def __lt__(self, other):
        return self.mod.name < other.mod.name

    def __le__(self, other):
        return self.mod.name <= other.mod.name

    def __eq__(self, other):
        return self.mod.name == other.mod.name

    def __ne__(self, other):
        return self.mod.name != other.mod.name

    def __gt__(self, other):
        return self.mod.name > other.mod.name

    def __ge__(self, other):
        return self.mod.name >= other.mod.name
