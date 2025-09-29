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
    all_door_candidates = []
    for room in dungeon.rooms:
        rx0 = room.x // TILE_SIZE
        ry0 = room.y // TILE_SIZE
        rx1 = (room.x + room.width) // TILE_SIZE
        ry1 = (room.y + room.height) // TILE_SIZE

        # Top edge
        for x in range(rx0, rx1):
            if dungeon.grid[ry0][x] == 1 and ry0 > 0 and dungeon.grid[ry0 - 1][x] == 0:
                all_door_candidates.append((x, ry0, room))

        # Bottom edge
        for x in range(rx0, rx1):
            if dungeon.grid[ry1 - 1][x] == 1 and ry1 < dungeon.height and dungeon.grid[ry1][x] == 0:
                all_door_candidates.append((x, ry1 - 1, room))

        # Left edge
        for y in range(ry0, ry1):
            if dungeon.grid[y][rx0] == 1 and rx0 > 0 and dungeon.grid[y][rx0 - 1] == 0:
                all_door_candidates.append((rx0, y, room))

        # Right edge
        for y in range(ry0, ry1):
            if dungeon.grid[y][rx1 - 1] == 1 and rx1 < dungeon.width and dungeon.grid[y][rx1] == 0:
                all_door_candidates.append((rx1 - 1, y, room))

    # Limit total doors per dungeon floor
    MAX_DOORS_PER_FLOOR = 5
    if len(all_door_candidates) > MAX_DOORS_PER_FLOOR:
        all_door_candidates = random.sample(all_door_candidates, MAX_DOORS_PER_FLOOR)

    # Create doors as shared objects between rooms
    door_objects = {}
    for x, y, room_ref in all_door_candidates:
        key = (x, y)
        if key not in door_objects:
            d = Door(x, y, connected_rooms={room_ref})
            d.dungeon_context = dungeon
            door_objects[key] = d
        doors.append(door_objects[key])

    # Place a door at the farthest walkable tile from the start room
    if dungeon.rooms:
        from collections import deque
        start_room = dungeon.rooms[0]
        sx = (start_room.x // TILE_SIZE) + (start_room.width // (2 * TILE_SIZE))
        sy = (start_room.y // TILE_SIZE) + (start_room.height // (2 * TILE_SIZE))
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

        end_door = Door(farthest[0], farthest[1], connected_rooms={start_room})
        end_door.is_end = True
        doors.append(end_door)

    # If entering from another dungeon, create a paired door
    if entry_door:
        start_room = dungeon.rooms[0]
        center_tile_x = (start_room.x // TILE_SIZE) + (start_room.width // (2 * TILE_SIZE))
        center_tile_y = (start_room.y // TILE_SIZE) + (start_room.height // (2 * TILE_SIZE))
        paired_door = Door(center_tile_x, center_tile_y, connected_rooms={start_room})
        paired_door.dungeon_context = dungeon
        entry_door.connected_rooms.add(start_room)
        doors.append(paired_door)

    return dungeon, doors
