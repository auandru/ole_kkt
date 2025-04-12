# file: my_complex_com_server.py
import sys
import pythoncom
import win32com.server.policy
import logging
from engineatol import OIFptr

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG для подробных сообщений)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[
        logging.FileHandler('com_server.log'),  # Запись в файл com_server.log
        logging.StreamHandler()  # Печать логов в консоль
    ]
)

debugging = 1

if debugging:
    from win32com.server.dispatcher import DefaultDebugDispatcher
    useDispatcher = DefaultDebugDispatcher
else:
    useDispatcher = None



class KktOleServer:
    _public_methods_ = ['open',
                        'cashincome',
                        'setmodel',
                        'setcomnum',
                        ]
    _public_attrs_ = ['version',
                      ]
    _reg_progid_ = "KKT.OleServer"
    _reg_clsid_ = pythoncom.CreateGuid()
    _reg_desc_ = "COM server ole KKT"
    _reg_clsctx_ = pythoncom.CLSCTX_LOCAL_SERVER

    def __init__(self):
        logging.info("Инициализация COM-сервера KktOleServer")
        # self._calculator = Calculator()
        self.o_interfase = OIFptr()
        self.version = 0.1

    def setmodel(self, model):
        self.model = model

    def setcomnum(self, com_number):
        self.comnum = com_number

    def open(self):
        self.o_interfase.set_settings_com(self.model, self.comnum)
        return self.o_interfase.open()

    def cashincome(self, summ):
        if not self.o_interfase.isOpened():
            self.o_interfase.open()
        return self.o_interfase.cashIncome(summ)


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
