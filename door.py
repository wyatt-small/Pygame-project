import pygame

class Door:
    def __init__(self, rect, image):
        self.rect = rect
        self.image = image
        self.locked = True
        self.open = False

    def draw(self, screen):
        # If the door is open, we just don't draw it
        if not self.open:
            screen.blit(self.image, self.rect.topleft)

    def blocks_circle(self, circle_pos, radius):
        # Only blocks you if it is NOT open
        if self.open:
            return False

        closest_x = max(self.rect.left, min(circle_pos.x, self.rect.right))
        closest_y = max(self.rect.top, min(circle_pos.y, self.rect.bottom))

        dx = circle_pos.x - closest_x
        dy = circle_pos.y - closest_y

        return (dx * dx + dy * dy) < (radius * radius)

    def try_open(self, player_pos, player_radius, has_key):
        # If you don't have a key, nothing happens
        if not has_key:
            return

        # If you do have a key AND you touch the door, open it
        if self.blocks_circle(player_pos, player_radius):
            self.locked = False
            self.open = True