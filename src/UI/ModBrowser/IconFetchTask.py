from PySide6.QtCore import QRunnable
import requests


class IconFetchTask(QRunnable):
    """
    A task which fetches an icon from mod.io.
    """

    def __init__(self, mod):
        super().__init__()
        self.mod = mod

    def run(self):
        """
        Runs the task.
        """
        self.mod.icon_data = requests.get(self.mod.logo.small).content
