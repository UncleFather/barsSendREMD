from initials_common import txt_log_path, txt_log_name, txt_level

from datetime import datetime as dt


# Процедура записи журнала выполнения программы
def log_write(mes_txt, indention=0, lvl='normal'):
    # Открываем файл журнала событий в режиме добавления
    handler = open(txt_log_path + txt_log_name, 'a', encoding='utf8')
    # Добавляем время, в случае, если отступ не равен нулю
    curr_time = "" if indention == 0 else f'({dt.now():%H:%M:%S})'
    # Если уровень записи сообщения соответствует глобальному уровню записи в журнал, то записываем
    # сообщение в файл журнала
    if lvl in txt_level:
        # Записываем в файл сообщение с отступом, переданными при вызове процедуры
        handler.write(f'{" " * indention}{mes_txt} {curr_time}\n')
    # Закрываем файл журнала событий
    handler.close()
