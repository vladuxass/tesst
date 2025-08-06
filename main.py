from logic import GameLogic, Color
import time

def main():
    """Простой пример использования игровой логики"""
    
    # Создаём игровую логику
    game = GameLogic(screen_width=800, screen_height=600)
    
    print("Игровая логика инициализирована!")
    print(f"Начальное количество шариков: {len(game.get_balls())}")
    print(f"Зона удаления: {game.get_delete_zone()}")
    
    # Симулируем несколько кадров игры
    dt = 1/60  # 60 FPS
    
    for frame in range(300):  # 5 секунд при 60 FPS
        # Обновляем игровое состояние
        game.update(dt)
        
        # Каждую секунду выводим информацию
        if frame % 60 == 0:
            balls = game.get_balls()
            inventory = game.get_inventory()
            print(f"Кадр {frame//60}: Шариков на экране: {len(balls)}, В инвентаре: {len(inventory)}")
            
            # Показываем цвета шариков на экране
            if balls:
                colors = [f"RGB{ball.color}" for ball in balls[:3]]  # Показываем первые 3
                print(f"  Цвета шариков: {colors}")
        
        # Симулируем всасывание на 2-й секунде
        if frame == 120:  # 2 секунда
            print("\nНачинаем всасывание...")
            game.set_mouse_position(400, 300)  # Центр экрана
            game.start_sucking()
        
        # Останавливаем всасывание на 3-й секунде
        if frame == 180:  # 3 секунда
            print("Останавливаем всасывание...")
            game.stop_sucking()
            
        # Симулируем выплёвывание на 4-й секунде
        if frame == 240:  # 4 секунда
            print("Выплёвываем шарики...")
            game.set_mouse_position(200, 200)
            game.set_mouse_direction(1, 0)  # Вправо
            game.start_spitting()
            
        # Останавливаем выплёвывание
        if frame == 241:
            game.stop_spitting()
    
    print(f"\nИгра завершена!")
    print(f"Финальное количество шариков: {len(game.get_balls())}")
    print(f"Шариков в инвентаре: {len(game.get_inventory())}")

if __name__ == "__main__":
    main()