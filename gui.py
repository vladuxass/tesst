#!/usr/bin/env python3
"""
Точка входа для игры про шарики
Запускает улучшенную версию игры с графическим интерфейсом
"""

import sys
import os

# Добавляем текущую директорию в путь для импорта
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from game_enhanced import main as run_enhanced_game
    print("Запуск улучшенной версии игры...")
    run_enhanced_game()
except ImportError:
    try:
        from game import main as run_basic_game
        print("Запуск базовой версии игры...")
        run_basic_game()
    except ImportError as e:
        print("Ошибка: Не удалось импортировать игровые модули")
        print(f"Детали: {e}")
        print("\nУбедитесь, что файлы game.py или game_enhanced.py находятся в той же папке")
        sys.exit(1)
except Exception as e:
    print(f"Ошибка при запуске игры: {e}")
    sys.exit(1) 