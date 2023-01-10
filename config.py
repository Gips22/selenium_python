"""Все приватные переменные заданы тут. При подключении к проекту - создать файл .env,
внести его в .gitignore и задать там переменные окружения"""
import os

from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")

PATH_TO_CHROME_DRIVER = os.getenv("PATH_TO_CHROME_DRIVER")
AVITO_URL_APPARTMENTS = os.getenv("AVITO_URL_APPARTMENTS")

USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.105 YaBrowser/21.3.3.230 Yowser/2.5 Safari/537.36"