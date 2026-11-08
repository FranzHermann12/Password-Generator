
"""
Password Generator
Input Validation Engine
Version: 1.0.0
"""


class ValidationError(Exception):
    """Custom exception for invalid application settings."""
    pass


class PasswordValidator:

    MIN_LENGTH = 8
    MAX_LENGTH = 256

    MIN_QUANTITY = 1
    MAX_QUANTITY = 100

    @classmethod
    def validate_length(cls, length):

        if type(length) is not int:
            raise ValidationError("Length must be an integer.")

        if not cls.MIN_LENGTH <= length <= cls.MAX_LENGTH:
            raise ValidationError(
                f"Length must be between {cls.MIN_LENGTH} "
                f"and {cls.MAX_LENGTH}."
            )

        return True

    @classmethod
    def validate_quantity(cls, quantity):

        if type(quantity) is not int:
            raise ValidationError("Quantity must be an integer.")

        if not cls.MIN_QUANTITY <= quantity <= cls.MAX_QUANTITY:
            raise ValidationError(
                f"Quantity must be between {cls.MIN_QUANTITY} "
                f"and {cls.MAX_QUANTITY}."
            )

        return True

    @staticmethod
    def validate_character_options(
        uppercase,
        lowercase,
        numbers,
        symbols
    ):

        options = [uppercase, lowercase, numbers, symbols]

        if any(type(option) is not bool for option in options):
            raise ValidationError(
                "Character options must be True or False."
            )

        if not any(options):
            raise ValidationError(
                "At least one character category must be enabled."
            )

        return True

    @staticmethod
    def validate_exclusions(excluded_characters):

        if not isinstance(excluded_characters, str):
            raise ValidationError(
                "Excluded characters must be a string."
            )

        return True

    @staticmethod
    def validate_required_characters(required_characters):

        if not isinstance(required_characters, str):
            raise ValidationError(
                "Required characters must be a string."
            )

        return True

    @classmethod
    def validate_all(cls, config):

        cls.validate_length(config.length)

        cls.validate_quantity(config.quantity)

        cls.validate_character_options(
            config.uppercase,
            config.lowercase,
            config.numbers,
            config.symbols
        )

        cls.validate_exclusions(
            config.excluded_characters
        )

        cls.validate_required_characters(
            config.required_characters
        )

        return True
