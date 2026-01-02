from __future__ import annotations

import shutil


def check_binary(binary: str) -> bool:
    """Return True if binary is in PATH."""
    return shutil.which(binary) is not None
