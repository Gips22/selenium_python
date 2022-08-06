from selenium import webdriver
from selenium.webdriver.chrome.service import Service # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
import pymysql
from config import host, user, password, db_name
from selenium.webdriver.common.keys import Keys # импортируем для иммитации нажатия на кнопки

# настройка браузера и драйвера
useragent = UserAgent(verify_ssl=False)
s = Service("/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/chromedriver") # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object.
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36") # verify_ssl=False помогла настроить работу пакета fake-useragent и зафиксила ошибку
options.add_argument('--disable-blink-features=AutomationControlled') # отключаем режим детекции вебдрайвера, сайт проверки "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"
# options.add_argument("--headless") # фоновый режим работы браузера. Альтернатива: options.headless = True
driver = webdriver.Chrome(service=s, options=options) # здесь в service удаляем прямой путь к драйверу и указываем переменную s



try:
    count = 1
    while count < 10:
        print(count)
        url = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok/3-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUklk?cd=1&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgUklkBRcaaDBp7ImZyb20iOjUwMDAwLCJ0byI6MTAwMDAwfQ&footWalkingMetro=15&p=" + str(count)
        driver.get(url)
        driver.implicitly_wait(30) # этот метод используем вместо time.sleep(), так как он ждет максимум секунд которые в него передаем, но если получится выполнить быстрее, то сделает это
        items = driver.find_elements(By.XPATH, "//div[@data-marker='item-photo']") # собираем список объявлений со страницы
        # переходим по объявлениям на странице (открытым вкладкам и парсим инфу)
        for i in range(len(items)):
            print("Новая страница")
            items[i].click()
            driver.switch_to.window(driver.window_handles[1]) # перемещаемся на эту вкладку. Обязательно(!)
            driver.implicitly_wait(30)
            title = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/h1/span').text
            driver.implicitly_wait(30)
            price = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div[1]/div/span/span/span[1]').text
            driver.implicitly_wait(30)
            print(f"Название: {title}, Цена: {price} рублей.")
            driver.implicitly_wait(30)
            driver.close() # закрываем окно
            driver.switch_to.window(driver.window_handles[0]) # переходим к главному окну
            driver.implicitly_wait(30)
            try:
                connection = pymysql.connect(
                    host=host,
                    port=8889,
                    user=user,
                    password=password,
                    database=db_name,
                    cursorclass=pymysql.cursors.DictCursor
                )
                print("successfully connected...")
                print("#" * 20)

               # insert data
                try:
                    with connection.cursor() as cursor:
                        insert_data = ("INSERT INTO `users` (name) VALUES ('%(price)s')" % {'price': price})
                        cursor.execute(insert_data)
                        connection.commit()


                finally:
                    connection.close()

            except Exception as ex:
                print("Connection refused...")
                print(ex)


        count += 1



except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

