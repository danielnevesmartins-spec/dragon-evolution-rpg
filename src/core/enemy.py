import pygame
import uuid
import math
from src.core.entity import Entity

class Enemy(Entity):
    """Classe base para inimigos com IA simples."""

    def __init__(self, name: str, position: tuple[int, int], health: int, speed: int, sprite: pygame.Surface, xp_reward: int = 20):
        enemy_id = uuid.uuid4()
        super().__init__(
            id=enemy_id,
            name=name,
            position=position,
            health=health,
            speed=speed,
            sprite=sprite
        )
        self.xp_reward = xp_reward
        self.chase_range = 200
        self.attack_range = 40
        self.attack_cooldown = 1.0
        self.attack_timer = 0
        self.damage = 10

    def update(self, dt: float, player, game_map=None):
        """Lógica de IA: Perseguir o jogador se estiver no alcance."""
        if self.health <= 0:
            return

        # Calcular distância até o jogador
        dx = player.position[0] - self.position[0]
        dy = player.position[1] - self.position[1]
        distance = math.sqrt(dx**2 + dy**2)

        if self.attack_timer > 0:
            self.attack_timer -= dt

        # IA de Perseguição
        if self.attack_range < distance < self.chase_range:
            # Normalizar direção
            dir_x = dx / distance
            dir_y = dy / distance
            
            move_x = dir_x * self.speed * dt
            move_y = dir_y * self.speed * dt
            
            if game_map:
                self.apply_collision(move_x, move_y, game_map)
            else:
                self.move(move_x, move_y)
        
        # IA de Ataque
        elif distance <= self.attack_range and self.attack_timer <= 0:
            self.attack(player)
            self.attack_timer = self.attack_cooldown

    def take_damage(self, amount: int, source_pos: tuple[int, int] = None):
        """Reduz a saúde da entidade com knockback opcional."""
        super().take_damage(amount)
            
        # Aplicar Knockback simples
        if source_pos and self.health > 0:
            dx = self.position[0] - source_pos[0]
            dy = self.position[1] - source_pos[1]
            dist = (dx**2 + dy**2)**0.5
            if dist > 0:
                self.position[0] += (dx / dist) * 15
                self.position[1] += (dy / dist) * 15
                self.rect.topleft = (int(self.position[0]), int(self.position[1]))

    def attack(self, player):
        """Causa dano ao jogador com knockback."""
        player.take_damage(self.damage, self.position)
        print(f"💥 {self.name} atacou você! Dano: {self.damage}")



    def render(self, screen: pygame.Surface, camera_offset: tuple[int, int]):
        """Renderiza o inimigo e sua barra de vida."""
        if self.health <= 0:
            return
            
        super().render(screen, camera_offset)
        
        # Barra de vida simples acima do inimigo
        bar_width = self.rect.width
        bar_height = 5
        health_ratio = self.health / self.max_health
        
        draw_x = self.rect.x - camera_offset[0]
        draw_y = self.rect.y - camera_offset[1] - 10
        
        # Fundo (vermelho)
        pygame.draw.rect(screen, (255, 0, 0), (draw_x, draw_y, bar_width, bar_height))
        # Vida atual (verde)
        pygame.draw.rect(screen, (0, 255, 0), (draw_x, draw_y, bar_width * health_ratio, bar_height))
