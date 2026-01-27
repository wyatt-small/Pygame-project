import pygame

class Obstacle:
    def __init__(self, rect, image):
        # rect is in WORLD coordinates
        self.rect = rect
        self.image = image

    def draw(self, screen, camera):
        # Convert world position -> screen position by subtracting camera
        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        screen.blit(self.image, (screen_x, screen_y))

    def blocks_circle(self, circle_pos, radius):
        # circle_pos is in WORLD coordinates
        closest_x = max(self.rect.left, min(circle_pos.x, self.rect.right))
        closest_y = max(self.rect.top, min(circle_pos.y, self.rect.bottom))

        dx = circle_pos.x - closest_x
        dy = circle_pos.y - closest_y

        return (dx * dx + dy * dy) < (radius * radius)