"""Модуль для разбора командной строки."""


class CommandParser:
    """Парсер командной строки с поддержкой кавычек."""

    def parse(self, line):
        """Разобрать командную строку на список аргументов.

        Args:
            line: входная строка от пользователя

        Returns:
            Список разобранных аргументов
        """
        if not line:
            return []

        args = []
        current = []
        in_quotes = False
        quote_char = None

        for char in line:
            if in_quotes:
                if char == quote_char:
                    in_quotes = False
                    quote_char = None
                else:
                    current.append(char)
            elif char in ('"', "'"):
                in_quotes = True
                quote_char = char
            elif char.isspace():
                if current:
                    args.append(''.join(current))
                    current = []
            else:
                current.append(char)

        if current:
            args.append(''.join(current))

        return args
