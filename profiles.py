
"""
Password Generator
Custom Profile Management
Version: 1.0.0
"""

import json
from pathlib import Path
from dataclasses import asdict

from config import AppConfig


class ProfileManager:

    PROFILE_FILE = Path("password_generator_profiles.json")

    @classmethod
    def load_profiles(cls):

        if not cls.PROFILE_FILE.exists():
            return {}

        try:
            with cls.PROFILE_FILE.open("r", encoding="utf-8") as file:
                profiles = json.load(file)

            if isinstance(profiles, dict):
                return profiles

            return {}

        except (OSError, json.JSONDecodeError):
            return {}

    @classmethod
    def save_profiles(cls, profiles):

        temporary_file = cls.PROFILE_FILE.with_suffix(".tmp")

        try:
            with temporary_file.open("w", encoding="utf-8") as file:
                json.dump(profiles, file, indent=4)

            temporary_file.replace(cls.PROFILE_FILE)

        except OSError:
            if temporary_file.exists():
                temporary_file.unlink(missing_ok=True)
            raise

    @classmethod
    def save_profile(cls, name, settings):

        if not isinstance(name, str) or not name.strip():
            raise ValueError("Profile name cannot be empty.")

        if len(name) > 40:
            raise ValueError("Profile name cannot exceed 40 characters.")

        profiles = cls.load_profiles()

        profiles[name.strip()] = asdict(settings)

        cls.save_profiles(profiles)

    @classmethod
    def load_profile(cls, name):

        profiles = cls.load_profiles()

        if name not in profiles:
            raise ValueError("Profile not found.")

        data = profiles[name]

        if not isinstance(data, dict):
            raise ValueError("Invalid profile data.")

        allowed_fields = AppConfig.__dataclass_fields__

        filtered_data = {
            key: value
            for key, value in data.items()
            if key in allowed_fields
        }

        return AppConfig(**filtered_data)

    @classmethod
    def delete_profile(cls, name):

        profiles = cls.load_profiles()

        if name not in profiles:
            raise ValueError("Profile not found.")

        del profiles[name]

        cls.save_profiles(profiles)

    @classmethod
    def list_profiles(cls):

        profiles = cls.load_profiles()

        return list(profiles.keys())
