import logging

# LOG_FILE = 'app.log'
#
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(name)s - %(message)s',
#     filename=LOG_FILE,
#     filemode='a'  # append mode
# )
#
# console = logging.StreamHandler()
# console.setFormatter(logging.Formatter('%(levelname)s - %(message)s'))
# logging.getLogger('').addHandler(console)

logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG для подробных сообщений)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[
        logging.FileHandler('D:\com_server.log'),  # Запись в файл com_server.log
        logging.StreamHandler()  # Печать логов в консоль
    ]
)