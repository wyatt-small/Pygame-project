import pygame

class Obstacle:
    def __init__(self, rect, color):
        self.rect = rect
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def blocks_circle(self, circle_pos, radius):
        """
        Returns True if a circle is touching this obstacle.
        The obstacle does the math, so main.py stays simple.
        """
        closest_x = max(self.rect.left, min(circle_pos.x, self.rect.right))
        closest_y = max(self.rect.top, min(circle_pos.y, self.rect.bottom))

        dx = circle_pos.x - closest_x
        dy = circle_pos.y - closest_y

        return (dx * dx + dy * dy) < (radius * radius)