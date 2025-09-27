import pygame

def draw_dungeon_with_camera(screen, dungeon, camera_x, camera_y):
    for y, row in enumerate(dungeon.grid):
        for x, cell in enumerate(row):
            color = (255, 255, 255) if cell == 1 else (0, 0, 0)
            rect_x = x * dungeon.tile_size - camera_x
            rect_y = y * dungeon.tile_size - camera_y
            if 0 <= rect_x < 800 and 0 <= rect_y < 600:
                pygame.draw.rect(screen, color, pygame.Rect(
                    rect_x, rect_y, dungeon.tile_size, dungeon.tile_size))

def draw_doors(screen, doors, camera_x, camera_y):
    for door in doors:
        color = (200, 50, 50) if door.opened else (200, 150, 50)
        rect_x = door.x * 32 - camera_x
        rect_y = door.y * 32 - camera_y
        pygame.draw.rect(screen, color, pygame.Rect(
            rect_x, rect_y, 32, 32))