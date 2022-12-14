from ruamel import yaml

yaml = yaml.YAML()


class Config(dict):
    """
    Config class for reading and writing of yaml config files.

    Inherits from dict.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the config class.
        """
        super(Config, self).__init__(*args, **kwargs)

    def read_config(self, config_file: str = None):
        """
        Read the config file.
        """
        if config_file is not None:
            with open(config_file, "r") as f:
                self.update(yaml.load(f))

    def write_config(self, config_file: str = None):
        """
        Write the config file.
        """
        if config_file is not None:
            with open(config_file, "w") as f:
                yaml.dump(self, f)

    @classmethod
    def from_file(cls, config_file: str = None, default_first: bool = True):
        """
        Create a new instance of Config from a config file.
        """
        if default_first:
            config = cls.default()
        else:
            config = cls()
        config.read_config(config_file)
        return config

    @classmethod
    def from_dict(cls, config_dict: dict = None, default_first: bool = True):
        """
        Create a new instance of Config from a dictionary.
        """
        if default_first:
            config = cls.default()
        else:
            config = cls()
        config.update(config_dict)
        return config

    @staticmethod
    def default():
        """
        Return a default config.
        """
        return Config.from_dict(
            {
                "modio": {
                    "api_key": "ab779d10d97eadfb36b43c27ec6292a3",
                    "game_id": 508
                },
                "mods_directory": "./mods"
            },
            default_first=False
        )


if __name__ == '__main__':
    test = Config.default()

    print(test)
