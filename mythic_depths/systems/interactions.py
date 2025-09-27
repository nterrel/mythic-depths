from mythic_depths.systems.world_generation import generate_dungeon


# Add history tracking for dungeon transitions
history = []


def interact_nearby_doors(player, doors, dungeon):
    for door in doors:
        if not door.opened:
            dist = ((player.x // player.tile_size - door.x) ** 2 + (player.y // player.tile_size - door.y) ** 2) ** 0.5
            if dist <= 2:
                door.opened = True
                history.append((dungeon, doors, player.x, player.y))  # Track current state

                # Find the current room the player is in
                current_room = None
                for room in dungeon.rooms:
                    rx0 = room.x // player.tile_size
                    ry0 = room.y // player.tile_size
                    rx1 = (room.x + room.width) // player.tile_size
                    ry1 = (room.y + room.height) // player.tile_size
                    px = player.x // player.tile_size
                    py = player.y // player.tile_size
                    if rx0 <= px < rx1 and ry0 <= py < ry1:
                        current_room = room
                        break

                # Generate a new dungeon if the door leads to a new area
                if len(door.connected_rooms) == 1:
                    dungeon_new, new_doors = generate_dungeon(entry_door=door)
                    door.connected_rooms.add(dungeon_new.rooms[0])
                    player.x = (dungeon_new.rooms[0].x + dungeon_new.rooms[0].width // 2) // player.tile_size * player.tile_size
                    player.y = (dungeon_new.rooms[0].y + dungeon_new.rooms[0].height // 2) // player.tile_size * player.tile_size
                    return dungeon_new, new_doors

                # Transition to the connected room
                other_rooms = door.connected_rooms - {current_room}
                if other_rooms:
                    target_room = next(iter(other_rooms))
                    player.x = (target_room.x + target_room.width // 2) // player.tile_size * player.tile_size
                    player.y = (target_room.y + target_room.height // 2) // player.tile_size * player.tile_size
                    return dungeon, doors