
"""
PASSWORD GENERATOR
Main Application
Version: 1.3.0
Developer: Franz_Hermann1
"""

from generator import PasswordGenerator, PasswordConfig
from strength import PasswordAnalyzer
from config import ConfigManager
from validator import PasswordValidator, ValidationError
from profiles import ProfileManager


class PasswordGeneratorApp:

    def __init__(self):
        self.settings = ConfigManager.load()
        self.active_preset = "Custom"

    def display_header(self):

        print("\n" + "=" * 55)
        print("                 PASSWORD GENERATOR")
        print("=" * 55)
        print(f"Version: {self.settings.version}")
        print(f"Developer: {self.settings.developer}")
        print("=" * 55)

    def display_menu(self):

        print("\nMAIN MENU")
        print("-" * 40)
        print("1. Generate Passwords")
        print("2. Customise Settings")
        print("3. View Current Settings")
        print("4. Save Settings")
        print("5. About")
        print("6. Select Password Preset")
        print("7. Manage Profiles")
        print("0. Exit")
        print("-" * 40)

    def get_integer(self, message, minimum, maximum):

        while True:
            try:
                value = int(input(message))

                if minimum <= value <= maximum:
                    return value

                print(f"Enter a number between {minimum} and {maximum}.")

            except ValueError:
                print("Please enter a valid whole number.")

    def toggle_setting(self, name, current):

        while True:

            answer = input(
                f"{name} (y/n) [{'y' if current else 'n'}]: "
            ).strip().lower()

            if answer == "":
                return current

            if answer in ("y", "yes"):
                return True

            if answer in ("n", "no"):
                return False

            print("Enter y or n.")

    def get_text_setting(self, name, current):

        print(f"\nCurrent {name}: {current!r}")
        print("Press Enter to keep it, or type CLEAR to remove it.")

        value = input(f"New {name}: ")

        if value.strip().upper() == "CLEAR":
            return ""

        if value == "":
            return current

        return value

    def select_preset(self):

        print("\n========== PASSWORD PRESETS ==========")
        print("1. Standard")
        print("2. Strong")
        print("3. PIN-style")
        print("4. Easy to Read")
        print("5. Custom")
        print("0. Cancel")

        choice = input("\nSelect a preset: ").strip()

        presets = {
            "1": "Standard",
            "2": "Strong",
            "3": "PIN-style",
            "4": "Easy to Read",
            "5": "Custom"
        }

        if choice == "0":
            print("Preset selection cancelled.")
            return

        if choice not in presets:
            print("Invalid preset selection.")
            return

        self.active_preset = presets[choice]

        print(f"\nActive preset: {self.active_preset}")
        print("Your saved custom settings have not been overwritten.")

    def customise_settings(self):

        self.active_preset = "Custom"

        print("\n========== CUSTOM SETTINGS ==========")

        self.settings.default_length = self.get_integer(
            "Password length (8-256): ", 8, 256
        )

        self.settings.default_quantity = self.get_integer(
            "Password quantity (1-100): ", 1, 100
        )

        print("\nCHARACTER OPTIONS")

        self.settings.uppercase = self.toggle_setting(
            "Uppercase letters", self.settings.uppercase
        )

        self.settings.lowercase = self.toggle_setting(
            "Lowercase letters", self.settings.lowercase
        )

        self.settings.numbers = self.toggle_setting(
            "Numbers", self.settings.numbers
        )

        self.settings.symbols = self.toggle_setting(
            "Symbols", self.settings.symbols
        )

        print("\nFILTER OPTIONS")

        self.settings.exclude_similar = self.toggle_setting(
            "Exclude similar characters",
            self.settings.exclude_similar
        )

        self.settings.exclude_ambiguous = self.toggle_setting(
            "Exclude ambiguous characters",
            self.settings.exclude_ambiguous
        )

        print("\nADVANCED CHARACTER SETTINGS")

        self.settings.custom_symbols = self.get_text_setting(
            "custom symbols",
            self.settings.custom_symbols
        )

        self.settings.excluded_characters = self.get_text_setting(
            "excluded characters",
            self.settings.excluded_characters
        )

        self.settings.required_characters = self.get_text_setting(
            "required characters",
            self.settings.required_characters
        )

        try:
            self.create_generator_config()
            print("\nSettings updated successfully.")

        except (ValueError, TypeError, ValidationError) as error:
            print(f"\nConfiguration warning: {error}")

    def create_generator_config(self):

        options = {
            "Standard": {
                "uppercase": True,
                "lowercase": True,
                "numbers": True,
                "symbols": False,
                "exclude_similar": False,
                "exclude_ambiguous": False
            },
            "Strong": {
                "uppercase": True,
                "lowercase": True,
                "numbers": True,
                "symbols": True,
                "exclude_similar": False,
                "exclude_ambiguous": False
            },
            "PIN-style": {
                "uppercase": False,
                "lowercase": False,
                "numbers": True,
                "symbols": False,
                "exclude_similar": False,
                "exclude_ambiguous": False
            },
            "Easy to Read": {
                "uppercase": True,
                "lowercase": True,
                "numbers": True,
                "symbols": False,
                "exclude_similar": True,
                "exclude_ambiguous": False
            }
        }

        if self.active_preset == "Custom":

            selected = {
                "uppercase": self.settings.uppercase,
                "lowercase": self.settings.lowercase,
                "numbers": self.settings.numbers,
                "symbols": self.settings.symbols,
                "exclude_similar": self.settings.exclude_similar,
                "exclude_ambiguous": self.settings.exclude_ambiguous
            }

            excluded = self.settings.excluded_characters
            required = self.settings.required_characters

        else:

            selected = options[self.active_preset]
            excluded = ""
            required = ""

        config = PasswordConfig(
            length=self.settings.default_length,
            quantity=self.settings.default_quantity,
            uppercase=selected["uppercase"],
            lowercase=selected["lowercase"],
            numbers=selected["numbers"],
            symbols=selected["symbols"],
            custom_symbols=self.settings.custom_symbols,
            excluded_characters=excluded,
            required_characters=required,
            exclude_similar=selected["exclude_similar"],
            exclude_ambiguous=selected["exclude_ambiguous"]
        )

        PasswordValidator.validate_all(config)

        return config

    def view_settings(self):

        print("\n========== CURRENT SETTINGS ==========")

        print(f"Active preset: {self.active_preset}")
        print(f"Password length: {self.settings.default_length}")
        print(f"Password quantity: {self.settings.default_quantity}")

        print(f"Uppercase: {self.settings.uppercase}")
        print(f"Lowercase: {self.settings.lowercase}")
        print(f"Numbers: {self.settings.numbers}")
        print(f"Symbols: {self.settings.symbols}")

        print(f"Exclude similar: {self.settings.exclude_similar}")
        print(f"Exclude ambiguous: {self.settings.exclude_ambiguous}")

        print(f"Custom symbols: {self.settings.custom_symbols!r}")
        print(f"Excluded characters: {self.settings.excluded_characters!r}")
        print(f"Required characters: {self.settings.required_characters!r}")

    def generate_passwords(self):

        try:

            config = self.create_generator_config()
            generator = PasswordGenerator(config)

            passwords = generator.generate_multiple()
            pool_size = generator.get_character_pool_size()

            print("\n========== GENERATED PASSWORDS ==========")
            print(f"Preset: {self.active_preset}")

            for index, password in enumerate(passwords, start=1):

                report = PasswordAnalyzer.analyze(
                    password,
                    pool_size
                )

                print(f"\nPassword {index}: {password}")

                if self.settings.show_password_analysis:

                    print(f"Length: {report.length} characters")
                    print(f"Character pool: {report.character_pool_size}")
                    print(f"Strength: {report.strength}")

                    if self.settings.show_entropy:
                        print(
                            f"Theoretical maximum estimate: "
                            f"{report.entropy_bits} bits"
                        )

                        print(f"Analysis note: {report.analysis_note}")

            print("\nGeneration completed successfully.")

        except (ValueError, TypeError, ValidationError) as error:
            print(f"\nGeneration error: {error}")

    # PROFILE MANAGEMENT

    def manage_profiles(self):

        while True:

            print("\n========== PROFILE MANAGER ==========")
            print("1. Save Current Settings as Profile")
            print("2. Load Profile")
            print("3. List Profiles")
            print("4. Delete Profile")
            print("0. Back to Main Menu")

            choice = input("\nSelect an option: ").strip()

            if choice == "1":
                self.save_profile()

            elif choice == "2":
                self.load_profile()

            elif choice == "3":
                self.list_profiles()

            elif choice == "4":
                self.delete_profile()

            elif choice == "0":
                break

            else:
                print("Invalid option.")

    def save_profile(self):

        name = input("\nEnter a profile name: ").strip()

        try:
            self.create_generator_config()
            ProfileManager.save_profile(name, self.settings)
            print(f"\nProfile '{name}' saved successfully.")

        except (ValueError, TypeError, OSError, ValidationError) as error:
            print(f"\nUnable to save profile: {error}")

    def load_profile(self):

        name = input("\nEnter the profile name to load: ").strip()

        try:

            profile = ProfileManager.load_profile(name)

            old_settings = self.settings
            self.settings = profile

            try:
                self.create_generator_config()
            except (ValueError, TypeError, ValidationError):
                self.settings = old_settings
                raise

            self.active_preset = "Custom"

            print(f"\nProfile '{name}' loaded successfully.")

        except (ValueError, TypeError, ValidationError) as error:
            print(f"\nUnable to load profile: {error}")

    def list_profiles(self):

        profiles = ProfileManager.list_profiles()

        print("\n========== SAVED PROFILES ==========")

        if not profiles:
            print("No profiles have been saved yet.")
            return

        for index, name in enumerate(profiles, start=1):
            print(f"{index}. {name}")

    def delete_profile(self):

        self.list_profiles()

        name = input("\nEnter the profile name to delete: ").strip()

        confirm = input(
            f"Delete profile '{name}'? (y/n): "
        ).strip().lower()

        if confirm != "y":
            print("Deletion cancelled.")
            return

        try:
            ProfileManager.delete_profile(name)
            print(f"\nProfile '{name}' deleted successfully.")

        except (ValueError, OSError) as error:
            print(f"\nUnable to delete profile: {error}")

    def save_settings(self):

        try:
            ConfigManager.save(self.settings)
            print("\nSettings saved successfully.")

        except OSError as error:
            print(f"\nUnable to save settings: {error}")

    def about(self):

        print("\n========== ABOUT ==========")
        print("Application: Password Generator")
        print(f"Version: {self.settings.version}")
        print(f"Developer: {self.settings.developer}")
        print("Generation engine: Python Secrets")
        print("Analysis engine: Entropy estimator")

    def run(self):

        self.display_header()

        while True:

            self.display_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.generate_passwords()

            elif choice == "2":
                self.customise_settings()

            elif choice == "3":
                self.view_settings()

            elif choice == "4":
                self.save_settings()

            elif choice == "5":
                self.about()

            elif choice == "6":
                self.select_preset()

            elif choice == "7":
                self.manage_profiles()

            elif choice == "0":
                print("\nThank you for using Password Generator.")
                break

            else:
                print("\nInvalid option. Try again.")


if __name__ == "__main__":

    application = PasswordGeneratorApp()
    application.run()
