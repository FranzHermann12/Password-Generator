
"""
Password Generator
Customisable Secure Generation Engine
Version: 1.1.0
"""

import secrets
import string
from dataclasses import dataclass, field


@dataclass
class PasswordConfig:

    length: int = 20
    quantity: int = 1

    uppercase: bool = True
    lowercase: bool = True
    numbers: bool = True
    symbols: bool = True

    custom_symbols: str = string.punctuation
    excluded_characters: str = ""
    required_characters: str = ""

    exclude_similar: bool = False
    exclude_ambiguous: bool = False

    MIN_LENGTH: int = field(default=8, init=False)
    MAX_LENGTH: int = field(default=256, init=False)

    SIMILAR = "il1Lo0O"
    AMBIGUOUS = "{}[]()/\\'\"`~,;:.<>"


class PasswordGenerator:

    def __init__(self, config: PasswordConfig):
        self.config = config
        self._validate()

    def _validate(self):

        if type(self.config.length) is not int:
            raise TypeError("Length must be an integer.")

        if not 8 <= self.config.length <= 256:
            raise ValueError("Length must be between 8 and 256.")

        if type(self.config.quantity) is not int:
            raise TypeError("Quantity must be an integer.")

        if not 1 <= self.config.quantity <= 100:
            raise ValueError("Quantity must be between 1 and 100.")

        options = [
            self.config.uppercase,
            self.config.lowercase,
            self.config.numbers,
            self.config.symbols
        ]

        if any(type(option) is not bool for option in options):
            raise TypeError("Character options must be Boolean.")

        if not any(options):
            raise ValueError("Enable at least one character category.")

        text_settings = [
            self.config.custom_symbols,
            self.config.excluded_characters,
            self.config.required_characters
        ]

        if any(not isinstance(value, str) for value in text_settings):
            raise TypeError("Custom character settings must be strings.")

    def _build_pool(self):

        groups = []

        if self.config.uppercase:
            groups.append(string.ascii_uppercase)

        if self.config.lowercase:
            groups.append(string.ascii_lowercase)

        if self.config.numbers:
            groups.append(string.digits)

        if self.config.symbols:

            if not self.config.custom_symbols:
                raise ValueError("Custom symbols cannot be empty.")

            groups.append(self.config.custom_symbols)

        exclusions = set(self.config.excluded_characters)

        if self.config.exclude_similar:
            exclusions.update(self.config.SIMILAR)

        if self.config.exclude_ambiguous:
            exclusions.update(self.config.AMBIGUOUS)

        groups = [
            "".join(character for character in group
                    if character not in exclusions)
            for group in groups
        ]

        if any(not group for group in groups):
            raise ValueError(
                "A selected character category has become empty."
            )

        pool = "".join(dict.fromkeys("".join(groups)))

        if not pool:
            raise ValueError("No characters are available.")

        required = self.config.required_characters

        if len(required) > self.config.length:
            raise ValueError(
                "Required characters exceed the password length."
            )

        if any(character not in pool for character in required):
            raise ValueError(
                "Every required character must belong to the selected "
                "character pool and must not be excluded."
            )

        return groups, pool

    def get_character_pool_size(self):

        _, pool = self._build_pool()
        return len(pool)

    def generate(self):

        groups, pool = self._build_pool()

        password = list(self.config.required_characters)

        # Ensure every enabled category appears at least once.
        for group in groups:

            if not any(character in group for character in password):

                if len(password) >= self.config.length:
                    raise ValueError(
                        "Not enough space for all required categories."
                    )

                password.append(secrets.choice(group))

        # Fill remaining positions.
        while len(password) < self.config.length:
            password.append(secrets.choice(pool))

        # Securely shuffle the final password.
        secrets.SystemRandom().shuffle(password)

        return "".join(password)

    def generate_multiple(self):

        return [
            self.generate()
            for _ in range(self.config.quantity)
        ]
