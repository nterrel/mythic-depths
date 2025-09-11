class NPC:
    """Base class for non-player characters."""

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.dialogue = []

    def talk(self):
        """Return the NPC's dialogue."""
        if self.dialogue:
            return self.dialogue[0]
        return "..."
