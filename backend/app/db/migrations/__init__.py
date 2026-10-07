from __future__ import annotations

import importlib.util
from pathlib import Path


# Supports CON-TECH-01, DOM-PDPA-01, IF-HIS-01
_module_path = Path(__file__).with_name("001_init.py")
_spec = importlib.util.spec_from_file_location("booking_migration_001", _module_path)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Unable to load migration module from {_module_path}")
_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_module)
upgrade = _module.upgrade
