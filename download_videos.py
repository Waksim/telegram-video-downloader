"""
Скрипт для скачивания видео из Telegram супергруппы и загрузки на Google Drive.
"""
import os
import sys
import json
import asyncio
import tempfile
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from dotenv import load_dotenv
from google_drive_uploader import GoogleDriveUploader

# Загружаем переменные окружения
load_dotenv()

# Конфигурация
API_ID = int(os.getenv('API_ID'))
API_HASH = os.getenv('API_HASH')
SESSION_STRING = os.getenv('SESSION_STRING')

# Файл конфигурации каналов
CHANNELS_CONFIG_FILE = 'channels_config.json'

# Файл для отслеживания прогресса
PROGRESS_FILE = 'download_progress.json'


class ChannelConfig:
    """Класс для работы с конфигурацией каналов."""

    def __init__(self, config_file: str):
        self.config_file = config_file
        self.channels = []
        self.load_config()

    def load_config(self):
        """Загружает конфигурацию из файла."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.channels = data.get('channels', [])
                    print(f"✓ Загружена конфигурация: {len(self.channels)} каналов")
            except Exception as e:
                print(f"⚠ Ошибка загрузки конфигурации: {e}")
                self.channels = []
        else:
            print(f"⚠ Файл конфигурации {self.config_file} не найден")

    def save_config(self):
        """Сохраняет конфигурацию в файл."""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'channels': self.channels
                }, f, indent=2, ensure_ascii=False)
            print(f"✓ Конфигурация сохранена")
        except Exception as e:
            print(f"⚠ Ошибка сохранения конфигурации: {e}")

    def add_channel(self, chat_id: int, topic_id: int, folder_path: str, description: str = ""):
        """Добавляет новый канал в конфигурацию."""
        # Проверяем, нет ли уже такого канала
        for channel in self.channels:
            if channel['chat_id'] == chat_id and channel['topic_id'] == topic_id:
                print(f"⚠ Канал уже существует в конфигурации")
                return False

        self.channels.append({
            'chat_id': chat_id,
            'topic_id': topic_id,
            'folder_path': folder_path,
            'description': description
        })
        self.save_config()
        return True


class DownloadProgress:
    """Класс для отслеживания прогресса скачивания."""

    def __init__(self, progress_file: str):
        self.progress_file = progress_file
        self.downloaded_ids = {}  # Изменено на словарь {channel_key: set(message_ids)}
        self.load_progress()

    def load_progress(self):
        """Загружает прогресс из файла."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Преобразуем обратно в словарь с множествами
                    self.downloaded_ids = {
                        key: set(ids) for key, ids in data.get('downloaded_ids', {}).items()
                    }
                    total = sum(len(ids) for ids in self.downloaded_ids.values())
                    print(f"✓ Загружен прогресс: {total} файлов уже скачано")
            except Exception as e:
                print(f"⚠ Ошибка загрузки прогресса: {e}")
                self.downloaded_ids = {}
        else:
            print("ℹ Файл прогресса не найден, начинаем с начала")

    def save_progress(self):
        """Сохраняет текущий прогресс в файл."""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                # Преобразуем множества в списки для JSON
                data_to_save = {
                    key: list(ids) for key, ids in self.downloaded_ids.items()
                }
                json.dump({
                    'downloaded_ids': data_to_save,
                    'last_update': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠ Ошибка сохранения прогресса: {e}")

    def get_channel_key(self, chat_id: int, topic_id: int) -> str:
        """Создает уникальный ключ для канала."""
        return f"{chat_id}_{topic_id}"

    def is_downloaded(self, chat_id: int, topic_id: int, message_id: int) -> bool:
        """Проверяет, был ли уже скачан файл."""
        channel_key = self.get_channel_key(chat_id, topic_id)
        return message_id in self.downloaded_ids.get(channel_key, set())

    def mark_downloaded(self, chat_id: int, topic_id: int, message_id: int):
        """Отмечает файл как скачанный."""
        channel_key = self.get_channel_key(chat_id, topic_id)
        if channel_key not in self.downloaded_ids:
            self.downloaded_ids[channel_key] = set()
        self.downloaded_ids[channel_key].add(message_id)
        self.save_progress()


async def download_channel_videos(client, chat_id: int, topic_id: int,
                                  folder_path: str, progress: DownloadProgress,
                                  drive_uploader: GoogleDriveUploader) -> Dict:
    """
    Скачивает видео из одного канала.

    Returns:
        Словарь со статистикой загрузки
    """
    print(f"\n{'='*60}")
    print(f"📥 Обработка канала: {folder_path}")
    print(f"   Chat ID: {chat_id}, Topic ID: {topic_id}")

    # Получаем информацию о чате
    try:
        chat = await client.get_entity(chat_id)
        print(f"✓ Найден чат: {getattr(chat, 'title', 'Unknown')}")
    except Exception as e:
        print(f"❌ Ошибка получения чата: {e}")
        return {'video_count': 0, 'downloaded': 0, 'skipped': 0}

    # Устанавливаем папку на Google Drive
    drive_uploader.set_folder(folder_path)

    video_count = 0
    skipped_count = 0
    downloaded_count = 0

    # Итерируем по сообщениям в топике
    async for message in client.iter_messages(
        chat_id,
        reply_to=topic_id,
        reverse=True
    ):
        # Проверяем, есть ли видео в сообщении
        if message.video or (message.media and isinstance(message.media, MessageMediaDocument)):
            is_video = False

            if message.video:
                is_video = True
            elif hasattr(message.media, 'document'):
                mime_type = message.media.document.mime_type
                is_video = mime_type and mime_type.startswith('video/')

            if is_video:
                video_count += 1

                # Проверяем, был ли уже скачан
                if progress.is_downloaded(chat_id, topic_id, message.id):
                    skipped_count += 1
                    print(f"⏭ [{video_count}] Пропускаем уже загруженное видео (ID: {message.id})")
                    continue

                # Формируем имя файла
                filename = f"video_{message.id}"
                if message.file and message.file.ext:
                    filename += message.file.ext
                else:
                    filename += ".mp4"

                # Определяем MIME-тип
                mime_type = 'video/mp4'
                if message.video:
                    mime_type = message.video.mime_type or 'video/mp4'
                elif hasattr(message.media, 'document'):
                    mime_type = message.media.document.mime_type or 'video/mp4'

                # Скачиваем видео во временный файл и загружаем на Google Drive
                try:
                    print(f"\n📥 [{video_count}] Обрабатываем видео (ID: {message.id})...")
                    print(f"   Дата: {message.date}")
                    file_size_mb = 0
                    if message.file:
                        file_size_mb = message.file.size / (1024*1024)
                        print(f"   Размер: {file_size_mb:.2f} MB")

                    # Создаем временный файл
                    with tempfile.NamedTemporaryFile(delete=False, suffix=filename[filename.rfind('.'):]) as temp_file:
                        temp_filepath = temp_file.name

                    try:
                        # Скачиваем видео во временный файл
                        await message.download_media(file=temp_filepath)

                        # Загружаем на Google Drive
                        drive_uploader.upload_to_folder(
                            filepath=temp_filepath,
                            filename=filename,
                            mime_type=mime_type,
                            file_size_mb=file_size_mb
                        )

                        progress.mark_downloaded(chat_id, topic_id, message.id)
                        downloaded_count += 1

                        print(f"✓ Видео успешно загружено на Google Drive")

                    finally:
                        # Удаляем временный файл
                        if os.path.exists(temp_filepath):
                            os.remove(temp_filepath)

                except Exception as e:
                    print(f"❌ Ошибка обработки видео (ID: {message.id}): {e}")

    return {
        'video_count': video_count,
        'downloaded': downloaded_count,
        'skipped': skipped_count
    }


async def download_videos():
    """Основная функция для скачивания видео и загрузки на Google Drive."""

    # Загружаем конфигурацию каналов
    config = ChannelConfig(CHANNELS_CONFIG_FILE)

    if not config.channels:
        print("❌ Нет каналов для обработки. Добавьте каналы в channels_config.json")
        return

    # Инициализация клиента с сессией из строки
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

    # Инициализация отслеживания прогресса
    progress = DownloadProgress(PROGRESS_FILE)

    # Инициализация Google Drive
    try:
        drive_uploader = GoogleDriveUploader()
    except Exception as e:
        print(f"❌ Ошибка инициализации Google Drive: {e}")
        return

    try:
        await client.connect()

        if not await client.is_user_authorized():
            print("❌ Ошибка: сессия не авторизована")
            return

        print("✓ Успешно подключен к Telegram")

        # Обрабатываем каждый канал
        total_stats = {'video_count': 0, 'downloaded': 0, 'skipped': 0}

        for channel in config.channels:
            stats = await download_channel_videos(
                client=client,
                chat_id=channel['chat_id'],
                topic_id=channel['topic_id'],
                folder_path=channel['folder_path'],
                progress=progress,
                drive_uploader=drive_uploader
            )

            total_stats['video_count'] += stats['video_count']
            total_stats['downloaded'] += stats['downloaded']
            total_stats['skipped'] += stats['skipped']

        print(f"\n{'='*60}")
        print(f"✓ Все каналы обработаны!")
        print(f"  Всего найдено видео: {total_stats['video_count']}")
        print(f"  Загружено на Google Drive в этот раз: {total_stats['downloaded']}")
        print(f"  Пропущено (уже были): {total_stats['skipped']}")
        print(f"{'='*60}")

    except KeyboardInterrupt:
        print("\n\n⚠ Прервано пользователем")
        print(f"✓ Прогресс сохранен. Запустите скрипт снова для продолжения.")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.disconnect()


def parse_telegram_url(url: str) -> Optional[Dict]:
    """
    Парсит Telegram URL и извлекает chat_id и topic_id.

    Args:
        url: URL вида https://t.me/c/2406265529/8/602

    Returns:
        Словарь с chat_id и topic_id или None
    """
    import re

    # Паттерн для приватных чатов: https://t.me/c/CHAT_ID/TOPIC_ID/...
    pattern = r't\.me/c/(\d+)/(\d+)'
    match = re.search(pattern, url)

    if match:
        chat_id_without_prefix = int(match.group(1))
        topic_id = int(match.group(2))

        # Добавляем префикс -100 к chat_id
        chat_id = -1000000000000 - chat_id_without_prefix

        return {
            'chat_id': chat_id,
            'topic_id': topic_id
        }

    return None


def add_channel_command(url: str, folder_name: str):
    """Добавляет новый канал в конфигурацию."""
    print("="*60)
    print("📝 Добавление нового канала")
    print("="*60)

    # Парсим URL
    parsed = parse_telegram_url(url)
    if not parsed:
        print(f"❌ Ошибка: неверный формат URL. Ожидается: https://t.me/c/CHAT_ID/TOPIC_ID/...")
        return

    # Загружаем конфигурацию
    config = ChannelConfig(CHANNELS_CONFIG_FILE)

    # Формируем путь к папке
    folder_path = f"Собесы/{folder_name}"

    # Добавляем канал
    if config.add_channel(
        chat_id=parsed['chat_id'],
        topic_id=parsed['topic_id'],
        folder_path=folder_path,
        description=folder_name
    ):
        print(f"✓ Канал успешно добавлен!")
        print(f"  URL: {url}")
        print(f"  Chat ID: {parsed['chat_id']}")
        print(f"  Topic ID: {parsed['topic_id']}")
        print(f"  Папка: {folder_path}")
    else:
        print("❌ Не удалось добавить канал")


def main():
    """Точка входа в программу."""
    # Проверяем, если запущена команда добавления канала
    if len(sys.argv) == 3:
        # Формат: python download_videos.py URL FOLDER_NAME
        url = sys.argv[1]
        folder_name = sys.argv[2]
        add_channel_command(url, folder_name)
        return

    print("="*60)
    print("📹 Загрузчик видео из Telegram на Google Drive")
    print("="*60)

    # Проверка конфигурации
    if not API_ID or not API_HASH or not SESSION_STRING:
        print("❌ Ошибка: не заданы API_ID, API_HASH или SESSION_STRING")
        print("   Создайте файл .env на основе .env.example")
        return

    # Запуск асинхронной функции
    asyncio.run(download_videos())


if __name__ == '__main__':
    main()
