# Используем официальный образ Python
FROM python:3.11-slim

# Устанавливаем метаданные
LABEL maintainer="Ball Game Developer"
LABEL description="Игра про шарики с графическим интерфейсом"
LABEL version="1.0"

# Устанавливаем системные зависимости для графического интерфейса
RUN apt-get update && apt-get install -y \
    # X11 и графические библиотеки
    xvfb \
    x11-apps \
    x11-utils \
    x11-xserver-utils \
    # OpenGL поддержка
    libgl1-mesa-glx \
    libgl1-mesa-dri \
    # Дополнительные библиотеки для Pygame
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libfreetype6-dev \
    libportmidi-dev \
    # Шрифты
    fonts-liberation \
    # Очистка кэша
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /app

# Копируем файлы зависимостей
COPY requirements.txt .

# Устанавливаем Python зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код игры
COPY logic.py .
COPY game.py .
COPY game_enhanced.py .
COPY gui.py .

# Делаем gui.py исполняемым
RUN chmod +x gui.py

# Создаём пользователя для безопасности
RUN useradd -m -u 1000 gameuser && \
    chown -R gameuser:gameuser /app

# Переключаемся на пользователя
USER gameuser

# Устанавливаем переменные окружения для X11
ENV DISPLAY=:99
ENV PYTHONUNBUFFERED=1

# Создаём скрипт запуска
RUN echo '#!/bin/bash\n\
# Запускаем виртуальный дисплей\n\
Xvfb :99 -screen 0 1200x800x24 &\n\
sleep 2\n\
# Запускаем игру\n\
python gui.py\n\
' > /app/start.sh && chmod +x /app/start.sh

# Точка входа
ENTRYPOINT ["/app/start.sh"] 