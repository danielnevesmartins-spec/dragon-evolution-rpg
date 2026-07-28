import pygame
import unittest
from src.player.player import Player, PlayerState
from src.core.map import Map
from src.settings import TILE_SIZE

class DummySettings:
    DEBUG = True
    SHOW_HITBOXES = False

class TestPlayer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1, 1))
        cls.settings = DummySettings()

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_player_initialization(self):
        player = Player((100, 100), self.settings)
        self.assertEqual(player.position, [100, 100])
        self.assertEqual(player.state, PlayerState.IDLE)
        self.assertEqual(player.health, 100)

    def test_player_dash(self):
        player = Player((100, 100), self.settings)
        player.start_dash()
        self.assertTrue(player.is_dashing)
        self.assertEqual(player.state, PlayerState.DASHING)
        self.assertEqual(player.stamina, 80)

    def test_player_collision_with_map(self):
        # Criar um mapa pequeno com colisão na borda
        game_map = Map("Test Map", 128, 128, TILE_SIZE)
        # Colocar player perto da borda esquerda (x=0 é colisão)
        player = Player((TILE_SIZE + 5, TILE_SIZE + 5), self.settings)
        
        # Tentar mover para a esquerda (direção x = -1)
        player.direction = pygame.math.Vector2(-1, 0)
        # Simular update com dt grande para forçar colisão
        player.update(1.0, game_map)
        
        # O player não deve conseguir entrar na zona de colisão (x < TILE_SIZE)
        self.assertGreaterEqual(player.position[0], TILE_SIZE)

if __name__ == '__main__':
    unittest.main()
