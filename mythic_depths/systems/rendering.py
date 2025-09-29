import pygame
from mythic_depths.config.config import TILE_SIZE


def draw_dungeon_with_camera(screen, dungeon, camera):
    for y in range(dungeon.height):
        for x in range(dungeon.width):
            tile = dungeon.grid[y][x]
            screen_x = (x - camera.x) * TILE_SIZE
            screen_y = (y - camera.y) * TILE_SIZE

            if tile == 1:  # Floor
                pygame.draw.rect(screen, (200, 200, 200), (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
            elif tile == 0:  # Wall
                pygame.draw.rect(screen, (0, 0, 0), (screen_x, screen_y, TILE_SIZE, TILE_SIZE))


def draw_doors(screen, doors, camera):
    for door in doors:
        screen_x = (door.x - camera.x) * TILE_SIZE
        screen_y = (door.y - camera.y) * TILE_SIZE

        if door.is_end:
            color = (0, 255, 0)  # Green for end door
        elif door.paired_door:
            color = (255, 0, 0)  # Red for interacted doors
        else:
            color = (0, 0, 255)  # Blue for unexplored doors

        pygame.draw.rect(screen, color, (screen_x, screen_y, TILE_SIZE, TILE_SIZE))
