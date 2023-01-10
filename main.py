import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from loguru import logger

import db
from config import PATH_TO_CHROME_DRIVER, AVITO_URL_APPARTMENTS, USER_AGENT


logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")

# настройка браузера и драйвера
useragent = UserAgent(verify_ssl=False)
s = Service(PATH_TO_CHROME_DRIVER)  # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object.
options = webdriver.ChromeOptions()
options.add_argument(USER_AGENT)  # verify_ssl=False помогла настроить работу пакета fake-useragent и зафиксила ошибку
options.add_argument('--disable-blink-features=AutomationControlled')  # отключаем режим детекции вебдрайвера, сайт проверки "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"
options.add_argument("--headless")  # фоновый режим работы браузера. Альтернатива: options.headless = True
driver = webdriver.Chrome(service=s, options=options)  # здесь в service удаляем прямой путь к драйверу и указываем переменную s

db.check_db_exist()


def main_func(n):
    """Основная функция. Переходим с общей страницы объявлений на конкретное, парсим и сохраняем инфу в БД, закрываем окно, переходим на следующее"""
    count = 1
    while count < n:
        logger.debug(count)
        items = _find_ads_from_page(count)
        try:
            number_lot = 1
            for i in range(len(items)):
                this_item = items[i]
                _click_and_get_all_info(this_item, number_lot)
                _inserts_received_data_into_db(number_lot)
                number_lot += 1
        except Exception as ex:
            print("Error while parsing...", ex)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.implicitly_wait(30)
        finally:
            count += 1


def _find_ads_from_page(count):
    """Cобираем список объявлений со страницы"""
    url = AVITO_URL_APPARTMENTS + str(count)
    driver.get(url)
    driver.implicitly_wait(10)  # этот метод используем вместо time.sleep(), так как он ждет максимум секунд которые в него передаем, но если получится выполнить быстрее, то сделает это
    items = driver.find_elements(By.XPATH, "//div[@data-marker='item-photo']")
    return items


def _get_data_from_ad():
    """Собираем необходимые данные из объявления"""
    lot_name = _find_lot_name()
    price = _find_lot_price()
    url = _get_lot_url()
    return tuple((lot_name, price, url))


def _find_lot_name():
    """ Парсим название лота"""
    lot_name = driver.find_element(By.XPATH, "//span[@class='title-info-title-text']").text
    driver.implicitly_wait(10)
    return lot_name


def _find_lot_price():
    """ Парсим цену лота"""
    price = driver.find_element(By.XPATH,
                                "//span[@class='js-item-price style-item-price-text-_w822 text-text-LurtD text-size-xxl-UPhmI']").text
    driver.implicitly_wait(10)
    return price


def _get_lot_url():
    """Забираем URL лота"""
    url = driver.current_url
    return url


def _inserts_received_data_into_db(number_lot):
    """Вставляем полученные данные в табличку (1. Название лота | 2.Цена | 3. Ссылка на объявление | 4. Скриншот"""
    cursor = db.get_cursor()
    file = open(
        f'./screenshots/{number_lot}.png',
        'rb')
    name = file.read()  # можно еще вот так pymysql.Binary(и сюда уже вводить file.read())
    insert_data = (
        "INSERT INTO avito_lots (lot_name, price, url, screen) VALUES (%s, %s, %s, %s)")
    lot_name, price, url = _get_data_from_ad()
    cursor.execute(insert_data, (lot_name, price, url, name))
    driver.close()  # закрываем окно
    driver.switch_to.window(driver.window_handles[0])  # переходим к главному окну


def _click_and_swith_to_window(this_item):
    """Клик и переход к окну объявления"""
    this_item.click()
    driver.switch_to.window(driver.window_handles[1])  # перемещаемся на эту вкладку. Обязательно(!)
    driver.implicitly_wait(10)


def _make_and_save_screen(number_lot):
    """Делаем скрин лота и сохраняем его"""
    driver.execute_script(
        "document.body.style.zoom='40%'")  # делаем меньше масштаб окна, чтобы все влезло на скрин
    driver.get_screenshot_as_file(
        f'screenshots/{number_lot}.png')  # сохраняем скрин по порядковому номеру в папку /screenshots
    driver.implicitly_wait(15)


def _click_and_get_all_info(this_item, number_lot):
    """Функция срабатывающая при клике на объявление. Собирает данные, сохраняет скрин, логирует"""
    _click_and_swith_to_window(this_item)
    lot_name, price, url = _get_data_from_ad()
    _make_and_save_screen(number_lot)
    logger.info(f"Название: {lot_name}, Цена: {price} рублей, URL: {url}")
    driver.implicitly_wait(20)


def _create_folder_screens():
    """Cоздаем папку для скриншотов лотов"""
    try:
        os.mkdir('./screenshots')
    except Exception:
        logger.info("Папка уже создана")


_create_folder_screens()
main_func(10)

driver.close()
driver.quit()

"""
Вот тут как используя пандас скачать табличку в exel

https://ru.stackoverflow.com/questions/917354/%D0%92%D1%8B%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0-%D0%B8%D0%B7-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0-db-%D0%B2-excel
"""

"""
Что сделать осталось:

1) при создании таблицы- поле id сделать auto increment


2) Выкачать получившуюся табличку в exel
3) мб ее скинуть куда-то (мб в телеграмм)

** картинки перезаписываются после
"""
