import pygame
import uuid
from src.core.entity import Entity

class NPC(Entity):
    """Classe base para NPCs interativos."""

    def __init__(self, name: str, position: tuple[int, int], sprite: pygame.Surface, dialogues: list[str]):
        npc_id = uuid.uuid4()
        super().__init__(
            id=npc_id,
            name=name,
            position=position,
            health=100,
            speed=0,
            sprite=sprite
        )
        self.dialogues = dialogues
        self.current_dialogue_index = 0
        self.is_interacting = False
        self.interaction_range = 50

    def interact(self):
        """Inicia ou avança o diálogo."""
        self.is_interacting = True
        dialogue = self.dialogues[self.current_dialogue_index]
        
        # Avançar para o próximo diálogo ou resetar
        self.current_dialogue_index = (self.current_dialogue_index + 1) % len(self.dialogues)
        
        return dialogue

    def stop_interaction(self):
        """Finaliza a interação."""
        self.is_interacting = False
        self.current_dialogue_index = 0

    def update(self, dt: float, player_pos: tuple[int, int]):
        """Verifica se o jogador está perto para interação."""
        dx = player_pos[0] - self.position[0]
        dy = player_pos[1] - self.position[1]
        distance = (dx**2 + dy**2)**0.5
        
        if distance > self.interaction_range:
            self.stop_interaction()

    def render(self, screen: pygame.Surface, camera_offset: tuple[int, int]):
        """Renderiza o NPC e um indicador de interação se estiver perto."""
        super().render(screen, camera_offset)
        
        if self.is_interacting:
            # Desenhar um balão de fala simples ou indicador (Debug)
            font = pygame.font.SysFont(None, 24)
            text_surf = font.render("!", True, (255, 255, 0))
            draw_x = self.rect.x - camera_offset[0] + self.rect.width // 2
            draw_y = self.rect.y - camera_offset[1] - 20
            screen.blit(text_surf, (draw_x, draw_y))
