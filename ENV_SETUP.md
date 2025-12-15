# Настройка окружения

## Создание файла .env

Создайте файл `.env` в корне проекта со следующим содержимым:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
```

Или используйте Proxy API:

```env
# Alternative: Proxy API (if using proxy service)
PROXY_API_KEY=your_proxy_api_key_here
PROXY_API_URL=https://api.proxy.com/v1
```

**Важно**: 
- Никогда не загружайте файл `.env` в репозиторий
- Файл `.env` уже добавлен в `.gitignore`
- Храните API ключи в безопасности

## Где взять API ключ

1. **OpenAI API**: Зарегистрируйтесь на https://platform.openai.com/ и получите API ключ
2. **Proxy API**: Используйте сервис-прокси для доступа к OpenAI API (если требуется)

