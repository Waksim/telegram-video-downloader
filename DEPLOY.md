# Инструкция по деплою

## 1. Загрузка на GitHub

```bash
# Удалить лишние .md файлы из git
git rm --cached DEPLOYMENT.md PUBLISH.md QUICK_START.md START_HERE.md INSTALL_AS_ROOT.md ROOT_INSTALL_COMMANDS.txt

# Добавить все изменения
git add .

# Создать коммит
git commit -m "Add Google Drive upload feature with optimized memory usage"

# Отправить на GitHub
git push origin main
```

## 2. Передача credentials на сервер

```bash
# Скопировать token.json на сервер
scp /Users/mk/PycharmProjects/download_interview/token.json root@89.110.119.205:~/

# Скопировать credentials.json на сервер
scp /Users/mk/PycharmProjects/download_interview/credentials.json root@89.110.119.205:~/
```

## 3. Деплой на сервер

```bash
# Подключиться к серверу
ssh root@89.110.119.205

# На сервере:
# Установить git, python3 и pip (если еще не установлены)
apt update
apt install -y git python3 python3-pip python3-venv

# Клонировать репозиторий
cd ~
git clone <URL_ВАШЕГО_РЕПОЗИТОРИЯ> download_interview
cd download_interview

# Переместить credentials в папку проекта
mv ~/token.json .
mv ~/credentials.json .

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать .env файл
nano .env
# Добавить туда:
# API_ID=ваш_api_id
# API_HASH=ваш_api_hash
# SESSION_STRING=ваша_session_string

# Запустить скрипт
python download_videos.py
```

## 4. Запуск в фоне (опционально)

```bash
# Установить screen для фоновой работы
apt install -y screen

# Создать новую screen-сессию
screen -S telegram_downloader

# Запустить скрипт
python download_videos.py

# Отключиться от screen (Ctrl+A, затем D)
# Вернуться: screen -r telegram_downloader
```
