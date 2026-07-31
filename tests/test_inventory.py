import pygame
import unittest
import uuid
from src.core.inventory import Inventory
from src.core.item import Item, CollectibleItem

class TestInventory(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1, 1))
        cls.dummy_icon = pygame.Surface((16, 16))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_inventory_add_item(self):
        inv = Inventory(capacity=2)
        item1 = Item(uuid.uuid4(), "Item 1", "Desc", self.dummy_icon, stackable=False)
        item2 = Item(uuid.uuid4(), "Item 2", "Desc", self.dummy_icon, stackable=False)
        item3 = Item(uuid.uuid4(), "Item 3", "Desc", self.dummy_icon, stackable=False)

        self.assertTrue(inv.add_item(item1))
        self.assertTrue(inv.add_item(item2))
        self.assertFalse(inv.add_item(item3)) # Inventário cheio
        self.assertEqual(len(inv.items), 2)

    def test_inventory_stacking(self):
        inv = Inventory(capacity=5)
        item = Item(uuid.uuid4(), "Potion", "Heals", self.dummy_icon, stackable=True)
        
        inv.add_item(item, 1)
        inv.add_item(item, 2)
        
        self.assertEqual(len(inv.items), 1)
        self.assertEqual(inv.get_item_count("Potion"), 3)

    def test_collectible_item(self):
        inv = Inventory(capacity=5)
        item = Item(uuid.uuid4(), "Gold", "Shiny", self.dummy_icon, stackable=True)
        collectible = CollectibleItem(item, (50, 50))
        
        self.assertTrue(collectible.collect(inv))
        self.assertEqual(inv.get_item_count("Gold"), 1)

if __name__ == '__main__':
    unittest.main()
