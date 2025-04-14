# -*- coding: utf-8 -*-
import json
from datetime import datetime as datatime
import logging
from numbers import Number

from libfptr10 import IFptr
from progress_gui import show_progress_window
import dbengine as db
import time
import threading
import uuid

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG для подробных сообщений)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[
        logging.FileHandler('com_server.log'),  # Запись в файл com_server.log
        logging.StreamHandler()  # Печать логов в консоль
    ]
)

def create_uid():
    uid = str(uuid.uuid4())
    return uid

class OIFptr(IFptr):
    def __init__(self):
        super().__init__()
        db.init_db()

    def set_settings_com(self, model:str, com:str, br:str='115200'):
        try:
            logging.info(f'Try save setting com:  model{ model}')
            self.setSingleSetting(self.LIBFPTR_SETTING_MODEL, model)
            self.setSingleSetting(self.LIBFPTR_SETTING_PORT, str(self.LIBFPTR_PORT_COM))
            self.setSingleSetting(self.LIBFPTR_SETTING_COM_FILE, com)  # Замените на свой порт
            self.setSingleSetting(self.LIBFPTR_SETTING_BAUDRATE, br)

            self.applySingleSettings()
        except Exception as e:
            logging.error(f'Error save setting com: {e}')


    def open(self):
        res = super().open()
        logging.info(f'Open connect result: {res}')
        return res

    def cashOutcome(self, value):

        self.setParam(self.LIBFPTR_PARAM_SUM, value)
        res = super().cashOutcome()
        logging.info(f' Metod cashOutcome result: {res}')
        return res

    def cashIncome(self, value):
        self.setParam(self.LIBFPTR_PARAM_SUM, value)
        res = super().cashIncome()
        logging.info(f'Method cashIncome result: {res}')
        return res

    def reportX(self):
        self.setParam(self.LIBFPTR_PARAM_REPORT_TYPE, self.LIBFPTR_RT_X)
        return self.report()

    def openShift(self):
        try:
            # super().operatorLogin()
            super().openShift()
            logging.info(f'Method openShift result: ')
            return self.checkDocumentClosed()
        except Exception as e:
            logging.error(f'Error method openShift result: {e}')
            return -1

    def closeShift(self):
        self.setParam(self.LIBFPTR_PARAM_REPORT_TYPE, self.LIBFPTR_RT_CLOSE_SHIFT)
        self.report()
        return self.checkDocumentClosed()

    def checkDocumentClosed(self):
        return super().checkDocumentClosed()

    def _print_sale(self, datasale, uid):
        self.setParam(self.LIBFPTR_PARAM_RECEIPT_TYPE, self.LIBFPTR_RT_SELL)
        self.openReceipt()
        db.init_db()
        app, progress = show_progress_window(max_value=len(datasale))
        try:
            i = 0
            for sale in datasale:
                i += 1
                progress.update(i)
                time.sleep(0.05)
                self.setParam(self.LIBFPTR_PARAM_COMMODITY_NAME, sale.get('name'))
                self.setParam(self.LIBFPTR_PARAM_PRICE, sale.get('price'))
                self.setParam(self.LIBFPTR_PARAM_QUANTITY, sale.get('quantity'))
                # self.setParam(self.LIBFPTR_PARAM_TAX_TYPE, sale.get('tax'))
                self.setParam(self.LIBFPTR_PARAM_TAX_TYPE, self.LIBFPTR_TAX_NO)
                self.registration()
                res = self.closeReceipt()
                db.insert_sale(uid,res ,'')
        finally:
            progress.close()
            del app

    def sale(self, data):
        try:
            datasale = json.loads(data)
            datasale = datasale.get('sales',{})
        except Exception as e:
            logging.error(e)
            return -5
        uid = create_uid()
        thread = threading.Thread(target=self._print_sale, args=(datasale,uid))
        thread.daemon = True
        thread.start()
        return uid


    def get_status_sales(self, uid)->Number:
        return db.get_sale(uid)