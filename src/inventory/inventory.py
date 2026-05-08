"""
🎒 Inventory System - Sistema de Inventário
Gerencia items, slots, equipamento e consumo
"""

from typing import List, Optional, Dict
from src.loot import Item, EquippableItem, ConsumableItem

class InventorySlot:
    """Representa um slot do inventário"""
    
    def __init__(self, slot_id: int, max_quantity: int = 99):
        """
        Inicializa um slot
        
        Args:
            slot_id: ID do slot
            max_quantity: Quantidade máxima por slot
        """
        self.slot_id = slot_id
        self.item: Optional[Item] = None
        self.quantity = 0
        self.max_quantity = max_quantity
    
    def add_item(self, item: Item, quantity: int = 1) -> int:
        """
        Adiciona item ao slot
        
        Args:
            item: Item a adicionar
            quantity: Quantidade
            
        Returns:
            Quantidade que não coube
        """
        if self.item is None:
            self.item = item
            added = min(quantity, self.max_quantity)
            self.quantity = added
            return quantity - added
        
        # Se é o mesmo item
        if self.item.item_id == item.item_id:
            space = self.max_quantity - self.quantity
            added = min(quantity, space)
            self.quantity += added
            return quantity - added
        
        # Slot ocupado com item diferente
        return quantity
    
    def remove_item(self, quantity: int = 1) -> bool:
        """
        Remove item do slot
        
        Args:
            quantity: Quantidade a remover
            
        Returns:
            True se removeu
        """
        if self.item is None or self.quantity == 0:
            return False
        
        self.quantity -= quantity
        
        if self.quantity <= 0:
            self.item = None
            self.quantity = 0
        
        return True
    
    def is_empty(self) -> bool:
        """Verifica se slot está vazio"""
        return self.item is None or self.quantity == 0
    
    def __repr__(self) -> str:
        if self.item:
            return f"Slot({self.item.name} x{self.quantity})"
        return "Slot(empty)"

class Inventory:
    """Gerencia inventário do player"""
    
    def __init__(self, capacity: int = 20):
        """
        Inicializa inventário
        
        Args:
            capacity: Número de slots
        """
        self.capacity = capacity
        self.slots: List[InventorySlot] = [
            InventorySlot(i) for i in range(capacity)
        ]
        
        # Slots de equipamento
        self.equipped = {
            'weapon': None,
            'armor': None,
            'accessory': None
        }
        
        # Ouro
        self.gold = 0
    
    def add_item(self, item: Item, quantity: int = 1) -> bool:
        """
        Adiciona item ao inventário
        
        Args:
            item: Item a adicionar
            quantity: Quantidade
            
        Returns:
            True se coube tudo
        """
        remaining = quantity
        
        # Procurar slot com item igual
        for slot in self.slots:
            if slot.item and slot.item.item_id == item.item_id:
                remaining = slot.add_item(item, remaining)
                if remaining == 0:
                    return True
        
        # Procurar slot vazio
        for slot in self.slots:
            if slot.is_empty():
                remaining = slot.add_item(item, remaining)
                if remaining == 0:
                    return True
        
        # Não coube tudo
        return remaining == 0
    
    def remove_item(self, item_id: str, quantity: int = 1) -> bool:
        """
        Remove item do inventário
        
        Args:
            item_id: ID do item
            quantity: Quantidade
            
        Returns:
            True se removeu
        """
        remaining = quantity
        
        for slot in self.slots:
            if slot.item and slot.item.item_id == item_id:
                removed = min(remaining, slot.quantity)
                slot.remove_item(removed)
                remaining -= removed
                
                if remaining == 0:
                    return True
        
        return remaining == 0
    
    def find_item(self, item_id: str) -> Optional[InventorySlot]:
        """
        Encontra um item no inventário
        
        Args:
            item_id: ID do item
            
        Returns:
            Slot com o item ou None
        """
        for slot in self.slots:
            if slot.item and slot.item.item_id == item_id:
                return slot
        return None
    
    def get_item_quantity(self, item_id: str) -> int:
        """
        Retorna quantidade de um item
        
        Args:
            item_id: ID do item
            
        Returns:
            Quantidade total
        """
        total = 0
        for slot in self.slots:
            if slot.item and slot.item.item_id == item_id:
                total += slot.quantity
        return total
    
    def equip_item(self, slot_id: int) -> bool:
        """
        Equipa item de um slot
        
        Args:
            slot_id: ID do slot
            
        Returns:
            True se equipou
        """
        slot = self.slots[slot_id]
        
        if not slot.item or not isinstance(slot.item, EquippableItem):
            return False
        
        # Desequipar item anterior
        if slot.item.item_type.value == 'weapon' and self.equipped['weapon']:
            self.equipped['weapon'].unequip()
        elif slot.item.item_type.value == 'armor' and self.equipped['armor']:
            self.equipped['armor'].unequip()
        
        # Equipar novo item
        slot.item.equip()
        
        if slot.item.item_type.value == 'weapon':
            self.equipped['weapon'] = slot.item
        elif slot.item.item_type.value == 'armor':
            self.equipped['armor'] = slot.item
        
        return True
    
    def unequip_item(self, slot_type: str) -> bool:
        """
        Desequipa item
        
        Args:
            slot_type: Tipo de slot ('weapon', 'armor', 'accessory')
            
        Returns:
            True se desequipou
        """
        if self.equipped[slot_type]:
            self.equipped[slot_type].unequip()
            self.equipped[slot_type] = None
            return True
        return False
    
    def use_item(self, slot_id: int, target) -> bool:
        """
        Usa um item consumível
        
        Args:
            slot_id: ID do slot
            target: Alvo do item
            
        Returns:
            True se usou
        """
        slot = self.slots[slot_id]
        
        if not slot.item or not isinstance(slot.item, ConsumableItem):
            return False
        
        if slot.item.use(target):
            if slot.item.quantity <= 0:
                slot.remove_item(1)
            return True
        
        return False
    
    def get_total_stats_bonus(self) -> Dict[str, int]:
        """
        Calcula bônus total de stats dos itens equipados
        
        Returns:
            Dicionário com bônus de stats
        """
        bonus = {}
        
        for slot_type, item in self.equipped.items():
            if item and isinstance(item, EquippableItem):
                for stat, value in item.stat_bonuses.items():
                    bonus[stat] = bonus.get(stat, 0) + value
        
        return bonus
    
    def add_gold(self, amount: int):
        """Adiciona ouro"""
        self.gold += amount
    
    def remove_gold(self, amount: int) -> bool:
        """Remove ouro"""
        if self.gold >= amount:
            self.gold -= amount
            return True
        return False
    
    def get_empty_slots(self) -> int:
        """Retorna número de slots vazios"""
        return sum(1 for slot in self.slots if slot.is_empty())
    
    def get_used_slots(self) -> int:
        """Retorna número de slots usados"""
        return self.capacity - self.get_empty_slots()
    
    def is_full(self) -> bool:
        """Verifica se inventário está cheio"""
        return self.get_empty_slots() == 0
    
    def clear(self):
        """Limpa inventário"""
        for slot in self.slots:
            slot.item = None
            slot.quantity = 0
        self.gold = 0
    
    def __repr__(self) -> str:
        used = self.get_used_slots()
        return f"Inventory({used}/{self.capacity} slots, {self.gold} gold)"
