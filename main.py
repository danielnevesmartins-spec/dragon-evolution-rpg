#!/usr/bin/env python3
"""
🐉 Dragon Evolution RPG - Main Entry Point
Arquivo principal que inicia o jogo
"""

import sys
import os

# Adicionar src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import pygame
from src.settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, TILE_SIZE,
    Colors, DEBUG, SHOW_FPS, validate_config
)
import uuid
from src.core.map import Map
from src.core.item import Item, CollectibleItem
from src.core.enemy import Enemy
from src.player.player import Player

class Game:
    """Classe principal do jogo"""
    
    def __init__(self):
        """Inicializa o jogo"""
        # Validar configurações
        validate_config()
        
        # Inicializar Pygame
        pygame.init()
        
        # Criar tela
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)
        
        # Clock para FPS
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = FPS
        
        # Fonte para debug
        self.font = pygame.font.Font(None, 24)

        # Inicializar mapa
        self.current_map = Map("World 1", SCREEN_WIDTH * 2, SCREEN_HEIGHT * 2, TILE_SIZE)
        
        # Inicializar Player no centro do mapa
        self.player = Player((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), self)
        
        # Lista de itens no mundo
        self.world_items = []
        self._spawn_test_items()
        
        # Lista de inimigos
        self.enemies = []
        self._spawn_test_enemies()
        
        self.camera_offset = [0, 0] # Offset da câmera para rolagem

    def _spawn_test_enemies(self):
        """Cria alguns inimigos de teste no mapa."""
        slime_sprite = pygame.Surface((32, 32))
        slime_sprite.fill(Colors.GREEN.value)
        
        # Adicionar alguns Slimes em posições variadas
        self.enemies.append(Enemy("Slime Verde", (SCREEN_WIDTH // 2 + 200, SCREEN_HEIGHT // 2 + 100), 30, 80, slime_sprite, 25))
        self.enemies.append(Enemy("Slime Azul", (SCREEN_WIDTH // 2 - 200, SCREEN_HEIGHT // 2 - 100), 40, 60, slime_sprite, 35))

    def _spawn_test_items(self):
        """Cria alguns itens de teste no mapa."""
        # Criar uma poção de teste
        potion_icon = pygame.Surface((16, 16))
        potion_icon.fill(Colors.RED.value)
        
        test_potion = Item(
            id=uuid.uuid4(),
            name="Poção de Vida",
            description="Recupera 20 HP",
            icon=potion_icon,
            stackable=True,
            value=50
        )
        
        # Adicionar ao mundo em posições variadas
        self.world_items.append(CollectibleItem(test_potion, (SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT // 2)))
        self.world_items.append(CollectibleItem(test_potion, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 50)))
        
        print(f"✓ {GAME_TITLE} inicializado com sucesso!")
        print(f"  Resolução: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
        print(f"  FPS: {self.fps}")
        print(f"  Debug: {DEBUG}")
    
    def handle_events(self):
        """Processa eventos do jogo"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def update(self, dt):
        """Atualiza lógica do jogo"""
        # Atualizar Player (Passando a lista de inimigos para detecção de ataque)
        self.player.update(dt, self.current_map, self.enemies)

        # Atualizar Inimigos
        for enemy in self.enemies[:]:
            if enemy.health > 0:
                enemy.update(dt, self.player, self.current_map)
            else:
                # Se o inimigo morreu, remover da lista (ou deixar o corpo)
                self.enemies.remove(enemy)
                print(f"💀 {enemy.name} foi derrotado!")

        # Verificar coleta de itens
        for item in self.world_items[:]:
            if self.player.rect.colliderect(item.rect):
                if item.collect(self.player.inventory):
                    self.world_items.remove(item)
                    self.player.gain_xp(50) # Ganhar 50 XP por item coletado
                    print(f"Coletado: {item.name} (+50 XP)")

        # Atualizar Câmera para seguir o Player
        self.camera_offset[0] = self.player.rect.centerx - SCREEN_WIDTH // 2
        self.camera_offset[1] = self.player.rect.centery - SCREEN_HEIGHT // 2
        
        # Limitar câmera aos limites do mapa
        self.camera_offset[0] = max(0, min(self.camera_offset[0], self.current_map.width - SCREEN_WIDTH))
        self.camera_offset[1] = max(0, min(self.camera_offset[1], self.current_map.height - SCREEN_HEIGHT))
    
    def render(self):
        """Renderiza o jogo"""
        # Limpar tela
        self.screen.fill(Colors.DARK_GRAY.value)

        # Renderizar mapa
        self.current_map.render(self.screen, self.camera_offset)
        
        # Renderizar Player
        self.player.render(self.screen, self.camera_offset)
        
        # Renderizar Itens no Mundo
        for item in self.world_items:
            item.render(self.screen, self.camera_offset)
            
        # Renderizar Inimigos
        for enemy in self.enemies:
            enemy.render(self.screen, self.camera_offset)
            
        # Renderizar UI de Status (Simples)
        ui_y = 20
        status_lines = [
            f"Nível: {self.player.level} (XP: {self.player.xp}/{self.player.xp_to_next_level})",
            f"HP: {int(self.player.health)}/{self.player.max_hp}",
            f"MP: {int(self.player.mp)}/{self.player.max_mp}",
            f"Stamina: {int(self.player.stamina)}/{int(self.player.max_stamina)}",
            f"Inventário: {len(self.player.inventory.items)}/{self.player.inventory.capacity}"
        ]
        
        for line in status_lines:
            text_surf = self.font.render(line, True, Colors.WHITE.value)
            self.screen.blit(text_surf, (20, ui_y))
            ui_y += 25
        
        # Renderizar título
        title_text = self.font.render(f"🐉 {GAME_TITLE}", True, Colors.WHITE.value)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        # Renderizar status
        status_text = self.font.render("Estado: Planejamento - FASE 0", True, Colors.YELLOW.value)
        status_rect = status_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(status_text, status_rect)
        
        # Renderizar versão
        version_text = self.font.render("v0.0.0", True, Colors.GRAY.value)
        version_rect = version_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        self.screen.blit(version_text, version_rect)
        
        # Renderizar instruções
        instructions = [
            "Estrutura base do projeto criada com sucesso!",
            "",
            "Player System implementado com sucesso!",
            "",
            "Use WASD ou SETAS para mover o jogador.",
            "Pressione ESPAÇO para dar um DASH.",
            "Pressione ESC para sair"
        ]
        
        y_offset = 300
        for instruction in instructions:
            if instruction:
                text = self.font.render(instruction, True, Colors.WHITE.value)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
            y_offset += 40
        
        # Renderizar FPS se debug ativado
        if SHOW_FPS:
            fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, Colors.GREEN.value)
            self.screen.blit(fps_text, (10, 10))
        
        # Atualizar display
        pygame.display.flip()
    
    def run(self):
        """Loop principal do jogo"""
        print("\n🎮 Iniciando loop principal...")
        print("Pressione ESC para sair\n")
        
        while self.running:
            # Calcular delta time
            dt = self.clock.tick(self.fps) / 1000.0
            
            # Processar eventos
            self.handle_events()
            
            # Atualizar lógica
            self.update(dt)
            
            # Renderizar
            self.render()
        
        self.quit()
    
    def quit(self):
        """Encerra o jogo"""
        print("\n✓ Encerrando jogo...")
        pygame.quit()
        print("✓ Jogo finalizado com sucesso!")
        sys.exit(0)

def main():
    """Função principal"""
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"❌ Erro ao executar jogo: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
