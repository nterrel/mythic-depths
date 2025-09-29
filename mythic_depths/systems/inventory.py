from __future__ import annotations

from typing import Dict

from mythic_depths.systems.items import ITEM_REGISTRY, Item, create_item


class Inventory:
    """A small helper that tracks and consumes items for the player."""

    def __init__(self):
        self._items: Dict[str, int] = {}

    # ------------------------------------------------------------------
    # Management helpers
    def add_item(self, item: Item, quantity: int = 1) -> None:
        """Add ``quantity`` copies of ``item`` to the inventory."""

        if quantity <= 0:
            raise ValueError("quantity must be positive")
        self._items[item.name] = self._items.get(item.name, 0) + quantity

    def remove_item(self, item_name: str, quantity: int = 1) -> None:
        """Remove ``quantity`` items from the inventory.

        Raises ``KeyError`` if the item is missing or there are not enough
        copies to remove.
        """

        if quantity <= 0:
            raise ValueError("quantity must be positive")
        current = self._items.get(item_name)
        if current is None or current < quantity:
            raise KeyError(f"Not enough '{item_name}' in inventory")
        remaining = current - quantity
        if remaining:
            self._items[item_name] = remaining
        else:
            del self._items[item_name]

    def get_quantity(self, item_name: str) -> int:
        """Return how many copies of ``item_name`` are stored."""

        return self._items.get(item_name, 0)

    def items(self):
        """Iterate over ``(name, quantity)`` pairs stored in the inventory."""

        return self._items.items()

    # ------------------------------------------------------------------
    # Gameplay helpers
    def can_use(self, item_name: str) -> bool:
        """Check whether ``item_name`` exists and has an associated effect."""

        return item_name in self._items and item_name in ITEM_REGISTRY

    def use_item(self, item_name: str, player) -> int:
        """Consume an item, applying its effect to ``player``.

        Returns the result of ``Item.use`` so callers can react to the amount
        healed/restored. A return value of ``0`` indicates that no effect took
        place, either because the player was already at maximum capacity or
        because the item has no implemented behaviour.
        """

        if not self.can_use(item_name):
            return 0

        item = create_item(item_name)
        effect = item.use(player)
        # Only remove the item if an effect actually happened.
        if effect > 0:
            self.remove_item(item_name)
        return effect
