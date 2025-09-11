import random
from dungeon import Room
from config import TILE_SIZE


class InfiniteDungeon:
    def __init__(self, room_size=10):
        self.rooms = {}  # {(room_x, room_y): Room}
        self.corridors = {}  # {(room_x, room_y, direction): [(x, y)]}
        self.doors = []  # List of Door interactables
        self.room_size = room_size
        self.areas = {}  # {(area_id): set of (room_x, room_y)}
        self.current_area = 0

    def get_room(self, room_x, room_y):
        if (room_x, room_y) not in self.rooms:
            # Generate a new room procedurally
            w = random.randint(self.room_size, self.room_size + 4)
            h = random.randint(self.room_size, self.room_size + 4)
            x = room_x * self.room_size
            y = room_y * self.room_size
            room = Room(x, y, w, h, TILE_SIZE)
            self.rooms[(room_x, room_y)] = room
            # Generate corridors and doors only at corridor ends
            for direction, (dx, dy) in zip(['N', 'S', 'W', 'E'], [(-1, 0), (1, 0), (0, -1), (0, 1)]):
                adj_coords = (room_x + dx, room_y + dy)
                if adj_coords not in self.rooms:
                    # Generate corridor from this room to the edge, place door at end
                    if direction == 'N':
                        # Corridor goes up from center top
                        corridor = [(room_x * self.room_size + w // 2, y - i)
                                    for i in range(1, self.room_size + 1)]
                        door_x = room_x * self.room_size + w // 2
                        door_y = y - self.room_size
                    elif direction == 'S':
                        # Corridor goes down from center bottom
                        corridor = [(room_x * self.room_size + w // 2, y + h + i)
                                    for i in range(1, self.room_size + 1)]
                        door_x = room_x * self.room_size + w // 2
                        door_y = y + h + self.room_size
                    elif direction == 'W':
                        # Corridor goes left from center left
                        corridor = [(x - i, room_y * self.room_size + h // 2)
                                    for i in range(1, self.room_size + 1)]
                        door_x = x - self.room_size
                        door_y = room_y * self.room_size + h // 2
                    elif direction == 'E':
                        # Corridor goes right from center right
                        corridor = [(x + w + i, room_y * self.room_size + h // 2)
                                    for i in range(1, self.room_size + 1)]
                        door_x = x + w + self.room_size
                        door_y = room_y * self.room_size + h // 2
                    self.corridors[(room_x, room_y, direction)] = corridor
                    from interactables import Door
                    self.doors.append(
                        Door(door_x // TILE_SIZE, door_y // TILE_SIZE))
        return self.rooms[(room_x, room_y)]

    def get_adjacent_rooms(self, room_x, room_y):
        # Returns rooms in N, S, E, W directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        return [self.get_room(room_x + dx, room_y + dy) for dx, dy in directions]

    def enter_new_area(self):
        # Generate a new area (dungeon) and set as current
        self.current_area += 1
        self.areas[self.current_area] = set()
        # Optionally clear rooms, corridors, doors for new area
        self.rooms.clear()
        self.corridors.clear()
        self.doors.clear()
