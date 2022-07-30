from selenium import webdriver
from selenium.webdriver.chrome.service import Service # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys # импортируем для иммитации нажатия на кнопки

useragent = UserAgent(verify_ssl=False)
s = Service("/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/chromedriver") # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object.
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36") # verify_ssl=False помогла настроить работу пакета fake-useragent и зафиксила ошибку
options.add_argument('--disable-blink-features=AutomationControlled') # отключаем режим детекции вебдрайвера, сайт проверки "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"
url = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok/3-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUklk?cd=1&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgUklkBRcaaDBp7ImZyb20iOjUwMDAwLCJ0byI6MTAwMDAwfQ&footWalkingMetro=15&p="
driver = webdriver.Chrome(service=s, options=options) # здесь в service удаляем прямой путь к драйверу и указываем переменную s


try:
    count = 1
    while count < 10:
        print(count)
        url = "https://www.avito.ru/moskva/kvartiry/sdam/na_dlitelnyy_srok/3-komnatnye-ASgBAQICAkSSA8gQ8AeQUgFAzAgUklk?cd=1&f=ASgBAQECAkSSA8gQ8AeQUgFAzAgUklkBRcaaDBp7ImZyb20iOjUwMDAwLCJ0byI6MTAwMDAwfQ&footWalkingMetro=15&p=" + str(count)
        driver.get(url)
        time.sleep(5)
        items = driver.find_elements(By.XPATH, "//div[@data-marker='item-photo']") # собираем список объявлений со страницы
        # переходим по объявлениям на странице (открытым вкладкам и парсим инфу)
        for i in range(len(items)):
            items[i].click()
            driver.switch_to.window(driver.window_handles[1]) # перемещаемся на эту вкладку. Обязательно(!)
            time.sleep(5)
            title = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/div[1]/div[1]/div/div[1]/h1/span').text
            time.sleep(3)
            price = driver.find_element(By.XPATH, '/html/body/div[3]/div[1]/div/div/div[2]/div[2]/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div[1]/div/span/span/span[1]').text
            time.sleep(6)
            print(f"Название: {title}, Цена: {price} рублей.")
            time.sleep(3)
            driver.close() # закрываем окно
            driver.switch_to.window(driver.window_handles[0]) # переходим к главному окну
            time.sleep(10)


        count += 1



except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()

