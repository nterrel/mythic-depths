import pygame
from mythic_depths.world.dungeon import Dungeon
from mythic_depths.entities.player import Player
from mythic_depths.config.config import TILE_SIZE
from mythic_depths.systems.world_generation import generate_dungeon
from mythic_depths.systems.rendering import draw_dungeon_with_camera, draw_doors
from mythic_depths.systems.interactions import interact_nearby_doors


def main():
    pygame.init()
    WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Mythic Depths")

    clock = pygame.time.Clock()
    running = True

    # Initialize game state
    history = []
    visited_rooms = []
    dungeon, doors, (player_start_x, player_start_y) = generate_dungeon()

    # Ensure player starts at the center of the first walkable tile in the starting room
    if dungeon.rooms:
        start_room = dungeon.rooms[0]
        player_start_x = (start_room.x // TILE_SIZE) + (start_room.width // (2 * TILE_SIZE))
        player_start_y = (start_room.y // TILE_SIZE) + (start_room.height // (2 * TILE_SIZE))
        player = Player(player_start_x * TILE_SIZE, player_start_y * TILE_SIZE, TILE_SIZE)
    else:
        player = Player(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, TILE_SIZE)

    MOVE_DELAY = 5  # ms between tile moves
    last_move_time = pygame.time.get_ticks()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    result = interact_nearby_doors(player, doors, dungeon)
                    if result:
                        dungeon, doors = result

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

        current_time = pygame.time.get_ticks()
        if current_time - last_move_time >= MOVE_DELAY:
            player.move(dx, dy, dungeon)
            last_move_time = current_time

        camera_x = player.x - WINDOW_WIDTH // 2
        camera_y = player.y - WINDOW_HEIGHT // 2

        screen.fill((0, 0, 0))
        draw_dungeon_with_camera(screen, dungeon, camera_x, camera_y)
        draw_doors(screen, doors, camera_x, camera_y)
        pygame.draw.rect(screen, (50, 200, 200), pygame.Rect(
            player.x - camera_x, player.y - camera_y, TILE_SIZE, TILE_SIZE))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
