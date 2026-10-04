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


class UptimeCommand(Command):
    """Команда вывода времени работы эмулятора."""

    def execute(self, args, shell):
        """Выполнить команду uptime.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с временем работы
        """
        import time
        elapsed = time.time() - shell.start_time
        days = int(elapsed // 86400)
        hours = int((elapsed % 86400) // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        return (
            f"up {days} дн., "
            f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        )


class HeadCommand(Command):
    """Команда вывода первых N строк файла."""

    def execute(self, args, shell):
        """Выполнить команду head.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с содержимым файла
        """
        if shell.vfs is None:
            return "VFS не загружена"
        if not args:
            return "Использование: head [-n кол-во] <файл>"

        count = 10
        filename = args[-1]

        if len(args) >= 2 and args[0] == '-n':
            try:
                count = int(args[1])
                filename = args[2]
            except (ValueError, IndexError):
                return "Ошибка: неверный формат аргументов"

        node = shell.vfs.get_node(filename)
        if node is None:
            return f"Файл не найден: {filename}"
        if not node.is_file():
            return f"Не файл: {filename}"

        text = node.get_content_text()
        if text is None:
            return f"Не удалось прочитать: {filename}"

        lines = text.split('\n')
        return '\n'.join(lines[:count])


class TacCommand(Command):
    """Команда вывода содержимого файла в обратном порядке."""

    def execute(self, args, shell):
        """Выполнить команду tac.

        Args:
            args: список аргументов
            shell: экземпляр оболочки

        Returns:
            Строка с содержимым файла
        """
        if shell.vfs is None:
            return "VFS не загружена"
        if not args:
            return "Использование: tac <файл>"

        filename = args[0]
        node = shell.vfs.get_node(filename)
        if node is None:
            return f"Файл не найден: {filename}"
        if not node.is_file():
            return f"Не файл: {filename}"

        text = node.get_content_text()
        if text is None:
            return f"Не удалось прочитать: {filename}"

        lines = text.split('\n')
        return '\n'.join(reversed(lines))


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
