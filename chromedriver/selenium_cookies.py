from selenium import webdriver
from selenium.webdriver.chrome.service import Service # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
from fake_useragent import UserAgent
import time
from selenium.webdriver.common.by import By
from auth_data import vk_password, vk_phone # создал файлик с паролем и тел
from selenium.webdriver.common.keys import Keys # импортируем для иммитации нажатия на кнопки
import pickle # для сохранения кукис

useragent = UserAgent(verify_ssl=False)

s = Service("/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/chromedriver") # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object.
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36") # verify_ssl=False помогла настроить работу пакета fake-useragent и зафиксила ошибку
options.add_argument('--disable-blink-features=AutomationControlled') # отключаем режим детекции вебдрайвера, сайт проверки "https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html"

url = "https://www.avito.ru/"
driver = webdriver.Chrome(service=s, options=options) # здесь в service удаляем прямой путь к драйверу и указываем переменную s

for i in range(10):
    try:
        # driver.get("https://vk.com/")
        # time.sleep(2)
        # email_input = driver.find_element(By.XPATH, '//*[@id="index_login"]/div/form/button[1]').click() # поиск по XPath кнопки войти (иногда перебрасывает на страницу главную где нельзя сразу вввести логин и пароль)
        # time.sleep(3)
        # email_input_page2 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/form/div[1]/section/div/div/div/input')
        # email_input_page2.send_keys(vk_phone)
        # time.sleep(3)
        # buttom_enter = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/form/div[2]/div[1]/button/div').click()
        # time.sleep(3)
        # buttom_enter2 = driver.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/form/div[1]/div[3]/div[2]/div[1]/div/input')
        # buttom_enter2.send_keys(vk_password)
        # time.sleep(3)
        # buttom_enter2.send_keys(Keys.ENTER) # имитируем нажатие на enter
        # time.sleep(3)
        #
        # pickle.dump(driver.get_cookies(), open(f'{vk_phone}_cookies', 'wb')) # сохраняем кукис

        driver.get("https://vk.com/")
        time.sleep(5)
        # отправляем куки
        for cookie in pickle.load(open(f"{vk_phone}_cookies", "rb")):
            driver.add_cookie(cookie)
        time.sleep(5)
        driver.refresh()
        time.sleep(10)


    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

