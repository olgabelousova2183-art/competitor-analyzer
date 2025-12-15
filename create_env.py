"""
Скрипт для создания файла .env
Запустите этот скрипт и введите ваш API ключ
"""
import os

def create_env_file():
    """Создает файл .env с API ключом"""
    env_file = ".env"
    
    # Проверяем, существует ли уже файл
    if os.path.exists(env_file):
        response = input(f"Файл {env_file} уже существует. Перезаписать? (y/n): ")
        if response.lower() != 'y':
            print("Отменено.")
            return
    
    print("\n" + "="*60)
    print("Настройка файла .env для API ключа")
    print("="*60)
    print("\nВыберите тип API:")
    print("1. OpenAI API (стандартный)")
    print("2. Proxy API")
    
    choice = input("\nВаш выбор (1 или 2): ").strip()
    
    if choice == "1":
        print("\nВведите ваш OpenAI API ключ:")
        print("(Ключ начинается с 'sk-' и не должен содержать пробелов)")
        api_key = input("OPENAI_API_KEY: ").strip()
        
        if not api_key:
            print("Ошибка: API ключ не может быть пустым!")
            return
        
        content = f"# OpenAI API Configuration\nOPENAI_API_KEY={api_key}\n"
        
    elif choice == "2":
        print("\nВведите данные Proxy API:")
        print("(Убедитесь, что у вас есть оба значения)")
        proxy_key = input("PROXY_API_KEY: ").strip()
        proxy_url = input("PROXY_API_URL (например: https://api.proxy-service.com/v1): ").strip()
        
        if not proxy_key or not proxy_url:
            print("Ошибка: PROXY_API_KEY и PROXY_API_URL не могут быть пустыми!")
            return
        
        # Проверяем формат URL
        if not proxy_url.startswith("http"):
            print("⚠️  Внимание: URL должен начинаться с http:// или https://")
            confirm = input("Продолжить? (y/n): ")
            if confirm.lower() != 'y':
                return
        
        content = f"# Proxy API Configuration\nPROXY_API_KEY={proxy_key}\nPROXY_API_URL={proxy_url}\n"
    else:
        print("Неверный выбор!")
        return
    
    # Записываем файл
    try:
        with open(env_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"\n✅ Файл {env_file} успешно создан!")
        print(f"📁 Расположение: {os.path.abspath(env_file)}")
        print("\n⚠️  ВАЖНО: Файл .env уже добавлен в .gitignore и не будет загружен в репозиторий.")
        print("\nТеперь вы можете запустить проект:")
        print("  python run.py")
        
    except Exception as e:
        print(f"\n❌ Ошибка при создании файла: {e}")

if __name__ == "__main__":
    create_env_file()

