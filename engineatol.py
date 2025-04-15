# -*- coding: utf-8 -*-
import json
from datetime import datetime as datatime
from numbers import Number

from libfptr10 import IFptr
from progress_gui import show_progress_window
import dbengine as db
import time
import threading
import uuid
import logging
import log_config

logger = logging.getLogger(__name__)

def create_uid():

    uid = str(uuid.uuid4())
    logger.info(f"Create uid {uid}")
    return uid

class OIFptr(IFptr):
    def __init__(self):
        super().__init__()

    def set_settings_com(self, model:str, com:str, br:str='115200'):
        try:
            logger.info(f'Try save setting com:  model{ model}')
            self.setSingleSetting(self.LIBFPTR_SETTING_MODEL, model)
            self.setSingleSetting(self.LIBFPTR_SETTING_PORT, str(self.LIBFPTR_PORT_COM))
            self.setSingleSetting(self.LIBFPTR_SETTING_COM_FILE, com)  # Замените на свой порт
            self.setSingleSetting(self.LIBFPTR_SETTING_BAUDRATE, br)

            self.applySingleSettings()
        except Exception as e:
            logger.error(f'Error save setting com: {e}')


    def open(self):
        res = super().open()
        logger.info(f'Open connect result: {res}')
        return res

    def cashOutcome(self, value):

        self.setParam(self.LIBFPTR_PARAM_SUM, value)
        res = super().cashOutcome()
        logger.info(f' Metod cashOutcome result: {res}')
        return res

    def cashIncome(self, value):
        self.setParam(self.LIBFPTR_PARAM_SUM, value)
        res = super().cashIncome()
        logger.info(f'Method cashIncome result: {res}')
        return res

    def reportX(self):
        self.setParam(self.LIBFPTR_PARAM_REPORT_TYPE, self.LIBFPTR_RT_X)
        return self.report()

    def openShift(self):
        try:
            # super().operatorLogin()
            super().openShift()
            logger.info(f'Method openShift result: ')
            return self.checkDocumentClosed()
        except Exception as e:
            logger.error(f'Error method openShift result: {e}')
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

    def sale_threading(self, data):
        try:
            datasale = json.loads(data)
            datasale = datasale.get('sales',{})
        except Exception as e:
            logger.error(e)
            return -5
        uid = create_uid()
        thread = threading.Thread(target=self._print_sale, args=(datasale,uid))
        thread.daemon = True
        thread.start()
        return uid

    def sale(self, data):
        try:
            datasale = json.loads(data)
            datasale = datasale.get('sales',{})
            summa = datasale.get('summa')
            nalbezn = datasale.get('payment_type')
            sell_type = datasale.get('sell_type', None)
        except Exception as e:
            logger.error(e)
            return -5
        if sell_type == 2:
            self.setParam(self.LIBFPTR_PARAM_RECEIPT_TYPE, self.LIBFPTR_RT_SELL_RETURN)
        else:
            self.setParam(self.LIBFPTR_PARAM_RECEIPT_TYPE, self.LIBFPTR_RT_SELL)

        self.openReceipt()
        # app, progress = show_progress_window(max_value=len(datasale))
        i = 0
        for sale in datasale:
            i += 1
            # progress.update(i)
            self.setParam(self.LIBFPTR_PARAM_COMMODITY_NAME, sale.get('name'))
            self.setParam(self.LIBFPTR_PARAM_PRICE, sale.get('price'))
            self.setParam(self.LIBFPTR_PARAM_QUANTITY, sale.get('quantity'))
            # self.setParam(self.LIBFPTR_PARAM_TAX_TYPE, sale.get('tax'))
            self.setParam(self.LIBFPTR_PARAM_TAX_TYPE, self.LIBFPTR_TAX_NO)
            self.registration()
        if nalbezn or nalbezn is None :
            self.setParam(self.LIBFPTR_PARAM_PAYMENT_TYPE, self.LIBFPTR_PT_CASH)
            self.payment()
        else:
            self.setParam(self.LIBFPTR_PARAM_PAYMENT_TYPE, self.LIBFPTR_PT_ELECTRONICALLY)
            self.payment()
        if summa:
            self.setParam(self.LIBFPTR_PARAM_PAYMENT_SUM, summa)
            self.payment()

        return self.closeReceipt()


    def shiftstate(self):
        self.setParam(self.LIBFPTR_PARAM_DATA_TYPE, self.LIBFPTR_DT_SHIFT_STATE)
        self.queryData()

        state = self.getParamInt(self.LIBFPTR_PARAM_SHIFT_STATE)
        _number = self.getParamInt(self.LIBFPTR_PARAM_SHIFT_NUMBER)
        # Тип переменной datetime - datetime.datetime
        _dateTime = self.getParamDateTime(self.LIBFPTR_PARAM_DATE_TIME)
        logger.info(json.dumps({"state": state, "number": _number, "dateTime": str(_dateTime)}))
        return json.dumps({"state": state, "number": _number, "dateTime": str(_dateTime)})


def get_status_sales(self, uid)->Number:
        logger.info(f"Get status {uid}")
        return db.get_sale(uid)