import pygame
import unittest
import uuid
from src.player.player import Player
from src.core.enemy import Enemy
from src.settings import PLAYER_INITIAL_HP

class DummySettings:
    DEBUG = True
    SHOW_HITBOXES = False

class TestCombat(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((1, 1))
        cls.settings = DummySettings()
        cls.dummy_sprite = pygame.Surface((32, 32))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_enemy_chase_player(self):
        player = Player((200, 200), self.settings)
        enemy = Enemy("Test Slime", (100, 100), 50, 100, self.dummy_sprite)
        
        # Simular update do inimigo
        enemy.update(0.1, player)
        
        # O inimigo deve ter se movido em direção ao jogador (x > 100, y > 100)
        self.assertGreater(enemy.position[0], 100)
        self.assertGreater(enemy.position[1], 100)

    def test_player_attack_enemy(self):
        player = Player((100, 100), self.settings)
        enemy = Enemy("Test Slime", (120, 100), 50, 0, self.dummy_sprite)
        enemies = [enemy]
        
        # Jogador ataca
        player.facing_direction = pygame.math.Vector2(1, 0) # Olhando para a direita
        player.attack()
        player.check_attack_collision(enemies)
        
        # O inimigo deve ter recebido dano
        self.assertLess(enemy.health, 50)

    def test_enemy_attack_player(self):
        player = Player((100, 100), self.settings)
        enemy = Enemy("Test Slime", (110, 100), 50, 0, self.dummy_sprite)
        
        # Inimigo ataca o jogador
        enemy.attack(player)
        
        # O jogador deve ter recebido dano
        self.assertLess(player.health, player.max_hp)

if __name__ == '__main__':
    unittest.main()
