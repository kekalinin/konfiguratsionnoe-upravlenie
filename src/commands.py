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


class MvCommand(Command):
    """Команда перемещения/переименования файлов и папок."""

    def execute(self, args, shell):
        """Выполнить команду mv.

        Args:
            args: список аргументов [источник, назначение]
            shell: экземпляр оболочки

        Returns:
            Строка с результатом
        """
        if shell.vfs is None:
            return "VFS не загружена"
        if len(args) != 2:
            return "Использование: mv <источник> <назначение>"

        src_name = args[0]
        dst_name = args[1]

        # Найти источник в текущей директории
        src_node = shell.vfs.get_node(src_name)
        if src_node is None:
            return f"Не найдено: {src_name}"

        # Проверить, что назначение не совпадает с источником
        if src_name == dst_name:
            return "Нельзя переместить в себя"

        # Удалить источник из текущей директории
        shell.vfs.current_dir.remove_child(src_name)

        # Если назначение содержит путь (например, "folder/file")
        if '/' in dst_name:
            parts = dst_name.rsplit('/', 1)
            dir_path = parts[0]
            file_name = parts[1]

            # Сохранить текущую директорию
            old_dir = shell.vfs.current_dir

            # Перейти в целевую папку
            error = shell.vfs.change_dir(dir_path)
            if error:
                # Вернуть источник обратно
                shell.vfs.current_dir.add_child(src_node)
                return error

            # Переименовать и добавить в новую папку
            src_node.name = file_name
            shell.vfs.current_dir.add_child(src_node)

            # Вернуться в исходную директорию
            shell.vfs.current_dir = old_dir
        else:
            # Просто переименовать в текущей директории
            src_node.name = dst_name
            shell.vfs.current_dir.add_child(src_node)

        return ""


class CpCommand(Command):
    """Команда копирования файлов и папок."""

    def execute(self, args, shell):
        """Выполнить команду cp.

        Args:
            args: список аргументов [источник, назначение]
            shell: экземпляр оболочки

        Returns:
            Строка с результатом
        """
        if shell.vfs is None:
            return "VFS не загружена"
        if len(args) != 2:
            return "Использование: cp <источник> <назначение>"

        src_name = args[0]
        dst_name = args[1]

        # Найти источник в текущей директории
        src_node = shell.vfs.get_node(src_name)
        if src_node is None:
            return f"Не найдено: {src_name}"

        # Скопировать узел (глубокая копия)
        copied_node = self._deep_copy(src_node)

        # Если назначение содержит путь
        if '/' in dst_name:
            parts = dst_name.rsplit('/', 1)
            dir_path = parts[0]
            file_name = parts[1]

            # Сохранить текущую директорию
            old_dir = shell.vfs.current_dir

            # Перейти в целевую папку
            error = shell.vfs.change_dir(dir_path)
            if error:
                return error

            # Переименовать и добавить в новую папку
            copied_node.name = file_name
            shell.vfs.current_dir.add_child(copied_node)

            # Вернуться в исходную директорию
            shell.vfs.current_dir = old_dir
        else:
            # Просто скопировать в текущей директории
            copied_node.name = dst_name
            shell.vfs.current_dir.add_child(copied_node)

        return ""

    def _deep_copy(self, node):
        """Создать глубокую копию узла.

        Args:
            node: исходный узел

        Returns:
            Копия узла
        """
        from vfs import VFSNode

        copied = VFSNode(node.name, node.node_type)
        if node.is_file():
            copied.content = node.content
        else:
            for child in node.children:
                child_copy = self._deep_copy(child)
                copied.add_child(child_copy)
        return copied
