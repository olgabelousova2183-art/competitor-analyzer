# Решение проблемы с Python

## Проблема: При запуске `python run.py` выводится только "Python"

Это означает, что команда `python` указывает на заглушку Microsoft Store, а не на настоящий Python.

## Решение 1: Используйте `py` вместо `python`

Вместо:
```bash
python run.py
```

Используйте:
```bash
py run.py
```

Или:
```bash
py -3 run.py
```

---

## Решение 2: Проверьте установку Python

1. Откройте PowerShell
2. Выполните:
   ```powershell
   py --version
   ```

Если выводит версию (например, `Python 3.11.5`) - Python установлен правильно!

---

## Решение 3: Если `py` не работает

1. Установите Python с официального сайта: https://www.python.org/downloads/
2. **Важно:** При установке отметьте галочку "Add Python to PATH"
3. Перезапустите PowerShell
4. Проверьте: `py --version`

---

## Быстрая команда для запуска:

```bash
py run.py
```

Это должно работать!

