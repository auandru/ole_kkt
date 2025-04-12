import win32com.client
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Уровень логирования (DEBUG для подробных сообщений)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Формат логов
    handlers=[
        logging.FileHandler('com_client.log'),  # Запись в файл com_client.log
        logging.StreamHandler()  # Печать логов в консоль
    ]
)

def connect_to_com_server():
    try:
        # Подключаемся к COM-серверу
        logging.info("Подключение к COM-серверу...")
        com_server = win32com.client.Dispatch("KKT.OleServer")
        logging.info("Успешное подключение к COM-серверу.")
        return com_server
    except Exception as e:
        logging.error(f"Ошибка подключения к COM-серверу: {e}")
        return None

def use_calculator_server(com_server):
    try:
        # Получаем калькулятор с сервера
        calculator = com_server.getcalculator()
        logging.info("Получен объект калькулятора.")

        # Выполняем операции
        result_add = calculator #.Add(10, 20)
        logging.info(f"Результат сложения: {result_add}")

        result_sub = calculator #.Sub(30, 10)
        logging.info(f"Результат вычитания: {result_sub}")

        #calculator.StoreInMemory(100)
        memory_value = calculator #.ReadMemory()
        logging.info(f"Значение в памяти: {memory_value}")
    except Exception as e:
        logging.error(f"Ошибка при использовании калькулятора: {e}")

def use_settings_server(com_server):
    try:
        # Получаем настройки с сервера
        res= None
        logging.info(com_server.version)
        try:
            com_server.setmodel("61")
            com_server.setcomnum("COM31")
            res = com_server.open()
        except Exception as e:
            logging.info(f"Result opened. {e}")
        logging.info(f"Result opened. {res}")
    except Exception as e:
        logging.error(f"Ошибка при использовании настроек: {e}")

if __name__ == "__main__":
    # Подключаемся к серверу
    com_server = connect_to_com_server()

    if com_server:
        # Используем калькулятор
        #use_calculator_server(com_server)

        # Используем настройки
        use_settings_server(com_server)
