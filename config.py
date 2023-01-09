"""Все приватные переменные заданы тут. При подключении к проекту - создать файл .env,
внести его в .gitignore и задать там переменные окружения"""
import os

from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("PASSWORD")
DB_NAME = os.getenv("DB_NAME")

PATH_TO_CHROME_DRIVER = os.getenv("PATH_TO_CHROME_DRIVER")
AVITO_URL_APPARTMENTS = os.getenv("AVITO_URL_APPARTMENTS")