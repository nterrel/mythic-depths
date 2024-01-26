import pygame

pygame.init()
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mythic Depths")

player = Player(screen_width // 2, screen_height // 2)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
    
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_a]:
        dx = -1
    if keys[pygame.K_d]:
        dx = 1
    if keys[pygame.K_w]:
        dy = 1
    if keys[pygame.K_s]:
        dy = -1

    player.move(dx, dy)

    screen.fill((0, 0, 0))  # Clear screen
    player.draw(screen)

pygame.quit()

