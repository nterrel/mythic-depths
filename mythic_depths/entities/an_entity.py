# This contains the general entity class that all entities will inherit from.
import pygame
from mythic_depths.config.config import TILE_SIZE
from mythic_depths.systems.inventory import Inventory


class Entity(pygame.sprite.Sprite):
    """
    Base class for all entities in the game.

    Attributes:
        x (int): X-coordinate of the entity.
        y (int): Y-coordinate of the entity.
        tile_size (int): Size of the entity's tile.
        inventory (Inventory): The entity's inventory.
    """

    def __init__(self, x, y, tile_size=TILE_SIZE):
        super().__init__()
        self.image = pygame.Surface((tile_size, tile_size))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.inventory = Inventory()

    def update(self):
        """Update the entity's state."""
        pass
