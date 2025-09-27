from mythic_depths.systems.world_generation import generate_dungeon


def interact_nearby_doors(player, doors):
    for door in doors:
        if not door.opened:
            dist = ((player.x // 32 - door.x) ** 2 + (player.y // 32 - door.y) ** 2) ** 0.5
            if dist <= 2:
                door.opened = True

                # Generate a new dungeon if the door leads to a new area
                dungeon, new_doors = generate_dungeon(entry_door=door)
                return dungeon, new_doors