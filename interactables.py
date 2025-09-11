class Interactable:
    """Base class for interactable objects in the dungeon."""

    def __init__(self, x, y, name, action=None):
        self.x = x
        self.y = y
        self.name = name
        self.action = action  # Callable or string describing the action
        self.active = True

    def interact(self, player):
        """Trigger the interactable's action if active."""
        if self.action and self.active:
            return self.action(player)
        return None


class Door(Interactable):
    """A door that can be opened by the player."""

    def __init__(self, x, y, leads_to=None):
        super().__init__(x, y, "Door", action=self.open)
        self.leads_to = leads_to
        self.opened = False

    def open(self, player):
        """Open the door and allow passage."""
        self.opened = True
        self.active = False
        # Logic to connect rooms or allow passage
        return f"Door at ({self.x}, {self.y}) opened!"
