#!/usr/bin/env python3
"""Resolve CGP project paths from project_config.json written by /setup."""

import json
from pathlib import Path

_CONFIG_CACHE = None


def load_project_config() -> dict:
    global _CONFIG_CACHE
    if _CONFIG_CACHE is None:
        config_path = Path(__file__).parent / "project_config.json"
        if not config_path.exists():
            raise FileNotFoundError(
                "project_config.json introuvable — lancez /setup d'abord"
            )
        _CONFIG_CACHE = json.loads(config_path.read_text(encoding="utf-8"))
    return _CONFIG_CACHE


def project_dir() -> Path:
    return Path(load_project_config()["project_dir"])


def cgp_root() -> Path:
    return project_dir() / "CGP"


def production_dir() -> Path:
    return cgp_root() / "Production"


def cabinet_dir() -> Path:
    return production_dir() / "_cabinet"


def clients_production_dir() -> Path:
    return production_dir() / "Clients"


def config_dir() -> Path:
    return cgp_root() / "_config"


def registry_path() -> Path:
    return config_dir() / "client-registry.json"


def clients_dir() -> Path:
    return config_dir() / "clients"


def clients_private_dir() -> Path:
    return config_dir() / "clients-private"


def sessions_dir() -> Path:
    return config_dir() / "sessions"


def fiscal_alert_stamp() -> Path:
    return config_dir() / "last-fiscal-alert"


def venv_python() -> str:
    return load_project_config()["venv_python"]
