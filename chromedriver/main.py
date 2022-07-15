from selenium import webdriver
from selenium.webdriver.chrome.service import Service # чтобы не вылезала ошибка "Executable path has been deprecated please pass in a Service object"
import time
import datetime

s = Service("/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/chromedriver") # создаем переменную, чтобы не вылезала ошибка Executable path has been deprecated please pass in a Service object
options = webdriver.ChromeOptions()
options.add_argument("user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0")
options.add_argument("--disable-blink-features=AutomationControlled")

url = "https://www.instagram.com/"
driver = webdriver.Chrome(service=s) # здесь удаляем прямой путь к драйверу и указываем переменную s

try:
    driver.get(url=url)
    time.sleep(5)

except Exception as ex:
    print(ex)
finally:
    driver.close()
    driver.quit()