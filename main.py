from initials_common import mis_accounts, mis_threads

from bars_opers import main_bars
from txt_opers import log_write

from datetime import datetime as dt
from time import sleep
from atexit import register
from threading import Thread
from selenium import webdriver
import sys
import threading


# Класс для обработки события выхода из программы
class ExitHooks(object):
    # Инициализируем конструктор объектов класса
    def __init__(self):
        self.exit_code = None
        self.exception = None

    # Описываем метод hook, возникающий при генерации исключения, в том числе и выхода из программы
    def hook(self):
        self._orig_exit = sys.exit
        sys.exit = self.exit
        sys.excepthook = self.exc_handler

    # Описываем метод exit, получающий код исключения
    def exit(self, code=0):
        self.exit_code = code
        self._orig_exit(code)

    # Описываем метод exc_handler, получающий описание исключения
    def exc_handler(self, exc_type, exc, *args):
        self.exception = exc


# Процедура обработки выхода из программы
def exit_proc():
    # Инициализируем текстовую переменную значением, возникающем при генерации исключения
    mes_txt = f'{"*" * 18} В процессе генерации отчета от {curr_date:%Y.%m.%d} возникли ошибки ' \
              f'(время окончания {dt.now():%H:%M:%S}) {"*" * 18}'
    # Если возникло исключение с кодом, отличным от нуля
    if hooks.exit_code is not None and hooks.exit_code != 0:
        # Добавляем к тексту сообщения код сгенерированного исключения
        mes_txt = f'{"!" * 8 } Возникло исключение с кодом {hooks.exit_code} {"!" * 8 }\n{mes_txt}'
    # Если возникло исключение с непустым описанием
    elif hooks.exception is not None:
        # Добавляем к тексту сообщения описание сгенерированного исключения
        mes_txt = f'{"!" * 8} Возникло исключение: {hooks.exception} {"!" * 8}\n{mes_txt}'
    # Если у исключения отсутствует описание и код либо отсутствует, либо равен нулю
    else:
        # Переписываем текст выводимого сообщения
        mes_txt = f'{"*" * 22} Успешное окончание генерации отчета от {curr_date:%Y.%m.%d} (время ' \
                  f'окончания {dt.now():%H:%M:%S}) {"*" * 22}'
    # Записываем сообщение в журнал
    log_write(mes_txt)


# Инициализируем переменную класса ExitHooks для получения кода сгенерированного исключения
hooks = ExitHooks()
# Вызываем метод получения сгенерированного исключения
hooks.hook()

# Инициализируем процедуру обработки выхода из программы, в том числе при возникновении ошибки
register(exit_proc)
# Инициализируем переменную с текущей датой
curr_date = dt.now()
# Инициализируем переменную, указывающую количество отступов для файла отчета
indention = 2
# Записываем время начала в журнал
log_write(f'{"*" * 30} Начало генерации отчета от {curr_date:%Y.%m.%d} время начала {curr_date:%H:%M:%S}) '
          f'{"*" * 30}')
# Открываем экземпляр драйвера Google Chrome (без этого действия сначала запустится только один поток)
driver = webdriver.Chrome("chromedriver")
# Перебираем все учетные записи из словаря пользователей
for key, value in mis_accounts.items():
    # Запускаем основной модуль работы с МИС «Барс» в нескольких потоках
    log_write(f'Отправка запросов в МИС «Барс» и получение файлов выгрузок от имени {key}', indention)
    thread = Thread(target=main_bars, args=(key, value))
    thread.start()
    # Контролируем, чтобы количество активных потоков было не больше заданного
    while threading.active_count() > mis_threads:
        sleep(10)

# Закрываем экземпляр драйвера Google Chrome
driver.close()
# Выполняем выход
exit(0)
