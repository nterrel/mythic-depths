# Mythic Depths

A procedurally generated, tile-based dungeon crawler built with Python and Pygame.

## Features

- Infinite progression: Each dungeon is randomly generated and traversing a door at the end leads to a new dungeon.
- Tile-based movement: Classic grid movement inspired by old-school RPGs.
- Dynamic camera: The view scrolls to keep the player centered within the dungeon bounds.
- Room and corridor generation: Multiple rooms per dungeon, connected by corridors.
- Interactable doors: Doors at dungeon edges and at the farthest point allow transitions to new dungeons.
- Extensible architecture: Ready for future features like items, inventory, NPCs, and magic.

## How to Play

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the game**

   ```bash
   python pygame_test.py
   ```

3. **Controls**

   - Move: WASD
   - Interact: E (to open doors)
   - Quit: Close the window

## Project Structure

- `pygame_test.py` — Main game loop and rendering
- `dungeon.py` — Dungeon and room generation logic
- `player.py` — Player movement and collision
- `interactables.py` — Interactable objects (doors)
- `config.py` — Game configuration constants
- `inventory.py`, `items.py`, `npcs.py` — Stubs for future features

## Extending the Game

- Add new interactables (keys, chests, etc.) in `interactables.py`
- Implement inventory and items in `inventory.py` and `items.py`
- Add NPCs and combat in `npcs.py`
- Tweak dungeon generation in `dungeon.py`

## Requirements

- Python 3.11+
- Pygame 2.6+

## Credits

Created by nterrel. Powered by Python and Pygame.
