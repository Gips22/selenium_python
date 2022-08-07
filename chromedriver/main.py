from selenium import webdriver
from selenium.webdriver.chrome.service import Service # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
from fake_useragent import UserAgent
import time

useragent = UserAgent(verify_ssl=False)

s = Service("/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/chromedriver") # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object.
options = webdriver.ChromeOptions()
options.add_argument(f"user-agent={useragent.random}") # verify_ssl=False помогла настроить работу пакета fake-useragent и зафиксила ошибку

# set proxy
# добавляем новый аргумент в объект опций
# options.add_argument("--proxy-server=138.128.91.65:8000")


url = "https://www.avito.ru/"
driver = webdriver.Chrome(service=s, options=options) # здесь в service удаляем прямой путь к драйверу и указываем переменную s

try:
    driver.get("https://www.whatismybrowser.com/detect/what-is-my-user-agent/")
    time.sleep(2)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()