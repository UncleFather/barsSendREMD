from initials import txt_log_path, txt_log_name

from datetime import datetime as dt


# Процедура записи журнала выполнения программы
def log_write(mes_txt, indention=0):
    # Открываем файл журнала событий в режиме добавления
    handler = open(txt_log_path + txt_log_name, 'a', encoding='utf8')
    # Записываем в файл сообщение с отступом, переданными при вызове процедуры
    # Добавляем время, в случае, если отступ не равен нулю
    curr_time = "" if indention == 0 else f'({dt.now():%H:%M:%S})'
    handler.write(f'{" " * indention}{mes_txt} {curr_time}\n')
    # Закрываем файл журнала событий
    handler.close()
