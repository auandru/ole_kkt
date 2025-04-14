import logging
import sys

LOG_FILENAME = "app.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILENAME, mode='a', encoding='utf-8'),
        logging.StreamHandler(sys.stdout)
    ]
)


# logging.basicConfig(
#     level=logging.INFO,  # Уровень логирования (DEBUG для подробных сообщений)
#     format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
#     handlers=[
#         logging.FileHandler('D:\com_server.log'),  # Запись в файл com_server.log
#         # logging.StreamHandler()  # Печать логов в консоль
#     ]
# )