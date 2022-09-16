from src.ModManager.InstalledMod import InstalledMod
from src.utils.logger import get_logger
from src.Config.Config import Config
from modio import Client
from modio.game import Game, Mod
from zipfile import ZipFile
from typing import List
import requests
import json
import os


class ModManager:
    """
    A mod manager for Cortex Command.
    """
    def __init__(self, config: Config = None):
        self.logger = get_logger()
        self.logger.debug("ModManager initialising")

        self.config = config or Config.default()

        self.client: Client = None
        self.game: Game = None

        self.cached_mods: List[Mod] = []
        self.cached_installed_mods: List[InstalledMod] = []

        self.init_client()

    def init_client(self):
        """
        Initialize the mod.io client.
        """
        api_key = self.config["modio"]["api_key"]
        game_id = self.config["modio"]["game_id"]

        self.client = Client(api_key=api_key)
        self.logger.debug("Mod.io client initialized")

        self.game = self.client.get_game(game_id=game_id)
        self.logger.debug(f"Mod.io game initialized with game {self.game.name}")

    async def init_async(self):
        """
        Start the async client.
        """
        await self.client.start()
        self.logger.debug("Mod.io client async started")

    def get_mods(self, tag_filters: list = None, name_filter: str = None):
        """
        Get all mods from the game.
        """
        mods = self.game.get_mods().results
        self.logger.debug(f"Found {len(mods)} mods")

        mods = self.filter_mods(mods, tag_filters, name_filter)

        self.cached_mods = mods

        return mods

    def filter_mods(self, mods: list = None, tag_filters: list = None, name_filter: str = None):
        """
        Filter mods by tags and name.
        :param mods: The mods to filter.
        :param tag_filters: The tags to filter by.
        :param name_filter: The name to filter by.
        :return: The filtered mods.
        """
        if mods is None:
            mods = self.cached_mods

        # TODO: Match tags partially
        if tag_filters is not None:
            mods = [mod for mod in mods if all(tag.lower() in self.mod_tags(mod, lower=True) for tag in tag_filters)]
            self.logger.debug(f"Filtered by tags {tag_filters} to {len(mods)} mods")

        if name_filter is not None:
            mods = [mod for mod in mods if name_filter.lower() in mod.name.lower()]
            self.logger.debug(f"Filtered by name {name_filter} to {len(mods)} mods")

        return mods

    def get_mod(self, mod_id: int):
        """
        Get a mod from the game.
        """
        mod = self.game.get_mod(mod_id=mod_id)
        if mod is None:
            self.logger.error(f"Mod with id {mod_id} not found")
            return False

        return mod

    def save_mod(self, mod: Mod):
        """
        Save a mod to the mods directory.
        """
        mod_file = mod.get_files().results[-1]
        self.logger.debug(f"Found mod file {mod_file}")

        version = mod_file.version
        tags = self.mod_tags(mod)
        mod_file = requests.get(mod.file.url)

        with open(f"{self.config['mods_directory']}/{mod.name}.zip", "wb") as f:
            f.write(mod_file.content)

        self.logger.debug(f"Downloaded mod zip {mod.name} to {self.config['mods_directory']}/{mod.name}.zip")

        zip_file = ZipFile(f"{self.config['mods_directory']}/{mod.name}.zip")

        rte_name = [file for file in zip_file.namelist() if file[:-1].endswith(".rte")][0]

        zip_file.extractall(f"{self.config['mods_directory']}")
        self.logger.debug(f"Extracted mod {mod.name} to {self.config['mods_directory']}/{rte_name}")
        zip_file.close()

        self.logger.debug(f"Deleting mod {mod.name} zip file")
        os.remove(f"{self.config['mods_directory']}/{mod.name}.zip")
        self.logger.debug(f"Deleted mod {mod.name} zip file")

        self.logger.debug(f"Finished downloading mod {mod.name}")

        with open(f"{self.config['mods_directory']}/{rte_name}/ccmm.json", "w") as f:
            data = {
                "name": mod.name,
                "version": version,
                "tags": tags
            }
            json.dump(data, f)

        return True

    def get_installed_mods(self):
        """
        Get all installed mods.
        """
        mod_dirs = os.listdir(self.config["mods_directory"])
        mod_dirs = [mod_dir for mod_dir in mod_dirs if mod_dir.endswith(".rte") and mod_dir != "Base.rte"]
        self.logger.debug(f"Found {len(mod_dirs)} installed mods")

        mods = []

        mod_io_mods = self.cached_mods
        if mod_io_mods is None:
            mod_io_mods = self.get_mods()

        for mod_dir in mod_dirs:
            index_ini_path = os.path.join(self.config["mods_directory"], mod_dir, "index.ini")
            if not os.path.exists(index_ini_path):
                self.logger.debug(f"Found mod without index.ini: {mod_dir}")
                continue

            ccmm_json_path = os.path.join(self.config["mods_directory"], mod_dir, "ccmm.json")
            if os.path.exists(ccmm_json_path):
                with open(ccmm_json_path, "r") as f:
                    data = json.load(f)
                self.logger.debug(f"Found valid ccmm.json: {data}")
                mod = InstalledMod(index_ini_path, data)

            else:
                mod = InstalledMod(index_ini_path)

            mod_io_mod = self.filter_mods(mod_io_mods, name_filter=mod.name)
            if len(mod_io_mod) > 0:
                mod_io_mod = mod_io_mod[0]
                mod.mod = mod_io_mod
                self.logger.debug(f"Found matching mod.io mod: {mod_io_mod.name}")

            mods.append(mod)

        self.cached_installed_mods = mods

        self.logger.debug(f"Found {len(mods)} valid installed mods")
        return mods

    @staticmethod
    def mod_tags(mod: Mod, lower: bool = False):
        """
        Get a list of tags for a mod.
        """
        tags = [tag for tag in mod.tags]
        if lower:
            tags = [tag.lower() for tag in tags]
        return tags
