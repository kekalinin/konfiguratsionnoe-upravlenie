"""Модуль выполнения стартового скрипта."""

import os


class ScriptRunner:
    """Выполняет команды из стартового скрипта."""

    COMMENT_CHAR = '#'

    def __init__(self, shell, gui):
        """Инициализировать раннер.

        Args:
            shell: экземпляр Shell
            gui: экземпляр ShellGUI
        """
        self.shell = shell
        self.gui = gui

    def run(self, script_path):
        """Выполнить стартовый скрипт.

        Args:
            script_path: путь к файлу скрипта

        Returns:
            True при успехе, False при ошибке
        """
        if not os.path.exists(script_path):
            msg = f"Скрипт не найден: {script_path}"
            self.gui.append_text(msg + '\n')
            self.shell.logger.log_command(
                'script', [script_path], error=msg
            )
            return False

        try:
            with open(
                    script_path, 'r', encoding='utf-8'
            ) as f:
                lines = f.readlines()
        except OSError as e:
            msg = f"Ошибка чтения скрипта: {e}"
            self.gui.append_text(msg + '\n')
            return False

        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith(self.COMMENT_CHAR):
                continue
            self._execute_line(line)

        return True

    def _execute_line(self, line):
        """Выполнить одну строку скрипта.

        Args:
            line: строка с командой
        """
        self.gui.append_text(
            self.shell.get_prompt() + line + '\n'
        )
        output = self.shell.execute(line)
        if output:
            self.gui.append_text(output + '\n')
