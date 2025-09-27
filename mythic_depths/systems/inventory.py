from mythic_depths.config.config import TILE_SIZE
from mythic_depths.systems import items

class Inventory:
    """
    Manages the player's inventory of items.

    Attributes:
        items (dict): A dictionary of item names and their quantities.
    """

    def __init__(self):
        self.items = {}

    def add_item(self, item):
        """
        Add an item to the inventory.

        Args:
            item: The item to add.
        """
        self.items[item.name] = self.items.get(item.name, 0) + 1
