from __future__ import annotations

import os
import sys

from .app import WhisperGnomeApplication


def _ensure_dev_schema_dir() -> None:
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
    data_dir = os.path.join(base_dir, "data")
    if os.path.isdir(data_dir) and "GSETTINGS_SCHEMA_DIR" not in os.environ:
        os.environ["GSETTINGS_SCHEMA_DIR"] = data_dir


def main() -> int:
    _ensure_dev_schema_dir()
    app = WhisperGnomeApplication()
    return app.run(sys.argv)


if __name__ == "__main__":
    raise SystemExit(main())
