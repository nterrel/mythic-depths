from mythic_depths.config.config import TILE_SIZE
from mythic_depths.systems.inventory import Inventory


class Player:
    """
    Represents the player character in the dungeon crawler game.

    Attributes:
        x (int): X-coordinate of the player.
        y (int): Y-coordinate of the player.
        tile_size (int): Size of the player's tile.
        speed (int): Movement speed of the player.
        name (str): Name of the player.
        health (int): Health points of the player.
        strength (int): Strength attribute of the player.
        inventory (Inventory): The player's inventory.
    """

    def __init__(self, x, y,
                 name: str = 'Fella',
                 health: int = 100,
                 strength: int = 10,
                 tile_size: int = 20):
        self.x = x
        self.y = y
        self.tile_size = tile_size
        self.speed = self.tile_size // 4
        self.name = name
        self.health = health
        self.strength = strength
        self.inventory = Inventory()

    def move(self, dx, dy, dungeon):
        """
        Move the player by dx, dy if no collision with walls.

        Args:
            dx (int): Change in x-direction.
            dy (int): Change in y-direction.
            dungeon: The dungeon object to check for collisions.
        """
        # Debug print to trace movement
        print(f"Attempting to move player: dx={dx}, dy={dy}")
        print(f"Player position before move: x={self.x}, y={self.y}")
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed
        print(f"New position: x={new_x}, y={new_y}")
        size = int(self.tile_size * 0.6)
        offset = (self.tile_size - size) // 2
        # Check all four corners for collision
        corners = [
            (new_x + offset, new_y + offset),
            (new_x + offset + size - 1, new_y + offset),
            (new_x + offset, new_y + offset + size - 1),
            (new_x + offset + size - 1, new_y + offset + size - 1)
        ]
        print(f"Collision check corners: {corners}")
        can_move = True
        for cx, cy in corners:
            grid_x = int(cx // self.tile_size)
            grid_y = int(cy // self.tile_size)
            # For InfiniteDungeon, get the room at this grid
            if hasattr(dungeon, 'get_room'):
                room_x = grid_x // dungeon.room_size
                room_y = grid_y // dungeon.room_size
                room = dungeon.get_room(room_x, room_y)
                # Check if inside room bounds
                rx0 = room.x // self.tile_size
                ry0 = room.y // self.tile_size
                rx1 = (room.x + room.width) // self.tile_size
                ry1 = (room.y + room.height) // self.tile_size
                if not (rx0 <= grid_x < rx1 and ry0 <= grid_y < ry1):
                    can_move = False
                    break
            else:
                # Static dungeon
                if not (0 <= grid_x < dungeon.width and 0 <= grid_y < dungeon.height):
                    can_move = False
                    break
                if dungeon.grid[grid_y][grid_x] != 1:
                    can_move = False
                    break
        if can_move:
            self.x = new_x
            self.y = new_y
        else:
            # Move as close as possible to the wall
            test_x = self.x + dx * self.speed
            test_corners_x = [
                (test_x + offset, self.y + offset),
                (test_x + offset + size - 1, self.y + offset),
                (test_x + offset, self.y + offset + size - 1),
                (test_x + offset + size - 1, self.y + offset + size - 1)
            ]
            can_move_x = True
            for cx, cy in test_corners_x:
                grid_x = int(cx // self.tile_size)
                grid_y = int(cy // self.tile_size)
                if hasattr(dungeon, 'get_room'):
                    room_x = grid_x // dungeon.room_size
                    room_y = grid_y // dungeon.room_size
                    room = dungeon.get_room(room_x, room_y)
                    rx0 = room.x // self.tile_size
                    ry0 = room.y // self.tile_size
                    rx1 = (room.x + room.width) // self.tile_size
                    ry1 = (room.y + room.height) // self.tile_size
                    if not (rx0 <= grid_x < rx1 and ry0 <= grid_y < ry1):
                        can_move_x = False
                        break
                else:
                    if not (0 <= grid_x < dungeon.width and 0 <= grid_y < dungeon.height):
                        can_move_x = False
                        break
                    if dungeon.grid[grid_y][grid_x] != 1:
                        can_move_x = False
                        break
            if can_move_x:
                self.x = test_x
            else:
                test_y = self.y + dy * self.speed
                test_corners_y = [
                    (self.x + offset, test_y + offset),
                    (self.x + offset + size - 1, test_y + offset),
                    (self.x + offset, test_y + offset + size - 1),
                    (self.x + offset + size - 1, test_y + offset + size - 1)
                ]
                can_move_y = True
                for cx, cy in test_corners_y:
                    grid_x = int(cx // self.tile_size)
                    grid_y = int(cy // self.tile_size)
                    if hasattr(dungeon, 'get_room'):
                        room_x = grid_x // dungeon.room_size
                        room_y = grid_y // dungeon.room_size
                        room = dungeon.get_room(room_x, room_y)
                        rx0 = room.x // self.tile_size
                        ry0 = room.y // self.tile_size
                        rx1 = (room.x + room.width) // self.tile_size
                        ry1 = (room.y + room.height) // self.tile_size
                        if not (rx0 <= grid_x < rx1 and ry0 <= grid_y < ry1):
                            can_move_y = False
                            break
                    else:
                        if not (0 <= grid_x < dungeon.width and 0 <= grid_y < dungeon.height):
                            can_move_y = False
                            break
                        if dungeon.grid[grid_y][grid_x] != 1:
                            can_move_y = False
                            break
                if can_move_y:
                    self.y = test_y
        # Simplify collision detection for static dungeons
        if not hasattr(dungeon, 'get_room'):
            if 0 <= new_x // self.tile_size < dungeon.width and 0 <= new_y // self.tile_size < dungeon.height:
                if dungeon.grid[new_y // self.tile_size][new_x // self.tile_size] == 1:
                    self.x = new_x
                    self.y = new_y
        # Debug print to show final position after move attempt
        print(f"Player position after move: x={self.x}, y={self.y}")


def initialize_player(dungeon):
    if dungeon.rooms:
        first_room = dungeon.rooms[0]
        center_x = (first_room.x // TILE_SIZE) + (first_room.width // (2 * TILE_SIZE))
        center_y = (first_room.y // TILE_SIZE) + (first_room.height // (2 * TILE_SIZE))
        return Player(center_x, center_y)
    return Player(0, 0)  # Default to (0, 0) if no rooms exist

# EOF
