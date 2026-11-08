
"""
Password Generator
Automated Unit Tests
"""

import unittest

from generator import PasswordGenerator, PasswordConfig


class TestPasswordGenerator(unittest.TestCase):

    def test_password_length(self):

        config = PasswordConfig(length=32)
        generator = PasswordGenerator(config)

        password = generator.generate()

        self.assertEqual(len(password), 32)

    def test_uppercase_requirement(self):

        config = PasswordConfig(
            uppercase=True,
            lowercase=False,
            numbers=False,
            symbols=False
        )

        password = PasswordGenerator(config).generate()

        self.assertTrue(any(c.isupper() for c in password))

    def test_lowercase_requirement(self):

        config = PasswordConfig(
            uppercase=False,
            lowercase=True,
            numbers=False,
            symbols=False
        )

        password = PasswordGenerator(config).generate()

        self.assertTrue(any(c.islower() for c in password))

    def test_number_requirement(self):

        config = PasswordConfig(
            uppercase=False,
            lowercase=False,
            numbers=True,
            symbols=False
        )

        password = PasswordGenerator(config).generate()

        self.assertTrue(any(c.isdigit() for c in password))

    def test_symbol_requirement(self):

        config = PasswordConfig(
            uppercase=False,
            lowercase=False,
            numbers=False,
            symbols=True,
            custom_symbols="!@#$"
        )

        password = PasswordGenerator(config).generate()

        self.assertTrue(any(c in "!@#$" for c in password))

    def test_exclude_similar(self):

        config = PasswordConfig(
            length=32,
            exclude_similar=True
        )

        password = PasswordGenerator(config).generate()

        for character in "il1Lo0O":
            self.assertNotIn(character, password)

    def test_exclude_ambiguous(self):

        config = PasswordConfig(
            length=32,
            exclude_ambiguous=True
        )

        password = PasswordGenerator(config).generate()

        for character in PasswordConfig.AMBIGUOUS:
            self.assertNotIn(character, password)

    def test_invalid_length(self):

        config = PasswordConfig(length=300)

        with self.assertRaises(ValueError):
            PasswordGenerator(config)

    def test_no_character_categories(self):

        config = PasswordConfig(
            uppercase=False,
            lowercase=False,
            numbers=False,
            symbols=False
        )

        with self.assertRaises(ValueError):
            PasswordGenerator(config)

    def test_multiple_passwords(self):

        config = PasswordConfig(
            length=20,
            quantity=5
        )

        passwords = PasswordGenerator(config).generate_multiple()

        self.assertEqual(len(passwords), 5)

        for password in passwords:
            self.assertEqual(len(password), 20)


if __name__ == "__main__":
    unittest.main()
