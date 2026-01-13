import pygame

# Start pygame
pygame.init()

# Screen size
WIDTH = 500
HEIGHT = 350
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Project")

clock = pygame.time.Clock()

# Colors
BACKGROUND = (80, 160, 200)
BOX_COLOR = (240, 220, 120)
PLAYER_COLOR = (200, 80, 80)

# Box in the middle
box = pygame.Rect(160, 115, 180, 120)

# Player (circle)
player = pygame.Vector2(250, 175)
target = pygame.Vector2(player)
speed = 4

running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            target = pygame.Vector2(event.pos)

    # Move player toward target
    if player.distance_to(target) > speed:
        player += (target - player).normalize() * speed
    else:
        player = target

    # Draw everything
    screen.fill(BACKGROUND)
    pygame.draw.rect(screen, BOX_COLOR, box)
    pygame.draw.circle(screen, PLAYER_COLOR, player, 15)

    pygame.display.flip()

pygame.quit()