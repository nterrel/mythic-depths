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
    """
    A door that connects two rooms or areas. Supports bidirectional traversal and is reusable.
    """

    def __init__(self, x, y, connected_rooms=None):
        super().__init__(x, y, "Door", action=self.open)
        self.connected_rooms = set(
            connected_rooms) if connected_rooms else set()
        self.opened = False  # For visual feedback

    def open(self, player, current_room):
        """Open the door and move player to the other connected room."""
        self.opened = True  # Set opened for visual feedback
        # Move to the other room in connected_rooms
        other_rooms = self.connected_rooms - {current_room}
        if other_rooms:
            target_room = next(iter(other_rooms))
            # Move player to center of target room
            center_x = (target_room.x // player.tile_size) + \
                (target_room.width // (2 * player.tile_size))
            center_y = (target_room.y // player.tile_size) + \
                (target_room.height // (2 * player.tile_size))
            player.x = center_x * player.tile_size
            player.y = center_y * player.tile_size
            return f"Player moved to room {getattr(target_room, 'room_id', '')} via door!"
        return "Door does not connect to another room."


class Portal(Interactable):
    """
    A one-way portal for plane/level transition. Works only once, deactivates after use, and does not create a return portal.
    Attributes:
        destination_x, destination_y: Where the portal sends the player
        target_plane, target_level: For future progression system (optional)
    """

    def __init__(self, x, y, destination_x, destination_y, target_plane=None, target_level=None):
        super().__init__(x, y, "Portal", action=self.activate)
        self.destination_x = destination_x
        self.destination_y = destination_y
        self.target_plane = target_plane
        self.target_level = target_level
        self.used = False
        self.opened = False  # For visual feedback

    def activate(self, player):
        """Teleport the player to a new plane/level and deactivate the portal. No return portal is created."""
        if not self.used:
            player.x = self.destination_x * player.tile_size
            player.y = self.destination_y * player.tile_size
            # Future: handle plane/level transition logic here
            self.used = True
            self.active = False
            self.opened = True  # For visual feedback
            return f"Player teleported to ({self.destination_x}, {self.destination_y}) on plane {self.target_plane}, level {self.target_level}!"
        return "Portal already used."
