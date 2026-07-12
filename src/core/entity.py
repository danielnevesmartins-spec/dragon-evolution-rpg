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

    def move(self, dx: int, dy: int):
        """Move a entidade por dx e dy unidades."""
        self.position[0] += dx
        self.position[1] += dy
        self.rect.topleft = self.position

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
