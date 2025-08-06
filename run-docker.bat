@echo off
chcp 65001 >nul

echo 🎮 Запуск игры про шарики в Docker...

REM Проверяем, установлен ли Docker
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker не установлен. Установите Docker Desktop и попробуйте снова.
    pause
    exit /b 1
)

REM Проверяем, установлен ли docker-compose
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ docker-compose не установлен. Установите docker-compose и попробуйте снова.
    pause
    exit /b 1
)

echo 🪟 Windows обнаружен
echo 📺 Используется виртуальный дисплей
echo 🎮 Игра будет работать в консольном режиме

REM Запускаем контейнер
docker-compose up --build

echo ✅ Игра завершена
pause 