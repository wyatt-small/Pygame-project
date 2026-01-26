import pygame

class Obstacle:
    def __init__(self, rect, image):
        self.rect = rect
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    def blocks_circle(self, circle_pos, radius):
        closest_x = max(self.rect.left, min(circle_pos.x, self.rect.right))
        closest_y = max(self.rect.top, min(circle_pos.y, self.rect.bottom))

        dx = circle_pos.x - closest_x
        dy = circle_pos.y - closest_y

        return (dx * dx + dy * dy) < (radius * radius)