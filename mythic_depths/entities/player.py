from mythic_depths.config.config import TILE_SIZE
from mythic_depths.systems.inventory import Inventory
from mythic_depths.systems.collision import can_move


class Player:
    """
    Represents the player character in the dungeon crawler game.

    Attributes:
        x (int): X-coordinate of the player.
        y (int): Y-coordinate of the player.
        tile_size (int): Size of the player's tile.
        speed (int): Movement speed of the player.
        name (str): Name of the player.
        health (int): Maximum health points of the player.
        strength (int): Strength attribute of the player.
        mana (int): Maximum mana points of the player.
        inventory (Inventory): The player's inventory.
    """

    def __init__(self, x, y,
                 name: str = 'Fella',
                 health: int = 100,
                 strength: int = 10,
                 mana: int = 50,
                 tile_size: int = 20):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.speed = self.tile_size // 4
        self.name = name
        self.max_health = max(0, health)
        self.health = self.max_health
        self.strength = strength
        self.max_mana = max(0, mana)
        self.mana = self.max_mana
        self.inventory = Inventory()

    # ------------------------------------------------------------------
    # Basic stat helpers
    def restore_health(self, amount: int) -> int:
        """Restore up to ``amount`` health and return the amount healed."""

        if amount <= 0 or self.max_health == 0:
            return 0
        previous = self.health
        self.health = min(self.max_health, self.health + amount)
        return self.health - previous

    def restore_mana(self, amount: int) -> int:
        """Restore up to ``amount`` mana and return the amount recovered."""

        if amount <= 0 or self.max_mana == 0:
            return 0
        previous = self.mana
        self.mana = min(self.max_mana, self.mana + amount)
        return self.mana - previous

    def move(self, dx, dy, dungeon):
        """
        Move the player by dx, dy if no collision with walls.

        Args:
            dx (int): Change in x-direction.
            dy (int): Change in y-direction.
            dungeon: The dungeon object to check for collisions.
        """
        if can_move(self, dx, dy, dungeon):
            self.x += dx * self.speed
            self.y += dy * self.speed


def initialize_player(dungeon):
    if dungeon.rooms:
        first_room = dungeon.rooms[0]
        center_x = (first_room.x // TILE_SIZE) + (first_room.width // (2 * TILE_SIZE))
        center_y = (first_room.y // TILE_SIZE) + (first_room.height // (2 * TILE_SIZE))
        return Player(center_x, center_y)
    return Player(0, 0)  # Default to (0, 0) if no rooms exist

# EOF
