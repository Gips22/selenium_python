"""Подключение, проверка и инициализация БД в этом модуле. Также возвращаем курсор тут для доступа из других модулей"""
from loguru import logger
import psycopg2

from config import PASSWORD, DB_NAME

logger.add("debug.log", format="{time} {level} {message}", level="DEBUG", rotation="10 MB")

try:
    connection = psycopg2.connect(
        host="127.0.0.1",
        user="postgres",
        password=PASSWORD,
        database=DB_NAME
    )
    logger.debug("connected successfully")

except Exception as ex:
    logger.error("Connection refused...", ex)

connection.autocommit = True
cursor = connection.cursor()


def get_cursor():
    return cursor


def _init_db():
    """Инициализируем БД"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
        cursor.execute(sql)


def check_db_exist():
    """Проверяет инициализирована ли БД, если нет - инициализирует"""
    try:
        cursor.execute("select * from avito_lots;")
    except Exception:
        logger.info("Инициализирую таблицу avito_lots")
        _init_db()
    else:
        logger.debug("База уже создана")


if __name__ == "__main__":
    check_db_exist()
