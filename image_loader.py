import logging
from pathlib import Path
import zipfile
import cv2
from PIL import Image
import os
import json

from config import settings


class LoadWinAmpSkin:
    """
    The class gets a path to a WSZ file and unzips it to a directory.
    It updates winamp.json with the path to the skin. If the winamp.json
    file does not exist, it creates one. The class also creates a
    directory to store the skin files.
    """

    def __init__(self, path: Path):
        self.path: str = path.absolute()
        self.file_name: str = path.name
        self.winamp_path: Path = settings.base_path
        self.base_skin: Path = settings.read_or_create_config(
            'base_skin',
            self.winamp_path / 'base_skin'
        )
        self.skins_folder = settings.read_or_create_config(
            'skins_folder',
            self.winamp_path / 'skins'
        )

    def load_skin(self):
        """
        Function to load a WinAmp skin
        """
        try:
            # Unzip the skin file
            with zipfile.ZipFile(self.path, 'r') as zip_ref:
                zip_ref.extractall(self.skins_folder / self.file_name)
        except Exception as e:
            logging.error(f"Failed to unzip {self.path}.")
            return None

        settings.add_config(key='skin', value=self.skins_folder / self.file_name)



# TODO: Fix to use settings
class ImageLoader:
    def __init__(self, path: Path):
        self.path: str = path.absolute()
        self.file_name: str = path.name
        self.base_skin: Path = Path(os.getcwd()) / 'base_skin'

    def load_image(self):
        """
        Function to load an image
        """
        try:
            sprite_image = cv2.imread(self.path)
            if sprite_image is None:
                sprite_image = cv2.imread(self.base_skin / self.file_name)
        except Exception as e:
            logging.error(f"Failed to read {self.path} using OpenCV.")
            return None

