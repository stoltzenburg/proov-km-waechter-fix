# config_loader.py
# Reads settings.cfg. Hand-rolled in 2013; modernised 2025.

SETTINGS_FILE = "settings.cfg"

KNOWN_KEYS = [
    "service_interval_km",
    "warn_at_percent",
    "report_title",
    "history_file",
    "log_file",
    "mileage_unit",
]


def load_settings(path: str | None = None) -> dict[str, str]:
    """Parse settings.cfg and return a dict of known keys.

    Unknown keys are silently ignored (a typo in the file therefore never
    surfaces — keep in mind when debugging).  All values are strings; use
    ``get_int`` when you need an integer.
    """
    if path is None:
        path = SETTINGS_FILE
    settings: dict[str, str] = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)   # maxsplit=1 handles values that contain "="
            key = key.strip()
            value = value.strip()
            if key in KNOWN_KEYS:
                settings[key] = value
    return settings


def get_int(settings: dict[str, str], key: str, fallback: int) -> int:
    """Return settings[key] as int, or fallback if missing or not numeric."""
    if key in settings:
        try:
            return int(settings[key])
        except ValueError:
            return fallback
    return fallback


def get_setting(settings: dict[str, str], key: str, fallback: str = "") -> str:
    """Return settings[key], or fallback if the key is absent.

    This is a thin wrapper around ``dict.get``; prefer ``settings.get(key, fallback)``
    in new code.
    """
    return settings.get(key, fallback)
