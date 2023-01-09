from selenium import webdriver
from selenium.webdriver.chrome.service import Service  # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import pymysql
from config import host, user, password, db_name
import os  # модуль для создания папки под скриншоты лотов

# настройка браузера и драйвера
useragent = UserAgent(verify_ssl=False)
s = Service("/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/chromedriver")  # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object.
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36")  # verify_ssl=False помогла настроить работу пакета fake-useragent и зафиксила ошибку
options.add_argument('--disable-blink-features=AutomationControlled')  # отключаем режим детекции вебдрайвера, сайт проверки "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"
# options.add_argument("--headless")  # фоновый режим работы браузера. Альтернатива: options.headless = True
driver = webdriver.Chrome(service=s,
                          options=options)  # здесь в service удаляем прямой путь к драйверу и указываем переменную s

# Устанавливаем соединение с БД
try:
    connection = pymysql.connect(
        host=host,
        port=8889,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print("Successfully connected...")
    print("#" * 20)
    cursor = connection.cursor()

    # Создаем табличку в нашей БД для данных с парсинга
    cursor.execute('CREATE TABLE avito_lots(id INT AUTO_INCREMENT,'
                   ' lot_name VARCHAR(250),'
                   ' price VARCHAR(250),'
                   ' url VARCHAR(250),'
                   ' screen LONGBLOB,'
                   ' PRIMARY KEY(id));')

except Exception as ex:
    print("Connection refused...")
    print(ex)

try:
    count = 1
    os.mkdir('./screenshots')  # создаем папку для скриншотов лотов

    while count < 10:
        print(count)
        url = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok/3-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUklk?cd=1&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgUklkBRcaaDBp7ImZyb20iOjUwMDAwLCJ0byI6MTAwMDAwfQ&footWalkingMetro=15&p=" + str(
            count)
        driver.get(url)
        driver.implicitly_wait(
            30)  # этот метод используем вместо time.sleep(), так как он ждет максимум секунд которые в него передаем, но если получится выполнить быстрее, то сделает это
        items = driver.find_elements(By.XPATH,
                                     "//div[@data-marker='item-photo']")  # собираем список объявлений со страницы
        # переходим по объявлениям на странице (открытым вкладкам и парсим инфу)
        try:
            number_lot = 1
            for i in range(len(items)):
                items[i].click()
                driver.switch_to.window(driver.window_handles[1])  # перемещаемся на эту вкладку. Обязательно(!)
                driver.implicitly_wait(30)
                try:
                    # парсим название лота
                    lot_name = driver.find_element(By.XPATH,
                                                   '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/h1/span').text
                    driver.implicitly_wait(30)

                    # парсим цену
                    price = driver.find_element(By.XPATH,
                                                '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div[1]/div/span/span/span[1]').text
                    driver.implicitly_wait(30)

                    # забираем URL лота
                    url = driver.current_url

                    # делаем скрин лота
                    driver.execute_script(
                        "document.body.style.zoom='40%'")  # делаем меньше масштаб окна, чтобы все влезло на скрин
                    driver.get_screenshot_as_file(
                        f'screenshots/{number_lot}.png')  # сохраняем скрин по порядковому номеру в папку /screenshots
                    driver.implicitly_wait(15)

                    print(f"Название: {lot_name}, Цена: {price} рублей, URL: {url}")

                    driver.close()  # закрываем окно
                    driver.switch_to.window(driver.window_handles[0])  # переходим к главному окну
                    driver.implicitly_wait(20)


                # Обработка исключений во время парсинга странички конкретного лота
                except Exception as ex:
                    print('Ошибка в объявлении', ex)
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    driver.implicitly_wait(30)

                # Работа с БД: вставляем полученные данные в табличку (1. Название лота | 2.Цена | 3. Ссылка на объявление | 4. Скриншот (вставим когда соберем все скриншоты))
                with connection.cursor() as cursor:
                    file = open(
                        f'/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/avito_selenium/screenshots/{number_lot}.png',
                        'rb')
                    name = file.read()  # можно еще вот так pymysql.Binary(и сюда уже вводить file.read())
                    insert_data = (
                                "INSERT INTO `avito_lots` (lot_name, price, url, screen) VALUES (%s, %s, %s, %s)")
                    cursor.execute(insert_data, (lot_name, price, url, name))
                    connection.commit()
                number_lot += 1



        except Exception as ex:
            print("Error while parsing...", ex)
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            driver.implicitly_wait(30)

        count += 1
    connection.close()

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()


"""
Вот тут как используя пандас скачать табличку в exel

https://ru.stackoverflow.com/questions/917354/%D0%92%D1%8B%D0%B3%D1%80%D1%83%D0%B7%D0%BA%D0%B0-%D0%B8%D0%B7-%D1%84%D0%B0%D0%B9%D0%BB%D0%B0-db-%D0%B2-excel
"""

"""
Что сделать осталось:
1) разобраться с переносом скрина в БД. Что-то толи с форматированием то ли еще с чем.
2) Выкачать получившуюся табличку в exel
3) мб ее скинуть куда-то (мб в телеграмм)
"""

"""
Что сделал: 1. Сделал подключение к БД в основном файле программы. 2.Сделал автоматическое создание папки для скриншотов 3. Сделал рабочую выгрузку в БД всех данных кроме скриншотов
"""