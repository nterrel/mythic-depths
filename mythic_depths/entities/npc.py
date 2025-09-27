class NPC:
    """
    Represents a non-player character (NPC) in the game.

    Attributes:
        name (str): The name of the NPC.
        x (int): X-coordinate of the NPC.
        y (int): Y-coordinate of the NPC.
        dialogue (list): List of dialogue strings for the NPC.
    """

    def __init__(self, name, x, y):
        """Initialize an NPC with a name, x and y coordinates."""
        self.name = name
        self.x = x
        self.y = y
        self.dialogue = []

    def talk(self):
        """
        Return the NPC's dialogue.

        Returns:
            str: The first dialogue string, or "..." if no dialogue is available.
        """
        if self.dialogue:
            return self.dialogue[0]
        return "..."
