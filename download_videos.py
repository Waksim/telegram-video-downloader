"""
Скрипт для скачивания видео из Telegram супергруппы и загрузки на Google Drive.
"""
import os
import json
import asyncio
import tempfile
from pathlib import Path
from datetime import datetime
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

# ID супергруппы (без -100 префикса, просто число из ссылки)
CHAT_ID = -1002406265529  # 2406265529 с префиксом -100
TOPIC_ID = 4  # ID топика из ссылки

# Настройки Google Drive
GOOGLE_DRIVE_FOLDER = 'Собесы'  # Имя папки на Google Drive

# Файл для отслеживания прогресса
PROGRESS_FILE = 'download_progress.json'


class DownloadProgress:
    """Класс для отслеживания прогресса скачивания."""

    def __init__(self, progress_file: str):
        self.progress_file = progress_file
        self.downloaded_ids = set()
        self.load_progress()

    def load_progress(self):
        """Загружает прогресс из файла."""
        if os.path.exists(self.progress_file):
            try:
                with open(self.progress_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.downloaded_ids = set(data.get('downloaded_ids', []))
                    print(f"✓ Загружен прогресс: {len(self.downloaded_ids)} файлов уже скачано")
            except Exception as e:
                print(f"⚠ Ошибка загрузки прогресса: {e}")
                self.downloaded_ids = set()
        else:
            print("ℹ Файл прогресса не найден, начинаем с начала")

    def save_progress(self):
        """Сохраняет текущий прогресс в файл."""
        try:
            with open(self.progress_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'downloaded_ids': list(self.downloaded_ids),
                    'last_update': datetime.now().isoformat()
                }, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠ Ошибка сохранения прогресса: {e}")

    def is_downloaded(self, message_id: int) -> bool:
        """Проверяет, был ли уже скачан файл."""
        return message_id in self.downloaded_ids

    def mark_downloaded(self, message_id: int):
        """Отмечает файл как скачанный."""
        self.downloaded_ids.add(message_id)
        self.save_progress()


async def download_videos():
    """Основная функция для скачивания видео и загрузки на Google Drive."""

    # Инициализация клиента с сессией из строки
    client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

    # Инициализация отслеживания прогресса
    progress = DownloadProgress(PROGRESS_FILE)

    # Инициализация Google Drive
    try:
        drive_uploader = GoogleDriveUploader()
        drive_uploader.set_folder(GOOGLE_DRIVE_FOLDER)
    except Exception as e:
        print(f"❌ Ошибка инициализации Google Drive: {e}")
        return

    try:
        await client.connect()

        if not await client.is_user_authorized():
            print("❌ Ошибка: сессия не авторизована")
            return

        print("✓ Успешно подключен к Telegram")

        # Получаем информацию о чате
        try:
            chat = await client.get_entity(CHAT_ID)
            print(f"✓ Найден чат: {getattr(chat, 'title', 'Unknown')}")
        except Exception as e:
            print(f"❌ Ошибка получения чата: {e}")
            return

        print(f"\n📥 Начинаем поиск видео в топике {TOPIC_ID}...")

        video_count = 0
        skipped_count = 0
        downloaded_count = 0

        # Итерируем по сообщениям в топике
        async for message in client.iter_messages(
            CHAT_ID,
            reply_to=TOPIC_ID,  # Фильтруем по топику
            reverse=True  # Начинаем с самых старых сообщений
        ):
            # Проверяем, есть ли видео в сообщении
            if message.video or (message.media and isinstance(message.media, MessageMediaDocument)):
                # Проверяем, является ли это видео
                is_video = False

                if message.video:
                    is_video = True
                elif hasattr(message.media, 'document'):
                    mime_type = message.media.document.mime_type
                    is_video = mime_type and mime_type.startswith('video/')

                if is_video:
                    video_count += 1

                    # Проверяем, был ли уже скачан
                    if progress.is_downloaded(message.id):
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

                            progress.mark_downloaded(message.id)
                            downloaded_count += 1

                            print(f"✓ Видео успешно загружено на Google Drive")

                        finally:
                            # Удаляем временный файл
                            if os.path.exists(temp_filepath):
                                os.remove(temp_filepath)

                    except Exception as e:
                        print(f"❌ Ошибка обработки видео (ID: {message.id}): {e}")

        print(f"\n{'='*60}")
        print(f"✓ Завершено!")
        print(f"  Всего найдено видео: {video_count}")
        print(f"  Загружено на Google Drive в этот раз: {downloaded_count}")
        print(f"  Пропущено (уже были): {skipped_count}")
        print(f"  Папка на Google Drive: {GOOGLE_DRIVE_FOLDER}")
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


def main():
    """Точка входа в программу."""
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
