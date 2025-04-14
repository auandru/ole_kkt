import wx


class ProgressDialog(wx.TopLevelWindow):
    def __init__(self, parent, max_value):
        super().__init__(parent, title="Обробка", style=wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW)

        # Панель вікна
        panel = wx.Panel(self)
        self.gauge = wx.Gauge(panel, range=max_value, size=(250, 25), pos=(20, 20))
        self.CentreOnScreen()
        self.Show()

    def update(self, value):
        self.gauge.SetValue(value)
        wx.YieldIfNeeded()  # Оновлює інтерфейс без зависання


def show_progress_window(max_value):
    app = wx.App(False)
    frame = ProgressDialog(None, max_value)
    return app, frame
