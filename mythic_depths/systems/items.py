# Here is where you can implement item attributes from `items.json`

from __future__ import annotations

from typing import Dict, Type


class Item:
    """Base class for consumable items."""

    #: Default amount restored or applied when the item is consumed.
    amount: int = 0
    #: Human readable name. Sub-classes should override this.
    name: str = "Generic Item"
    #: Short flavour description that can be surfaced in UI tooling later.
    description: str = ""

    def use(self, player) -> int:
        """Apply the item's effect to the provided ``player``.

        The default implementation performs no action and returns ``0`` to
        indicate that nothing happened. Sub-classes should override this
        method and return the effective amount of healing/energy granted so
        that higher level systems (UI, logging, etc.) can report the outcome.
        """

        return 0


class HealthPotion(Item):
    """Restore a chunk of the player's health."""

    name = "Health Potion"
    amount = 30
    description = "A soothing tonic that closes wounds and restores vitality."

    def use(self, player) -> int:
        return player.restore_health(self.amount)


class ArcanePotion(Item):
    """Restore a chunk of the player's mana pool."""

    name = "Arcane Potion"
    amount = 20
    description = "A swirling elixir that rekindles the drinker's mana."

    def use(self, player) -> int:
        return player.restore_mana(self.amount)


ITEM_REGISTRY: Dict[str, Type[Item]] = {
    HealthPotion.name: HealthPotion,
    ArcanePotion.name: ArcanePotion,
}


def create_item(name: str) -> Item:
    """Factory helper that instantiates the item associated with ``name``.

    Raises ``KeyError`` if the item has not been registered yet.
    """

    item_cls = ITEM_REGISTRY[name]
    return item_cls()
