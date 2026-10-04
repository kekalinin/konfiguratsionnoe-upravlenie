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
    """Команда вывода содержимого каталога."""

    def execute(self, args, shell):
        """Выполнить команду ls.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с содержимым директории
        """
        if shell.vfs is None:
            return "VFS не загружена"

        items = shell.vfs.list_dir()
        if not items:
            return "(пусто)"
        return '  '.join(items)


class CdCommand(Command):
    """Команда смены каталога."""

    def execute(self, args, shell):
        """Выполнить команду cd.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с результатом
        """
        if shell.vfs is None:
            return "VFS не загружена"

        if not args:
            shell.vfs.current_dir = shell.vfs.root
            return ""

        path = args[0]
        error = shell.vfs.change_dir(path)
        if error:
            return error
        return ""


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
        if shell.vfs:
            path = shell.vfs.get_current_path()
            lines.append(f"  current_dir: {path}")
        return '\n'.join(lines)
