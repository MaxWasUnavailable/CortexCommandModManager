from PySide6.QtCore import QRunnable
from modio.mod import Mod
import requests


class ImagesFetchTask(QRunnable):
    """
    A task which fetches all images from mod.io.
    """

    def __init__(self, mod: Mod):
        super().__init__()
        self.mod = mod

    def run(self):
        """
        Runs the task.
        """
        self.mod.images_data = []
        for image in self.mod.media.images:
            self.mod.images_data.append(requests.get(image.original).content)
