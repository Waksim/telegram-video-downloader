"""
Модуль для работы с Google Drive API.
"""
import os
from pathlib import Path
from typing import Optional
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


class GoogleDriveUploader:
    """Класс для загрузки файлов на Google Drive."""

    def __init__(self, credentials_file: str = 'credentials.json', token_file: str = 'token.json'):
        """
        Инициализация загрузчика.

        Args:
            credentials_file: путь к файлу credentials.json
            token_file: путь к файлу token.json
        """
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.service = None
        self.folder_id = None
        self._authenticate()

    def _authenticate(self):
        """Аутентификация в Google Drive."""
        if not os.path.exists(self.token_file):
            raise FileNotFoundError(f"Файл {self.token_file} не найден")

        creds = Credentials.from_authorized_user_file(self.token_file)
        self.service = build('drive', 'v3', credentials=creds)

    def get_or_create_folder(self, folder_name: str, parent_id: Optional[str] = None) -> str:
        """
        Получает ID папки или создает новую, если не существует.

        Args:
            folder_name: имя папки
            parent_id: ID родительской папки (опционально)

        Returns:
            ID папки
        """
        # Поиск существующей папки
        query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
        if parent_id:
            query += f" and '{parent_id}' in parents"

        results = self.service.files().list(
            q=query,
            spaces='drive',
            fields='files(id, name)'
        ).execute()

        items = results.get('files', [])

        if items:
            folder_id = items[0]['id']
            print(f"✓ Найдена существующая папка '{folder_name}' (ID: {folder_id})")
            return folder_id

        # Создание новой папки
        file_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }

        if parent_id:
            file_metadata['parents'] = [parent_id]

        folder = self.service.files().create(
            body=file_metadata,
            fields='id'
        ).execute()

        folder_id = folder.get('id')
        print(f"✓ Создана новая папка '{folder_name}' (ID: {folder_id})")
        return folder_id

    def upload_file(self, filepath: str, filename: str,
                   folder_id: Optional[str] = None, mime_type: str = 'video/mp4') -> str:
        """
        Загружает файл с диска на Google Drive.

        Args:
            filepath: путь к файлу на диске
            filename: имя файла на Google Drive
            folder_id: ID папки для загрузки (опционально)
            mime_type: MIME-тип файла

        Returns:
            ID загруженного файла
        """
        file_metadata = {'name': filename}

        if folder_id:
            file_metadata['parents'] = [folder_id]

        media = MediaFileUpload(
            filepath,
            mimetype=mime_type,
            resumable=True,
            chunksize=256*1024  # 256KB chunks для экономии памяти
        )

        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id, name, size'
        ).execute()

        return file.get('id')

    def set_folder(self, folder_path: str):
        """
        Устанавливает папку для загрузки файлов.
        Поддерживает вложенные папки через разделитель '/'.

        Args:
            folder_path: путь к папке (например, 'Собесы/NLP' или 'Собесы')
        """
        folders = folder_path.split('/')
        parent_id = None

        for folder_name in folders:
            folder_name = folder_name.strip()
            if folder_name:
                parent_id = self.get_or_create_folder(folder_name, parent_id)

        self.folder_id = parent_id

    def file_exists_in_folder(self, filename: str) -> bool:
        """
        Проверяет, существует ли файл с заданным именем в текущей папке.

        Args:
            filename: имя файла для проверки

        Returns:
            True если файл существует, False иначе
        """
        if not self.folder_id:
            return False

        query = f"name='{filename}' and '{self.folder_id}' in parents and trashed=false"

        try:
            results = self.service.files().list(
                q=query,
                spaces='drive',
                fields='files(id, name)',
                pageSize=1
            ).execute()

            items = results.get('files', [])
            return len(items) > 0
        except Exception as e:
            print(f"⚠ Ошибка проверки существования файла: {e}")
            return False

    def upload_to_folder(self, filepath: str, filename: str,
                        mime_type: str = 'video/mp4', file_size_mb: float = 0) -> str:
        """
        Загружает файл с диска в установленную папку.

        Args:
            filepath: путь к файлу на диске
            filename: имя файла на Google Drive
            mime_type: MIME-тип файла
            file_size_mb: размер файла в MB (для отображения)

        Returns:
            ID загруженного файла
        """
        print(f"📤 Загружаем на Google Drive: {filename} ({file_size_mb:.2f} MB)...")

        file_id = self.upload_file(
            filepath=filepath,
            filename=filename,
            folder_id=self.folder_id,
            mime_type=mime_type
        )

        print(f"✓ Загружено на Google Drive (ID: {file_id})")
        return file_id
