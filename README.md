# 📥 Telegram Video Downloader

Скрипт для скачивания всех видео из топика Telegram супергруппы с возможностью возобновления процесса.

## ✨ Возможности

- ✅ Скачивание всех видео из указанного топика супергруппы
- ✅ Сохранение прогресса - можно прервать и продолжить позже
- ✅ Автоматический пропуск уже скачанных файлов
- ✅ Информативный вывод с прогрессом скачивания
- ✅ Обработка ошибок и возможность возобновления
- ✅ Готовые скрипты для деплоя на Ubuntu сервер

## 📋 Требования

- Python 3.8+
- Telegram API credentials (API_ID, API_HASH)
- Telegram Session String

## 🚀 Быстрый старт

### Локальная установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/YOUR_USERNAME/download_interview.git
cd download_interview
```

2. Установите зависимости:

1. Установите зависимости:
```bash
pip install -r requirements.txt
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp .env.example .env
```

3. Отредактируйте `.env` и укажите ваши Telegram API данные

4. Настройте параметры в `download_videos.py`:
   - `CHAT_ID` - ID вашей супергруппы
   - `TOPIC_ID` - ID топика
   - `DOWNLOAD_DIR` - папка для сохранения видео

### Деплой на Ubuntu сервер

Автоматическая установка:

```bash
wget https://raw.githubusercontent.com/YOUR_USERNAME/download_interview/main/install.sh
chmod +x install.sh
./install.sh
```

📖 **Подробная инструкция по деплою:** [DEPLOYMENT.md](DEPLOYMENT.md)

## 📖 Использование

Просто запустите скрипт:

```bash
python download_videos.py
```

### Возобновление скачивания

Если процесс был прерван (Ctrl+C или ошибка):
- Прогресс автоматически сохраняется в `download_progress.json`
- Просто запустите скрипт снова - он продолжит с того места, где остановился
- Уже скачанные файлы будут пропущены

### Структура проекта

```
download_interview/
├── download_videos.py      # Основной скрипт
├── requirements.txt        # Зависимости
├── .env                    # Конфигурация (не в git)
├── .env.example           # Пример конфигурации
├── download_progress.json # Файл прогресса (создается автоматически)
└── downloaded_videos/     # Папка со скачанными видео
```

## ⚙️ Конфигурация

### Переменные окружения (.env)

```bash
API_ID=ваш_api_id
API_HASH=ваш_api_hash
SESSION_STRING=ваша_session_строка
```

### Параметры в скрипте

В файле `download_videos.py` настройте:

```python
CHAT_ID = -1002406265529  # ID вашей супергруппы
TOPIC_ID = 4               # ID топика
DOWNLOAD_DIR = Path('downloaded_videos')  # Папка для сохранения
```

## 🔧 Получение Telegram API данных

1. **API_ID и API_HASH:**
   - Перейдите на https://my.telegram.org
   - Войдите в аккаунт
   - Перейдите в "API development tools"
   - Создайте приложение и получите API_ID и API_HASH

2. **SESSION_STRING:**
   - Используйте библиотеку `telethon`
   - Запустите скрипт для генерации session string
   - Сохраните полученную строку

## 🐧 Деплой и автоматизация

Проект включает готовые решения для деплоя:

- **[install.sh](install.sh)** - автоматический установочный скрипт
- **[telegram-downloader.service](telegram-downloader.service)** - systemd service файл
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - подробная инструкция по деплою

### Запуск через systemd

```bash
sudo systemctl start telegram-downloader
sudo systemctl enable telegram-downloader  # Автозапуск при старте системы
sudo systemctl status telegram-downloader   # Проверка статуса
```

### Запуск через screen/tmux

```bash
screen -S downloader
cd ~/download_interview
source venv/bin/activate
python download_videos.py
# Ctrl+A, D для отключения (скрипт продолжит работать)
```

## 📊 Мониторинг

```bash
# Просмотр прогресса
cat download_progress.json

# Количество скачанных видео
ls -1 downloaded_videos | wc -l

# Размер скачанных файлов
du -sh downloaded_videos

# Логи systemd service
sudo journalctl -u telegram-downloader -f
```

## 🛠 Управление

```bash
# Остановить скачивание
Ctrl+C  # При ручном запуске
sudo systemctl stop telegram-downloader  # При запуске через systemd

# Продолжить с того же места
python download_videos.py  # Или sudo systemctl start telegram-downloader

# Очистить прогресс и начать заново
rm download_progress.json

# Удалить все скачанные видео
rm -rf downloaded_videos/*
```

## 📝 Примечания

- Видео сохраняются с именами `video_{message_id}.mp4`
- Поддерживаются все видеоформаты из Telegram
- Прогресс сохраняется после каждого скачанного файла
- При прерывании скрипт можно запустить снова - он продолжит с того места

## 🤝 Вклад в проект

Pull requests приветствуются! Для серьезных изменений сначала откройте issue для обсуждения.

## 📄 Лицензия

[MIT](LICENSE)

## ⚠️ Дисклеймер

Используйте этот скрипт ответственно и в соответствии с правилами Telegram. Убедитесь, что у вас есть право скачивать контент из указанного канала.
