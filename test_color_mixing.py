from logic import Ball, Vector2D

def test_color_mixing():
    """Тестирует математическое смешивание цветов"""
    
    print("=== Тест математического смешивания цветов ===\n")
    
    # Создаём шарики с разными цветами
    test_cases = [
        ("Красный", (255, 0, 0)),
        ("Зелёный", (0, 255, 0)),
        ("Синий", (0, 0, 255)),
        ("Жёлтый", (255, 255, 0)),
        ("Пурпурный", (255, 0, 255)),
        ("Голубой", (0, 255, 255)),
        ("Белый", (255, 255, 255)),
        ("Чёрный", (0, 0, 0)),
        ("Оранжевый", (255, 165, 0)),
        ("Розовый", (255, 192, 203))
    ]
    
    # Создаём шарики
    balls = []
    for name, color in test_cases:
        ball = Ball(
            position=Vector2D(0, 0),
            velocity=Vector2D(0, 0),
            color=color
        )
        balls.append((name, ball))
    
    # Тестируем смешивание всех комбинаций
    print("Результаты смешивания цветов:")
    print("-" * 60)
    
    for i, (name1, ball1) in enumerate(balls):
        for j, (name2, ball2) in enumerate(balls[i+1:], i+1):
            mixed_color = ball1.mix_colors_with(ball2)
            
            print(f"{name1:12} + {name2:12} = RGB{mixed_color}")
            
            # Показываем компоненты
            r, g, b = mixed_color
            print(f"              R:{r:3d} G:{g:3d} B:{b:3d}")
            print()
    
    # Демонстрация цепочки смешивания
    print("=== Демонстрация цепочки смешивания ===")
    print()
    
    # Начинаем с красного и синего
    current_ball = Ball(
        position=Vector2D(0, 0),
        velocity=Vector2D(0, 0),
        color=(255, 0, 0)  # Красный
    )
    
    colors_to_mix = [
        ("Синий", (0, 0, 255)),
        ("Зелёный", (0, 255, 0)),
        ("Жёлтый", (255, 255, 0)),
        ("Пурпурный", (255, 0, 255))
    ]
    
    print(f"Начальный цвет: RGB{current_ball.color}")
    
    for name, color in colors_to_mix:
        temp_ball = Ball(
            position=Vector2D(0, 0),
            velocity=Vector2D(0, 0),
            color=color
        )
        
        new_color = current_ball.mix_colors_with(temp_ball)
        print(f"Смешиваем с {name:12} = RGB{new_color}")
        current_ball.color = new_color
    
    print(f"\nФинальный цвет: RGB{current_ball.color}")

if __name__ == "__main__":
    test_color_mixing() 