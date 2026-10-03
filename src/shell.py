"""Модуль с логикой оболочки."""

import getpass
import socket
from parser import CommandParser
from commands import LsCommand, CdCommand, ExitCommand


class Shell:
    """Логика эмулятора оболочки."""

    def __init__(self):
        """Инициализировать оболочку парсером и командами."""
        self.parser = CommandParser()
        self.commands = {
            'ls': LsCommand(),
            'cd': CdCommand(),
            'exit': ExitCommand(),
        }
        self.is_running = True
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()

    def get_prompt(self):
        """Получить строку приглашения к вводу.

        Returns:
            Строка приглашения с именем пользователя и хостом
        """
        return f"{self.username}@{self.hostname}:~$ "

    def get_window_title(self):
        """Получить строку заголовка окна.

        Returns:
            Заголовок окна с именем пользователя и хостом
        """
        return f"Эмулятор-[{self.username}@{self.hostname}]"

    def execute(self, line):
        """Выполнить командную строку.

        Args:
            line: введённая командная строка

        Returns:
            Строка с результатом выполнения команды
        """
        args = self.parser.parse(line)
        if not args:
            return ""

        cmd_name = args[0]
        cmd_args = args[1:]

        if cmd_name not in self.commands:
            return f"Неизвестная команда: {cmd_name}"

        return self.commands[cmd_name].execute(cmd_args, self)

    def close(self):
        """Закрыть оболочку."""
        self.is_running = False
