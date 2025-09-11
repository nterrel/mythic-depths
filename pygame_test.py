import time
import pygame
import random
from player import Player
from inventory import Inventory
from dungeon import Dungeon, Room
from config import TILE_SIZE
from interactables import Door

pygame.init()
WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mythic Depths")

# Static dungeon system
WORLD_WIDTH, WORLD_HEIGHT = 40, 30


# Track dungeon history and visited rooms for mapping
history = []  # Stack of (dungeon, doors, player_x, player_y)
visited_rooms = []  # List of dicts: {size, shape, position}

# Persistent mapping of room pairs to generated dungeons/doors
# key: (room1_key, room2_key), value: (dungeon1, doors1, dungeon2, doors2, doorA, doorB)
room_connections = {}


def generate_dungeon(entry_door=None):
    dungeon = Dungeon(WORLD_WIDTH, WORLD_HEIGHT, TILE_SIZE)
    doors = []
    # Add random rooms to the dungeon, min size 6x6
    for _ in range(8):
        w, h = random.randint(6, 10), random.randint(6, 10)
        x = random.randint(0, dungeon.width - w - 1)
        y = random.randint(0, dungeon.height - h - 1)
        dungeon.add_room(Room(x, y, w, h, TILE_SIZE))
    dungeon.connect_rooms()
    # Place up to 2 doors per edge, only at valid exits (walkable next to wall)
    for room in dungeon.rooms:
        rx0 = room.x // TILE_SIZE
        ry0 = room.y // TILE_SIZE
        rx1 = (room.x + room.width) // TILE_SIZE
        ry1 = (room.y + room.height) // TILE_SIZE
        # Top edge
        top_candidates = [x for x in range(rx0, rx1)
                         if dungeon.grid[ry0][x] == 1 and ry0 > 0 and dungeon.grid[ry0 - 1][x] == 0]
        for x in random.sample(top_candidates, min(2, len(top_candidates))):
            d = Door(x, ry0, connected_rooms={room})
            d.dungeon_context = dungeon
            doors.append(d)
        # Bottom edge
        bot_candidates = [x for x in range(rx0, rx1)
                         if dungeon.grid[ry1 - 1][x] == 1 and ry1 < dungeon.height and dungeon.grid[ry1][x] == 0]
        for x in random.sample(bot_candidates, min(2, len(bot_candidates))):
            d = Door(x, ry1 - 1, connected_rooms={room})
            d.dungeon_context = dungeon
            doors.append(d)
        # Left edge
        left_candidates = [y for y in range(ry0, ry1)
                           if dungeon.grid[y][rx0] == 1 and rx0 > 0 and dungeon.grid[y][rx0 - 1] == 0]
        for y in random.sample(left_candidates, min(2, len(left_candidates))):
            d = Door(rx0, y, connected_rooms={room})
            d.dungeon_context = dungeon
            doors.append(d)
        # Right edge
        right_candidates = [y for y in range(ry0, ry1)
                            if dungeon.grid[y][rx1 - 1] == 1 and rx1 < dungeon.width and dungeon.grid[y][rx1] == 0]
        for y in random.sample(right_candidates, min(2, len(right_candidates))):
            d = Door(rx1 - 1, y, connected_rooms={room})
            d.dungeon_context = dungeon
            doors.append(d)
    # Place a door at the farthest walkable tile from the start room
    if dungeon.rooms:
        from collections import deque
        start_room = dungeon.rooms[0]
        sx = (start_room.x // TILE_SIZE) + \
            (start_room.width // (2 * TILE_SIZE))
        sy = (start_room.y // TILE_SIZE) + \
            (start_room.height // (2 * TILE_SIZE))
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
    # Place a door at the farthest tile, mark it as 'end_door'
    end_door = Door(farthest[0], farthest[1], connected_rooms={start_room})
    end_door.is_end = True
    doors.append(end_door)
    # If entering from another dungeon, create a paired door
    if entry_door:
        # Place paired door in start room and connect both rooms
        start_room = dungeon.rooms[0]
        center_tile_x = (start_room.x // TILE_SIZE) + \
            (start_room.width // (2 * TILE_SIZE))
        center_tile_y = (start_room.y // TILE_SIZE) + \
            (start_room.height // (2 * TILE_SIZE))
        paired_door = Door(center_tile_x, center_tile_y,
                           connected_rooms={start_room})
        paired_door.dungeon_context = dungeon
        # Connect both doors to both rooms
        paired_door.connected_rooms.add(
            getattr(entry_door, 'connected_rooms', {start_room}).copy().pop())
        entry_door.connected_rooms.add(start_room)
        doors.append(paired_door)
    return dungeon, doors


dungeon, doors = generate_dungeon()

# Start player centered in the first walkable tile of the first room
if dungeon.rooms:
    start_room = dungeon.rooms[0]
    center_tile_x = (start_room.x // TILE_SIZE) + \
        (start_room.width // (2 * TILE_SIZE))
    center_tile_y = (start_room.y // TILE_SIZE) + \
        (start_room.height // (2 * TILE_SIZE))
    player_x = center_tile_x * TILE_SIZE
    player_y = center_tile_y * TILE_SIZE
else:
    player_x = (WINDOW_WIDTH // 2 // TILE_SIZE) * TILE_SIZE
    player_y = (WINDOW_HEIGHT // 2 // TILE_SIZE) * TILE_SIZE
player = Player(player_x, player_y, tile_size=TILE_SIZE)

MOVE_DELAY = 5  # ms between tile moves (faster)
last_move_time = 0

clock = pygame.time.Clock()


def draw_dungeon_with_camera(screen, dungeon, camera_x, camera_y):
    for y, row in enumerate(dungeon.grid):
        for x, cell in enumerate(row):
            color = (255, 255, 255) if cell == 1 else (0, 0, 0)
            rect_x = x * dungeon.tile_size - camera_x
            rect_y = y * dungeon.tile_size - camera_y
            if 0 <= rect_x < WINDOW_WIDTH and 0 <= rect_y < WINDOW_HEIGHT:
                pygame.draw.rect(screen, color, pygame.Rect(
                    rect_x, rect_y, dungeon.tile_size, dungeon.tile_size))


def draw_doors(screen, doors, camera_x, camera_y):
    for door in doors:
        color = (200, 150, 50) if not door.opened else (100, 200, 100)
        rect_x = door.x * TILE_SIZE - camera_x
        rect_y = door.y * TILE_SIZE - camera_y
        pygame.draw.rect(screen, color, pygame.Rect(
            rect_x, rect_y, TILE_SIZE, TILE_SIZE))


def interact_nearby_doors(player, doors):
    global dungeon, history, visited_rooms
    for door in doors:
        if not door.opened:
            dist = ((player.x // TILE_SIZE - door.x) ** 2 + (player.y // TILE_SIZE - door.y) ** 2) ** 0.5
            if dist <= 2:
                # Find which room the player is currently in
                current_room = None
                for room in dungeon.rooms:
                    rx0 = room.x // TILE_SIZE
                    ry0 = room.y // TILE_SIZE
                    rx1 = (room.x + room.width) // TILE_SIZE
                    ry1 = (room.y + room.height) // TILE_SIZE
                    px = player.x // TILE_SIZE
                    py = player.y // TILE_SIZE
                    if rx0 <= px < rx1 and ry0 <= py < ry1:
                        current_room = room
                        break
                # If door only knows one room, generate and connect a new room
                if len(door.connected_rooms) == 1:
                    history.append((dungeon, doors, player.x, player.y))
                    dungeon_new, new_doors = generate_dungeon()
                    # Find the room in the new dungeon closest to the door's position
                    min_dist = float('inf')
                    new_room = None
                    for room in dungeon_new.rooms:
                        rx0 = room.x // TILE_SIZE
                        ry0 = room.y // TILE_SIZE
                        rx1 = (room.x + room.width) // TILE_SIZE
                        ry1 = (room.y + room.height) // TILE_SIZE
                        # Use center of room for distance
                        cx = (rx0 + rx1) // 2
                        cy = (ry0 + ry1) // 2
                        d2 = (door.x - cx) ** 2 + (door.y - cy) ** 2
                        if d2 < min_dist:
                            min_dist = d2
                            new_room = room
                    door.connected_rooms.add(new_room)
                    # Place paired door at closest edge of new_room, only on walkable tile with valid exit
                    edge_candidates = []
                    rx0 = new_room.x // TILE_SIZE
                    ry0 = new_room.y // TILE_SIZE
                    rx1 = (new_room.x + new_room.width) // TILE_SIZE
                    ry1 = (new_room.y + new_room.height) // TILE_SIZE
                    # Top edge
                    top_candidates = [x for x in range(rx0, rx1)
                                     if dungeon_new.grid[ry0][x] == 1 and ry0 > 0 and dungeon_new.grid[ry0 - 1][x] == 0]
                    for x in top_candidates:
                        edge_candidates.append((x, ry0))
                    # Bottom edge
                    bot_candidates = [x for x in range(rx0, rx1)
                                     if dungeon_new.grid[ry1 - 1][x] == 1 and ry1 < dungeon_new.height and dungeon_new.grid[ry1][x] == 0]
                    for x in bot_candidates:
                        edge_candidates.append((x, ry1 - 1))
                    # Left edge
                    left_candidates = [y for y in range(ry0, ry1)
                                       if dungeon_new.grid[y][rx0] == 1 and rx0 > 0 and dungeon_new.grid[y][rx0 - 1] == 0]
                    for y in left_candidates:
                        edge_candidates.append((rx0, y))
                    # Right edge
                    right_candidates = [y for y in range(ry0, ry1)
                                        if dungeon_new.grid[y][rx1 - 1] == 1 and rx1 < dungeon_new.width and dungeon_new.grid[y][rx1] == 0]
                    for y in right_candidates:
                        edge_candidates.append((rx1 - 1, y))
                    # Pick closest edge tile
                    min_edge_dist = float('inf')
                    best_edge = None
                    for ex, ey in edge_candidates:
                        d2 = (door.x - ex) ** 2 + (door.y - ey) ** 2
                        if d2 < min_edge_dist:
                            min_edge_dist = d2
                            best_edge = (ex, ey)
                    if best_edge:
                        paired_door = Door(best_edge[0], best_edge[1], connected_rooms={current_room, new_room})
                        paired_door.dungeon_context = dungeon_new
                        new_doors.append(paired_door)
                        globals()['dungeon'] = dungeon_new
                        globals()['doors'] = new_doors
                        paired_door.open(player, new_room)
                        return new_doors
                else:
                    # Move to the other room
                    door.open(player, current_room)


# MAIN GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                interact_nearby_doors(player, doors)

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    if keys[pygame.K_w]:
        dy = -1
    if keys[pygame.K_s]:
        dy = 1

    # Camera centers on player
    camera_x = player.x - WINDOW_WIDTH // 2
    camera_y = player.y - WINDOW_HEIGHT // 2

    screen.fill((0, 0, 0))
    draw_dungeon_with_camera(screen, dungeon, camera_x, camera_y)
    draw_doors(screen, doors, camera_x, camera_y)
    player.move(dx, dy, dungeon)
    # Draw player as a rectangle
    pygame.draw.rect(screen, (50, 200, 200), pygame.Rect(
        player.x - camera_x, player.y - camera_y, TILE_SIZE, TILE_SIZE))
    pygame.display.update()
    clock.tick(60)

pygame.quit()
