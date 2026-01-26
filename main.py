import pygame
from obstacle import Obstacle
from key import Key
from door import Door

pygame.init()

WIDTH, HEIGHT = 500, 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Project - Inventory & Door")
clock = pygame.time.Clock()

# Background color (still useful!)
BACKGROUND = (80, 160, 200)

# ----------------------------
# Load Images
# ----------------------------
player_img = pygame.image.load("assets/player.png").convert_alpha()
key_img = pygame.image.load("assets/key.png").convert_alpha()
obstacle_img = pygame.image.load("assets/obstacle.png").convert_alpha()
door_img = pygame.image.load("assets/door.png").convert_alpha()

# (Optional) Resize images so they fit nicely
player_img = pygame.transform.smoothscale(player_img, (30, 30))
key_img = pygame.transform.smoothscale(key_img, (24, 24))
obstacle_img = pygame.transform.smoothscale(obstacle_img, (180, 120))
door_img = pygame.transform.smoothscale(door_img, (60, 90))

# ----------------------------
# Player
# ----------------------------
player_radius = 15
player_pos = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
target_pos = pygame.Vector2(player_pos)
player_speed = 220

# Inventory
has_key = False

# ----------------------------
# Obstacles
# ----------------------------
obstacles = [
    Obstacle(pygame.Rect(160, 115, 180, 120), obstacle_img),
    Obstacle(pygame.Rect(60, 60, 90, 40), pygame.transform.smoothscale(obstacle_img, (90, 40))),
    Obstacle(pygame.Rect(360, 260, 100, 50), pygame.transform.smoothscale(obstacle_img, (100, 50))),
]

# ----------------------------
# Key
# ----------------------------
key = Key((430, 80), key_img)

# ----------------------------
# Door (starts locked)
# ----------------------------
door_rect = pygame.Rect(30, 200, 60, 90)
door = Door(door_rect, door_img)

# We'll treat the door like an obstacle too (when it's closed)
def is_blocked(pos):
    # blocked by obstacles?
    for obs in obstacles:
        if obs.blocks_circle(pos, player_radius):
            return True

    # blocked by door?
    if door.blocks_circle(pos, player_radius):
        return True

    return False

running = True

while running:
    dt = clock.tick(60) / 1000

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            target_pos = pygame.Vector2(event.pos)

    # Movement
    to_target = target_pos - player_pos
    distance = to_target.length()

    if distance > 1:
        direction = to_target.normalize()
        step = player_speed * dt

        if step >= distance:
            new_pos = pygame.Vector2(target_pos)
        else:
            new_pos = player_pos + direction * step

        if not is_blocked(new_pos):
            player_pos = new_pos
        else:
            # Sliding around stuff
            slide_x = pygame.Vector2(player_pos.x + direction.x * step, player_pos.y)
            slide_y = pygame.Vector2(player_pos.x, player_pos.y + direction.y * step)

            if not is_blocked(slide_x):
                player_pos = slide_x
            elif not is_blocked(slide_y):
                player_pos = slide_y

    # Pick up key
    if not key.collected and key.touches_circle(player_pos, player_radius):
        key.collect()
        has_key = True

    # Try opening the door (only works if you have the key)
    door.try_open(player_pos, player_radius, has_key)

    # Draw
    screen.fill(BACKGROUND)

    for obs in obstacles:
        obs.draw(screen)

    key.draw(screen)
    door.draw(screen)

    # Draw player image centered on player_pos
    player_rect = player_img.get_rect(center=(int(player_pos.x), int(player_pos.y)))
    screen.blit(player_img, player_rect.topleft)

    # ----------------------------
    # Inventory (top-left)
    # ----------------------------
    if has_key:
        # Draw the key image in the inventory corner
        screen.blit(key_img, (10, 10))

    pygame.display.flip()

pygame.quit()