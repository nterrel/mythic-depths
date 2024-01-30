import pygame
from inventory import Inventory


class Player:
    def __init__(self, x, y,
                 name: str = 'Fella',
                 health: int = 100,
                 strength: int = 10,
                 tile_size: int = 20):
        self.x = x
        self.y = y
        self.speed = 5
        self.name = name
        self.health = health
        self.strength = strength
        self.tile_size = tile_size
        self.inventory = Inventory()

    def draw(self, screen):
        pygame.draw.rect(screen, (0, 128, 255),
                         pygame.Rect(self.x, self.y, 60, 60))

    def move(self, dx, dy, dungeon):
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        # Check if the new position is within a walkable area in the dungeon
        if dungeon.grid[new_y // self.tile_size][new_x // self.tile_size] == 1:
            self.x = new_x
            self.y = new_y

    def add_item_to_inventory(self, item):
        self.inventory.add_item(item)


player = Player(1, 1, "Hero", 100, 10)
# enemy = Player("Goblin", 50, 5)

'''
while True:
    action = input("Do you want to attack the goblin? (yes/no): ")
    if action.lower() == "yes":
        enemy.health -= player.strength
        print(f"You attacked the goblin! Goblin's health is now {enemy.health}")
        if enemy.health <= 0:
            print("You defeated the goblin!")
            break
    elif action.lower() == "no":
        print("You chose not to attack. The goblin attacks you!")
        player.health -= enemy.strength
        print(f"The goblin attacked you! Your health is now {player.health}")
        if player.health <= 0:
            print("You were defeated by the goblin!")
            break
    else:
        print("Invalid action.")
'''

# EOF
