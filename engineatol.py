# -*- coding: utf-8 -*-
from datetime import datetime as datatime
import logging
from libfptr10 import IFptr

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG для подробных сообщений)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[
        logging.FileHandler('com_server.log'),  # Запись в файл com_server.log
        logging.StreamHandler()  # Печать логов в консоль
    ]
)


class OIFptr(IFptr):
    def __init__(self):
        super().__init__()

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
        while super().checkDocumentClosed() < 0:
            # Не удалось проверить состояние документа. Вывести пользователю текст ошибки, попросить устранить неполадку и повторить запрос
            print(self.errorDescription())
            continue
        return 0

#
# print(f' Open {datatime.now()}')
# fptr.open()
# if not fptr.isOpened():
#     print("Code", fptr.errorCode())
#     print("Error:", fptr.errorDescription())
#     exit(1)
# print(f' Set param {datatime.now()}')
# #fptr.setParam(fptr.LIBFPTR_PARAM_DATA_TYPE, fptr.LIBFPTR_DT_STATUS)
# #fptr.queryData()
# print(f' Get param {datatime.now()}')
# fptr.setParam(IFptr.LIBFPTR_PARAM_DATA_TYPE, IFptr.LIBFPTR_DT_MODEL_INFO)
# fptr.queryData()
#
# model           = fptr.getParamInt(IFptr.LIBFPTR_PARAM_MODEL)
# modelName       = fptr.getParamString(IFptr.LIBFPTR_PARAM_MODEL_NAME)
# firmwareVersion = fptr.getParamString(IFptr.LIBFPTR_PARAM_UNIT_VERSION)
# print(f'{model} {modelName} {firmwareVersion}')
# print(f'{datatime.now()}')
#
# fptr.setParam(fptr.LIBFPTR_PARAM_RECEIPT_TYPE, fptr.LIBFPTR_RT_SELL);
# fptr.openReceipt();
#
# fptr.setParam(fptr.LIBFPTR_PARAM_COMMODITY_NAME, 'Tovar')
# fptr.setParam(fptr.LIBFPTR_PARAM_PRICE, 100)
# fptr.setParam(fptr.LIBFPTR_PARAM_QUANTITY, 5.15)
# fptr.setParam(fptr.LIBFPTR_PARAM_TAX_TYPE, fptr.LIBFPTR_TAX_VAT0)
# fptr.registration()
#
# print(f'Closed check - {datatime.now()} {fptr.checkDocumentClosed()}')
# fptr.logWrite("MyTag", IFptr.LIBFPTR_LOG_DEBUG, "Мое отладочное сообщение")
# fptr.close()
#
# print(f' Close {datatime.now()}')