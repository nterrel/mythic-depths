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


def generate_dungeon():
    dungeon = Dungeon(WORLD_WIDTH, WORLD_HEIGHT, TILE_SIZE)
    doors = []
    # Add random rooms to the dungeon, min size 6x6
    for _ in range(8):
        w, h = random.randint(6, 10), random.randint(6, 10)
        x, y = random.randint(0, dungeon.width - w -
                              1), random.randint(0, dungeon.height - h - 1)
        dungeon.add_room(Room(x, y, w, h, TILE_SIZE))
    dungeon.connect_rooms()
    # Place doors at dungeon edges (for area transition)
    for y in range(dungeon.height):
        if dungeon.grid[y][0] == 1:
            doors.append(Door(0, y))
        if dungeon.grid[y][dungeon.width - 1] == 1:
            doors.append(Door(dungeon.width - 1, y))
    for x in range(dungeon.width):
        if dungeon.grid[0][x] == 1:
            doors.append(Door(x, 0))
        if dungeon.grid[dungeon.height - 1][x] == 1:
            doors.append(Door(x, dungeon.height - 1))
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
        end_door = Door(farthest[0], farthest[1])
        end_door.is_end = True
        doors.append(end_door)
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

running = True
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
            dist = ((player.x // TILE_SIZE - door.x) ** 2 +
                    (player.y // TILE_SIZE - door.y) ** 2) ** 0.5
            if dist <= 2:
                door.open(player)
                # Cache all rooms in this dungeon on entry
                for room in dungeon.rooms:
                    visited_rooms.append({
                        'x': room.x, 'y': room.y,
                        'width': room.width, 'height': room.height,
                        'dungeon_id': len(history)
                    })
                # If backtracking (door already opened and history exists), pop previous dungeon
                if hasattr(door, 'back_link') and door.back_link:
                    prev = history.pop()
                    dungeon, doors, player.x, player.y = prev
                    return doors
                # Otherwise, push current dungeon to history and generate new
                history.append((dungeon, doors, player.x, player.y))
                dungeon, new_doors = generate_dungeon()
                # Link the new door for backtracking
                for d in new_doors:
                    if getattr(d, 'is_end', False) or d.x == 0 or d.x == dungeon.width - 1 or d.y == 0 or d.y == dungeon.height - 1:
                        d.back_link = True
                # Move player to center of new start room
                if dungeon.rooms:
                    start_room = dungeon.rooms[0]
                    center_tile_x = (start_room.x // TILE_SIZE) + \
                        (start_room.width // (2 * TILE_SIZE))
                    center_tile_y = (start_room.y // TILE_SIZE) + \
                        (start_room.height // (2 * TILE_SIZE))
                    player.x = center_tile_x * TILE_SIZE
                    player.y = center_tile_y * TILE_SIZE
                else:
                    player.x = (WINDOW_WIDTH // 2 // TILE_SIZE) * TILE_SIZE
                    player.y = (WINDOW_HEIGHT // 2 // TILE_SIZE) * TILE_SIZE
                return new_doors
    return doors


def draw_player_with_camera(screen, player, camera_x, camera_y):
    size = int(player.tile_size * 0.6)
    offset = (player.tile_size - size) // 2
    rect_x = player.x - camera_x + offset
    rect_y = player.y - camera_y + offset
    pygame.draw.rect(screen, (0, 128, 255),
                     pygame.Rect(rect_x, rect_y, size, size))


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            new_doors = interact_nearby_doors(player, doors)
            if new_doors is not None:
                doors = new_doors

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a]:
        dx -= 1
    if keys[pygame.K_d]:
        dx += 1
    if keys[pygame.K_w]:
        dy -= 1
    if keys[pygame.K_s]:
        dy += 1

    now = pygame.time.get_ticks()
    if (dx != 0 or dy != 0) and now - last_move_time > MOVE_DELAY:
        player.move(dx, dy, dungeon)
        last_move_time = now

    # Camera centers on player
    camera_x = player.x + player.tile_size // 2 - WINDOW_WIDTH // 2
    camera_y = player.y + player.tile_size // 2 - WINDOW_HEIGHT // 2
    camera_x = max(0, min(camera_x, WORLD_WIDTH * TILE_SIZE - WINDOW_WIDTH))
    camera_y = max(0, min(camera_y, WORLD_HEIGHT * TILE_SIZE - WINDOW_HEIGHT))

    screen.fill((0, 0, 0))  # Clear screen
    draw_dungeon_with_camera(screen, dungeon, camera_x, camera_y)
    draw_doors(screen, doors, camera_x, camera_y)
    draw_player_with_camera(screen, player, camera_x, camera_y)
    pygame.display.update()
    clock.tick(60)

pygame.quit()
