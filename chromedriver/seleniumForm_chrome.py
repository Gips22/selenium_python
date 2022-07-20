from selenium import webdriver
from selenium.webdriver.chrome.service import Service # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
from fake_useragent import UserAgent
import time

from selenium.webdriver.common.by import By

from auth_data import vk_password # создал файлик с паролем

useragent = UserAgent(verify_ssl=False)

s = Service("/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/chromedriver") # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object.
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36") # verify_ssl=False помогла настроить работу пакета fake-useragent и зафиксила ошибку
options.add_argument('--disable-blink-features=AutomationControlled') # отключаем режим детекции вебдрайвера, сайт проверки "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"
# set proxy
# добавляем новый аргумент в объект опций
# options.add_argument("--proxy-server=138.128.91.65:8000")


url = "https://www.avito.ru/"
driver = webdriver.Chrome(service=s, options=options) # здесь в service удаляем прямой путь к драйверу и указываем переменную s

for i in range(10):
    try:
        driver.get("https://vk.com/")
        time.sleep(4)

        # email_input = driver.find_element('id', "index_email") # находим поле ввода по id
        # email_input.clear() # очищаем поле на всякий случай
        # email_input.send_keys('79154305267')
        # time.sleep(3)
        # pass_input = driver.find_element('id', "index_pass")
        # pass_input.send_keys(vk_password) # выгружаю пароль из файлика
        # time.sleep(2)
        # login_buttom = driver.find_element('id', 'index_login_button').click() # кликаем по кнопке войти
        # time.sleep(1000)
        email_input = driver.find_element(By.XPATH, '//*[@id="index_login"]/div/form/button[1]').click() # поиск по XPath кнопки войти (иногда перебрасывает на страницу главную где нельзя сразу вввести логин и пароль)

        time.sleep(7)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

