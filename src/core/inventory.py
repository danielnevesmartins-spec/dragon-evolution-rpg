from typing import List, Optional
from src.core.item import Item

class Inventory:
    """Gerencia a coleção de itens de uma entidade."""

    def __init__(self, capacity: int = 20):
        self.capacity = capacity
        self.items: List[dict] = []  # Lista de dicionários: {"item": Item, "quantity": int}

    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """Adiciona um item ao inventário. Retorna True se for bem-sucedido."""
        # Verificar se o item já existe e é empilhável
        if item.stackable:
            for entry in self.items:
                if entry["item"].name == item.name:
                    entry["quantity"] += quantity
                    return True

        # Se não for empilhável ou não existir, verificar capacidade
        if len(self.items) < self.capacity:
            self.items.append({"item": item, "quantity": quantity})
            return True
        
        return False

    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove uma quantidade de um item pelo nome. Retorna True se for bem-sucedido."""
        for i, entry in enumerate(self.items):
            if entry["item"].name == item_name:
                if entry["quantity"] > quantity:
                    entry["quantity"] -= quantity
                    return True
                elif entry["quantity"] == quantity:
                    self.items.pop(i)
                    return True
        return False

    def get_item_count(self, item_name: str) -> int:
        """Retorna a quantidade total de um item pelo nome."""
        for entry in self.items:
            if entry["item"].name == item_name:
                return entry["quantity"]
        return 0

    def is_full(self) -> bool:
        """Verifica se o inventário está cheio."""
        return len(self.items) >= self.capacity

    def __repr__(self):
        return f"Inventory({len(self.items)}/{self.capacity} slots used)"
