"""Модуль с командами оболочки."""


class Command:
    """Базовый класс для команд оболочки."""

    def execute(self, args, shell):
        """Выполнить команду с переданными аргументами.

        Args:
            args: список аргументов команды
            shell: ссылка на экземпляр оболочки

        Returns:
            Строка с результатом выполнения
        """
        raise NotImplementedError


class LsCommand(Command):
    """Команда вывода содержимого каталога (заглушка)."""

    def execute(self, args, shell):
        """Выполнить команду ls.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с результатом
        """
        return f"ls вызвана с аргументами: {args}"


class CdCommand(Command):
    """Команда смены каталога (заглушка)."""

    def execute(self, args, shell):
        """Выполнить команду cd.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с результатом
        """
        return f"cd вызвана с аргументами: {args}"


class ExitCommand(Command):
    """Команда выхода из оболочки."""

    def execute(self, args, shell):
        """Выполнить команду exit.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Пустая строка
        """
        shell.close()
        return ""


class ConfDumpCommand(Command):
    """Команда вывода параметров эмулятора."""

    def execute(self, args, shell):
        """Выполнить команду conf-dump.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с параметрами
        """
        lines = ["Текущие параметры эмулятора:"]
        for key, value in shell.config.to_dict().items():
            lines.append(f"  {key}: {value}")
        return '\n'.join(lines)
