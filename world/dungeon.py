import pygame
import random
from config import TILE_SIZE


class Room:
    """
    Represents a room in the dungeon.
    Attributes:
        x (int): X position (in pixels)
        y (int): Y position (in pixels)
        width (int): Width (in pixels)
        height (int): Height (in pixels)
        tile_size (int): Size of each tile
        doors (list): List of doors in the room
        room_id (str): Unique identifier for the room
        metadata (dict): Additional room metadata (for mapping, type, etc)
    """

    def __init__(self, x, y, width, height, tile_size, room_id=None, metadata=None):
        self.x = x * tile_size
        self.y = y * tile_size
        self.width = width * tile_size
        self.height = height * tile_size
        self.tile_size = tile_size
        self.doors = []
        self.room_id = room_id if room_id else f"room_{x}_{y}"
        self.metadata = metadata if metadata else {}

    def get_shape(self):
        """Return the room's shape and position info for mapping."""
        return {
            "room_id": self.room_id,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "doors": [door for door in self.doors],
            "metadata": self.metadata
        }


class Dungeon:
    """
    Represents the dungeon grid and room/corridor logic.
    Attributes:
        width (int): Grid width in tiles
        height (int): Grid height in tiles
        grid (list): 2D grid of walkable tiles
        rooms (list): List of Room objects
        tile_size (int): Size of each tile
        start_room (Room): First room added
        end_room (Room): Last room added
    """

    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.tile_size = tile_size
        self.start_room = None
        self.end_room = None

    def add_room(self, room):
        """Add a room to the dungeon and mark its area as walkable."""
        self.rooms.append(room)
        for x in range(room.x // self.tile_size, (room.x + room.width) // self.tile_size):
            for y in range(room.y // self.tile_size, (room.y + room.height) // self.tile_size):
                self.grid[y][x] = 1     # Mark room area on grid
        if not self.start_room:
            self.start_room = room  # First room is start
        self.end_room = room        # Last room is end

    def connect_rooms(self):
        """Connect all rooms with corridors."""
        for i in range(len(self.rooms) - 1):
            room_a, room_b = self.rooms[i], self.rooms[i + 1]
            # Connect rooms horizontally
            for x in range(min(room_a.x, room_b.x) // self.tile_size, (max(room_a.x, room_b.x) + self.tile_size) // self.tile_size):
                if x < self.width:
                    self.grid[room_a.y // self.tile_size][x] = 1
            # Connect rooms vertically
            for y in range(min(room_a.y, room_b.y) // self.tile_size, (max(room_a.y, room_b.y) + self.tile_size) // self.tile_size):
                if y < self.height:
                    self.grid[y][room_b.x // self.tile_size] = 1

    def print_dungeon(self):
        """Print a text representation of the dungeon grid."""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if self.start_room and x == self.start_room.x // self.tile_size and y == self.start_room.y // self.tile_size:
                    print('S', end='')      # Start room
                elif self.end_room and x == self.end_room.x // self.tile_size and y == self.end_room.y // self.tile_size:
                    print('F', end='')      # Finish room
                else:
                    print('#' if cell == 1 else '.', end='')
            print()

    def draw(self, screen):
        """Draw the dungeon grid to the screen."""
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = (255, 255, 255) if cell == 1 else (0, 0, 0)
                pygame.draw.rect(screen, color, pygame.Rect(x * self.tile_size,
                                                            y * self.tile_size,
                                                            self.tile_size,
                                                            self.tile_size))

    def get_map_data(self):
        """Return a list of all rooms' shape and metadata for mapping."""
        return [room.get_shape() for room in self.rooms]


# Example usage:
if __name__ == "__main__":
    dungeon = Dungeon(30, 20, 20)
    for i in range(5):
        w, h = random.randint(3, 6), random.randint(3, 6)
        x, y = random.randint(0, dungeon.width - w -
                              1), random.randint(0, dungeon.height - h - 1)
        metadata = {"type": "normal", "index": i}
        room = Room(x, y, w, h, 20, room_id=f"room_{i}", metadata=metadata)
        dungeon.add_room(room)
    dungeon.connect_rooms()
    dungeon.print_dungeon()
    print("Map data:", dungeon.get_map_data())
