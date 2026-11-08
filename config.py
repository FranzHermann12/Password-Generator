
"""
Password Generator
Application Configuration
Version: 1.1.0
"""

from dataclasses import dataclass, asdict
import json
from pathlib import Path


@dataclass
class AppConfig:

    app_name: str = "Password Generator"
    version: str = "1.1.0"
    developer: str = "Franz_Hermann1"

    # Generation defaults
    default_length: int = 20
    default_quantity: int = 5

    # Character categories
    uppercase: bool = True
    lowercase: bool = True
    numbers: bool = True
    symbols: bool = True

    # Custom character preferences
    custom_symbols: str = "!@#$%^&*()-_=+"
    excluded_characters: str = ""
    required_characters: str = ""

    # Filtering
    exclude_similar: bool = False
    exclude_ambiguous: bool = False

    # Analysis
    show_password_analysis: bool = True
    show_entropy: bool = True


class ConfigManager:

    CONFIG_FILE = Path("password_generator_config.json")

    @classmethod
    def load(cls):

        if not cls.CONFIG_FILE.exists():
            return AppConfig()

        try:
            with cls.CONFIG_FILE.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, dict):
                return AppConfig()

            allowed_fields = AppConfig.__dataclass_fields__

            filtered_data = {
                key: value
                for key, value in data.items()
                if key in allowed_fields
            }

            return AppConfig(**filtered_data)

        except (OSError, json.JSONDecodeError, TypeError, ValueError):
            return AppConfig()

    @classmethod
    def save(cls, config: AppConfig):

        temporary_file = cls.CONFIG_FILE.with_suffix(".tmp")

        try:
            with temporary_file.open("w", encoding="utf-8") as file:
                json.dump(asdict(config), file, indent=4)

            temporary_file.replace(cls.CONFIG_FILE)

        except OSError:
            if temporary_file.exists():
                temporary_file.unlink(missing_ok=True)
            raise
