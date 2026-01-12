from pathlib import Path
from typing import Any
import warnings
import tomllib

import omegaconf

config_files = sorted(Path("config").glob("*.toml"))


# Read TOML config file (OmegaConf does not support TOML by default)
def read_toml_config(file: str) -> dict[str, Any] | None:
    path = Path(file)
    if not path.exists():
        warnings.warn(f"Could not load config file '{path}'.")
        return None
    with Path(file).open("rb") as f:
        return tomllib.load(f)


# Load base and local config
toml_configs = [read_toml_config(file) for file in config_files]
configs = [
    omegaconf.OmegaConf.create(config) for config in toml_configs if config is not None
]

# Merge recursively — subsequent files override earlier files
settings = omegaconf.OmegaConf.merge(*configs)
omegaconf.OmegaConf.resolve(settings)


# Convert all path strings to Path objects
def convert_paths(obj):
    for k, v in obj.items():
        if isinstance(v, str):
            obj[k] = Path(v)
            if not obj[k].exists():
                warnings.warn(f"Could not find configured path '{obj[k]}'.")
        elif isinstance(v, omegaconf.omegaconf.DictConfig):
            convert_paths(v)


convert_paths(settings.paths)
