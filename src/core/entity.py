import pygame
import uuid

class Entity:
    """Classe base para todas as entidades interativas no jogo."""

    def __init__(self, id: uuid.UUID, name: str, position: tuple[int, int], health: int, speed: int, sprite: pygame.Surface):
        self.id = id
        self.name = name
        self.position = list(position)  # Convert to list for mutability
        self.health = health
        self.max_health = health
        self.speed = speed
        self.sprite = sprite
        self.rect = self.sprite.get_rect(topleft=self.position)

    def move(self, dx: float, dy: float):
        """Move a entidade por dx e dy unidades."""
        self.position[0] += dx
        self.position[1] += dy
        self.rect.topleft = (int(self.position[0]), int(self.position[1]))

    def apply_collision(self, dx: float, dy: float, game_map):
        """Aplica colisão nos eixos X e Y separadamente usando o mapa."""
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

    def take_damage(self, amount: int):
        """Reduz a saúde da entidade."""
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def heal(self, amount: int):
        """Aumenta a saúde da entidade."""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health

    def update(self, dt: float):
        """Lógica de atualização da entidade por frame."""
        pass

    def render(self, screen: pygame.Surface, camera_offset: tuple[int, int]):
        """Desenha a entidade na tela."""
        screen.blit(self.sprite, (self.rect.x - camera_offset[0], self.rect.y - camera_offset[1]))
