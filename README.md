## Копирование проекта на сервер

`scp -r local_path_project user_name_server@ip_server:server_path_project`


**Пример**

`scp -r /home/user/Pyth/djng-test-ex user@192.168.56.13:~/`

> Он спросит про fingerprint - нажать "y"

## Зайти на сервер (без ssh ключа)

`ssh user_name_server@ip_server`

> Он спросит про fingerprint - нажать "y"

> Ввести пароль 


## Зайти на сервер (с ssh ключом)
1. <span id="step1"></span>`ssh-keygen -f path/key` (можно просто `ssh-keygen` без параметров)

2. Везде нажимать на `enter`

3. `ssh-copy-id -i path/key.pub user_name_server@ip_server`
    > Он спросит про fingerprint - нажать "y"
    
    > (можно без -i если не указывали путь в [1 пункте](#step1))

4. `ssh user_name_server@ip_server`

## Настройка и запуск проекта на сервере

1. Добавление `localhost` и IP-адреса сервера в `settings.py` в параметр `ALLOWED_HOSTS`:
   ```python
   ALLOWED_HOSTS = ['localhost']
   ```

2. Создание и активация виртуального окружения:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Установка зависимостей:
   ```bash
   pip install -r reuirements.txt
   ```

4. Переход в папку с проектом (где находится `manage.py`) и применение миграций:
   ```bash
   cd название_папки_главного_приложения
   python manage.py migrate
   ```

5. Запуск сервера разработки:
   ```bash
   python manage.py runserver 0.0.0.0:port
   ```

6. Открыть в браузере
`http://localhost:port`
Пример `http://localhost:8000`