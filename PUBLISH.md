# 📤 Инструкция по публикации на GitHub

## Шаг 1: Создайте репозиторий на GitHub

1. Перейдите на https://github.com/new
2. Заполните информацию:
   - **Repository name:** `telegram-video-downloader` (или другое имя)
   - **Description:** Скрипт для скачивания видео из Telegram супергруппы с возможностью возобновления
   - **Public** или **Private** - на ваш выбор
   - ❌ **НЕ** инициализируйте с README, .gitignore или license (они уже есть в проекте)
3. Нажмите **Create repository**

## Шаг 2: Инициализация локального репозитория

Выполните следующие команды в терминале:

```bash
# Перейдите в папку проекта
cd /Users/mk/PycharmProjects/download_interview

# Инициализируйте git репозиторий (если еще не инициализирован)
git init

# Добавьте все файлы (кроме тех что в .gitignore)
git add .

# Проверьте что .env НЕ добавлен (должен быть в .gitignore)
git status

# Создайте первый коммит
git commit -m "Initial commit: Telegram video downloader with resume capability

- Added main download script with progress tracking
- Added installation script for Ubuntu
- Added systemd service configuration
- Added comprehensive deployment documentation
- Added .gitignore to protect sensitive data"

# Переименуйте ветку в main (если нужно)
git branch -M main

# Добавьте удаленный репозиторий (ЗАМЕНИТЕ YOUR_USERNAME на ваш GitHub username!)
git remote add origin https://github.com/YOUR_USERNAME/telegram-video-downloader.git

# Отправьте код на GitHub
git push -u origin main
```

## Шаг 3: Проверьте что загрузилось

Откройте ваш репозиторий на GitHub и убедитесь что:

✅ Загружены все файлы кроме `.env`
✅ README.md отображается на главной странице
✅ Файл `.env` НЕ загружен (это важно для безопасности!)

## Шаг 4: Обновите ссылки в документации

После публикации обновите ссылки в файлах:

### В README.md:

Замените `YOUR_USERNAME` на ваш GitHub username в строках:
- `git clone https://github.com/YOUR_USERNAME/download_interview.git`
- `wget https://raw.githubusercontent.com/YOUR_USERNAME/download_interview/main/install.sh`

### В DEPLOYMENT.md:

Замените `YOUR_USERNAME` на ваш GitHub username.

Выполните:

```bash
# После редактирования файлов
git add README.md DEPLOYMENT.md
git commit -m "Update repository URLs with actual username"
git push
```

## Команды для работы с GitHub

### Обновление кода на GitHub

```bash
# Добавить измененные файлы
git add .

# Создать коммит с описанием изменений
git commit -m "Описание ваших изменений"

# Отправить на GitHub
git push
```

### Проверка статуса

```bash
# Посмотреть какие файлы изменены
git status

# Посмотреть что именно изменилось
git diff

# История коммитов
git log --oneline
```

### Создание новых веток

```bash
# Создать и переключиться на новую ветку
git checkout -b feature/new-feature

# Отправить новую ветку на GitHub
git push -u origin feature/new-feature
```

### Откат изменений

```bash
# Откатить незакоммиченные изменения в файле
git checkout -- filename

# Откатить последний коммит (но сохранить изменения)
git reset --soft HEAD~1

# Откатить последний коммит (удалить изменения)
git reset --hard HEAD~1
```

## Безопасность

### ⚠️ ВАЖНО: Проверьте что секретные данные не попали в Git

```bash
# Проверьте что .env в .gitignore
cat .gitignore | grep .env

# Убедитесь что .env не отслеживается git
git ls-files | grep .env

# Если .env случайно добавлен, удалите его из git:
git rm --cached .env
git commit -m "Remove .env from git tracking"
git push
```

### Если вы случайно запушили .env с секретами:

1. **НЕМЕДЛЕННО** смените все секреты (API_HASH, SESSION_STRING)
2. Удалите файл из истории:
```bash
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch .env" \
  --prune-empty --tag-name-filter cat -- --all

git push origin --force --all
```
3. Смените все ключи API в Telegram

## Настройка GitHub Pages (опционально)

Если хотите создать красивую страницу для проекта:

1. Перейдите в Settings → Pages
2. Source: выберите ветку `main` и папку `/root`
3. Сохраните

Ваша документация будет доступна по адресу:
`https://YOUR_USERNAME.github.io/telegram-video-downloader/`

## Добавление GitHub Actions (опционально)

Для автоматической проверки кода создайте `.github/workflows/python-app.yml`:

```yaml
name: Python application

on: [push, pull_request]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    - name: Lint with flake8
      run: |
        pip install flake8
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

## Создание Release

```bash
# Создать тег для версии
git tag -a v1.0.0 -m "First stable release"

# Отправить тег на GitHub
git push origin v1.0.0
```

Затем на GitHub:
1. Перейдите в Releases
2. Нажмите "Create a new release"
3. Выберите тег v1.0.0
4. Опишите что нового в релизе
5. Опубликуйте

## Полезные ссылки

- [GitHub Documentation](https://docs.github.com/)
- [Git Cheat Sheet](https://education.github.com/git-cheat-sheet-education.pdf)
- [Markdown Guide](https://www.markdownguide.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)
