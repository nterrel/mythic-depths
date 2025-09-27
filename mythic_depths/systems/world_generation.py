import random
from mythic_depths.world.dungeon import Dungeon, Room
from mythic_depths.world.interactables import Door
from collections import deque

TILE_SIZE = 32

def generate_dungeon(entry_door=None):
    dungeon = Dungeon(40, 30, TILE_SIZE)
    doors = []
    # Add random rooms to the dungeon, min size 6x6
    for _ in range(8):
        w, h = random.randint(6, 10), random.randint(6, 10)
        x = random.randint(0, dungeon.width - w - 1)
        y = random.randint(0, dungeon.height - h - 1)
        dungeon.add_room(Room(x, y, w, h, TILE_SIZE))
    dungeon.connect_rooms()

    # Place doors at room edges
    for room in dungeon.rooms:
        rx0 = room.x // TILE_SIZE
        ry0 = room.y // TILE_SIZE
        rx1 = (room.x + room.width) // TILE_SIZE
        ry1 = (room.y + room.height) // TILE_SIZE
        # Example: Add a door at the center of the top edge
        if ry0 > 0:
            doors.append(Door((rx0 + rx1) // 2, ry0 - 1))

    # Place the farthest door as the "end door"
    if dungeon.rooms:
        start_room = dungeon.rooms[0]
        sx = (start_room.x + start_room.width // 2) // TILE_SIZE
        sy = (start_room.y + start_room.height // 2) // TILE_SIZE
        visited = set()
        queue = deque([(sx, sy, 0)])
        farthest = (sx, sy, 0)
        while queue:
            x, y, dist = queue.popleft()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if dungeon.grid[y][x] == 1 and dist > farthest[2]:
                farthest = (x, y, dist)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < dungeon.width and 0 <= ny < dungeon.height and dungeon.grid[ny][nx] == 1:
                    queue.append((nx, ny, dist + 1))
        end_door = Door(farthest[0], farthest[1])
        end_door.is_end = True
        doors.append(end_door)

    # If entering from another dungeon, create a paired door
    if entry_door:
        start_room = dungeon.rooms[0]
        center_tile_x = (start_room.x + start_room.width // 2) // TILE_SIZE
        center_tile_y = (start_room.y + start_room.height // 2) // TILE_SIZE
        paired_door = Door(center_tile_x, center_tile_y)
        paired_door.connected_rooms.add(start_room)
        entry_door.connected_rooms.add(start_room)
        doors.append(paired_door)

    # Add logic to limit the number of doors per dungeon floor
    MAX_DOORS_PER_FLOOR = 5
    if len(doors) > MAX_DOORS_PER_FLOOR:
        doors = random.sample(doors, MAX_DOORS_PER_FLOOR)

    # Return the dungeon, doors, and player's starting position
    return dungeon, doors, (sx, sy)