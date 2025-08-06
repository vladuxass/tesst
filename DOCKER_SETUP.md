# 🐳 Настройка Docker для игры про шарики

## Установка Docker

### Windows

1. **Скачайте Docker Desktop**:
   - Перейдите на [Docker Desktop для Windows](https://docs.docker.com/desktop/install/windows/)
   - Скачайте установщик для Windows

2. **Установите Docker Desktop**:
   - Запустите скачанный файл
   - Следуйте инструкциям установщика
   - Перезагрузите компьютер при необходимости

3. **Проверьте установку**:
   ```cmd
   docker --version
   docker-compose --version
   ```

### macOS

1. **Установите Docker Desktop**:
   ```bash
   # Через Homebrew
   brew install --cask docker
   
   # Или скачайте с официального сайта
   # https://docs.docker.com/desktop/install/mac/
   ```

2. **Запустите Docker Desktop**:
   - Найдите Docker в Applications
   - Запустите приложение
   - Дождитесь иконки Docker в строке меню

3. **Проверьте установку**:
   ```bash
   docker --version
   docker-compose --version
   ```

### Linux (Ubuntu/Debian)

1. **Установите Docker Engine**:
   ```bash
   # Обновите пакеты
   sudo apt-get update
   
   # Установите необходимые пакеты
   sudo apt-get install \
       ca-certificates \
       curl \
       gnupg \
       lsb-release
   
   # Добавьте официальный GPG ключ Docker
   sudo mkdir -p /etc/apt/keyrings
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
   
   # Настройте репозиторий
   echo \
     "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
     $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
   
   # Установите Docker Engine
   sudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
   ```

2. **Добавьте пользователя в группу docker**:
   ```bash
   sudo usermod -aG docker $USER
   # Перезапустите терминал или выполните:
   newgrp docker
   ```

3. **Проверьте установку**:
   ```bash
   docker --version
   docker compose version
   ```

## Установка docker-compose (если не включен)

### Linux
```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

### Windows/macOS
Docker Compose включен в Docker Desktop.

## Настройка графического интерфейса

### Linux

1. **Убедитесь, что X11 запущен**:
   ```bash
   echo $DISPLAY
   # Должно вывести что-то вроде :0
   ```

2. **Разрешите подключение к X11**:
   ```bash
   xhost +local:docker
   ```

### macOS

1. **Установите XQuartz**:
   ```bash
   brew install --cask xquartz
   ```

2. **Запустите XQuartz**:
   ```bash
   open -a XQuartz
   ```

3. **Настройте DISPLAY**:
   ```bash
   export DISPLAY=:0
   ```

### Windows

Для Windows используется виртуальный дисплей (Xvfb), поэтому дополнительная настройка не требуется.

## Запуск игры в Docker

### Автоматический запуск

```bash
# Linux/macOS
chmod +x run-docker.sh
./run-docker.sh

# Windows
run-docker.bat
```

### Ручной запуск

```bash
# Сборка образа
docker build -t ball-game .

# Запуск контейнера
docker run -it --rm ball-game
```

### Запуск с графическим интерфейсом (Linux)

```bash
# Разрешить подключение к X11
xhost +local:docker

# Запустить контейнер
docker run -it --rm \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  ball-game

# Восстановить настройки
xhost -local:docker
```

## Устранение неполадок

### Ошибка "Docker not found"
- Убедитесь, что Docker установлен и запущен
- Перезапустите терминал после установки

### Ошибка "Permission denied" (Linux)
```bash
sudo usermod -aG docker $USER
# Перезапустите терминал
```

### Ошибка "Cannot connect to the Docker daemon"
```bash
# Запустите Docker сервис
sudo systemctl start docker
sudo systemctl enable docker
```

### Графический интерфейс не работает
- **Linux**: Проверьте, что X11 сервер запущен
- **macOS**: Убедитесь, что XQuartz установлен и запущен
- **Windows**: Используется виртуальный дисплей

### Ошибка "No space left on device"
```bash
# Очистите неиспользуемые образы
docker system prune -a
```

## Полезные команды Docker

```bash
# Посмотреть запущенные контейнеры
docker ps

# Посмотреть все контейнеры
docker ps -a

# Остановить контейнер
docker stop <container_id>

# Удалить контейнер
docker rm <container_id>

# Посмотреть образы
docker images

# Удалить образ
docker rmi <image_id>

# Очистить систему
docker system prune
```

## Альтернативный запуск без Docker

Если у вас проблемы с Docker, вы можете запустить игру локально:

```bash
# Установите Python зависимости
pip install pygame

# Запустите игру
python gui.py
``` 