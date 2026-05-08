"""
🎮 Player System - Sistema de Jogador
Implementa movimentação, animações e mecânicas do player
"""

import pygame
import math
from enum import Enum
from typing import Tuple

class PlayerState(Enum):
    """Estados possíveis do player"""
    IDLE = "idle"
    WALKING = "walking"
    DASHING = "dashing"
    ATTACKING = "attacking"
    HURT = "hurt"
    DEAD = "dead"

class Player(pygame.sprite.Sprite):
    """Classe principal do jogador"""
    
    def __init__(self, x: float, y: float, settings):
        """
        Inicializa o player
        
        Args:
            x: Posição X inicial
            y: Posição Y inicial
            settings: Objeto de configurações do jogo
        """
        super().__init__()
        
        # Configurações
        self.settings = settings
        
        # Posição e dimensões
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        
        # Velocidade
        self.vx = 0
        self.vy = 0
        self.speed = settings.PLAYER_SPEED
        
        # Dash
        self.dash_speed = settings.PLAYER_DASH_SPEED
        self.dash_duration = settings.PLAYER_DASH_DURATION
        self.dash_cooldown = settings.PLAYER_DASH_COOLDOWN
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.is_dashing = False
        
        # Stats
        self.max_hp = settings.PLAYER_INITIAL_HP
        self.hp = self.max_hp
        self.max_stamina = settings.PLAYER_INITIAL_STAMINA
        self.stamina = self.max_stamina
        self.stamina_regen = 30  # por segundo
        
        # Estado
        self.state = PlayerState.IDLE
        self.direction = (0, 0)  # Direção atual
        self.facing_direction = (1, 0)  # Direção para onde o player está olhando
        
        # Animação
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 0.1  # segundos por frame
        
        # Hitbox
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hurtbox = pygame.Rect(self.x + 5, self.y + 5, self.width - 10, self.height - 10)
        
        # Invulnerabilidade
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 0.5  # segundos
        
        # Criar surface
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((100, 200, 255))  # Cor temporária (azul claro)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
    
    def handle_input(self, keys):
        """
        Processa entrada do teclado
        
        Args:
            keys: Dicionário de teclas pressionadas
        """
        # Movimento
        dx = 0
        dy = 0
        
        if keys.get(pygame.K_w):
            dy -= 1
        if keys.get(pygame.K_s):
            dy += 1
        if keys.get(pygame.K_a):
            dx -= 1
        if keys.get(pygame.K_d):
            dx += 1
        
        # Normalizar direção
        if dx != 0 or dy != 0:
            magnitude = math.sqrt(dx**2 + dy**2)
            self.direction = (dx / magnitude, dy / magnitude)
            self.facing_direction = self.direction
            
            if self.state != PlayerState.DASHING:
                self.state = PlayerState.WALKING
        else:
            self.direction = (0, 0)
            if self.state != PlayerState.DASHING:
                self.state = PlayerState.IDLE
        
        # Dash
        if keys.get(pygame.K_SPACE) and self.dash_cooldown_timer <= 0 and self.stamina >= 20:
            self.start_dash()
    
    def start_dash(self):
        """Inicia um dash"""
        if not self.is_dashing and self.dash_cooldown_timer <= 0:
            self.is_dashing = True
            self.dash_timer = self.dash_duration
            self.dash_cooldown_timer = self.dash_cooldown
            self.stamina -= 20
            self.state = PlayerState.DASHING
    
    def update(self, dt: float, obstacles: list = None):
        """
        Atualiza o player
        
        Args:
            dt: Delta time em segundos
            obstacles: Lista de obstáculos para colisão
        """
        # Atualizar dash
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
        
        # Atualizar cooldown de dash
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= dt
        
        # Atualizar invulnerabilidade
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False
        
        # Calcular velocidade
        if self.is_dashing:
            speed = self.dash_speed
        else:
            speed = self.speed
        
        self.vx = self.direction[0] * speed
        self.vy = self.direction[1] * speed
        
        # Atualizar posição
        new_x = self.x + self.vx * dt
        new_y = self.y + self.vy * dt
        
        # Verificar colisões
        if obstacles:
            self.check_collisions(new_x, new_y, obstacles)
        else:
            self.x = new_x
            self.y = new_y
        
        # Atualizar stamina
        if not self.is_dashing:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen * dt)
        
        # Atualizar hitbox
        self.hitbox.topleft = (self.x, self.y)
        self.hurtbox.topleft = (self.x + 5, self.y + 5)
        
        # Atualizar rect
        self.rect.topleft = (self.x, self.y)
        
        # Atualizar animação
        self.update_animation(dt)
    
    def check_collisions(self, new_x: float, new_y: float, obstacles: list):
        """
        Verifica colisões com obstáculos
        
        Args:
            new_x: Nova posição X
            new_y: Nova posição Y
            obstacles: Lista de obstáculos
        """
        # Criar rect temporário para verificar colisão
        temp_rect = pygame.Rect(new_x, new_y, self.width, self.height)
        
        # Verificar colisão com cada obstáculo
        collision = False
        for obstacle in obstacles:
            if temp_rect.colliderect(obstacle):
                collision = True
                break
        
        # Se não colidiu, atualizar posição
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
    
    def update_animation(self, dt: float):
        """
        Atualiza animação do player
        
        Args:
            dt: Delta time em segundos
        """
        self.animation_timer += dt
        
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.animation_frame = (self.animation_frame + 1) % 4
    
    def take_damage(self, damage: int):
        """
        Player recebe dano
        
        Args:
            damage: Quantidade de dano
        """
        if not self.invulnerable:
            self.hp -= damage
            self.invulnerable = True
            self.invulnerable_timer = self.invulnerable_duration
            self.state = PlayerState.HURT
            
            if self.hp <= 0:
                self.hp = 0
                self.state = PlayerState.DEAD
    
    def heal(self, amount: int):
        """
        Player recupera HP
        
        Args:
            amount: Quantidade de cura
        """
        self.hp = min(self.max_hp, self.hp + amount)
    
    def draw(self, surface: pygame.Surface):
        """
        Desenha o player
        
        Args:
            surface: Surface para desenhar
        """
        # Desenhar player (temporário - apenas um retângulo)
        color = (100, 200, 255)
        
        # Se invulnerável, piscar
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            color = (255, 100, 100)
        
        # Se dashing, cor diferente
        if self.is_dashing:
            color = (255, 200, 0)
        
        pygame.draw.rect(surface, color, (self.x, self.y, self.width, self.height))
        
        # Desenhar direção (linha)
        end_x = self.x + self.width // 2 + self.facing_direction[0] * 15
        end_y = self.y + self.height // 2 + self.facing_direction[1] * 15
        pygame.draw.line(surface, (255, 255, 255), 
                        (self.x + self.width // 2, self.y + self.height // 2),
                        (end_x, end_y), 2)
        
        # Desenhar hitbox se debug
        if self.settings.SHOW_HITBOXES:
            pygame.draw.rect(surface, (0, 255, 0), self.hitbox, 1)
            pygame.draw.rect(surface, (255, 0, 0), self.hurtbox, 1)
    
    def get_position(self) -> Tuple[float, float]:
        """Retorna a posição do player"""
        return (self.x, self.y)
    
    def get_center(self) -> Tuple[float, float]:
        """Retorna o centro do player"""
        return (self.x + self.width // 2, self.y + self.height // 2)
    
    def is_alive(self) -> bool:
        """Retorna se o player está vivo"""
        return self.hp > 0
    
    def __repr__(self) -> str:
        """Representação em string"""
        return f"Player(x={self.x:.1f}, y={self.y:.1f}, hp={self.hp}/{self.max_hp}, state={self.state.value})"
