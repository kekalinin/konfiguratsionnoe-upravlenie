"""Модуль обработки параметров командной строки."""

import argparse


class EmulatorConfig:
    """Конфигурация эмулятора."""

    def __init__(self):
        """Инициализировать значения по умолчанию."""
        self.vfs_path = None
        self.log_path = None
        self.script_path = None

    def parse_args(self):
        """Разобрать аргументы командной строки.

        Returns:
            Сам объект конфигурации
        """
        parser = argparse.ArgumentParser(
            description='Эмулятор оболочки UNIX'
        )
        parser.add_argument(
            '--vfs',
            help='Путь к файлу VFS (JSON)'
        )
        parser.add_argument(
            '--log',
            help='Путь к файлу лога (JSON)'
        )
        parser.add_argument(
            '--script',
            help='Путь к стартовому скрипту'
        )
        args = parser.parse_args()

        self.vfs_path = args.vfs
        self.log_path = args.log
        self.script_path = args.script
        return self

    def to_dict(self):
        """Получить параметры в виде словаря.

        Returns:
            Словарь с параметрами
        """
        return {
            'vfs_path': self.vfs_path or 'не указан',
            'log_path': self.log_path or 'не указан',
            'script_path': (
                    self.script_path or 'не указан'
            ),
        }
