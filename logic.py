import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

class Color(Enum):
    """Цвета шариков"""
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    MAGENTA = (255, 0, 255)
    CYAN = (0, 255, 255)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)

@dataclass
class Vector2D:
    """2D вектор для позиции и скорости"""
    x: float
    y: float
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: float) -> 'Vector2D':
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def magnitude(self) -> float:
        return math.sqrt(self.x**2 + self.y**2)
    
    def normalize(self) -> 'Vector2D':
        mag = self.magnitude()
        if mag == 0:
            return Vector2D(0, 0)
        return Vector2D(self.x / mag, self.y / mag)
    
    def distance_to(self, other: 'Vector2D') -> float:
        return (self - other).magnitude()

@dataclass
class Ball:
    """Класс шарика"""
    position: Vector2D
    velocity: Vector2D
    color: tuple  # RGB цвет как кортеж (r, g, b)
    radius: float = 15.0
    mass: float = 1.0
    
    def update_position(self, dt: float, screen_width: float, screen_height: float):
        """Обновляет позицию шарика с учётом границ экрана"""
        # Обновляем позицию
        self.position += self.velocity * dt
        
        # Отскок от границ экрана
        if self.position.x - self.radius <= 0:
            self.position.x = self.radius
            self.velocity.x = abs(self.velocity.x)
        elif self.position.x + self.radius >= screen_width:
            self.position.x = screen_width - self.radius
            self.velocity.x = -abs(self.velocity.x)
            
        if self.position.y - self.radius <= 0:
            self.position.y = self.radius
            self.velocity.y = abs(self.velocity.y)
        elif self.position.y + self.radius >= screen_height:
            self.position.y = screen_height - self.radius
            self.velocity.y = -abs(self.velocity.y)
    
    def is_colliding_with(self, other: 'Ball') -> bool:
        """Проверяет столкновение с другим шариком"""
        distance = self.position.distance_to(other.position)
        return distance < (self.radius + other.radius)
    
    def mix_colors_with(self, other: 'Ball') -> tuple:
        """Смешивает цвета двух шариков математически"""
        color1 = self.color
        color2 = other.color
        
        # Математическое смешивание RGB компонентов
        # Используем взвешенное среднее (можно настроить веса)
        mixed_r = int((color1[0] + color2[0]) / 2)
        mixed_g = int((color1[1] + color2[1]) / 2)
        mixed_b = int((color1[2] + color2[2]) / 2)
        
        # Ограничиваем значения в диапазоне 0-255
        mixed_r = max(0, min(255, mixed_r))
        mixed_g = max(0, min(255, mixed_g))
        mixed_b = max(0, min(255, mixed_b))
        
        return (mixed_r, mixed_g, mixed_b)

class GameLogic:
    """Основной класс игровой логики"""
    
    def __init__(self, screen_width: float = 800, screen_height: float = 600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.balls: List[Ball] = []
        self.inventory: List[Ball] = []
        self.mouse_position = Vector2D(0, 0)
        self.is_sucking = False
        self.is_spitting = False
        
        # Зона удаления (правый верхний угол)
        self.delete_zone = {
            'x': screen_width - 100,
            'y': 0,
            'width': 100,
            'height': 100
        }
        
        # Параметры всасывания
        self.suck_radius = 50.0
        self.suck_force = 200.0
        
        # Параметры выплёвывания
        self.spit_force = 300.0
        
        # Инициализируем начальные шарики
        self._initialize_balls()
    
    def _initialize_balls(self, num_balls: int = 8):
        """Создаёт начальные шарики на экране"""
        for _ in range(num_balls):
            x = random.uniform(50, self.screen_width - 50)
            y = random.uniform(50, self.screen_height - 50)
            
            # Случайная скорость
            vx = random.uniform(-100, 100)
            vy = random.uniform(-100, 100)
            
            # Случайный RGB цвет
            color = (
                random.randint(50, 255),  # Красный компонент
                random.randint(50, 255),  # Зелёный компонент
                random.randint(50, 255)   # Синий компонент
            )
            
            ball = Ball(
                position=Vector2D(x, y),
                velocity=Vector2D(vx, vy),
                color=color
            )
            self.balls.append(ball)
    
    def update(self, dt: float):
        """Обновляет игровое состояние"""
        # Обновляем позиции всех шариков
        for ball in self.balls:
            ball.update_position(dt, self.screen_width, self.screen_height)
        
        # Обрабатываем всасывание
        if self.is_sucking:
            self._handle_sucking(dt)
        
        # Обрабатываем выплёвывание
        if self.is_spitting:
            self._handle_spitting()
        
        # Проверяем столкновения между шариками
        self._handle_collisions()
        
        # Проверяем зону удаления
        self._check_delete_zone()
    
    def _handle_sucking(self, dt: float):
        """Обрабатывает всасывание шариков мышкой"""
        for ball in self.balls[:]:  # Копируем список для безопасного удаления
            distance = ball.position.distance_to(self.mouse_position)
            
            if distance < self.suck_radius:
                # Применяем силу всасывания
                direction = (self.mouse_position - ball.position).normalize()
                ball.velocity += direction * self.suck_force * dt
                
                # Если шарик достаточно близко, добавляем в инвентарь
                if distance < ball.radius:
                    self.inventory.append(ball)
                    self.balls.remove(ball)
    
    def _handle_spitting(self):
        """Обрабатывает выплёвывание шариков из инвентаря"""
        if self.inventory and self.is_spitting:
            ball = self.inventory.pop()
            
            # Позиция выплёвывания (немного впереди мыши)
            spit_direction = Vector2D(1, 0)  # По умолчанию вправо
            if hasattr(self, 'mouse_direction'):
                spit_direction = self.mouse_direction
            
            # Устанавливаем позицию и скорость
            ball.position = self.mouse_position + spit_direction * 30
            ball.velocity = spit_direction * self.spit_force
            
            # Добавляем обратно на экран
            self.balls.append(ball)
    
    def _handle_collisions(self):
        """Обрабатывает столкновения между шариками"""
        for i in range(len(self.balls)):
            for j in range(i + 1, len(self.balls)):
                ball1 = self.balls[i]
                ball2 = self.balls[j]
                
                if ball1.is_colliding_with(ball2):
                    # Смешиваем цвета математически
                    new_color = ball1.mix_colors_with(ball2)
                    ball1.color = new_color
                    ball2.color = new_color
                    
                    # Шарики не отталкиваются, просто продолжают движение
                    # Можно добавить небольшое изменение траектории для реалистичности
                    if random.random() < 0.3:  # 30% шанс изменения направления
                        ball1.velocity = Vector2D(
                            random.uniform(-100, 100),
                            random.uniform(-100, 100)
                        )
                        ball2.velocity = Vector2D(
                            random.uniform(-100, 100),
                            random.uniform(-100, 100)
                        )
    
    def _check_delete_zone(self):
        """Проверяет шарики в зоне удаления"""
        for ball in self.balls[:]:
            if (self.delete_zone['x'] <= ball.position.x <= self.delete_zone['x'] + self.delete_zone['width'] and
                self.delete_zone['y'] <= ball.position.y <= self.delete_zone['y'] + self.delete_zone['height']):
                self.balls.remove(ball)
    
    def set_mouse_position(self, x: float, y: float):
        """Устанавливает позицию мыши"""
        self.mouse_position = Vector2D(x, y)
    
    def set_mouse_direction(self, dx: float, dy: float):
        """Устанавливает направление мыши для выплёвывания"""
        self.mouse_direction = Vector2D(dx, dy).normalize()
    
    def start_sucking(self):
        """Начинает всасывание"""
        self.is_sucking = True
    
    def stop_sucking(self):
        """Останавливает всасывание"""
        self.is_sucking = False
    
    def start_spitting(self):
        """Начинает выплёвывание"""
        self.is_spitting = True
    
    def stop_spitting(self):
        """Останавливает выплёвывание"""
        self.is_spitting = False
    
    def add_ball(self, x: float, y: float, color: Optional[tuple] = None):
        """Добавляет новый шарик на экран"""
        if color is None:
            color = (
                random.randint(50, 255),  # Красный компонент
                random.randint(50, 255),  # Зелёный компонент
                random.randint(50, 255)   # Синий компонент
            )
        
        ball = Ball(
            position=Vector2D(x, y),
            velocity=Vector2D(random.uniform(-50, 50), random.uniform(-50, 50)),
            color=color
        )
        self.balls.append(ball)
    
    def get_balls(self) -> List[Ball]:
        """Возвращает список всех шариков на экране"""
        return self.balls
    
    def get_inventory(self) -> List[Ball]:
        """Возвращает список шариков в инвентаре"""
        return self.inventory
    
    def get_delete_zone(self) -> dict:
        """Возвращает параметры зоны удаления"""
        return self.delete_zone
    
    def clear_inventory(self):
        """Очищает инвентарь"""
        self.inventory.clear()
    
    def get_inventory_count(self) -> int:
        """Возвращает количество шариков в инвентаре"""
        return len(self.inventory) 