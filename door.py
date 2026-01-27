import pygame

class Door:
    def __init__(self, rect, image):
        # rect is in WORLD coordinates
        self.rect = rect
        self.image = image
        self.locked = True
        self.open = False

    def draw(self, screen, camera):
        if self.open:
            return

        screen_x = self.rect.x - camera.x
        screen_y = self.rect.y - camera.y
        screen.blit(self.image, (screen_x, screen_y))

    def blocks_circle(self, circle_pos, radius):
        if self.open:
            return False

        closest_x = max(self.rect.left, min(circle_pos.x, self.rect.right))
        closest_y = max(self.rect.top, min(circle_pos.y, self.rect.bottom))

        dx = circle_pos.x - closest_x
        dy = circle_pos.y - closest_y

        return (dx * dx + dy * dy) < (radius * radius)

    def try_open(self, player_pos, player_radius, has_key):
        if not has_key:
            return

        # If you touch the door and you have the key, it opens!
        if self.blocks_circle(player_pos, player_radius):
            self.locked = False
            self.open = True