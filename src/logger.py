"""Модуль логирования событий эмулятора."""

import json
import getpass
from datetime import datetime


class Logger:
    """Логгер событий в формате JSON."""

    def __init__(self, log_path):
        """Инициализировать логгер.

        Args:
            log_path: путь к файлу лога
        """
        self.log_path = log_path
        self.username = getpass.getuser()
        self.events = []

    def log_command(self, command, args, error=None):
        """Записать событие вызова команды.

        Args:
            command: имя команды
            args: список аргументов
            error: сообщение об ошибке или None
        """
        event = {
            'timestamp': datetime.now().isoformat(),
            'user': self.username,
            'command': command,
            'args': args,
        }
        if error:
            event['error'] = error
        self.events.append(event)
        self._flush()

    def _flush(self):
        """Записать события в файл."""
        try:
            with open(
                    self.log_path, 'w', encoding='utf-8'
            ) as f:
                json.dump(
                    self.events, f,
                    ensure_ascii=False, indent=2
                )
        except OSError as e:
            print(f"Ошибка записи лога: {e}")


class NullLogger:
    """Пустой логгер, если логирование отключено."""

    def log_command(self, command, args, error=None):
        """Ничего не делает.

        Args:
            command: имя команды
            args: список аргументов
            error: сообщение об ошибке
        """
        pass
