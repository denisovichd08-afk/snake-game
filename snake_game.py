
import pygame
import sys
import random
import math

# --- Инициализация Pygame ---
pygame.init()

# --- Настройки экрана ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Плавная Змейка')

# --- Цвета ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 170, 0)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)

# --- Настройки игры ---
clock = pygame.time.Clock()
FPS = 60

# --- Параметры змейки ---
SNAKE_SPEED = 4
SNAKE_SIZE = 10  # Радиус сегмента
# Расстояние между центрами сегментов. Чуть меньше диаметра для плавного перекрытия.
SEGMENT_DISTANCE = SNAKE_SIZE * 1.5 

# --- Шрифты ---
font = pygame.font.Font(None, 48)

def main():
    """Основной игровой цикл"""
    # --- Начальные условия ---
    
    # Создаем начальную змейку, вытянутую горизонтально
    snake_segments = [pygame.math.Vector2(SCREEN_WIDTH / 2 - i * SEGMENT_DISTANCE, SCREEN_HEIGHT / 2) for i in range(5)]
    
    # Генерируем еду
    food_pos = pygame.math.Vector2(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))
    
    score = 0
    game_over = False

    while not game_over:
        # --- Обработка событий ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- Управление ---
        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        head = snake_segments[0]

        # --- Логика движения ---
        # Вектор направления от головы к мыши
        direction = mouse_pos - head
        if direction.length() > 0:
            direction.normalize_ip()
        
        # Двигаем голову
        snake_segments[0] += direction * SNAKE_SPEED

        # Двигаем остальное тело (логика "веревки")
        for i in range(1, len(snake_segments)):
            leader = snake_segments[i-1]
            follower = snake_segments[i]
            
            dir_to_leader = leader - follower
            dist = dir_to_leader.length()
            
            # Если сегмент слишком отдалился, подтягиваем его
            if dist > SEGMENT_DISTANCE:
                dir_to_leader.normalize_ip()
                follower += dir_to_leader * (dist - SEGMENT_DISTANCE)
                snake_segments[i] = follower

        # --- Проверка столкновений ---
        # Со стенами
        if not (SNAKE_SIZE < head.x < SCREEN_WIDTH - SNAKE_SIZE and SNAKE_SIZE < head.y < SCREEN_HEIGHT - SNAKE_SIZE):
            game_over = True

        # С едой
        if head.distance_to(food_pos) < SNAKE_SIZE * 2:
            score += 1
            # Добавляем новый сегмент на место хвоста
            snake_segments.append(snake_segments[-1].copy())
            food_pos = pygame.math.Vector2(random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))

        # С собой (проверяем столкновение головы с сегментами дальше 3-го)
        for segment in snake_segments[3:]:
            if head.distance_to(segment) < SNAKE_SIZE:
                game_over = True
                break

        # --- Отрисовка ---
        screen.fill(BLACK)

        # Еда
        pygame.draw.circle(screen, RED, (int(food_pos.x), int(food_pos.y)), SNAKE_SIZE + 2)

        # Змейка (рисуем с хвоста, чтобы голова была сверху)
        for i in range(len(snake_segments) - 1, -1, -1):
            segment = snake_segments[i]
            color = DARK_GREEN if i % 2 == 0 else GREEN
            pygame.draw.circle(screen, color, (int(segment.x), int(segment.y)), SNAKE_SIZE)
        
        # Голова (рисуем поверх, чтобы была заметна)
        pygame.draw.circle(screen, (50, 255, 50), (int(head.x), int(head.y)), SNAKE_SIZE)

        # Счет
        score_text = font.render(f"Счет: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    # --- Экран конца игры ---
    game_over_text = font.render("Игра окончена!", True, RED)
    final_score_text = font.render(f"Ваш счет: {score}", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
