import pygame
from obstacle import Obstacle
from key import Key
from door import Door
from inventory import Inventory

pygame.init()

# ----------------------------
# Window (what we see)
# ----------------------------
WIDTH, HEIGHT = 500, 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lesson 4 - Big World Camera!")
clock = pygame.time.Clock()

BACKGROUND = (80, 160, 200)

# ----------------------------
# World (big map)
# ----------------------------
WORLD_WIDTH, WORLD_HEIGHT = 2000, 2000

def clamp(value, low, high):
    return max(low, min(value, high))

# ----------------------------
# Load Images
# ----------------------------
player_img = pygame.image.load("assets/player.png").convert_alpha()
key_img = pygame.image.load("assets/key.png").convert_alpha()
obstacle_img = pygame.image.load("assets/obstacle.png").convert_alpha()
door_img = pygame.image.load("assets/door.png").convert_alpha()

# Resize images so they fit nicely
player_img = pygame.transform.smoothscale(player_img, (30, 30))
key_img = pygame.transform.smoothscale(key_img, (24, 24))
door_img = pygame.transform.smoothscale(door_img, (60, 90))

# Reuse obstacle.png at different sizes
obstacle_big = pygame.transform.smoothscale(obstacle_img, (180, 120))
obstacle_small1 = pygame.transform.smoothscale(obstacle_img, (120, 60))
obstacle_small2 = pygame.transform.smoothscale(obstacle_img, (160, 50))

# ----------------------------
# Player (WORLD coordinates)
# ----------------------------
player_radius = 15
player_pos = pygame.Vector2(10, 10)     # IMPORTANT: safe start!
target_pos = pygame.Vector2(player_pos)
player_speed = 220

# ----------------------------
# Inventory
# ----------------------------
inventory = Inventory()
inventory.set_image("key", key_img)

# ----------------------------
# Obstacles (WORLD coordinates)
# Put some obstacles OFF SCREEN so we have to travel to see them!
# ----------------------------
obstacles = [
    Obstacle(pygame.Rect(300, 200, 180, 120), obstacle_big),
    Obstacle(pygame.Rect(900, 700, 120, 60), obstacle_small1),
    Obstacle(pygame.Rect(1500, 400, 160, 50), obstacle_small2),
    Obstacle(pygame.Rect(400, 1500, 160, 50), obstacle_small2),
]

# ----------------------------
# Key (WORLD coordinates)
# Put it far away so the camera scrolling is obvious
# ----------------------------
key = Key((1700, 300), key_img)

# ----------------------------
# Door (WORLD coordinates)
# Put it somewhere different than the key so we explore
# ----------------------------
door = Door(pygame.Rect(1850, 1700, 60, 90), door_img)

def is_blocked(pos):
    for obs in obstacles:
        if obs.blocks_circle(pos, player_radius):
            return True
    if door.blocks_circle(pos, player_radius):
        return True
    return False

running = True

while running:
    dt = clock.tick(60) / 1000

    # ----------------------------
    # Camera (WORLD -> SCREEN)
    # Try to keep player in the center, but stop at world edges.
    # ----------------------------
    camera_x = clamp(player_pos.x - WIDTH / 2, 0, WORLD_WIDTH - WIDTH)
    camera_y = clamp(player_pos.y - HEIGHT / 2, 0, WORLD_HEIGHT - HEIGHT)
    camera = pygame.Vector2(camera_x, camera_y)

    # ----------------------------
    # Events
    # ----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Click is in SCREEN coordinates
            mouse_screen = pygame.Vector2(event.pos)

            # Convert screen click -> world click
            target_pos = mouse_screen + camera

    # ----------------------------
    # Movement (WORLD coordinates)
    # ----------------------------
    to_target = target_pos - player_pos
    distance = to_target.length()

    if distance > 1:
        direction = to_target.normalize()
        step = player_speed * dt

        if step >= distance:
            new_pos = pygame.Vector2(target_pos)
        else:
            new_pos = player_pos + direction * step

        # Keep player inside the world boundaries
        new_pos.x = clamp(new_pos.x, 0, WORLD_WIDTH)
        new_pos.y = clamp(new_pos.y, 0, WORLD_HEIGHT)

        if not is_blocked(new_pos):
            player_pos = new_pos
        else:
            # Sliding around obstacles/door
            slide_x = pygame.Vector2(player_pos.x + direction.x * step, player_pos.y)
            slide_y = pygame.Vector2(player_pos.x, player_pos.y + direction.y * step)

            slide_x.x = clamp(slide_x.x, 0, WORLD_WIDTH)
            slide_x.y = clamp(slide_x.y, 0, WORLD_HEIGHT)

            slide_y.x = clamp(slide_y.x, 0, WORLD_WIDTH)
            slide_y.y = clamp(slide_y.y, 0, WORLD_HEIGHT)

            if not is_blocked(slide_x):
                player_pos = slide_x
            elif not is_blocked(slide_y):
                player_pos = slide_y

    # ----------------------------
    # Pick up key (WORLD coordinates)
    # ----------------------------
    if not key.collected and key.touches_circle(player_pos, player_radius):
        key.collect()
        inventory.add_item("key")

    # ----------------------------
    # Door open logic
    # ----------------------------
    door.try_open(player_pos, player_radius, inventory.has_item("key"))

    # ----------------------------
    # Draw (use camera!)
    # ----------------------------
    screen.fill(BACKGROUND)

    for obs in obstacles:
        obs.draw(screen, camera)

    key.draw(screen, camera)
    door.draw(screen, camera)

    # Draw player using camera conversion
    player_screen_x = player_pos.x - camera.x
    player_screen_y = player_pos.y - camera.y
    player_rect = player_img.get_rect(center=(int(player_screen_x), int(player_screen_y)))
    screen.blit(player_img, player_rect.topleft)

    # Inventory is UI (no camera)
    inventory.draw(screen)

    pygame.display.flip()

pygame.quit()