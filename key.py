import pygame

class Key:
    def __init__(self, pos, image):
        # pos is in WORLD coordinates
        self.pos = pygame.Vector2(pos)
        self.image = image
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.collected = False

    def draw(self, screen, camera):
        if self.collected:
            return

        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        screen.blit(self.image, (screen_x, screen_y))

    def touches_circle(self, circle_pos, radius):
        dx = circle_pos.x - self.rect.centerx
        dy = circle_pos.y - self.rect.centery
        return (dx * dx + dy * dy) < (radius * radius)

    def collect(self):
        self.collected = True