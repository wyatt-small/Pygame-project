import pygame

class Key:
    def __init__(self, pos, image):
        self.pos = pygame.Vector2(pos)
        self.image = image
        self.rect = self.image.get_rect(center=(int(self.pos.x), int(self.pos.y)))
        self.collected = False

    def draw(self, screen):
        if not self.collected:
            screen.blit(self.image, self.rect.topleft)

    def touches_circle(self, circle_pos, radius):
        # Treat key as a point at its center
        dx = circle_pos.x - self.rect.centerx
        dy = circle_pos.y - self.rect.centery
        return (dx * dx + dy * dy) < (radius * radius)

    def collect(self):
        self.collected = True