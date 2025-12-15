# Скрипт для быстрой публикации на GitHub
# Использование: .\git_publish.ps1

Write-Host "🚀 Подготовка к публикации на GitHub" -ForegroundColor Cyan
Write-Host ""

# Проверка наличия Git
try {
    $gitVersion = git --version
    Write-Host "✅ Git найден: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git не установлен!" -ForegroundColor Red
    Write-Host "Установите Git с https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Проверка, что .env не будет добавлен
Write-Host ""
Write-Host "🔒 Проверка безопасности..." -ForegroundColor Cyan

if (Test-Path .env) {
    $envInGitignore = Select-String -Path .gitignore -Pattern "^\.env$" -Quiet
    if ($envInGitignore) {
        Write-Host "✅ .env найден и правильно исключен в .gitignore" -ForegroundColor Green
    } else {
        Write-Host "⚠️  .env найден, но не исключен в .gitignore!" -ForegroundColor Yellow
        Write-Host "Добавьте '.env' в .gitignore перед продолжением!" -ForegroundColor Yellow
        exit 1
    }
} else {
    Write-Host "ℹ️  .env не найден (это нормально, если еще не создан)" -ForegroundColor Gray
}

# Инициализация репозитория (если еще не инициализирован)
if (-not (Test-Path .git)) {
    Write-Host ""
    Write-Host "📦 Инициализация Git репозитория..." -ForegroundColor Cyan
    git init
    Write-Host "✅ Репозиторий инициализирован" -ForegroundColor Green
} else {
    Write-Host "✅ Git репозиторий уже инициализирован" -ForegroundColor Green
}

# Добавление файлов
Write-Host ""
Write-Host "📝 Добавление файлов..." -ForegroundColor Cyan
git add .

# Проверка статуса
Write-Host ""
Write-Host "📊 Статус репозитория:" -ForegroundColor Cyan
git status

# Проверка, что .env не добавлен
$envInStaging = git ls-files | Select-String "^\.env$"
if ($envInStaging) {
    Write-Host ""
    Write-Host "⚠️  ВНИМАНИЕ: .env найден в staging area!" -ForegroundColor Red
    Write-Host "Удаляю .env из staging..." -ForegroundColor Yellow
    git reset HEAD .env
    Write-Host "✅ .env удален из staging" -ForegroundColor Green
}

Write-Host ""
Write-Host "⚠️  ВНИМАНИЕ: Просмотрите список файлов выше!" -ForegroundColor Yellow
Write-Host "Убедитесь, что .env НЕ в списке 'Changes to be committed'" -ForegroundColor Yellow
Write-Host ""

$confirm = Read-Host "Продолжить создание коммита? (y/n)"
if ($confirm -ne "y" -and $confirm -ne "Y") {
    Write-Host "Отменено." -ForegroundColor Yellow
    exit 0
}

# Создание коммита
Write-Host ""
Write-Host "💾 Создание коммита..." -ForegroundColor Cyan
git commit -m "Initial commit: AI Competitor Market Analyzer

- FastAPI backend with OpenAI integration
- Image and text analysis with design_score and animation_potential
- Selenium-based competitor website parsing
- PyQt6 desktop application
- Complete documentation and setup instructions"

Write-Host "✅ Коммит создан" -ForegroundColor Green

# Переименование ветки в main
Write-Host ""
Write-Host "🌿 Настройка ветки main..." -ForegroundColor Cyan
git branch -M main
Write-Host "✅ Ветка переименована в main" -ForegroundColor Green

Write-Host ""
Write-Host "✅ Локальный репозиторий готов!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Следующие шаги:" -ForegroundColor Cyan
Write-Host "1. Создайте репозиторий на https://github.com/new" -ForegroundColor White
Write-Host "2. Скопируйте URL репозитория (например: https://github.com/USERNAME/repo.git)" -ForegroundColor White
Write-Host "3. Выполните следующие команды:" -ForegroundColor White
Write-Host ""
Write-Host "   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "Или используйте GitHub Desktop / GitHub CLI для публикации" -ForegroundColor Gray

