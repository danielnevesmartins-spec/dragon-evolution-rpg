"""
👹 Enemy System - Sistema de Inimigos
Implementa IA, patrulha, perseguição e combate
"""

import pygame
import math
import random
from enum import Enum
from typing import Tuple, Optional

class EnemyState(Enum):
    """Estados possíveis do inimigo"""
    IDLE = "idle"
    PATROLLING = "patrolling"
    CHASING = "chasing"
    ATTACKING = "attacking"
    HURT = "hurt"
    DEAD = "dead"
    FLEEING = "fleeing"

class Enemy(pygame.sprite.Sprite):
    """Classe de inimigo"""
    
    def __init__(self, x: float, y: float, enemy_type: str, level: int, settings):
        """
        Inicializa um inimigo
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            enemy_type: Tipo de inimigo
            level: Nível do inimigo
            settings: Objeto de configurações
        """
        super().__init__()
        
        self.settings = settings
        self.enemy_type = enemy_type
        self.level = level
        
        # Posição e dimensões
        self.x = x
        self.y = y
        self.width = 28
        self.height = 28
        
        # Velocidade
        self.vx = 0
        self.vy = 0
        self.speed = 80 + (level * 10)  # Aumenta com nível
        
        # Stats baseado no nível
        self.max_hp = 30 + (level * 5)
        self.hp = self.max_hp
        self.attack_power = 5 + (level * 2)
        self.defense = 2 + (level * 1)
        self.xp_reward = 50 + (level * 10)
        
        self.stats = {
            'ATK': self.attack_power,
            'DEF': self.defense,
            'SPD': 6,
            'SP.ATK': 4,
            'SP.DEF': 3
        }
        
        # Estado
        self.state = EnemyState.IDLE
        self.direction = (0, 0)
        
        # IA
        self.patrol_timer = 0
        self.patrol_duration = random.uniform(2, 5)
        self.patrol_range = self.settings.ENEMY_PATROL_RANGE
        self.chase_range = self.settings.ENEMY_CHASE_RANGE
        self.attack_range = self.settings.ENEMY_ATTACK_RANGE
        
        # Perseguição
        self.target = None
        self.target_lost_timer = 0
        self.target_lost_duration = 3.0  # segundos
        
        # Combate
        self.attack_cooldown = 1.0
        self.attack_cooldown_timer = 0
        self.attack_damage = self.attack_power
        
        # Invulnerabilidade
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 0.3
        
        # Hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hurtbox = pygame.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)
        
        # Criar surface
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 100, 100))  # Cor temporária (vermelho)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def update(self, dt: float, player=None, obstacles: list = None):
        """
        Atualiza o inimigo
        
        Args:
            dt: Delta time em segundos
            player: Referência ao player
            obstacles: Lista de obstáculos
        """
        # Atualizar invulnerabilidade
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        
        # Atualizar cooldown de ataque
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt
        
        # IA do inimigo
        self.update_ai(dt, player)
        
        # Aplicar velocidade
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt
        
        # Verificar colisões
        if obstacles:
            self.check_collisions(new_x, new_y, obstacles)
        else:
            self.x = new_x
            self.y = new_y
        
        # Atualizar hitbox
        self.hitbox.topleft = (self.x, self.y)
        self.hurtbox.topleft = (self.x + 5, self.y + 5)
        
        # Atualizar rect
        self.rect.topleft = (self.x, self.y)
    
    def update_ai(self, dt: float, player=None):
        """
        Atualiza a IA do inimigo
        
        Args:
            dt: Delta time
            player: Referência ao player
        """
        if self.state == EnemyState.DEAD:
            self.vx = 0
            self.vy = 0
            return
        
        # Se tem player, fazer IA de perseguição
        if player and player.is_alive():
            player_pos = player.get_center()
            enemy_pos = self.get_center()
            
            distance = math.sqrt((player_pos[0] - enemy_pos[0])**2 + 
                               (player_pos[1] - enemy_pos[1])**2)
            
            # Verificar se está no alcance de perseguição
            if distance < self.chase_range:
                self.chase_player(player)
                self.target = player
                self.target_lost_timer = 0
            elif self.target == player:
                # Perdeu o alvo
                self.target_lost_timer += dt
                if self.target_lost_timer > self.target_lost_duration:
                    self.target = None
                    self.state = EnemyState.PATROLLING
                else:
                    # Continuar em direção ao último alvo
                    self.chase_player(player)
            else:
                # Patrulhar
                self.patrol(dt)
        else:
            # Patrulhar
            self.patrol(dt)
    
    def chase_player(self, player):
        """
        Persegue o player
        
        Args:
            player: Referência ao player
        """
        player_pos = player.get_center()
        enemy_pos = self.get_center()
        
        # Calcular direção
        dx = player_pos[0] - enemy_pos[0]
        dy = player_pos[1] - enemy_pos[1]
        
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return
        
        # Normalizar direção
        dx /= distance
        dy /= distance
        
        # Aplicar velocidade
        self.vx = dx * self.speed
        self.vy = dy * self.speed
        self.direction = (dx, dy)
        
        # Verificar se está no alcance de ataque
        if distance < self.attack_range:
            self.state = EnemyState.ATTACKING
        else:
            self.state = EnemyState.CHASING
    
    def patrol(self, dt: float):
        """
        Patrulha a área
        
        Args:
            dt: Delta time
        """
        self.patrol_timer += dt
        
        if self.patrol_timer >= self.patrol_duration:
            # Escolher nova direção
            angle = random.uniform(0, 2 * math.pi)
            self.direction = (math.cos(angle), math.sin(angle))
            self.patrol_timer = 0
            self.patrol_duration = random.uniform(2, 5)
        
        # Aplicar velocidade
        self.vx = self.direction[0] * self.speed * 0.5  # Patrulha mais lenta
        self.vy = self.direction[1] * self.speed * 0.5
        
        self.state = EnemyState.PATROLLING
    
    def check_collisions(self, new_x: float, new_y: float, obstacles: list):
        """
        Verifica colisões com obstáculos
        
        Args:
            new_x: Nova posição X
            new_y: Nova posição Y
            obstacles: Lista de obstáculos
        """
        temp_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        collision = False
        for obstacle in obstacles:
            if temp_rect.colliderect(obstacle):
                collision = True
                break
        
        if not collision:
            self.x = new_x
            self.y = new_y
        else:
            # Tentar mover apenas em X
            temp_rect_x = pygame.Rect(new_x, self.y, self.width, self.height)
            collision_x = False
            for obstacle in obstacles:
                if temp_rect_x.colliderect(obstacle):
                    collision_x = True
                    break
            
            if not collision_x:
                self.x = new_x
            
            # Tentar mover apenas em Y
            temp_rect_y = pygame.Rect(self.x, new_y, self.width, self.height)
            collision_y = False
            for obstacle in obstacles:
                if temp_rect_y.colliderect(obstacle):
                    collision_y = True
                    break
            
            if not collision_y:
                self.y = new_y
    
    def take_damage(self, damage: int):
        """
        Inimigo recebe dano
        
        Args:
            damage: Quantidade de dano
        """
        if not self.invulnerable:
            self.hp -= damage
            self.invulnerable = True
            self.invulnerable_timer = self.invulnerable_duration
            self.state = EnemyState.HURT
            
            if self.hp <= 0:
                self.hp = 0
                self.state = EnemyState.DEAD
    
    def can_attack(self) -> bool:
        """Verifica se pode atacar"""
        return self.attack_cooldown_timer <= 0
    
    def attack(self):
        """Realiza um ataque"""
        self.attack_cooldown_timer = self.attack_cooldown
    
    def draw(self, surface: pygame.Surface):
        """
        Desenha o inimigo
        
        Args:
            surface: Surface para desenhar
        """
        color = (255, 100, 100)
        
        # Se invulnerável, piscar
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            color = (255, 200, 200)
        
        # Se morto, cor cinza
        if self.state == EnemyState.DEAD:
            color = (100, 100, 100)
        
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        
        # Desenhar nível
        font = pygame.font.Font(None, 16)
        level_text = font.render(str(self.level), True, (255, 255, 255))
        surface.blit(level_text, (self.x + 5, self.y + 5))
        
        # Desenhar barra de HP
        bar_width = self.width
        bar_height = 3
        bar_x = self.x
        bar_y = self.y - 5
        
        # Fundo da barra
        pygame.draw.rect(surface, (100, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Barra de HP
        hp_percentage = self.hp / self.max_hp
        hp_width = bar_width * hp_percentage
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, hp_width, bar_height))
        
        # Desenhar hitbox se debug
        if self.settings.SHOW_HITBOXES:
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 1)
            pygame.draw.rect(surface, (255, 0, 0), self.hurtbox, 1)
    
    def get_position(self) -> Tuple[float, float]:
        """Retorna a posição do inimigo"""
        return (self.x, self.y)
    
    def get_center(self) -> Tuple[float, float]:
        """Retorna o centro do inimigo"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def is_alive(self) -> bool:
        """Retorna se o inimigo está vivo"""
        return self.hp > 0
    
    def __repr__(self) -> str:
        """Representação em string"""
        return f"Enemy(type={self.enemy_type}, level={self.level}, hp={self.hp}/{self.max_hp}, state={self.state.value})"
