# import tkinter as tk
# from tkinter import ttk
# import threading
#
# class ProgressWindow:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Выполняется...")
#         self.root.geometry("300x80")
#         self.root.resizable(False, False)
#
#         self.progress = ttk.Progressbar(self.root, orient="horizontal", length=250, mode="determinate")
#         self.progress.pack(pady=20)
#         self.progress["value"] = 0
#
#     def update(self, value):
#         self.progress["value"] = value
#         self.root.update_idletasks()
#
#     def start(self):
#         self.root.mainloop()
#
# def show_progress_window():
#     win = ProgressWindow()
#     threading.Thread(target=win.start, daemon=True).start()
#     return win

import wx

class ProgressWindow:
    def __init__(self, max_value):
        self.app = wx.App(False)
        self.frame = wx.Frame(None, title="Прогресс", size=(300, 100))
        panel = wx.Panel(self.frame)
        self.gauge = wx.Gauge(panel, range=max_value, size=(250, 25), pos=(20, 20))
        self.frame.Show()
        self.frame.Raise()  # На передний план

    def update(self, value):
        self.gauge.SetValue(value)
        wx.Yield()  # Обновление GUI

    def destroy(self):
        self.frame.Destroy()
        self.app.ExitMainLoop()