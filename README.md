# Курсовая работа по Визуальному программированию
Тут будет небольшое пояснение по запуску и тд и тп.

## Установка 
- `pyhton -m venv <название_окружения>`
- `source ./<название_окружения>/bin/activate`
- `pip install -r requirements.txt`

## Создание БД
По условию задания надо было использовать sqlite3
- `sqlite3 DataBase.db`
- `CREATE TABLE users (ID INTEGER PRIMARY KEY, login TEXT NOT NULL, password_hash TEXT NOT NULL, last_file TEXT);`
- `INSERT INTO users (1, "admin", "password hash");`

В курсовой используется MD5 хэширование, соответственно прогоните пароль через MD5

## Запуск
Для запуска используйте команду `python app.py`
