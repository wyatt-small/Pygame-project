import pygame

class Key:
    def __init__(self, pos, size, color):
        self.pos = pygame.Vector2(pos)
        self.size = size
        self.color = color
        self.collected = False

    def triangle_points(self):
        x, y = self.pos.x, self.pos.y
        s = self.size
        return [
            (x, y - s),     # top point
            (x - s, y + s), # bottom left
            (x + s, y + s), # bottom right
        ]

    def draw(self, screen):
        if not self.collected:
            pygame.draw.polygon(screen, self.color, self.triangle_points())

    def touches_circle(self, circle_pos, radius):
        """
        Simple collision: treat the key like a point in the middle.
        If the player circle touches that point, you got the key!
        """
        dx = circle_pos.x - self.pos.x
        dy = circle_pos.y - self.pos.y
        return (dx * dx + dy * dy) < (radius * radius)