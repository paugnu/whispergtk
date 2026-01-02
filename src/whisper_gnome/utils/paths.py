from __future__ import annotations

import os
from pathlib import Path


def app_data_dir() -> Path:
    return Path(os.getenv("XDG_DATA_HOME", Path.home() / ".local" / "share")) / "whisper-gnome"
