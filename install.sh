#!/bin/bash

# Скрипт автоматической установки Telegram Video Downloader на Ubuntu

set -e  # Остановка при ошибке

echo "========================================"
echo "📥 Telegram Video Downloader"
echo "Автоматическая установка"
echo "========================================"
echo ""

# Проверка, что скрипт не запущен от root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Не запускайте этот скрипт от root!"
    echo "   Используйте: ./install.sh"
    exit 1
fi

# Обновление системы
echo "📦 Обновление системы..."
sudo apt update
sudo apt upgrade -y

# Установка зависимостей
echo "📦 Установка зависимостей..."
sudo apt install -y python3 python3-pip python3-venv git wget curl

# Проверка версии Python
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
echo "✓ Python версия: $PYTHON_VERSION"

# Клонирование репозитория (если еще не склонирован)
if [ ! -d "download_interview" ]; then
    echo "📥 Клонирование репозитория..."
    read -p "Введите URL вашего GitHub репозитория: " REPO_URL
    git clone "$REPO_URL" download_interview
    cd download_interview
else
    echo "✓ Репозиторий уже существует"
    cd download_interview
fi

# Создание виртуального окружения
echo "🐍 Создание виртуального окружения..."
python3 -m venv venv

# Активация виртуального окружения
echo "🐍 Активация виртуального окружения..."
source venv/bin/activate

# Установка Python зависимостей
echo "📦 Установка Python пакетов..."
pip install --upgrade pip
pip install -r requirements.txt

# Создание .env файла
if [ ! -f ".env" ]; then
    echo ""
    echo "⚙️  Настройка конфигурации..."
    cp .env.example .env

    echo ""
    echo "Пожалуйста, введите ваши данные Telegram API:"
    echo ""

    read -p "API_ID: " API_ID
    read -p "API_HASH: " API_HASH
    echo "SESSION_STRING (длинная строка):"
    read -p "> " SESSION_STRING

    # Запись в .env
    cat > .env << EOF
API_ID=$API_ID
API_HASH=$API_HASH
SESSION_STRING=$SESSION_STRING
EOF

    chmod 600 .env
    echo "✓ Конфигурация сохранена"
else
    echo "✓ Файл .env уже существует"
fi

# Создание папки для видео
mkdir -p downloaded_videos

# Настройка systemd service (опционально)
echo ""
read -p "Хотите настроить автоматический запуск через systemd? (y/n): " SETUP_SYSTEMD

if [ "$SETUP_SYSTEMD" = "y" ] || [ "$SETUP_SYSTEMD" = "Y" ]; then
    echo "⚙️  Настройка systemd service..."

    USERNAME=$(whoami)
    WORKING_DIR=$(pwd)

    # Создание service файла с правильными путями
    sudo tee /etc/systemd/system/telegram-downloader.service > /dev/null << EOF
[Unit]
Description=Telegram Video Downloader
After=network.target

[Service]
Type=simple
User=$USERNAME
WorkingDirectory=$WORKING_DIR
Environment="PATH=$WORKING_DIR/venv/bin"
ExecStart=$WORKING_DIR/venv/bin/python download_videos.py
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

    # Перезагрузка systemd
    sudo systemctl daemon-reload

    echo "✓ Systemd service создан"
    echo ""
    echo "Для управления сервисом используйте:"
    echo "  sudo systemctl start telegram-downloader    # Запуск"
    echo "  sudo systemctl stop telegram-downloader     # Остановка"
    echo "  sudo systemctl status telegram-downloader   # Статус"
    echo "  sudo systemctl enable telegram-downloader   # Автозапуск"
fi

# Тестовый запуск (опционально)
echo ""
read -p "Хотите запустить тестовое скачивание сейчас? (y/n): " RUN_TEST

if [ "$RUN_TEST" = "y" ] || [ "$RUN_TEST" = "Y" ]; then
    echo ""
    echo "🚀 Запуск скрипта..."
    echo "   (Нажмите Ctrl+C для остановки)"
    echo ""
    sleep 2
    python download_videos.py
fi

echo ""
echo "========================================"
echo "✅ Установка завершена!"
echo "========================================"
echo ""
echo "📁 Проект установлен в: $(pwd)"
echo "📹 Видео будут сохранены в: $(pwd)/downloaded_videos"
echo ""
echo "Для ручного запуска:"
echo "  cd $(pwd)"
echo "  source venv/bin/activate"
echo "  python download_videos.py"
echo ""
echo "Для просмотра документации по деплою:"
echo "  cat DEPLOYMENT.md"
echo ""
