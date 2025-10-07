# ⚡ Быстрый старт

## 📤 Публикация на GitHub (Одной командой)

```bash
# 1. Перейдите на https://github.com/new и создайте репозиторий
#    Название: telegram-video-downloader
#    НЕ инициализируйте с README!

# 2. Выполните эти команды (ЗАМЕНИТЕ YOUR_USERNAME на ваш GitHub username!):

cd /Users/mk/PycharmProjects/download_interview

git init
git add .
git commit -m "Initial commit: Telegram video downloader

- Main download script with resume capability
- Ubuntu installation scripts
- Systemd service configuration
- Complete deployment documentation"

git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/telegram-video-downloader.git
git push -u origin main
```

**✅ Готово!** Ваш проект опубликован.

---

## 🚀 Деплой на чистый Ubuntu сервер

### Вариант 1: Автоматическая установка

```bash
# На вашем Ubuntu сервере выполните:

wget https://raw.githubusercontent.com/YOUR_USERNAME/telegram-video-downloader/main/install.sh
chmod +x install.sh
./install.sh
```

Скрипт сам установит всё необходимое и запросит ваши API данные.

### Вариант 2: Ручная установка (полный контроль)

```bash
# 1. Подготовка сервера
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip python3-venv git -y

# 2. Клонирование проекта
cd ~
git clone https://github.com/YOUR_USERNAME/telegram-video-downloader.git
cd telegram-video-downloader

# 3. Установка зависимостей
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Настройка .env
cp .env.example .env
nano .env  # Вставьте ваши API_ID, API_HASH, SESSION_STRING

# 5. Запуск
python download_videos.py
```

---

## 🔧 Настройка автозапуска через systemd

```bash
# На Ubuntu сервере:

# 1. Создайте service файл (ЗАМЕНИТЕ mk на ваше имя пользователя!)
sudo nano /etc/systemd/system/telegram-downloader.service

# Вставьте (замените mk на ваш username):
[Unit]
Description=Telegram Video Downloader
After=network.target

[Service]
Type=simple
User=mk
WorkingDirectory=/home/mk/telegram-video-downloader
Environment="PATH=/home/mk/telegram-video-downloader/venv/bin"
ExecStart=/home/mk/telegram-video-downloader/venv/bin/python download_videos.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target

# 2. Активируйте сервис
sudo systemctl daemon-reload
sudo systemctl enable telegram-downloader
sudo systemctl start telegram-downloader

# 3. Проверьте статус
sudo systemctl status telegram-downloader

# 4. Смотрите логи
sudo journalctl -u telegram-downloader -f
```

---

## 📋 Полезные команды

### Git команды

```bash
# Обновить код на GitHub
git add .
git commit -m "Описание изменений"
git push

# Проверить статус
git status

# Посмотреть историю
git log --oneline
```

### Управление на сервере

```bash
# Systemd
sudo systemctl start telegram-downloader    # Запуск
sudo systemctl stop telegram-downloader     # Остановка
sudo systemctl restart telegram-downloader  # Перезапуск
sudo systemctl status telegram-downloader   # Статус
sudo journalctl -u telegram-downloader -f   # Логи в реальном времени

# Screen (альтернатива systemd)
screen -S downloader                        # Создать сессию
# Внутри screen: запустите скрипт
# Ctrl+A, затем D - отключиться от screen
screen -r downloader                        # Вернуться к сессии
screen -ls                                  # Список сессий

# Мониторинг
cat download_progress.json                  # Прогресс
ls -1 downloaded_videos | wc -l            # Количество видео
du -sh downloaded_videos                    # Размер папки
df -h                                       # Свободное место
```

---

## 🔐 Безопасность

```bash
# Защита .env файла
chmod 600 .env

# Проверка что .env не в git
git status | grep .env  # Не должен отображаться!

# Если .env случайно добавлен в git:
git rm --cached .env
git commit -m "Remove .env from tracking"
git push
# ЗАТЕМ СМЕНИТЕ ВСЕ КЛЮЧИ API!
```

---

## ❓ Решение проблем

### "Permission denied"
```bash
chmod +x install.sh
chmod +x download_videos.py
```

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "Session not authorized"
```bash
# Проверьте правильность SESSION_STRING в .env
# Сгенерируйте новую сессию если нужно
```

### Недостаточно места
```bash
df -h                          # Проверить место
sudo apt clean                 # Очистить кеш
sudo apt autoremove -y         # Удалить ненужные пакеты
```

---

## 📚 Подробная документация

- **[README.md](README.md)** - Основная документация проекта
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Подробная инструкция по деплою
- **[PUBLISH.md](PUBLISH.md)** - Подробная инструкция по публикации на GitHub

---

## 🎯 Чеклист для деплоя

- [ ] Создал репозиторий на GitHub
- [ ] Запушил код на GitHub
- [ ] Обновил YOUR_USERNAME в README.md и DEPLOYMENT.md
- [ ] Подключился к Ubuntu серверу
- [ ] Запустил install.sh или установил вручную
- [ ] Настроил .env с API данными
- [ ] Настроил CHAT_ID и TOPIC_ID в download_videos.py
- [ ] Запустил тестовое скачивание
- [ ] Настроил systemd service (опционально)
- [ ] Проверил что всё работает
- [ ] Настроил мониторинг

**✅ Всё готово! Видео будут скачиваться автоматически.**
