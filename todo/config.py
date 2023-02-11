"""Config loader."""
from pathlib import Path
from json import load
from .sources import GoogleScriptSource, Source

CONFIG_FILE_PATH = Path("~/.config/tmq/todo.json").expanduser()

SOURCES_CONFIG_NAMES = {
    "google_script": GoogleScriptSource,
}


def get_source_from_config(path: Path = CONFIG_FILE_PATH) -> Source:
    """Get config from file."""
    with path.open() as f:
        conf = load(f)

    source = SOURCES_CONFIG_NAMES[conf["source"]["name"]](
        **(conf["source"]["params"] if "params" in conf["source"].keys() else {})
    )
    return source


def get_source_from_dict(conf: dict) -> Source:
    """TODO: implement later."""
