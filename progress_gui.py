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

class ProgressDialog(wx.Dialog):
    def __init__(self, max_value):
        super().__init__(None, title="Обработка продажи", size=(300, 100), style=wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW)
        panel = wx.Panel(self)
        self.gauge = wx.Gauge(panel, range=max_value, size=(250, 25), pos=(20, 20))
        self.Centre()
        self.Show()
        self.Raise()

    def update(self, value):
        self.gauge.SetValue(value)
        wx.Yield()  # Позволяет обновить GUI

def show_progress_window(max_value):
    app = wx.App(False)
    dialog = ProgressDialog(max_value)
    return app, dialog
