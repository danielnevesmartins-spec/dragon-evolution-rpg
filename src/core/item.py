import pygame
import uuid

class Item:
    """Classe base para todos os itens no jogo."""

    def __init__(self, id: uuid.UUID, name: str, description: str, icon: pygame.Surface, stackable: bool = False, value: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.icon = icon
        self.stackable = stackable
        self.value = value

    def use(self, target):
        """Lógica de uso do item (a ser implementada por subclasses)."""
        # Este método será sobrescrito por subclasses de itens específicos
        pass

    def get_info(self) -> str:
        """Retorna informações formatadas sobre o item."""
        info = f"{self.name}\n"
        info += f"  Descrição: {self.description}\n"
        info += f"  Valor: {self.value} moedas\n"
        if self.stackable:
            info += "  Empilhável\n"
        return info
