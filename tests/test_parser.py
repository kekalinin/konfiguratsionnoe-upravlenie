"""Тесты парсера команд."""

import unittest
import sys
import os

sys.path.insert(
    0,
    os.path.join(
        os.path.dirname(__file__), '..', 'src'
    )
)
from parser import CommandParser


class TestCommandParser(unittest.TestCase):
    """Набор тестов для CommandParser."""

    def setUp(self):
        """Подготовка тестовых данных."""
        self.parser = CommandParser()

    def test_empty_line(self):
        """Тест разбора пустой строки."""
        self.assertEqual(
            self.parser.parse(''), []
        )

    def test_simple_command(self):
        """Тест разбора простой команды."""
        self.assertEqual(
            self.parser.parse('ls'), ['ls']
        )

    def test_command_with_args(self):
        """Тест разбора команды с аргументами."""
        self.assertEqual(
            self.parser.parse('ls -l -a'),
            ['ls', '-l', '-a']
        )

    def test_double_quotes(self):
        """Тест разбора с двойными кавычками."""
        self.assertEqual(
            self.parser.parse('ls "моя папка"'),
            ['ls', 'моя папка']
        )

    def test_single_quotes(self):
        """Тест разбора с одинарными кавычками."""
        self.assertEqual(
            self.parser.parse("ls 'моя папка'"),
            ['ls', 'моя папка']
        )

    def test_multiple_spaces(self):
        """Тест разбора с несколькими пробелами."""
        self.assertEqual(
            self.parser.parse('ls   -l   -a'),
            ['ls', '-l', '-a']
        )

    def test_mixed_quotes(self):
        """Тест разбора со смешанными кавычками."""
        result = self.parser.parse(
            'echo "привет" \'мир\''
        )
        self.assertEqual(
            result, ['echo', 'привет', 'мир']
        )


if __name__ == '__main__':
    unittest.main()
