import pygame
from entities.player import Player
from systems.inventory import Inventory
from dungeon import Dungeon
from config import TILE_SIZE


def main():
    """Main function to run the game."""
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Mythic Depths")

    player = Player(screen_width // 2, screen_height // 2, tile_size=TILE_SIZE)

    dungeon = Dungeon(screen_width // TILE_SIZE,
                      screen_height // TILE_SIZE, TILE_SIZE)
    dungeon.connect_rooms()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

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

        screen.fill((0, 0, 0))  # Clear screen

        dungeon.draw(screen)

        player.move(dx, dy, dungeon)
        player.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
