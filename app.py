# file: my_complex_com_server.py
import sys
import pythoncom
import win32com.server.policy
import logging

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG для подробных сообщений)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[
        logging.FileHandler('com_server.log'),  # Запись в файл com_server.log
        logging.StreamHandler()  # Печать логов в консоль
    ]
)

class Settings:
    def __init__(self):
        self._values = {
            "username": "admin",
            "mode": "standard",
            "version": "1.0"
        }

    def Get(self, key):
        logging.debug(f"Get Settings: {key}")
        return self._values.get(key, f"[{key} not found]")

    def Set(self, key, value):
        logging.debug(f"Set Settings: {key} = {value}")
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
    _public_methods_ = ['getcalculator', 'getsettings']
    _reg_progid_ = "KKT.OleServer"
    _reg_clsid_ = "{21C6C83C-FAD7-4CE4-B16A-B5948F492200}"
    _reg_desc_ = "COM server ole KKT"
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER

    def __init__(self):
        logging.info("Инициализация COM-сервера KktOleServer")
        self._calculator = Calculator()
        self._settings = Settings()

    def getcalculator(self):
        logging.info("Вызов метода GetCalculator")
        return "self._calculator"

    def getsettings(self):
        logging.info("Вызов метода GetSettings")
        return "self._settings"


if __name__ == "__main__":
    import win32com.server.register
    if "--register" in sys.argv:
        print("register OLE-сервер...")
        logging.info("Регистрация OLE-сервера...")
        win32com.server.register.UseCommandLine(KktOleServer)
    elif "--unregister" in sys.argv:
        print("unregister OLE-сервера...")
        win32com.server.register.UnregisterClasses(KktOleServer)
    else:
        print("Укажи --register или --unregister")
