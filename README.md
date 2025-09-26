# Mythic Depths

![Mythic Depths Logo](assets/images/logo.png)

A dark, medieval high-fantasy roguelike adventure game. Procedurally generated, tile-based dungeon crawler built with Python and Pygame.

## Features

- Infinite progression: Each dungeon is randomly generated and traversing a door at the end leads to a new dungeon.
- Tile-based movement: Classic grid movement inspired by old-school RPGs.
- Dynamic camera: The view scrolls to keep the player centered within the dungeon bounds.
- Room and corridor generation: Multiple rooms per dungeon, connected by corridors.
- Interactable doors: Doors at dungeon edges and at the farthest point allow transitions to new dungeons.
- Extensible architecture: Ready for future features like items, inventory, NPCs, and magic.

## Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/nterrel/mythic-depths.git
   cd mythic-depths
   ```

2. **(Recommended) Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Run the game**

   ```bash
   python pygame_test.py
   ```

5. **Troubleshooting**

   - If you see errors about missing packages, ensure your virtual environment is activated.
   - If Pygame fails to initialize, make sure your Python version is 3.11+ and you have the latest Pygame.

## Controls

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
