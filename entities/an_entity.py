# This contains the general entity class that all entities will inherit from.
import pygame
from ..config import TILE_SIZE
from ..systems.inventory import Inventory

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size=TILE_SIZE):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.inventory = Inventory()

    def update(self):
        pass