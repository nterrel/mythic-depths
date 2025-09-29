import pytest

from mythic_depths.entities.player import Player
from mythic_depths.systems.items import ArcanePotion, HealthPotion


def test_health_potion_consumption_reduces_inventory():
    player = Player(0, 0, health=80, mana=40)
    player.health = 30

    inventory = player.inventory
    inventory.add_item(HealthPotion())

    healed = inventory.use_item(HealthPotion.name, player)

    assert healed == 30
    assert player.health == 60
    assert inventory.get_quantity(HealthPotion.name) == 0


def test_arcane_potion_restores_only_missing_mana():
    player = Player(0, 0, health=100, mana=50)
    player.mana = 45

    inventory = player.inventory
    inventory.add_item(ArcanePotion())

    restored = inventory.use_item(ArcanePotion.name, player)

    assert restored == 5
    assert player.mana == 50
    assert inventory.get_quantity(ArcanePotion.name) == 0


def test_consuming_at_full_health_keeps_item():
    player = Player(0, 0, health=60, mana=20)

    inventory = player.inventory
    inventory.add_item(HealthPotion())

    healed = inventory.use_item(HealthPotion.name, player)

    assert healed == 0
    assert inventory.get_quantity(HealthPotion.name) == 1


def test_remove_item_validates_quantity():
    player = Player(0, 0)
    inventory = player.inventory
    inventory.add_item(HealthPotion())

    with pytest.raises(KeyError):
        inventory.remove_item(HealthPotion.name, quantity=2)

    with pytest.raises(ValueError):
        inventory.remove_item(HealthPotion.name, quantity=0)
