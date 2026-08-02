import pygame
import uuid
import math
from enum import Enum
from src.core.entity import Entity
from src.core.inventory import Inventory
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
        
        # Combate
        self.attack_cooldown = 0.5
        self.attack_timer = 0
        self.is_attacking = False
        self.attack_duration = 0.2
        self.attack_rect = pygame.Rect(0, 0, 40, 40)
        
        # Atributos Primários
        self.strength = 10      # Dano Físico
        self.agility = 10       # Velocidade / Stamina
        self.intelligence = 10  # Dano Mágico / MP
        
        # Stats Derivados
        self.max_hp = PLAYER_INITIAL_HP + (self.strength * 5)
        self.health = self.max_hp
        self.max_mp = 50 + (self.intelligence * 5)
        self.mp = self.max_mp
        self.max_stamina = 100 + (self.agility * 2)
        self.stamina = self.max_stamina
        self.stamina_regen = 20 + (self.agility * 0.5)
        
        # Progressão
        self.level = 1
        self.xp = 0
        self.xp_to_next_level = 100
        
        # Estado
        self.state = PlayerState.IDLE
        self.invulnerable = False
        self.invulnerable_timer = 0
        self.invulnerable_duration = 0.5
        
        # Inventário
        self.inventory = Inventory(capacity=24)

    def handle_input(self):
        """Captura os inputs do teclado para movimentação e ações."""
        keys = pygame.key.get_pressed()
        mouse_buttons = pygame.mouse.get_pressed()
        
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
            if not self.is_dashing and not self.is_attacking:
                self.state = PlayerState.WALKING
        else:
            if not self.is_dashing and not self.is_attacking:
                self.state = PlayerState.IDLE

        # Dash
        if keys[pygame.K_SPACE] and self.dash_cooldown_timer <= 0 and self.stamina >= 20:
            self.start_dash()
            
        # Ataque
        if (mouse_buttons[0] or keys[pygame.K_j]) and self.attack_timer <= 0:
            self.attack()

    def start_dash(self):
        """Inicia um dash."""
        self.is_dashing = True
        self.dash_timer = self.dash_duration
        self.dash_cooldown_timer = self.dash_cooldown
        self.stamina -= 20
        self.state = PlayerState.DASHING

    def attack(self):
        """Inicia um ataque."""
        self.is_attacking = True
        self.attack_timer = self.attack_cooldown
        self.state = PlayerState.ATTACKING
        
        # Posicionar hitbox de ataque à frente do jogador
        self.attack_rect.center = (
            self.rect.centerx + self.facing_direction.x * 30,
            self.rect.centery + self.facing_direction.y * 30
        )

    def check_attack_collision(self, enemies):
        """Verifica se o ataque atingiu algum inimigo."""
        damage = 10 + (self.strength // 2)
        for enemy in enemies:
            if self.attack_rect.colliderect(enemy.rect) and enemy.health > 0:
                enemy.take_damage(damage)
                if enemy.health <= 0:
                    self.gain_xp(enemy.xp_reward)
                print(f"⚔️ Você atingiu {enemy.name}! Dano: {damage}")

    def update(self, dt: float, game_map=None, enemies=None):
        """Atualiza a lógica do jogador."""
        # Timers
        if self.dash_timer > 0:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False
        
        if self.dash_cooldown_timer > 0:
            self.dash_cooldown_timer -= dt
            
        if self.attack_timer > 0:
            self.attack_timer -= dt
            if self.attack_timer <= (self.attack_cooldown - self.attack_duration):
                self.is_attacking = False
            
        if self.invulnerable:
            self.invulnerable_timer -= dt
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

        # Input
        self.handle_input()
        
        # Lógica de Ataque
        if self.is_attacking and enemies:
            self.check_attack_collision(enemies)

        # Movimentação
        bonus_speed = (self.agility - 10) * 2
        current_speed = (self.dash_speed if self.is_dashing else self.speed) + bonus_speed
        
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
            
    def gain_xp(self, amount: int):
        """Adiciona XP e verifica Level Up."""
        self.xp += amount
        while self.xp >= self.xp_to_next_level:
            self.level_up()

    def level_up(self):
        """Aumenta o nível e melhora atributos."""
        self.xp -= self.xp_to_next_level
        self.level += 1
        self.xp_to_next_level = int(self.xp_to_next_level * 1.1)
        
        self.strength += 2
        self.agility += 2
        self.intelligence += 2
        
        self.max_hp = PLAYER_INITIAL_HP + (self.strength * 5)
        self.max_mp = 50 + (self.intelligence * 5)
        self.max_stamina = 100 + (self.agility * 2)
        self.stamina_regen = 20 + (self.agility * 0.5)
        
        self.health = self.max_hp
        self.mp = self.max_mp
        self.stamina = self.max_stamina
        
        print(f"🎉 LEVEL UP! Agora você é nível {self.level}!")

    def apply_collision(self, dx: float, dy: float, game_map):
        """Aplica colisão nos eixos X e Y separadamente."""
        old_x = self.position[0]
        self.position[0] += dx
        self.rect.x = int(self.position[0])
        if game_map.is_collision(self.rect):
            self.position[0] = old_x
            self.rect.x = int(self.position[0])

        old_y = self.position[1]
        self.position[1] += dy
        self.rect.y = int(self.position[1])
        if game_map.is_collision(self.rect):
            self.position[1] = old_y
            self.rect.y = int(self.position[1])

    def render(self, screen: pygame.Surface, camera_offset: tuple[int, int]):
        """Desenha o jogador na tela com efeitos visuais."""
        color = (100, 200, 255)
        if self.invulnerable and int(self.invulnerable_timer * 10) % 2 == 0:
            color = (255, 100, 100)
        if self.is_dashing:
            color = (255, 200, 0)

        draw_pos = (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1])
        pygame.draw.rect(screen, color, (*draw_pos, self.rect.width, self.rect.height))
        
        center_x = draw_pos[0] + self.rect.width // 2
        center_y = draw_pos[1] + self.rect.height // 2
        end_x = center_x + self.facing_direction.x * 20
        end_y = center_y + self.facing_direction.y * 20
        pygame.draw.line(screen, (255, 255, 255), (center_x, center_y), (end_x, end_y), 2)

        if self.is_attacking:
            attack_draw_pos = (self.attack_rect.x - camera_offset[0], self.attack_rect.y - camera_offset[1])
            pygame.draw.rect(screen, (255, 255, 255), (*attack_draw_pos, self.attack_rect.width, self.attack_rect.height), 2)

        if self.settings.DEBUG:
            pygame.draw.rect(screen, (0, 255, 0), (*draw_pos, self.rect.width, self.rect.height), 1)
            if self.is_attacking:
                attack_draw_pos = (self.attack_rect.x - camera_offset[0], self.attack_rect.y - camera_offset[1])
                pygame.draw.rect(screen, (255, 255, 0), (*attack_draw_pos, self.attack_rect.width, self.attack_rect.height), 1)
