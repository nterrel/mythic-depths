from mythic_depths.systems.world_generation import generate_dungeon


# Add history tracking for dungeon transitions
history = []


def interact_nearby_doors(player, doors, dungeon_history):
    # Check for nearby doors
    for door in doors:
        if abs(player.x - door.x) <= 1 and abs(player.y - door.y) <= 1:
            # If the door leads to an unexplored dungeon, generate it
            if not door.paired_door:
                new_dungeon, new_doors = generate_dungeon(entry_door=door)
                dungeon_history.append((new_dungeon, new_doors))

                # Pair the doors
                paired_door = next((d for d in new_doors if d.is_end), None)
                if paired_door:
                    door.paired_door = paired_door
                    paired_door.paired_door = door

            # Transition the player to the paired door's dungeon
            if door.paired_door:
                paired_door = door.paired_door
                player.x = paired_door.x
                player.y = paired_door.y
                return dungeon_history[-1]  # Return the new dungeon and doors

    return None  # No interaction occurred
