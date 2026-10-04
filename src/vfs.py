"""Модуль виртуальной файловой системы."""

import json
import base64
import os


class VFSNode:
    """Узел файловой системы (файл или папка)."""

    FILE_TYPE = 'file'
    DIR_TYPE = 'dir'

    def __init__(self, name, node_type):
        """Инициализировать узел.

        Args:
            name: имя узла
            node_type: тип ('file' или 'dir')
        """
        self.name = name
        self.node_type = node_type
        self.children = [] if node_type == self.DIR_TYPE else None
        self.content = None

    def is_dir(self):
        """Проверить, является ли узел папкой.

        Returns:
            True если узел — папка
        """
        return self.node_type == self.DIR_TYPE

    def is_file(self):
        """Проверить, является ли узел файлом.

        Returns:
            True если узел — файл
        """
        return self.node_type == self.FILE_TYPE

    def find_child(self, name):
        """Найти дочерний узел по имени.

        Args:
            name: имя искомого узла

        Returns:
            Найденный узел или None
        """
        if not self.is_dir():
            return None
        for child in self.children:
            if child.name == name:
                return child
        return None

    def add_child(self, child):
        """Добавить дочерний узел.

        Args:
            child: узел для добавления
        """
        if self.is_dir():
            self.children.append(child)

    def remove_child(self, name):
        """Удалить дочерний узел по имени.

        Args:
            name: имя удаляемого узла

        Returns:
            True если удалён, False если не найден
        """
        if not self.is_dir():
            return False
        for i, child in enumerate(self.children):
            if child.name == name:
                self.children.pop(i)
                return True
        return False

    def get_content_text(self):
        """Получить содержимое файла как текст.

        Returns:
            Текст содержимого или None
        """
        if self.content is None:
            return None
        try:
            return base64.b64decode(self.content).decode('utf-8')
        except (ValueError, UnicodeDecodeError):
            return None


class VFS:
    """Виртуальная файловая система в памяти."""

    def __init__(self):
        """Инициализировать пустую VFS."""
        self.root = None
        self.current_dir = None

    def load_from_json(self, path):
        """Загрузить VFS из JSON-файла.

        Args:
            path: путь к JSON-файлу

        Returns:
            Сообщение об ошибке или None при успехе
        """
        if not os.path.exists(path):
            return f"Файл VFS не найден: {path}"

        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            return f"Неверный формат JSON: {e}"
        except OSError as e:
            return f"Ошибка чтения файла: {e}"

        error = self._validate_structure(data)
        if error:
            return error

        self.root = self._build_tree(data)
        if self.root is None:
            return "Неверная структура VFS"

        self.current_dir = self.root
        return None

    def _validate_structure(self, data):
        """Проверить структуру JSON.

        Args:
            data: данные из JSON

        Returns:
            Сообщение об ошибке или None
        """
        if not isinstance(data, dict):
            return "VFS должна быть объектом"
        if 'type' not in data:
            return "Отсутствует поле 'type'"
        if 'name' not in data:
            return "Отсутствует поле 'name'"
        return None

    def _build_tree(self, data):
        """Построить дерево из JSON.

        Args:
            data: данные узла

        Returns:
            Построенный узел или None
        """
        node_type = data.get('type')
        name = data.get('name', 'unknown')

        if node_type == VFSNode.DIR_TYPE:
            node = VFSNode(name, VFSNode.DIR_TYPE)
            for child_data in data.get('children', []):
                child = self._build_tree(child_data)
                if child:
                    node.add_child(child)
            return node

        if node_type == VFSNode.FILE_TYPE:
            node = VFSNode(name, VFSNode.FILE_TYPE)
            node.content = data.get('content')
            return node

        return None

    def create_default(self):
        """Создать VFS по умолчанию в памяти."""
        self.root = VFSNode('root', VFSNode.DIR_TYPE)
        self.current_dir = self.root

    def get_current_path(self):
        """Получить путь к текущей директории.

        Returns:
            Строка пути
        """
        if self.current_dir is None:
            return '/'
        return self._build_path(self.root, self.current_dir, '/')

    def _build_path(self, node, target, current_path):
        """Построить путь к узлу.

        Args:
            node: текущий узел
            target: целевой узел
            current_path: текущий путь

        Returns:
            Путь к целевому узлу
        """
        if node is target:
            return current_path
        if node.is_dir():
            for child in node.children:
                child_path = (
                        current_path.rstrip('/') + '/' + child.name
                )
                result = self._build_path(
                    child, target, child_path
                )
                if result:
                    return result
        return None

    def change_dir(self, path):
        """Сменить текущую директорию.

        Args:
            path: путь к новой директории

        Returns:
            Сообщение об ошибке или None
        """
        if path == '/' or path == '':
            self.current_dir = self.root
            return None

        if path == '..':
            if self.current_dir is self.root:
                return None
            parent = self._find_parent(
                self.root, self.current_dir
            )
            if parent:
                self.current_dir = parent
            return None

        parts = path.strip('/').split('/')
        current = self.current_dir

        for part in parts:
            if part == '..':
                if current is not self.root:
                    parent = self._find_parent(
                        self.root, current
                    )
                    if parent:
                        current = parent
                continue

            child = current.find_child(part)
            if child is None:
                return f"Папка не найдена: {part}"
            if not child.is_dir():
                return f"Не папка: {part}"
            current = child

        self.current_dir = current
        return None

    def _find_parent(self, root, target):
        """Найти родительский узел.

        Args:
            root: корневой узел
            target: целевой узел

        Returns:
            Родительский узел или None
        """
        if root is target:
            return None
        if root.is_dir():
            for child in root.children:
                if child is target:
                    return root
                parent = self._find_parent(child, target)
                if parent:
                    return parent
        return None

    def list_dir(self):
        """Получить содержимое текущей директории.

        Returns:
            Список имён дочерних узлов
        """
        if self.current_dir is None:
            return []
        if not self.current_dir.is_dir():
            return []
        return [child.name for child in self.current_dir.children]

    def get_node(self, name):
        """Получить узел по имени в текущей директории.

        Args:
            name: имя узла

        Returns:
            Узел или None
        """
        if self.current_dir is None:
            return None
        return self.current_dir.find_child(name)
