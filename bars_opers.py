from initials import mis_url, mis_username, mis_password

from txt_opers import log_write

from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def main_bars():
    # Инициализируем переменную, указывающую количество отступов для файла отчета
    indention = 4
    # Устанавливаем константы с учетными данными
    username = mis_username
    password = mis_password
    # Инициализируем драйвер Google Chrome
    driver = webdriver.Chrome("chromedriver")
    log_write(f'Открыт экземпляр Google Chrome', indention)
    # Переходим на страницу входа на сайт
    driver.get(mis_url)
    log_write(f'Выполнен переход на страницу входа на сайт', indention)
    # Устанавливаем размер окна открывшегося экземпляра браузера
    driver.set_window_size(1561, 1060)

    # Парсим страничку входа. Находим поле для ввода имени пользователя и записываем в него имя
    driver.find_element(By.NAME, "DBLogin").find_element(By.CLASS_NAME, "input-ctrl").send_keys(username)
    log_write(f'Введено имя пользователя', indention)
    # Находим поле для ввода пароля и записываем в него пароль
    driver.find_element(By.NAME, "DBPassword").find_element(By.CLASS_NAME, "input-ctrl").send_keys(password)
    log_write(f'Введен пароль пользователя', indention)
    # Находим кнопку отправки и нажимаем ее
    driver.find_element(By.CLASS_NAME, "bt").click()
    log_write(f'Инициирован процесс авторизации в МИС «Барс»', indention)

    # Ждем 3 секунды
    sleep(3)
    # Подтверждаем организацию и кабинет (находим кнопку и кликаем по ней)
    driver.find_element(By.CLASS_NAME, "bt").click()
    log_write(f'Подтвержден кабинет и ЛПУ', indention)

    # Ждем 4 секунды
    sleep(4)

    # Парсим страничку, на предмет нахождения на ней всплывающих сообщений и закрываем их
    try:
        driver.find_element(By.LINK_TEXT, 'Закрыть все').click()
    except Exception:
        indention = 6
        log_write(f'ВНИМАНИЕ!!! Новые сообщения в МИС «Барс»', indention)
        indention = 4

    # Парсим страничку, находим нужные пункты меню и кликаем по ним
    driver.find_element(By.LINK_TEXT, 'Рабочие места').click()
    log_write(f'Выбран пункт меню «Рабочие места»', indention)
    driver.find_element(By.LINK_TEXT, 'Отчеты на подпись').click()
    log_write(f'Выбран пункт меню «Отчеты на подпись»', indention)

    # Ждем 4 секунды
    sleep(4)

    # Парсим форму, находим первое поле списка (с должностями) и разворачиваем список
    driver.find_element(By.ID, "_mainContainer").find_element(By.CLASS_NAME, "cmbb-button").click()
    # Парсим список, находим должность «Главный врач» и выбираем ее
    driver.find_element(By.XPATH, "//span[contains(text(), 'Главный врач')]").click()
    # Ждем 4 секунды
    sleep(4)
    # Парсим форму, находим второе поле списка (со статусом документов) и разворачиваем список
    driver.find_element(By.ID, "_mainContainer").find_elements(By.CLASS_NAME, "cmbb-input")[1].click()
    # Парсим список, находим статус «Подписан» и выбираем его
    driver.find_element(By.XPATH, "//span[text()='Подписан']").click()
    # Ждем 4 секунды
    sleep(4)
    # Парсим форму, находим шестое поле ввода текста (номером версии документа) устанавливаем значение «1» и нажимаем «Enter»
    driver.find_elements(By.XPATH, "//input[@cmpparse='Edit']")[5].send_keys('1' + Keys.RETURN)
    # Ждем 4 секунды
    sleep(4)

    # Парсим форму, находим третье поле списка (статус в РЭМД) и разворачиваем список
    driver.find_element(By.ID, "_mainContainer").find_elements(By.CLASS_NAME, "cmbb-input")[2].click()
    # Парсим список, находим статус «Ошибка получения ответа от РЭМД» и выбираем его
    driver.find_element(By.XPATH, "//span[text()='Ошибка получения ответа от РЭМД']").click()
    # Ждем 4 секунды
    sleep(4)

    # Перебираем все записи из полученной таблицы
    while True:
        try:
            # Пытаемся найти запись
            curr_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Настройки подписи для СЭМД')]")
            # Делаем правый клик
            ActionChains(driver).context_click(curr_element).perform()
            # Ждем 1 секунду
            sleep(1)
            # Парсим контекстное меню, находим пункт «Зарегистрировать в РЭМД» и выбираем его
            driver.find_element(By.XPATH, "//span[text()='Зарегистрировать в РЭМД']").click()
        except Exception:
            # Если не можем найти очередную запись, то считаем что список пуст и выходим из модуля
            break
        # Инициализируем переменную для прерывания цикла проверки окончания отправки в РЭМД очередной записи
        bool_1 = True
        # Начинаем цикл проверки
        while bool_1:
            # Ждем 1 секунду
            sleep(1)
            try:
                # Пытаемся найти на форме кнопку «Ок»
                driver.find_element(By.XPATH, "//div[text()='Ок']")
                # Пытаемся нажать кнопку
                driver.find_element(By.CLASS_NAME, "btn_caption").click()
                # Ждем 2 секунды
                sleep(2)
                # Если все прошло успешно, считаем, что документ отправился и выходим из цикла
                bool_1 = False
            except Exception:
                # Если возникли ошибки, считаем, что документ все еще отправляется и продолжаем цикл проверки
                pass

    # Находим кнопку выхода и нажимаем ее
    driver.find_element(By.CLASS_NAME, "Exit").click()
    # Ждем 4 секунды
    sleep(4)
    # Закрываем экземпляр драйвера Google Chrome
    driver.close()
