## Копирование проекта на сервер

`scp -r local_path_project user_name_server@ip_server:server_path_project`

**scp - утилита для копирования. Флаг -r - рекурсивно**
> перед копированием удалить venv, тк scp будет долго копировать

**Пример**

`scp -r /home/user/Pyth/djng-test-ex user@192.168.56.13:~/`

> Он спросит про fingerprint - нажать "yes"

## Зайти на сервер (без ssh ключа)

`ssh user_name_server@ip_server`

> Он спросит про fingerprint - нажать "yes"

> Ввести пароль 


## Зайти на сервер (с ssh ключом)
1. <span id="step1"></span>`ssh-keygen -f path/key` (можно просто `ssh-keygen` без параметров)

2. Везде нажимать на `enter`

3. `ssh-copy-id -i path/key.pub user_name_server@ip_server`
    > Он спросит про fingerprint - нажать "yes"
    
    > (можно без -i если не указывали путь в [1 пункте](#step1))

4. `ssh user_name_server@ip_server`

## Настройка и запуск проекта на сервере

1. Добавление всех ip в список разрешенных хостов `settings.py` в параметр `ALLOWED_HOSTS`:
   ```python
   ALLOWED_HOSTS = ['*']
   ```

2. Создание и активация виртуального окружения:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Если пишет что-то вроде apt install python3-venv:
   ```bash
   sudo apt install python3-venv
   ```

   и повторить 2 пункт

3. Установка зависимостей:
   ```bash
   pip install -r requirements.txt
   ```

4. Запуск сервера разработки:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

5. Открыть в браузере
`http://localhost:port`
Пример `http://localhost:8000` или `http://192.168.1.{...}:8000` 