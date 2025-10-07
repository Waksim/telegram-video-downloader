# 🚀 Инструкция по деплою на Ubuntu сервер

## Быстрая установка (автоматическая)

```bash
# Скачать и запустить скрипт установки
wget https://raw.githubusercontent.com/YOUR_USERNAME/download_interview/main/install.sh
chmod +x install.sh
./install.sh
```

## Ручная установка

### 1. Подготовка сервера

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Python 3.10+ и pip
sudo apt install python3 python3-pip python3-venv git -y

# Проверка версии Python (должна быть 3.8+)
python3 --version
```

### 2. Клонирование проекта

```bash
# Клонирование репозитория
cd ~
git clone https://github.com/YOUR_USERNAME/download_interview.git
cd download_interview
```

### 3. Настройка окружения

```bash
# Создание виртуального окружения
python3 -m venv venv

# Активация виртуального окружения
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
```

### 4. Конфигурация

```bash
# Создание файла .env
cp .env.example .env

# Редактирование .env с вашими данными
nano .env
```

Заполните следующие поля:
```
API_ID=ваш_api_id
API_HASH=ваш_api_hash
SESSION_STRING=ваша_session_строка
```

Сохраните файл: `Ctrl+O`, `Enter`, `Ctrl+X`

### 5. Настройка параметров скачивания

Откройте `download_videos.py` и настройте:

```python
CHAT_ID = -1002406265529  # ID вашей супергруппы
TOPIC_ID = 4               # ID топика
DOWNLOAD_DIR = Path('downloaded_videos')  # Папка для видео
```

```bash
nano download_videos.py
```

### 6. Тестовый запуск

```bash
# Активируйте виртуальное окружение если не активировано
source venv/bin/activate

# Запуск скрипта
python download_videos.py
```

## Автоматический запуск через systemd

### 1. Создание systemd service

```bash
# Создание service файла
sudo nano /etc/systemd/system/telegram-downloader.service
```

Вставьте содержимое:

```ini
[Unit]
Description=Telegram Video Downloader
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/download_interview
Environment="PATH=/home/YOUR_USERNAME/download_interview/venv/bin"
ExecStart=/home/YOUR_USERNAME/download_interview/venv/bin/python download_videos.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

⚠️ **Важно:** Замените `YOUR_USERNAME` на ваше имя пользователя Ubuntu!

### 2. Запуск и управление сервисом

```bash
# Перезагрузка конфигурации systemd
sudo systemctl daemon-reload

# Включение автозапуска при старте системы
sudo systemctl enable telegram-downloader

# Запуск сервиса
sudo systemctl start telegram-downloader

# Проверка статуса
sudo systemctl status telegram-downloader

# Просмотр логов
sudo journalctl -u telegram-downloader -f

# Остановка сервиса
sudo systemctl stop telegram-downloader

# Перезапуск сервиса
sudo systemctl restart telegram-downloader
```

## Запуск в screen/tmux (альтернатива)

### Использование screen

```bash
# Установка screen
sudo apt install screen -y

# Создание новой сессии
screen -S downloader

# Активация виртуального окружения и запуск
cd ~/download_interview
source venv/bin/activate
python download_videos.py

# Отключение от сессии (скрипт продолжит работать)
# Нажмите: Ctrl+A, затем D

# Подключение обратно к сессии
screen -r downloader

# Список всех сессий
screen -ls
```

### Использование tmux

```bash
# Установка tmux
sudo apt install tmux -y

# Создание новой сессии
tmux new -s downloader

# Активация виртуального окружения и запуск
cd ~/download_interview
source venv/bin/activate
python download_videos.py

# Отключение от сессии (скрипт продолжит работать)
# Нажмите: Ctrl+B, затем D

# Подключение обратно к сессии
tmux attach -t downloader

# Список всех сессий
tmux ls
```

## Настройка расписания (cron)

Для периодического запуска скрипта:

```bash
# Открыть crontab
crontab -e

# Добавить строку для ежедневного запуска в 3:00
0 3 * * * cd /home/YOUR_USERNAME/download_interview && /home/YOUR_USERNAME/download_interview/venv/bin/python download_videos.py >> /home/YOUR_USERNAME/download_interview/cron.log 2>&1
```

## Полезные команды

```bash
# Проверка места на диске
df -h

# Размер папки со скачанными видео
du -sh ~/download_interview/downloaded_videos

# Количество скачанных видео
ls -1 ~/download_interview/downloaded_videos | wc -l

# Просмотр прогресса
cat ~/download_interview/download_progress.json

# Очистка скачанных видео (будьте осторожны!)
rm -rf ~/download_interview/downloaded_videos/*
rm ~/download_interview/download_progress.json
```

## Обновление проекта

```bash
cd ~/download_interview

# Остановка сервиса (если используется)
sudo systemctl stop telegram-downloader

# Обновление кода
git pull origin main

# Обновление зависимостей
source venv/bin/activate
pip install -r requirements.txt --upgrade

# Запуск сервиса (если используется)
sudo systemctl start telegram-downloader
```

## Безопасность

### Ограничение доступа к .env файлу

```bash
# Установка прав доступа только для владельца
chmod 600 ~/.env
chmod 600 ~/download_interview/.env
```

### Настройка firewall (опционально)

```bash
# Установка ufw
sudo apt install ufw -y

# Базовые правила
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Разрешить SSH
sudo ufw allow ssh

# Включить firewall
sudo ufw enable

# Проверить статус
sudo ufw status
```

## Решение проблем

### Ошибка "Permission denied"
```bash
chmod +x download_videos.py
```

### Ошибка "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Скрипт не видит .env файл
```bash
# Убедитесь, что .env находится в той же папке что и скрипт
ls -la ~/download_interview/.env

# Проверьте права доступа
chmod 600 ~/download_interview/.env
```

### Недостаточно места на диске
```bash
# Проверка свободного места
df -h

# Очистка старых логов
sudo journalctl --vacuum-time=7d

# Удаление неиспользуемых пакетов
sudo apt autoremove -y
sudo apt clean
```

## Мониторинг

### Проверка работы скрипта

```bash
# Статус systemd service
sudo systemctl status telegram-downloader

# Последние 50 строк логов
sudo journalctl -u telegram-downloader -n 50

# Живые логи
sudo journalctl -u telegram-downloader -f

# Проверка процесса
ps aux | grep download_videos
```

### Настройка уведомлений (опционально)

Можно добавить отправку уведомлений в Telegram при завершении скачивания, редактируя `download_videos.py`.

## Бэкап

```bash
# Создание бэкапа прогресса и конфигурации
tar -czf backup_$(date +%Y%m%d).tar.gz \
  ~/download_interview/.env \
  ~/download_interview/download_progress.json \
  ~/download_interview/downloaded_videos

# Восстановление из бэкапа
tar -xzf backup_20240101.tar.gz -C ~/
```
