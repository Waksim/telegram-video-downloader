# 🎯 НАЧНИТЕ ЗДЕСЬ!

## Что у вас есть?

✅ Полностью готовый проект для скачивания видео из Telegram
✅ Автоматические скрипты установки
✅ Подробная документация
✅ Все необходимые файлы

---

## 📋 Следуйте этим шагам:

### ШАГ 1: Публикация на GitHub (5 минут)

1. **Создайте репозиторий:**
   - Откройте https://github.com/new
   - Название: `telegram-video-downloader`
   - ❌ НЕ ставьте галочки "Initialize with README"
   - Нажмите "Create repository"

2. **Запустите команды из терминала:**
   ```bash
   # Откройте COMMANDS.txt и скопируйте команды из раздела
   # "КОМАНДЫ ДЛЯ ПУБЛИКАЦИИ НА GITHUB"

   cat COMMANDS.txt
   ```

   Или просто выполните:
   ```bash
   cd /Users/mk/PycharmProjects/download_interview
   git init
   git add .
   git commit -m "Initial commit: Telegram video downloader"
   git branch -M main
   # ЗАМЕНИТЕ YOUR_USERNAME на ваш GitHub логин!
   git remote add origin https://github.com/YOUR_USERNAME/telegram-video-downloader.git
   git push -u origin main
   ```

3. **Обновите ссылки в документации:**
   - Откройте `README.md` и `DEPLOYMENT.md`
   - Найдите все `YOUR_USERNAME` и замените на ваш GitHub username
   - Выполните:
     ```bash
     git add README.md DEPLOYMENT.md
     git commit -m "Update repository URLs"
     git push
     ```

**✅ GitHub готов!**

---

### ШАГ 2: Деплой на Ubuntu сервер (10 минут)

**СПОСОБ А: Автоматическая установка (рекомендуется)**

На вашем Ubuntu сервере выполните ОДНУ команду:

```bash
wget https://raw.githubusercontent.com/YOUR_USERNAME/telegram-video-downloader/main/install.sh && chmod +x install.sh && ./install.sh
```

Скрипт сам всё установит и попросит ввести ваши API данные.

**СПОСОБ Б: Ручная установка**

Откройте `COMMANDS.txt` и следуйте разделу "ВАРИАНТ 2: РУЧНАЯ УСТАНОВКА"

**✅ Сервер настроен!**

---

### ШАГ 3: Настройка автозапуска (опционально, 5 минут)

**Если хотите чтобы скрипт работал постоянно:**

1. Следуйте инструкции из `COMMANDS.txt` раздел "ВАРИАНТ 3: SYSTEMD SERVICE"

2. Или используйте screen (проще):
   ```bash
   screen -S downloader
   cd ~/telegram-video-downloader
   source venv/bin/activate
   python download_videos.py
   # Нажмите Ctrl+A, затем D чтобы отключиться
   ```

**✅ Автозапуск настроен!**

---

## 📚 Где что находится?

| Файл | Описание |
|------|----------|
| **[COMMANDS.txt](COMMANDS.txt)** | ⭐ ВСЕ команды для копирования |
| **[QUICK_START.md](QUICK_START.md)** | Быстрый старт с примерами |
| **[README.md](README.md)** | Основная документация |
| **[DEPLOYMENT.md](DEPLOYMENT.md)** | Подробная инструкция по деплою |
| **[PUBLISH.md](PUBLISH.md)** | Как работать с GitHub |
| **[install.sh](install.sh)** | Скрипт автоустановки |
| **[download_videos.py](download_videos.py)** | Основной скрипт |

---

## 🎯 Быстрые ссылки на команды

### Публикация на GitHub:
```bash
cat COMMANDS.txt  # Смотрите раздел "КОМАНДЫ ДЛЯ ПУБЛИКАЦИИ"
```

### Деплой на сервер:
```bash
cat COMMANDS.txt  # Смотрите раздел "КОМАНДЫ ДЛЯ ДЕПЛОЯ"
```

### Управление на сервере:
```bash
cat COMMANDS.txt  # Смотрите раздел "УПРАВЛЕНИЕ НА СЕРВЕРЕ"
```

---

## ❓ Возникли проблемы?

1. **Откройте [COMMANDS.txt](COMMANDS.txt)** и найдите раздел "РЕШЕНИЕ ПРОБЛЕМ"
2. **Проверьте [DEPLOYMENT.md](DEPLOYMENT.md)** для подробных объяснений
3. **Откройте issue** на GitHub если ничего не помогло

---

## ✅ Чеклист

### Локально (ваш Mac):
- [ ] Создал репозиторий на GitHub
- [ ] Выполнил `git init`, `git add .`, `git commit`, `git push`
- [ ] Обновил `YOUR_USERNAME` в документации
- [ ] Запушил обновления

### На сервере (Ubuntu):
- [ ] Подключился к серверу
- [ ] Запустил `install.sh` или установил вручную
- [ ] Настроил `.env` с API данными
- [ ] Настроил `CHAT_ID` и `TOPIC_ID` в `download_videos.py`
- [ ] Запустил тестовое скачивание
- [ ] Настроил systemd или screen (опционально)
- [ ] Проверил что скачивание работает

---

## 🚀 Готово!

После выполнения всех шагов:
- ✅ Ваш код опубликован на GitHub
- ✅ Скрипт работает на сервере
- ✅ Видео скачиваются автоматически
- ✅ Прогресс сохраняется

**Видео будут сохраняться в папку `downloaded_videos/`**

---

## 💡 Полезные команды

```bash
# Проверить статус на сервере
sudo systemctl status telegram-downloader

# Посмотреть логи
sudo journalctl -u telegram-downloader -f

# Проверить прогресс
cat ~/telegram-video-downloader/download_progress.json

# Сколько видео скачано?
ls -1 ~/telegram-video-downloader/downloaded_videos | wc -l

# Обновить код с GitHub
cd ~/telegram-video-downloader
git pull
sudo systemctl restart telegram-downloader
```

---

**🎉 Удачи с проектом!**

Если что-то непонятно - все команды есть в **[COMMANDS.txt](COMMANDS.txt)**
