
"""
Password Generator
Password Analysis Engine
Version: 1.1.0
"""

import math
from dataclasses import dataclass


@dataclass
class StrengthReport:

    length: int
    character_pool_size: int
    entropy_bits: float
    search_space: int
    strength: str
    analysis_note: str


class PasswordAnalyzer:

    THRESHOLDS = {
        "Weak": 28,
        "Moderate": 60,
        "Strong": 80,
        "Very Strong": 100
    }

    @staticmethod
    def calculate_entropy(length: int, pool_size: int) -> float:

        if type(length) is not int or length <= 0:
            raise ValueError("Invalid password length.")

        if type(pool_size) is not int or pool_size < 2:
            raise ValueError(
                "Character pool must contain at least 2 characters."
            )

        return length * math.log2(pool_size)

    @staticmethod
    def calculate_search_space(length: int, pool_size: int) -> int:

        if type(length) is not int or length <= 0:
            raise ValueError("Invalid password length.")

        if type(pool_size) is not int or pool_size < 2:
            raise ValueError("Invalid character pool size.")

        return pool_size ** length

    @classmethod
    def classify_strength(cls, entropy: float) -> str:

        if entropy < cls.THRESHOLDS["Weak"]:
            return "Weak"

        if entropy < cls.THRESHOLDS["Moderate"]:
            return "Moderate"

        if entropy < cls.THRESHOLDS["Strong"]:
            return "Strong"

        if entropy < cls.THRESHOLDS["Very Strong"]:
            return "Very Strong"

        return "Exceptional"

    @classmethod
    def analyze(cls, password: str, pool_size: int) -> StrengthReport:

        if not isinstance(password, str) or not password:
            raise ValueError("Password cannot be empty.")

        if not isinstance(pool_size, int) or pool_size < 2:
            raise ValueError("Invalid character pool size.")

        length = len(password)

        entropy = cls.calculate_entropy(length, pool_size)

        search_space = cls.calculate_search_space(
            length,
            pool_size
        )

        strength = cls.classify_strength(entropy)

        return StrengthReport(
            length=length,
            character_pool_size=pool_size,
            entropy_bits=round(entropy, 2),
            search_space=search_space,
            strength=strength,
            analysis_note=(
                "Theoretical upper-bound estimate. "
                "Actual password entropy may be lower."
            )
        )
