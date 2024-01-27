import pygame
import random


class Room:
    def __init__(self, x, y, width, height, tile_size):
        self.x, self.y = x, y
        self.width, self.height = width, height


class Dungeon:
    def __init__(self, width, height, tile_size):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.tile_size = tile_size
        self.start_room = None
        self.end_room = None

    def add_room(self, room):
        self.rooms.append(room)
        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                self.grid[y][x] = 1     # Mark room area on grid
        if not self.start_room:
            self.start_room = room  # This makes the first room added the start
        self.end_room = room        # End room is the last room to be added

    def connect_rooms(self):
        for i in range(len(self.rooms) - 1):
            room_a, room_b = self.rooms[i], self.rooms[i + 1]
            # Connect rooms at the center
            for x in range(min(room_a.x, room_b.x), max(room_a.x, room_b.x) + 1):
                self.grid[room_a.y][x] = 1
            for y in range(min(room_a.y, room_b.y), max(room_a.y, room_b.y) + 1):
                self.grid[y][room_b.x] = 1

    def print_dungeon(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if x == self.start_room.x and y == self.start_room.y:
                    print('S', end='')      # Start room
                elif x == self.end_room.x and y == self.end_room.y:
                    print('F', end='')      # Finish room
                else:
                    print('#' if cell == 1 else '.', end='')
            print()

    def draw(self, screen):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                color = (255, 255, 255) if cell == 1 else (0, 0, 0)
                pygame.draw.rect(screen, color, pygame.Rect(x * self.tile_size,
                                                            y * self.tile_size,
                                                            self.tile_size,
                                                            self.tile_size))

# How to use:

if __name__ == "__main__":
    # Initialize a dungeon
    dungeon = Dungeon(30, 20)
    # Create 5 rooms at random
    for _ in range(5):
        w, h = random.randint(3, 6), random.randint(3, 6)
        x, y = random.randint(0, dungeon.width - w), random.randint(0, dungeon.height - h)
        dungeon.add_room(Room(x, y, w, h))

    dungeon.connect_rooms()
    dungeon.print_dungeon()
