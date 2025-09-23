import items

class Inventory:
    """Manages the player's inventory of items."""

    def __init__(self):
        self.items = {}

    def add_item(self, item):
        """Add an item to the inventory."""
        self.items[item.name] = self.items.get(item.name, 0) + 1
