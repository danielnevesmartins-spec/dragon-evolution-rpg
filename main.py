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
    SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GAME_TITLE, 
    Colors, DEBUG, SHOW_FPS, validate_config
)

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
        pass
    
    def render(self):
        """Renderiza o jogo"""
        # Limpar tela
        self.screen.fill(Colors.BLACK.value)
        
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
            "Próximo passo: Implementar Player System",
            "",
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
