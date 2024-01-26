import pygame

class Room:
    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height

class Dungeon:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[0 for _ in range(width)] for _ in range(height)]
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)
        for x in range(room.x, room.x + room.width):
            for y in range(room.y, room.y + room.height):
                self.grid[y][x] = 1     # Mark room area on grid

    def connect_rooms(self):
        for i in range(len(self.rooms) - 1):
            room_a, room_b = self.rooms[i], self.rooms[i + 1]
            # Connect rooms at the center
            for x in range(min(room_a.x, room_b.x), max(room_a.x, room_b.x) + 1):
                self.grid[room_a.y][x] = 1
            for y in range(min(room_a.y, room_b.y), max(room_a.y, room_b.y) + 1):
                self.grid[y][room_b.x] = 1

    def print_dungeon(self):
        for row in self.grid:
            print(''.join(['#' if cell == 1 else '.' for cell in row]))

# How to use:

import random

# Initialize a dungeon
dungeon = Dungeon(30, 20)
# Create 5 rooms at random
for _ in range(5):
    w, h = random.randint(3, 6), random.randint(3, 6)
    x, y = random.randint(0, dungeon.width - w), random.randint(0, dungeon.height - h)
    dungeon.add_room(Room(x, y, w, h))

dungeon.connect_rooms()
dungeon.print_dungeon()
