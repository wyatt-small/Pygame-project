import pygame

class Inventory:
    def __init__(self):
        self.items = set()
        self.images = {}

    def add_item(self, name):
        self.items.add(name)

    def has_item(self, name):
        return name in self.items

    def set_image(self, name, image):
        self.images[name] = image

    def draw(self, screen):
        # Draw a simple inventory box in the top-left
        box_rect = pygame.Rect(8, 8, 44, 44)
        pygame.draw.rect(screen, (20, 20, 20), box_rect)        # dark box
        pygame.draw.rect(screen, (255, 255, 255), box_rect, 2)  # white outline

        # If we have a key, draw it inside the box
        if self.has_item("key") and "key" in self.images:
            screen.blit(self.images["key"], (18, 18))