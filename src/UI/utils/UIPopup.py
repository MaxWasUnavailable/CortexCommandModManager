from PySide6 import QtCore, QtWidgets


class UIPopup(QtWidgets.QWidget):
    """
    Simple text popup.
    """
    def __init__(self, message):
        """
        Sets its content to the given message, and enabled rich text representation as well as opening links through the browser.
        Shows itself when it's created, so no further action is necessary after creating this object.
        (Make sure the object doesn't go out of scope, otherwise it'll instantly close)
        # TODO: Replace with built-in QT Dialogue?
        :param message: Message to display.
        """
        super().__init__()
        label = QtWidgets.QLabel(message)
        label.setTextFormat(QtCore.Qt.RichText)
        label.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        label.setOpenExternalLinks(True)
        label.setAlignment(QtCore.Qt.AlignCenter)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(label)
        layout.setAlignment(QtCore.Qt.AlignCenter)

        self.setLayout(layout)
        self.setFixedSize(400, 120)
        self.show()