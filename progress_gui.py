import tkinter as tk
from tkinter import ttk
import threading

class ProgressWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Выполняется...")
        self.root.geometry("300x80")
        self.root.resizable(False, False)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
        self.progress.pack(pady=20)
        self.progress["value"] = 0

    def update(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()

    def start(self):
        self.root.mainloop()

def show_progress_window():
    win = ProgressWindow()
    threading.Thread(target=win.start, daemon=True).start()
    return win
