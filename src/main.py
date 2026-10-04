"""Главный модуль с GUI эмулятора оболочки."""

import tkinter as tk
from shell import Shell
from config import EmulatorConfig
from logger import Logger
from script_runner import ScriptRunner
from vfs import VFS


class ShellGUI:
    """Графический интерфейс эмулятора оболочки."""

    def __init__(self, config=None):
        """Инициализировать GUI и оболочку.

        Args:
            config: объект EmulatorConfig
        """
        self.config = config or EmulatorConfig()
        self.shell = Shell(self.config)

        if self.config.log_path:
            self.shell.set_logger(
                Logger(self.config.log_path)
            )

        self._init_vfs()

        self.root = tk.Tk()
        self.root.title(
            self.shell.get_window_title()
        )
        self.root.geometry("800x600")

        self.text_area = tk.Text(
            self.root,
            height=30,
            width=100,
            state=tk.DISABLED,
            bg='black',
            fg='white',
            font=('Consolas', 11),
        )
        self.text_area.pack(
            fill=tk.BOTH, expand=True,
            padx=5, pady=5
        )

        self.entry = tk.Entry(
            self.root,
            width=100,
            bg='black',
            fg='white',
            font=('Consolas', 11),
            insertbackground='white',
            relief=tk.SUNKEN,
            bd=2,
        )
        self.entry.pack(
            fill=tk.X, padx=5, pady=5
        )
        self.entry.bind(
            '<Return>', self.on_enter
        )
        self.entry.focus_set()

        self.show_prompt()

        if self.config.script_path:
            self._run_startup_script()

    def _init_vfs(self):
        """Инициализировать VFS."""
        vfs = VFS()
        if self.config.vfs_path:
            error = vfs.load_from_json(
                self.config.vfs_path
            )
            if error:
                self._vfs_error = error
            else:
                self.shell.set_vfs(vfs)
        else:
            vfs.create_default()
            self.shell.set_vfs(vfs)

    def show_prompt(self):
        """Отобразить приглашение к вводу."""
        self.append_text(self.shell.get_prompt())

    def append_text(self, text):
        """Добавить текст в текстовую область.

        Args:
            text: текст для добавления
        """
        self.text_area.config(state=tk.NORMAL)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state=tk.DISABLED)
        self.text_area.see(tk.END)

    def on_enter(self, event):
        """Обработать нажатие клавиши Enter.

        Args:
            event: событие tkinter
        """
        line = self.entry.get()
        self.entry.delete(0, tk.END)
        self.append_text(line + '\n')

        output = self.shell.execute(line)
        if output:
            self.append_text(output + '\n')

        if not self.shell.is_running:
            self.root.destroy()
            return

        self.show_prompt()
        self.entry.focus_set()

    def _run_startup_script(self):
        """Выполнить стартовый скрипт."""
        if hasattr(self, '_vfs_error'):
            self.append_text(
                f"Ошибка VFS: {self._vfs_error}\n"
            )
            return

        runner = ScriptRunner(self.shell, self)
        path = self.config.script_path
        self.append_text(
            f"--- Запуск скрипта: {path} ---\n"
        )
        success = runner.run(path)
        if success:
            self.append_text(
                "--- Скрипт завершён ---\n"
            )
        else:
            self.append_text(
                "--- Скрипт завершён "
                "с ошибкой ---\n"
            )
        self.show_prompt()
        self.entry.focus_set()

    def run(self):
        """Запустить главный цикл GUI."""
        self.root.mainloop()


def main():
    """Главная точка входа."""
    config = EmulatorConfig().parse_args()
    app = ShellGUI(config)
    app.run()


if __name__ == "__main__":
    main()
