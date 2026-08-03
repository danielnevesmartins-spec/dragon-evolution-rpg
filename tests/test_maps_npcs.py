import pygame
import unittest
import os
from src.core.tiled_map import TiledMap
from src.core.npc import NPC
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TestMapsNPCs(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pygame.init()
        cls.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        cls.dummy_sprite = pygame.Surface((32, 32))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def test_tiled_map_loading(self):
        # Verificar se o mapa de teste existe
        map_path = "maps/test_map.tmx"
        self.assertTrue(os.path.exists(map_path))
        
        # Carregar o mapa
        tiled_map = TiledMap(map_path)
        self.assertEqual(tiled_map.width, 20 * 32)
        self.assertEqual(tiled_map.height, 20 * 32)
        
        # Verificar colisões (o tile ID 3 no nosso XML é parede)
        # No nosso CSV, a borda é preenchida com 3.
        # Rect na posição (0,0) deve colidir
        rect_wall = pygame.Rect(0, 0, 32, 32)
        self.assertTrue(tiled_map.is_collision(rect_wall))
        
        # Rect no centro (320, 320) não deve colidir (é grama ID 1)
        rect_grass = pygame.Rect(320, 320, 32, 32)
        self.assertFalse(tiled_map.is_collision(rect_grass))

    def test_npc_interaction(self):
        dialogues = ["Olá!", "Tudo bem?"]
        npc = NPC("Test NPC", (100, 100), self.dummy_sprite, dialogues)
        
        # Primeira interação
        msg1 = npc.interact()
        self.assertEqual(msg1, "Olá!")
        self.assertTrue(npc.is_interacting)
        
        # Segunda interação
        msg2 = npc.interact()
        self.assertEqual(msg2, "Tudo bem?")
        
        # Afastar o jogador deve parar a interação
        npc.update(0.1, (500, 500))
        self.assertFalse(npc.is_interacting)

if __name__ == '__main__':
    unittest.main()
