from .settings_prod import *

# Development overrides
DEBUG = True

# Lokale database: SQLite
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Lokaal hosten we gewoon op localhost
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
