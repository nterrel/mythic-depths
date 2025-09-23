import pygame
from systems.inventory import Inventory


class Player:
    """Represents the player character in the dungeon crawler game."""

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
        """Move the player by dx, dy if no collision with walls."""
        if dx != 0 or dy != 0:
            new_x = self.x + dx * self.speed
            new_y = self.y + dy * self.speed
            size = int(self.tile_size * 0.6)
            offset = (self.tile_size - size) // 2
            # Check all four corners for collision
            corners = [
                (new_x + offset, new_y + offset),
                (new_x + offset + size - 1, new_y + offset),
                (new_x + offset, new_y + offset + size - 1),
                (new_x + offset + size - 1, new_y + offset + size - 1)
            ]
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
# EOF
