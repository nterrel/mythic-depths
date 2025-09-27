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
    dungeon, doors = generate_dungeon()
    player = Player(100, 100, TILE_SIZE)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    result = interact_nearby_doors(player, doors)
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

        camera_x = player.x - WINDOW_WIDTH // 2
        camera_y = player.y - WINDOW_HEIGHT // 2

        screen.fill((0, 0, 0))
        draw_dungeon_with_camera(screen, dungeon, camera_x, camera_y)
        draw_doors(screen, doors, camera_x, camera_y)
        player.move(dx, dy, dungeon)
        pygame.draw.rect(screen, (50, 200, 200), pygame.Rect(
            player.x - camera_x, player.y - camera_y, TILE_SIZE, TILE_SIZE))
        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()