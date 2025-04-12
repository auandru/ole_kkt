# file: my_complex_com_server.py
import sys
import pythoncom
import win32com.server.policy

class Settings:
    def __init__(self):
        self._values = {
            "username": "admin",
            "mode": "standard",
            "version": "1.0"
        }

    def Get(self, key):
        return self._values.get(key, f"[{key} not found]")

    def Set(self, key, value):
        self._values[key] = value
        return f"[{key}] = {value}"

class Calculator:
    def __init__(self):
        self.memory = 0

    def Add(self, a, b):
        return a + b

    def Sub(self, a, b):
        return a - b

    def StoreInMemory(self, value):
        self.memory = value
        return "OK"

    def ReadMemory(self):
        return self.memory


class KktOleServer:
    _public_methods_ = ['GetCalculator', 'GetSettings']
    _reg_progid_ = "KKT.OleServer"
    _reg_clsid_ = "5C2594FF-2E33-4A0D-8192-BE6BBEBF7F05"
    _reg_desc_ = "COM server ole KKT"
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER

    def __init__(self):
        self._calculator = Calculator()
        self._settings = Settings()

    def GetCalculator(self):
        return win32com.server.util.wrap(self._calculator)

    def GetSettings(self):
        return win32com.server.util.wrap(self._settings)


if __name__ == "__main__":
    import win32com.server.register
    if "--register" in sys.argv:
        print("register OLE-сервер...")
        win32com.server.register.UseCommandLine(KktOleServer)
    elif "--unregister" in sys.argv:
        print("unregister OLE-сервера...")
        win32com.server.register.UnregisterClasses(KktOleServer)
    else:
        print("Укажи --register или --unregister")
