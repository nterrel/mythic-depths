from mythic_depths.config.config import TILE_SIZE

def can_move(entity, dx, dy, dungeon):
    """
    Check if an entity can move by dx, dy without colliding with walls.

    Args:
        entity: The entity attempting to move (must have x, y, and tile_size attributes).
        dx (int): Change in x-direction.
        dy (int): Change in y-direction.
        dungeon: The dungeon object to check for collisions.

    Returns:
        bool: True if the entity can move, False otherwise.
    """
    new_x = entity.x + dx * entity.speed
    new_y = entity.y + dy * entity.speed
    size = int(entity.tile_size * 0.6)
    offset = (entity.tile_size - size) // 2

    # Check all four corners for collision
    corners = [
        (new_x + offset, new_y + offset),
        (new_x + offset + size - 1, new_y + offset),
        (new_x + offset, new_y + offset + size - 1),
        (new_x + offset + size - 1, new_y + offset + size - 1)
    ]

    for cx, cy in corners:
        grid_x = int(cx // TILE_SIZE)
        grid_y = int(cy // TILE_SIZE)

        if hasattr(dungeon, 'get_room'):
            # InfiniteDungeon logic
            room_x = grid_x // dungeon.room_size
            room_y = grid_y // dungeon.room_size
            room = dungeon.get_room(room_x, room_y)
            if not room:
                return False
            rx0 = room.x // TILE_SIZE
            ry0 = room.y // TILE_SIZE
            rx1 = (room.x + room.width) // TILE_SIZE
            ry1 = (room.y + room.height) // TILE_SIZE
            if not (rx0 <= grid_x < rx1 and ry0 <= grid_y < ry1):
                return False
        else:
            # Static dungeon logic
            if not (0 <= grid_x < dungeon.width and 0 <= grid_y < dungeon.height):
                return False
            if dungeon.grid[grid_y][grid_x] != 1:
                return False

    return True