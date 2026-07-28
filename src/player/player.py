import pygame
import uuid
import math
from enum import Enum
from src.core.entity import Entity
from src.settings import PLAYER_SPEED, PLAYER_INITIAL_HP, PLAYER_DASH_SPEED, PLAYER_DASH_DURATION, PLAYER_DASH_COOLDOWN

class PlayerState(Enum):
    """Estados possíveis do player"""
    IDLE = "idle"
    WALKING = "walking"
    DASHING = "dashing"
    ATTACKING = "attacking"
    HURT = "hurt"
    DEAD = "dead"

class Player(Entity):
    """Classe principal do jogador, herdando de Entity."""

    def __init__(self, position: tuple[int, int], settings):
        # Criar uma surface temporária para o player (azul claro)
        sprite = pygame.Surface((32, 32))
        sprite.fill((100, 200, 255))
        
        player_id = uuid.uuid4()
        super().__init__(
            id=player_id,
            name="Dragon Hero",
            position=position,
            health=PLAYER_INITIAL_HP,
            speed=PLAYER_SPEED,
            sprite=sprite
        )
        
        self.settings = settings
        self.direction = pygame.math.Vector2(0, 0)
        self.facing_direction = pygame.math.Vector2(1, 0)
        
        # Dash
        self.dash_speed = PLAYER_DASH_SPEED
        self.dash_duration = PLAYER_DASH_DURATION
        self.dash_cooldown = PLAYER_DASH_COOLDOWN
        self.dash_timer = 0
        self.dash_cooldown_timer = 0
        self.is_dashing = False
        
        # Stats
        self.stamina = 100
        self.max_stamina = 100
        self.stamina_regen = 30
        self.level = 1
        self.xp = 0
        
        # Estado
        self.state = PlayerState.IDLE
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 0.5

    def handle_input(self):
        """Captura os inputs do teclado para movimentação e ações."""
        keys = pygame.key.get_pressed()
        
        # Resetar direção
        self.direction.x = 0
        self.direction.y = 0

        if keys[pygame.K_w] or keys[pygame.K_UP]:
            self.direction.y = -1
        elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
            self.direction.y = 1
            
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.direction.x = -1
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.direction.x = 1

        # Normalizar direção
        if self.direction.magnitude() > 0:
            self.direction = self.direction.normalize()
            self.facing_direction = self.direction.copy()
            if not self.is_dashing:
                self.state = PlayerState.WALKING
        else:
            if not self.is_dashing:
                self.state = PlayerState.IDLE

        # Dash
        if keys[pygame.K_SPACE] and self.dash_cooldown_timer <= 0 and self.stamina >= 20:
            self.start_dash()

    def start_dash(self):
        """Inicia um dash."""
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cooldown_timer = self.dash_cooldown
        self.stamina -= 20
        self.state = PlayerState.DASHING

    def update(self, dt: float, game_map=None):
        """Atualiza a lógica do jogador."""
        # Timers
        if self.dash_timer > 0:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
        
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= dt
            
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        # Input
        self.handle_input()

        # Movimentação
        current_speed = self.dash_speed if self.is_dashing else self.speed
        move_x = self.direction.x * current_speed * dt
        move_y = self.direction.y * current_speed * dt

        # Colisão
        if game_map:
            self.apply_collision(move_x, move_y, game_map)
        else:
            self.move(move_x, move_y)

        # Stamina
        if not self.is_dashing:
            self.stamina = min(self.max_stamina, self.stamina + self.stamina_regen * dt)

    def apply_collision(self, dx: float, dy: float, game_map):
        """Aplica colisão nos eixos X e Y separadamente."""
        # Eixo X
        old_x = self.position[0]
        self.position[0] += dx
        self.rect.x = int(self.position[0])
        if game_map.is_collision(self.rect):
            self.position[0] = old_x
            self.rect.x = int(self.position[0])

        # Eixo Y
        old_y = self.position[1]
        self.position[1] += dy
        self.rect.y = int(self.position[1])
        if game_map.is_collision(self.rect):
            self.position[1] = old_y
            self.rect.y = int(self.position[1])

    def render(self, screen: pygame.Surface, camera_offset: tuple[int, int]):
        """Desenha o jogador na tela com efeitos visuais."""
        # Cor base
        color = (100, 200, 255)
        
        # Efeito de dano (piscar vermelho)
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            color = (255, 100, 100)
        
        # Efeito de dash (amarelo)
        if self.is_dashing:
            color = (255, 200, 0)

        # Desenhar o corpo do player
        draw_pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        pygame.draw.rect(screen, color, (*draw_pos, self.rect.width, self.rect.height))
        
        # Desenhar linha de direção
        center_x = draw_pos[0] + self.rect.width // 2
        center_y = draw_pos[1] + self.rect.height // 2
        end_x = center_x + self.facing_direction.x * 20
        end_y = center_y + self.facing_direction.y * 20
        pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (end_x, end_y), 2)

        # Debug: Hitbox
        if self.settings.DEBUG:
            pygame.draw.rect(screen, (0, 255, 0), (*draw_pos, self.rect.width, self.rect.height), 1)
