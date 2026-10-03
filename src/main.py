"""Главный модуль с GUI эмулятора оболочки."""

import tkinter as tk
from shell import Shell


class ShellGUI:
    """Графический интерфейс эмулятора оболочки."""

    def __init__(self):
        """Инициализировать GUI и оболочку."""
        self.shell = Shell()
        self.root = tk.Tk()
        self.root.title(self.shell.get_window_title())

        self.text_area = tk.Text(
            self.root,
            height=20,
            width=80,
            state=tk.DISABLED,
            bg='black',
            fg='white',
            font=('Courier', 10)
        )
        self.text_area.pack()

        self.entry = tk.Entry(
            self.root,
            width=80,
            bg='black',
            fg='white',
            font=('Courier', 10)
        )
        self.entry.pack()
        self.entry.bind('<Return>', self.on_enter)
        self.entry.focus()
        self.show_prompt()

    def show_prompt(self):
        """Отобразить приглашение к вводу в текстовой области."""
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
        self.entry.focus()

    def run(self):
        """Запустить главный цикл GUI."""
        self.root.mainloop()


def main():
    """Главная точка входа."""
    app = ShellGUI()
    app.run()


if __name__ == "__main__":
    main()
