from PySide6 import QtCore, QtGui, QtWidgets
from modio.mod import Mod


class ModListItemStats(QtWidgets.QWidget):
    """
    Simple widget with a vertical layout that displays the download count & positive vote count.
    """
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignLeft)

        self.downloads = self.parent().total_download_count()
        self.likes = self.parent().total_likes()

        self.download_count_label = QtWidgets.QLabel(f"📥 {self.downloads}")
        self.download_count_label.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.download_count_label)

        self.like_count_label = QtWidgets.QLabel(f"👍 {self.likes}")
        self.like_count_label.setAlignment(QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.like_count_label)

        self.setFixedWidth(80)

        self.setLayout(self.layout)


class ModListItem(QtWidgets.QFrame):
    """
    A QWidget which represents a mod.
    """
    def __init__(self, parent, mod: Mod):
        super().__init__(parent)

        self.mod: Mod = mod

        self.mod_icon = None
        self.mod_name_label = None
        self.mod_summary_label = None
        self.mod_tags_label = None

        self.mod_stats_widget = None
        self.mod_last_updated_label = None

        self.layout = None

        self.setup_ui()

    def total_download_count(self):
        """
        Returns the total download count of this mod.
        """
        return self.mod.stats.downloads

    def total_subscriber_count(self):
        """
        Returns the total subscriber count of this mod.
        """
        return self.mod.stats.subscribers

    def mod_rank(self):
        """
        Returns the mod rank.
        """
        return self.mod.stats.rank

    def total_likes(self):
        """
        Returns the total likes of this mod.
        """
        return self.mod.stats.positive

    def total_dislikes(self):
        """
        Returns the total dislikes of this mod.
        """
        return self.mod.stats.negative

    def last_updated(self):
        """
        Returns the last updated date of this mod.
        """
        return self.mod.updated

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
            self.mod_icon.setMaximumWidth(64)
            self.mod_icon.setMaximumHeight(64)
            self.mod_icon.setPixmap(self.mod_icon.pixmap().scaled(64, 64, QtCore.Qt.KeepAspectRatio))

        self.mod_name_label = QtWidgets.QLabel(self.mod.name)
        self.mod_name_label.setWordWrap(True)
        self.mod_name_label.setFixedWidth(200)
        font = self.mod_name_label.font()
        font.setBold(True)
        self.mod_name_label.setFont(font)

        self.mod_summary_label = QtWidgets.QLabel(self.mod.summary)
        self.mod_summary_label.setWordWrap(True)
        self.mod_summary_label.setFixedWidth(320)

        self.mod_tags_label = QtWidgets.QLabel(", ".join(self.mod.tags))
        self.mod_tags_label.setWordWrap(True)
        self.mod_tags_label.setFixedWidth(400)
        font = self.mod_tags_label.font()
        font.setItalic(True)
        self.mod_tags_label.setFont(font)

        self.mod_stats_widget = ModListItemStats(self)

        self.mod_last_updated_label = QtWidgets.QLabel(f"Updated: {self.last_updated()}")

        self.layout = QtWidgets.QHBoxLayout()
        if self.mod_icon is not None:
            self.layout.addWidget(self.mod_icon)
        self.layout.addWidget(self.mod_name_label)
        self.layout.addWidget(self.mod_summary_label)
        self.layout.addWidget(self.mod_tags_label)
        self.layout.addWidget(self.mod_stats_widget)
        self.layout.addWidget(self.mod_last_updated_label)

        self.layout.setAlignment(QtCore.Qt.AlignLeft)

        self.setLayout(self.layout)

        self.setFrameShape(QtWidgets.QFrame.StyledPanel)

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
