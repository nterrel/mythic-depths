# Here is where you can define item attributes.
# Example items:
class Item:
    """Base class for items."""

    def __init__(self, name):
        self.name = name


class HealthPotion(Item):
    """Restores player health."""

    def __init__(self):
        super().__init__("Health Potion")


class ArcanePotion(Item):
    """Restores player magic."""

    def __init__(self):
        super().__init__("Arcane Potion")
