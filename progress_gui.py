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

    def close(self):
        self.Destroy()
        if wx.GetApp():
            wx.GetApp().ExitMainLoop()

def show_progress_window(max_value):
    app = wx.App(False)
    dialog = ProgressDialog(max_value)
    return app, dialog
