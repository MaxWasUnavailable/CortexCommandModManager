

class InstalledMod:
    """
    Simple class to represent an installed mod.
    """
    def __init__(self, index_ini_path: str, ccmm_data: dict = None):
        """
        Initialize the InstalledMod class.
        """
        self.index_ini_path = index_ini_path
        self.index_ini_dict = {}

        index_ini = open(self.index_ini_path, "r")
        for line in index_ini:
            line = line.strip()
            if "=" not in line:
                continue
            if line.startswith("#"):
                continue
            if line == "":
                continue
            key, value = line.split("=")
            key = key.strip()
            value = value.strip()

            self.index_ini_dict[key] = value
        index_ini.close()

        self.name = self.index_ini_dict.get("ModuleName", "Unknown")
        self.version = self.index_ini_dict.get("Version", "Unknown")

        if ccmm_data is not None:
            self.name = ccmm_data.get("name", self.name)
            self.version = ccmm_data.get("version", self.version)

        # Mod.io Mod object. None by default, in case of no internet connection or if the mod is not (or no longer) on mod.io.
        # Should be set by the ModManager class.
        self.mod = None

    def __str__(self):
        if self.mod is not None:
            return str(self.mod)
        return f"InstalledMod({self.name}, {self.version})"

    def __repr__(self):
        if self.mod is not None:
            return repr(self.mod)
        return self.__str__()
