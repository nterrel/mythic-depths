class Character:
    def __init__(self, name, health, strength):
        self.name = name
        self.health = health
        self.strength = strength


player = Character("Hero", 100, 10)
enemy = Character("Goblin", 50, 5)

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

