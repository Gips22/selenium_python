import pymysql
from config import host, user, password, db_name

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
    # cursor.execute('CREATE TABLE t1(id INT AUTO_INCREMENT,'
    #                ' screen BLOB,'
    #                ' PRIMARY KEY(id));')

except Exception as ex:
    print("Connection refused...")
    print(ex)

try:
    with open('/Users/andreynaletov/Desktop/PROJECTS/Projects/selenium_python/chromedriver/avito_selenium/screenshots/1.png', 'rb') as file:
        name = file.read() # можно еще вот так pymysql.Binary(и сюда уже вводить file.read())
        insert_data = ("INSERT INTO `t1` (screen) VALUES (%s)")
        cursor.execute(insert_data, name)
        connection.commit()
except Exception as ex:
    print('Ошибка скрина', ex)

