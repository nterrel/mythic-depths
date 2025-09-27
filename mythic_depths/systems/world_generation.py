import random
from mythic_depths.world.dungeon import Dungeon, Room
from mythic_depths.world.interactables import Door
from collections import deque

def generate_dungeon(entry_door=None):
    dungeon = Dungeon(40, 30, 32)
    doors = []
    # Add random rooms to the dungeon, min size 6x6
    for _ in range(8):
        w, h = random.randint(6, 10), random.randint(6, 10)
        x = random.randint(0, dungeon.width - w - 1)
        y = random.randint(0, dungeon.height - h - 1)
        dungeon.add_room(Room(x, y, w, h, 32))
    dungeon.connect_rooms()

    # Place doors at room edges
    for room in dungeon.rooms:
        rx0 = room.x // 32
        ry0 = room.y // 32
        rx1 = (room.x + room.width) // 32
        ry1 = (room.y + room.height) // 32
        # Example: Add a door at the center of the top edge
        if ry0 > 0:
            doors.append(Door((rx0 + rx1) // 2, ry0 - 1))

    # Place the farthest door as the "end door"
    if dungeon.rooms:
        start_room = dungeon.rooms[0]
        sx = (start_room.x + start_room.width // 2) // 32
        sy = (start_room.y + start_room.height // 2) // 32
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
        doors.append(Door(farthest[0], farthest[1]))

    return dungeon, doors