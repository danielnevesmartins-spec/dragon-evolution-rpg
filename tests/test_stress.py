import pygame
import unittest
import uuid
from src.player.player import Player
from src.core.item import Item
from src.core.inventory import Inventory

class DummySettings:
    DEBUG = True
    SHOW_HITBOXES = False

class TestStress(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1, 1))
        cls.settings = DummySettings()

    def test_inventory_overflow(self):
        inventory = Inventory(capacity=2)
        item1 = Item(uuid.uuid4(), "Item 1", "Desc", pygame.Surface((8,8)))
        item2 = Item(uuid.uuid4(), "Item 2", "Desc", pygame.Surface((8,8)))
        item3 = Item(uuid.uuid4(), "Item 3", "Desc", pygame.Surface((8,8)))
        
        self.assertTrue(inventory.add_item(item1))
        self.assertTrue(inventory.add_item(item2))
        self.assertFalse(inventory.add_item(item3)) # Deve falhar (cheio)
        self.assertEqual(len(inventory.items), 2)

    def test_player_death_state(self):
        player = Player((100, 100), self.settings)
        player.take_damage(200) # Dano fatal
        
        self.assertEqual(player.health, 0)
        from src.player.player import PlayerState
        self.assertEqual(player.state, PlayerState.DEAD)

    def test_rapid_level_up(self):
        player = Player((100, 100), self.settings)
        initial_str = player.strength
        
        # Ganhar XP suficiente para 2 levels
        player.gain_xp(300) 
        
        self.assertGreater(player.level, 1)
        self.assertGreater(player.strength, initial_str)
        self.assertEqual(player.health, player.max_hp) # Curado no level up

if __name__ == '__main__':
    unittest.main()
