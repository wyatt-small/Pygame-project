import pygame
from obstacle import Obstacle
from key import Key

# ----------------------------
# Setup
# ----------------------------
pygame.init()

WIDTH, HEIGHT = 500, 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Project - Obstacles & Key")

clock = pygame.time.Clock()

# Colors
BACKGROUND = (80, 160, 200)
OBSTACLE_COLOR = (240, 220, 120)
PLAYER_COLOR = (200, 80, 80)
KEY_COLOR = (60, 220, 90)

# Player (circle)
player_radius = 15
player_pos = pygame.Vector2(10, 10)
target_pos = pygame.Vector2(player_pos)
player_speed = 220  # pixels per second

# ----------------------------
# Obstacles (3 boxes)
# ----------------------------
obstacles = [
    # middle obstacle
    Obstacle(pygame.Rect(160, 115, 180, 120), OBSTACLE_COLOR),

    # extra obstacles
    Obstacle(pygame.Rect(60, 60, 90, 40), OBSTACLE_COLOR),
    Obstacle(pygame.Rect(360, 260, 100, 50), OBSTACLE_COLOR),
]

# ----------------------------
# Key (triangle)
# ----------------------------
key = Key((430, 80), 12, KEY_COLOR)

running = True

# ----------------------------
# Game Loop
# ----------------------------
while running:
    dt = clock.tick(60) / 1000  # seconds since last frame

    # ------------------------
    # Events
    # ------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            target_pos = pygame.Vector2(event.pos)

    # ------------------------
    # Movement (click-to-move)
    # ------------------------
    to_target = target_pos - player_pos
    distance = to_target.length()

    if distance > 1:
        direction = to_target.normalize()
        step = player_speed * dt

        # Try moving to a new spot
        if step >= distance:
            new_pos = pygame.Vector2(target_pos)
        else:
            new_pos = player_pos + direction * step

        # Ask the obstacles if they block the new position
        blocked = any(obs.blocks_circle(new_pos, player_radius) for obs in obstacles)

        if not blocked:
            player_pos = new_pos
        else:
            # If blocked, try sliding around the obstacle
            slide_x = pygame.Vector2(player_pos.x + direction.x * step, player_pos.y)
            slide_y = pygame.Vector2(player_pos.x, player_pos.y + direction.y * step)

            can_x = all(not obs.blocks_circle(slide_x, player_radius) for obs in obstacles)
            can_y = all(not obs.blocks_circle(slide_y, player_radius) for obs in obstacles)

            if can_x:
                player_pos = slide_x
            elif can_y:
                player_pos = slide_y
            # else: stuck this frame

    # ------------------------
    # Key pickup
    # ------------------------
    if not key.collected and key.touches_circle(player_pos, player_radius):
        key.collected = True

    # ------------------------
    # Draw
    # ------------------------
    screen.fill(BACKGROUND)

    for obs in obstacles:
        obs.draw(screen)

    key.draw(screen)

    pygame.draw.circle(
        screen,
        PLAYER_COLOR,
        (int(player_pos.x), int(player_pos.y)),
        player_radius
    )

    pygame.display.flip()

pygame.quit()