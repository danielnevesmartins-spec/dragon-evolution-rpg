#!/usr/bin/env python3
"""
🐉 Dragon Evolution RPG - Main Entry Point
Arquivo principal que inicia o jogo com suporte a Tiled Maps e NPCs
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE,
    Colors, DEBUG, SHOW_FPS, validate_config
)
import uuid
from src.core.tiled_map import TiledMap
from src.core.item import Item, CollectibleItem
from src.core.enemy import Enemy
from src.core.npc import NPC
from src.player.player import Player

class Game:
    """Classe principal do jogo"""
    
    def __init__(self):
        """Inicializa o jogo"""
        validate_config()
        pygame.init()
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = FPS
        self.font = pygame.font.Font(None, 24)
        self.dialogue_font = pygame.font.Font(None, 32)

        # Inicializar Mapa Tiled
        self.current_map = TiledMap("maps/test_map.tmx")
        
        # Inicializar Player
        self.player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), self)
        
        # Listas de entidades
        self.world_items = []
        self.enemies = []
        self.npcs = []
        
        self._spawn_entities()
        
        # Sistema de Diálogo
        self.active_dialogue = None
        self.dialogue_timer = 0

    def _spawn_entities(self):
        """Cria entidades iniciais no mundo."""
        # Itens
        potion_icon = pygame.Surface((16, 16))
        potion_icon.fill(Colors.RED.value)
        test_potion = Item(uuid.uuid4(), "Poção de Vida", "Recupera 20 HP", potion_icon, True, 50)
        self.world_items.append(CollectibleItem(test_potion, (400, 400)))
        
        # Inimigos
        slime_sprite = pygame.Surface((32, 32))
        slime_sprite.fill(Colors.GREEN.value)
        self.enemies.append(Enemy("Slime Verde", (600, 300), 30, 80, slime_sprite, 25))
        
        # NPCs
        npc_sprite = pygame.Surface((32, 32))
        npc_sprite.fill(Colors.PURPLE.value)
        self.npcs.append(NPC(
            "Ancião Dragão", 
            (300, 300), 
            npc_sprite, 
            ["Bem-vindo, jovem dragão!", "O mundo está em perigo.", "Encontre as esferas mágicas!"]
        ))

    def handle_events(self):
        """Processa eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                
                # Fechar diálogo com qualquer tecla se estiver ativo
                if self.active_dialogue:
                    self.active_dialogue = None

    def update(self, dt):
        """Atualiza lógica do jogo"""
        if self.active_dialogue:
            return # Pausar jogo durante diálogo

        # Atualizar Player
        self.player.update(dt, self.current_map, self.enemies)

        # Atualizar Inimigos
        for enemy in self.enemies[:]:
            if enemy.health > 0:
                enemy.update(dt, self.player, self.current_map)
            else:
                self.enemies.remove(enemy)

        # Atualizar NPCs e Interação
        for npc in self.npcs:
            npc.update(dt, self.player.position)
            
            # Verificar se o jogador quer interagir
            if self.player.wants_to_interact and self.player.interaction_timer <= 0:
                dx = self.player.position[0] - npc.position[0]
                dy = self.player.position[1] - npc.position[1]
                if (dx**2 + dy**2)**0.5 < npc.interaction_range:
                    self.active_dialogue = f"{npc.name}: {npc.interact()}"
                    self.player.interaction_timer = self.player.interaction_cooldown

        # Coleta de Itens
        for item in self.world_items[:]:
            if self.player.rect.colliderect(item.rect):
                if item.collect(self.player.inventory):
                    self.world_items.remove(item)
                    self.player.gain_xp(50)

        # Atualizar Câmera (Pyscroll)
        self.current_map.update(self.player.rect)

    def render(self):
        """Renderiza o jogo"""
        self.screen.fill(Colors.BLACK.value)

        # Renderizar Mapa (Camadas de fundo)
        self.current_map.render(self.screen)
        
        # Obter offset da câmera do pyscroll para renderizar entidades
        # O pyscrollGroup desenha as entidades se elas forem adicionadas a ele,
        # mas para manter compatibilidade com nosso sistema manual por enquanto:
        camera_offset = self.current_map.map_layer.view_rect.topleft
        
        # Renderizar Entidades
        for item in self.world_items:
            item.render(self.screen, camera_offset)
        
        for npc in self.npcs:
            npc.render(self.screen, camera_offset)
            
        for enemy in self.enemies:
            enemy.render(self.screen, camera_offset)
            
        self.player.render(self.screen, camera_offset)
        
        # Renderizar UI de Diálogo
        if self.active_dialogue:
            self._render_dialogue()

        # Renderizar UI de Status
        self._render_ui()
        
        pygame.display.flip()

    def _render_dialogue(self):
        """Desenha a caixa de diálogo."""
        margin = 50
        rect = pygame.Rect(margin, SCREEN_HEIGHT - 150, SCREEN_WIDTH - 2 * margin, 100)
        pygame.draw.rect(self.screen, (0, 0, 0), rect)
        pygame.draw.rect(self.screen, (255, 255, 255), rect, 2)
        
        text_surf = self.dialogue_font.render(self.active_dialogue, True, Colors.WHITE.value)
        self.screen.blit(text_surf, (rect.x + 20, rect.y + 35))

    def _render_ui(self):
        """Desenha a interface de usuário."""
        ui_y = 20
        status_lines = [
            f"Nível: {self.player.level} (XP: {self.player.xp}/{self.player.xp_to_next_level})",
            f"HP: {int(self.player.health)}/{self.player.max_hp}",
            f"MP: {int(self.player.mp)}/{self.player.max_mp}",
            f"Stamina: {int(self.player.stamina)}/{int(self.player.max_stamina)}",
            f"Inventário: {len(self.player.inventory.items)}/{self.player.inventory.capacity}",
            "[E] Interagir | [J/Mouse] Atacar | [Espaço] Dash"
        ]
        
        for line in status_lines:
            text_surf = self.font.render(line, True, Colors.WHITE.value)
            # Fundo preto para legibilidade
            bg_rect = text_surf.get_rect(topleft=(20, ui_y))
            pygame.draw.rect(self.screen, (0, 0, 0, 128), bg_rect.inflate(10, 5))
            self.screen.blit(text_surf, (20, ui_y))
            ui_y += 25

        if SHOW_FPS:
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, Colors.GREEN.value)
            self.screen.blit(fps_text, (SCREEN_WIDTH - 80, 10))

    def run(self):
        """Loop principal do jogo"""
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.update(dt)
            self.render()
        self.quit()
    
    def quit(self):
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    Game().run()
