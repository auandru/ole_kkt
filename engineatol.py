# -*- coding: utf-8 -*-
import logging
from datetime import datetime as datatime
from libfptr10 import IFptr


class OIFptr(IFptr):
    def __init__(self):
        super().__init__()

    def set_settings_com(self, model:str, com:str, br:str='115200'):

        self.setSingleSetting(self.LIBFPTR_SETTING_MODEL, model)
        self.setSingleSetting(self.LIBFPTR_SETTING_PORT, str(self.LIBFPTR_PORT_COM))
        self.setSingleSetting(self.LIBFPTR_SETTING_COM_FILE, com)  # Замените на свой порт
        self.setSingleSetting(self.LIBFPTR_SETTING_BAUDRATE, br)

        self.applySingleSettings()



    def open(self):
        res = super().open()
        logging.info(f'Open connect result: {res}')
        return res

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