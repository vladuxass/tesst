#!/bin/bash

# Скрипт для запуска игры в Docker с графическим интерфейсом

echo "🎮 Запуск игры про шарики в Docker..."

# Проверяем, установлен ли Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен. Установите Docker и попробуйте снова."
    exit 1
fi

# Проверяем, установлен ли docker-compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose не установлен. Установите docker-compose и попробуйте снова."
    exit 1
fi

# Определяем операционную систему
OS=$(uname -s)

if [[ "$OS" == "Linux" ]]; then
    echo "🐧 Linux обнаружен"
    
    # Разрешаем подключение к X11 серверу
    xhost +local:docker
    
    # Запускаем контейнер
    docker-compose up --build
    
    # Восстанавливаем настройки X11
    xhost -local:docker
    
elif [[ "$OS" == "Darwin" ]]; then
    echo "🍎 macOS обнаружен"
    
    # Для macOS нужен XQuartz
    if ! command -v xquartz &> /dev/null; then
        echo "❌ XQuartz не установлен. Установите XQuartz для macOS:"
        echo "   brew install --cask xquartz"
        exit 1
    fi
    
    # Запускаем XQuartz
    open -a XQuartz
    
    # Ждём запуска XQuartz
    sleep 3
    
    # Разрешаем подключение
    xhost +localhost
    
    # Запускаем контейнер
    docker-compose up --build
    
    # Восстанавливаем настройки
    xhost -localhost
    
elif [[ "$OS" == "MINGW"* ]] || [[ "$OS" == "MSYS"* ]] || [[ "$OS" == "CYGWIN"* ]]; then
    echo "🪟 Windows обнаружен"
    
    # Для Windows используем виртуальный дисплей
    echo "📺 Используется виртуальный дисплей (без графического интерфейса)"
    echo "🎮 Игра будет работать в консольном режиме"
    
    # Запускаем контейнер с виртуальным дисплеем
    docker-compose up --build
    
else
    echo "❓ Неизвестная операционная система: $OS"
    echo "🎮 Запуск с виртуальным дисплеем..."
    docker-compose up --build
fi

echo "✅ Игра завершена" 