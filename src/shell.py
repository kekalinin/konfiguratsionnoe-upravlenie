"""Модуль с логикой оболочки."""

import getpass
import socket
from parser import CommandParser
from commands import (
    LsCommand, CdCommand, ExitCommand,
    ConfDumpCommand,
)
from logger import NullLogger


class Shell:
    """Логика эмулятора оболочки."""

    def __init__(self, config=None):
        """Инициализировать оболочку.

        Args:
            config: объект EmulatorConfig или None
        """
        self.parser = CommandParser()
        self.commands = {
            'ls': LsCommand(),
            'cd': CdCommand(),
            'exit': ExitCommand(),
            'conf-dump': ConfDumpCommand(),
        }
        self.is_running = True
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()
        self.config = config
        self.logger = NullLogger()
        self.vfs = None

    def set_logger(self, logger):
        """Установить логгер.

        Args:
            logger: объект логгера
        """
        self.logger = logger

    def set_vfs(self, vfs):
        """Установить VFS.

        Args:
            vfs: объект VFS
        """
        self.vfs = vfs

    def get_prompt(self):
        """Получить строку приглашения к вводу.

        Returns:
            Строка приглашения
        """
        path = '~'
        if self.vfs and self.vfs.current_dir:
            current = self.vfs.get_current_path()
            if current:
                path = current
        return f"{self.username}@{self.hostname}:{path}$ "

    def get_window_title(self):
        """Получить строку заголовка окна.

        Returns:
            Заголовок окна
        """
        return f"Эмулятор-[{self.username}@{self.hostname}]"

    def execute(self, line):
        """Выполнить командную строку.

        Args:
            line: введённая командная строка

        Returns:
            Строка с результатом выполнения
        """
        args = self.parser.parse(line)
        if not args:
            return ""

        cmd_name = args[0]
        cmd_args = args[1:]

        if cmd_name not in self.commands:
            error_msg = (
                f"Неизвестная команда: {cmd_name}"
            )
            self.logger.log_command(
                cmd_name, cmd_args, error=error_msg
            )
            return error_msg

        self.logger.log_command(cmd_name, cmd_args)
        return self.commands[cmd_name].execute(
            cmd_args, self
        )

    def close(self):
        """Закрыть оболочку."""
        self.is_running = False
