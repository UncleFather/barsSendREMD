from initials_common import mis_url

from txt_opers import log_write

from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def main_bars(username, password):
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 4
    # Инициализируем драйвер Google Chrome
    driver = webdriver.Chrome("chromedriver")
    log_write(f'{username}: Открыт экземпляр Google Chrome', indention)
    # Переходим на страницу входа на сайт
    driver.get(mis_url)
    log_write(f'{username}: Выполнен переход на страницу входа на сайт', indention)
    # Устанавливаем размер окна открывшегося экземпляра браузера
    driver.set_window_size(1561, 1060)

    # Парсим страничку входа. Находим поле для ввода имени пользователя и записываем в него имя
    driver.find_element(By.NAME, "DBLogin").find_element(By.CLASS_NAME, "input-ctrl").send_keys(username)
    log_write(f'{username}: Введено имя пользователя', indention)
    # Находим поле для ввода пароля и записываем в него пароль
    driver.find_element(By.NAME, "DBPassword").find_element(By.CLASS_NAME, "input-ctrl").send_keys(password)
    log_write(f'{username}: Введен пароль пользователя', indention)
    # Находим кнопку отправки и нажимаем ее
    driver.find_element(By.CLASS_NAME, "bt").click()
    log_write(f'{username}: Инициирован процесс авторизации в МИС «Барс»', indention)

    # Ждем 3 секунды
    sleep(3)
    # Подтверждаем организацию и кабинет (находим кнопку и кликаем по ней)
    driver.find_element(By.CLASS_NAME, "bt").click()
    log_write(f'{username}: Подтвержден кабинет и ЛПУ', indention)

    # Ждем 4 секунды
    sleep(4)

    # Парсим страничку, на предмет нахождения на ней всплывающих сообщений и закрываем их
    try:
        driver.find_element(By.LINK_TEXT, 'Закрыть все').click()
    except Exception:
        indention = 6
        log_write(f'{username}: ВНИМАНИЕ!!! Новые сообщения в МИС «Барс»', indention)
        indention = 4

    # Парсим страничку, находим нужные пункты меню и кликаем по ним
    driver.find_element(By.LINK_TEXT, 'Рабочие места').click()
    log_write(f'{username}: Выбран пункт меню «Рабочие места»', indention)
    driver.find_element(By.LINK_TEXT, 'Отчеты на подпись').click()
    log_write(f'{username}: Выбран пункт меню «Отчеты на подпись»', indention)

    # Ждем 6 секунд
    sleep(6)

    # Выполняем цикл два раза. Первый - для еще не отправленных в РЭМД свидетельств, второй - для свидетельств
    # с ошибкой регистрации в РЭМД, отправляемых повторно
    for i in range(2):
        # При первом проходе цикла будем отправлять в РЭМД ранее не отправлявшиеся свидетельства
        if i == 0:
            # Парсим форму, находим первое поле списка (с должностями) и разворачиваем список
            driver.find_element(By.ID, "_mainContainer").find_element(By.CLASS_NAME, "cmbb-button").click()
            # Парсим список, находим должность «Главный врач» и выбираем ее
            driver.find_element(By.XPATH, "//span[contains(text(), 'Главный врач')]").click()
            log_write(f'{username}: Список отфильтрован по значению «Главный врач» поля «Роль»', indention)
            # Ждем 6 секунд
            sleep(6)
            # Парсим форму, находим второе поле списка (со статусом документов) и разворачиваем список
            driver.find_element(By.ID, "_mainContainer").find_elements(By.CLASS_NAME, "cmbb-input")[1].click()
            # Парсим список, находим статус «Подписан» и выбираем его
            driver.find_element(By.XPATH, "//span[text()='Подписан']").click()
            log_write(f'{username}: Список отфильтрован по значению «Подписан» поля «Статус подписи»', indention)
            # Ждем 6 секунд
            sleep(6)
            # Парсим форму, находим шестое поле ввода текста (номером версии документа) устанавливаем значение «1»
            # и нажимаем «Enter»
            driver.find_elements(By.XPATH, "//input[@cmpparse='Edit']")[5].send_keys('1' + Keys.RETURN)
            log_write(f'{username}: Список отфильтрован по значению «1» поля «Версия»', indention)
            # Ждем 6 секунд
            sleep(6)
        # При втором проходе цикла будем отправлять в РЭМД те свидетельства, которые ранее отправлялись и
        # вернулись с ошибкой
        else:
            # Парсим форму, находим третье поле списка (статус в РЭМД) и разворачиваем список
            driver.find_element(By.ID, "_mainContainer").find_elements(By.CLASS_NAME, "cmbb-input")[2].click()
            # Парсим список, находим статус «Ошибка получения ответа от РЭМД» и выбираем его
            driver.find_element(By.XPATH, "//span[text()='Ошибка получения ответа от РЭМД']").click()
            log_write(f'{username}: Список отфильтрован по значению «Ошибка получения ответа от РЭМД» поля '
                      f'«Статус в РЭМД»', indention)
            # Ждем 6 секунд
            sleep(6)

        doc_number = 1
        # Перебираем все записи из полученной таблицы
        while True:
            try:
                # Пытаемся найти записи
                log_write(f'{username}: Пытаемся найти записи', indention, 'debug')
                curr_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Нужен для хранения настроек') "
                                                             "or contains(text(), 'Настройки подписи для СЭМД')]")
            except Exception:
                log_write(f'{username}: 1-st try', indention, 'debug')
                # Если не можем найти записи, то считаем что список пуст и выходим из модуля
                break
            # Делаем правый клик
            log_write(f'{username}: Делаем правый клик', indention, 'debug')
            ActionChains(driver).context_click(curr_element).perform()
            # Ждем 1 секунду
            sleep(1)
            # Парсим контекстное меню, находим пункт «Зарегистрировать в РЭМД» и выбираем его
            log_write(f'{username}: Парсим контекстное меню, находим пункт «Зарегистрировать в РЭМД»',
                      indention, 'debug')
            driver.find_element(By.XPATH, "//span[text()='Зарегистрировать в РЭМД']").click()
            log_write(f'{username}: Отправляем в РЭМД свидетельство №{doc_number}', indention)
            doc_number += 1

            # Инициализируем переменную для прерывания цикла проверки окончания отправки в РЭМД очередной записи
            bool_1 = True
            # Начинаем цикл проверки
            while bool_1:
                # Ждем 2 секунды
                sleep(2)
                try:
                    # Пытаемся найти на форме кнопку «Ок» или «Продолжить» и нажать ее
                    log_write(f'{username}: Пытаемся найти на форме кнопку «Ок» или «Продолжить»',
                              indention, 'debug')
                    driver.find_element(By.XPATH, "//div[@name='CONTINUE_BUTTON' or text()='Ок']").click()
                    # Ждем 4 секунды
                    sleep(4)
                    # Если все прошло успешно, считаем, что документ отправился и выходим из цикла
                    log_write(f'{username}: Свидетельство №{doc_number} успешно отправлено в РЭМД', indention)
                    bool_1 = False
                except Exception:
                    log_write(f'{username}: 2-nd try', indention, 'debug')
                    # Если возникли ошибки, считаем, что документ все еще отправляется и продолжаем цикл проверки
                    pass

    # Находим кнопку выхода и нажимаем ее
    driver.find_element(By.CLASS_NAME, "Exit").click()
    log_write(f'{username}: Осуществлен выход из МИС «БАРС»', indention)
    # Ждем 4 секунды
    sleep(4)
    # Закрываем экземпляр драйвера Google Chrome
    driver.close()
    log_write(f'{username}: Закрыт экземпляр браузера Google Chrome', indention)
