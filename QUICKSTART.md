# Быстрый старт

## Шаг 1: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 2: Настройка API ключа

Создайте файл `.env` в корне проекта:
```env
OPENAI_API_KEY=your_api_key_here
```

## Шаг 3: Настройка URLs конкурентов

Откройте `config.py` и измените `COMPETITOR_URLS` на нужные вам сайты.

## Шаг 4: Запуск API сервера

В одном терминале:
```bash
python run.py
# или
uvicorn main:app --reload
```

Сервер будет доступен на `http://localhost:8000`

## Шаг 5: Тестирование

### Тест анализа изображения:
```bash
curl -X POST "http://localhost:8000/analyzeimage" -F "file=@path/to/image.jpg"
```

### Тест анализа текста:
```bash
curl -X POST "http://localhost:8000/analyzetext" -H "Content-Type: application/json" -d "{\"text\": \"Ваш текст для анализа\"}"
```

### Тест парсинга:
```bash
curl http://localhost:8000/parsedemo
```

## Шаг 6: Запуск Desktop приложения

В другом терминале (с запущенным API сервером):
```bash
python run_desktop.py
```

## Шаг 7: Сборка исполняемого файла (опционально)

```bash
python build.py
```

Исполняемый файл будет в `dist/competitionmonitor.exe`

