# file: my_complex_com_server.py
import sys
import pythoncom
import win32com.server.policy
from engineatol import OIFptr
from dbengine import init_db
import logging
import log_config

logger = logging.getLogger(__name__)

debugging = 1

if debugging:
    from win32com.server.dispatcher import DefaultDebugDispatcher
    useDispatcher = DefaultDebugDispatcher
else:
    useDispatcher = None



class KktOleServer:
    _public_methods_ = ['open',
                        'cashincome',
                        'cashoutcome',
                        'setmodel',
                        'setcomnum',
                        'reportx',
                        'closeshift',
                        'openshift',
                        'sale',
                        'getstatuscheck',
                        'initdb',
                        'checkdocumentclosed',
                        'geterrordescription',
                        ]
    _public_attrs_ = ['version',
                      ]
    _reg_progid_ = "KKT.OleServer"
    _reg_clsid_ = "{0F68B601-6C8D-4F53-B9C9-8A1E87BD9A7D}"
    _reg_appid_ = "{0F68B601-6C8D-4F53-B9C9-8A1E87BD9A7D}"
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

    def cashoutcome(self, summ):
        if not self.o_interfase.isOpened():
            self.o_interfase.open()
        return self.o_interfase.cashOutcome(summ)

    def cashoutcome(self, summ):
        if not self.o_interfase.isOpened():
            self.o_interfase.open()
        return self.o_interfase.cashOutcome(summ)

    def reportx(self):
        if not self.o_interfase.isOpened():
            self.o_interfase.open()
        return self.o_interfase.reportX()

    def openshift(self):
        if not self.o_interfase.isOpened():
            self.o_interfase.open()
        return self.o_interfase.openShift()

    def closeshift(self):
        if not self.o_interfase.isOpened():
            self.o_interfase.open()
        return self.o_interfase.closeShift()

    def sale(self, data):
        logging.info(data)
        if not self.o_interfase.isOpened():
            self.o_interfase.open()
        return self.o_interfase.sale(data)

    def checkdocumentclosed(self):
        return self.o_interfase.checkDocumentClosed()

    def geterrordescription(self):
        return self.o_interfase.errorDescription()

    def getstatuscheck(self, uid):
        return  self.o_interfase.get_status_sales(uid)

    def initdb(self):
        try:
            init_db()
            logging.info("init db  ok")
        except Exception as e:
            logging.info(f"init db {e}")

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
