import pygame
import unittest
import uuid
from unittest.mock import Mock

from src.core.entity import Entity
from src.core.item import Item
from src.core.map import Map
from src.settings import TILE_SIZE

class TestCoreClasses(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1, 1))
        cls.dummy_sprite = pygame.Surface((32, 32))
        cls.dummy_sprite.fill((255, 255, 255))
        cls.dummy_icon = pygame.Surface((16, 16))
        cls.dummy_icon.fill((0, 0, 255))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_entity_creation(self):
        entity_id = uuid.uuid4()
        entity = Entity(entity_id, "Test Entity", (0, 0), 100, 5, self.dummy_sprite)
        self.assertEqual(entity.id, entity_id)
        self.assertEqual(entity.name, "Test Entity")
        self.assertEqual(entity.health, 100)
        self.assertEqual(entity.max_health, 100)
        self.assertEqual(entity.speed, 5)
        self.assertEqual(entity.position, [0, 0])
        self.assertIsInstance(entity.rect, pygame.Rect)

    def test_entity_movement(self):
        entity_id = uuid.uuid4()
        entity = Entity(entity_id, "Test Entity", (0, 0), 100, 5, self.dummy_sprite)
        entity.move(10, 20)
        self.assertEqual(entity.position, [10, 20])
        self.assertEqual(entity.rect.topleft, (10, 20))

    def test_entity_take_damage_and_heal(self):
        entity_id = uuid.uuid4()
        entity = Entity(entity_id, "Test Entity", (0, 0), 100, 5, self.dummy_sprite)
        entity.take_damage(30)
        self.assertEqual(entity.health, 70)
        entity.heal(15)
        self.assertEqual(entity.health, 85)
        entity.heal(100) # Overheal
        self.assertEqual(entity.health, 100)
        entity.take_damage(200) # Overkill
        self.assertEqual(entity.health, 0)

    def test_item_creation(self):
        item_id = uuid.uuid4()
        item = Item(item_id, "Potion", "Heals 50 HP", self.dummy_icon, stackable=True, value=10)
        self.assertEqual(item.id, item_id)
        self.assertEqual(item.name, "Potion")
        self.assertEqual(item.description, "Heals 50 HP")
        self.assertTrue(item.stackable)
        self.assertEqual(item.value, 10)

    def test_item_get_info(self):
        item_id = uuid.uuid4()
        item = Item(item_id, "Sword", "Sharp blade", self.dummy_icon, stackable=False, value=50)
        expected_info = "Sword\n  Descrição: Sharp blade\n  Valor: 50 moedas\n"
        self.assertEqual(item.get_info(), expected_info)

    def test_map_creation(self):
        game_map = Map("Test Map", 640, 480, TILE_SIZE)
        self.assertEqual(game_map.name, "Test Map")
        self.assertEqual(game_map.width, 640)
        self.assertEqual(game_map.height, 480)
        self.assertEqual(game_map.tile_size, TILE_SIZE)
        self.assertGreater(len(game_map.tiles), 0)
        self.assertGreater(len(game_map.collision_rects), 0)

    def test_map_collision(self):
        game_map = Map("Test Map", 640, 480, TILE_SIZE)
        # Test collision with a known collision rect (border)
        collision_rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
        self.assertTrue(game_map.is_collision(collision_rect))

        # Test no collision with a rect far from any collision
        no_collision_rect = pygame.Rect(300, 300, TILE_SIZE, TILE_SIZE)
        self.assertFalse(game_map.is_collision(no_collision_rect))

if __name__ == '__main__':
    unittest.main()
