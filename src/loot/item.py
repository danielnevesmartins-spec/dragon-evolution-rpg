"""
💎 Item System - Sistema de Itens
Define itens, raridade e propriedades
"""

from enum import Enum
from typing import Dict, Optional

class ItemRarity(Enum):
    """Raridade de itens"""
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5

class ItemType(Enum):
    """Tipos de itens"""
    WEAPON = "weapon"
    ARMOR = "armor"
    CONSUMABLE = "consumable"
    MATERIAL = "material"
    QUEST = "quest"

class Item:
    """Classe base de item"""
    
    def __init__(self, item_id: str, name: str, description: str, 
                 item_type: ItemType, rarity: ItemRarity, 
                 value: int = 0, icon: str = ""):
        """
        Inicializa um item
        
        Args:
            item_id: ID único do item
            name: Nome do item
            description: Descrição
            item_type: Tipo de item
            rarity: Raridade
            value: Valor em ouro
            icon: Caminho do ícone
        """
        self.item_id = item_id
        self.name = name
        self.description = description
        self.item_type = item_type
        self.rarity = rarity
        self.value = value
        self.icon = icon
        self.quantity = 1
    
    def get_rarity_color(self) -> tuple:
        """Retorna cor baseada na raridade"""
        colors = {
            ItemRarity.COMMON: (200, 200, 200),      # Cinza
            ItemRarity.UNCOMMON: (0, 255, 0),        # Verde
            ItemRarity.RARE: (0, 0, 255),            # Azul
            ItemRarity.EPIC: (128, 0, 128),          # Roxo
            ItemRarity.LEGENDARY: (255, 215, 0)      # Ouro
        }
        return colors.get(self.rarity, (255, 255, 255))
    
    def __repr__(self) -> str:
        return f"Item({self.name}, {self.rarity.name}, qty={self.quantity})"

class EquippableItem(Item):
    """Item que pode ser equipado"""
    
    def __init__(self, item_id: str, name: str, description: str,
                 item_type: ItemType, rarity: ItemRarity,
                 value: int = 0, icon: str = "",
                 stat_bonuses: Optional[Dict[str, int]] = None):
        """
        Inicializa um item equipável
        
        Args:
            stat_bonuses: Dicionário de bônus de stats
        """
        super().__init__(item_id, name, description, item_type, rarity, value, icon)
        self.stat_bonuses = stat_bonuses or {}
        self.is_equipped = False
    
    def get_stat_bonus(self, stat: str) -> int:
        """Retorna bônus de um stat"""
        return self.stat_bonuses.get(stat, 0)
    
    def equip(self):
        """Equipa o item"""
        self.is_equipped = True
    
    def unequip(self):
        """Desequipa o item"""
        self.is_equipped = False

class ConsumableItem(Item):
    """Item consumível"""
    
    def __init__(self, item_id: str, name: str, description: str,
                 rarity: ItemRarity, value: int = 0, icon: str = "",
                 effect: Optional[Dict] = None):
        """
        Inicializa um item consumível
        
        Args:
            effect: Dicionário com efeito (tipo, valor)
        """
        super().__init__(item_id, name, description, ItemType.CONSUMABLE, rarity, value, icon)
        self.effect = effect or {}
        self.quantity = 1
    
    def use(self, target) -> bool:
        """
        Usa o item em um alvo
        
        Args:
            target: Alvo do item
            
        Returns:
            True se usou com sucesso
        """
        if self.quantity <= 0:
            return False
        
        effect_type = self.effect.get('type', 'none')
        effect_value = self.effect.get('value', 0)
        
        if effect_type == 'heal':
            if hasattr(target, 'heal'):
                target.heal(effect_value)
                self.quantity -= 1
                return True
        
        elif effect_type == 'restore_stamina':
            if hasattr(target, 'stamina'):
                target.stamina = min(target.max_stamina, 
                                    target.stamina + effect_value)
                self.quantity -= 1
                return True
        
        elif effect_type == 'buff':
            # Aplicar buff (implementar depois)
            self.quantity -= 1
            return True
        
        return False

# Definição de itens pré-configurados
ITEM_DATABASE = {
    # Armas
    'iron_sword': EquippableItem(
        'iron_sword', 'Espada de Ferro', 'Uma espada comum de ferro',
        ItemType.WEAPON, ItemRarity.COMMON, value=50,
        stat_bonuses={'ATK': 5}
    ),
    'steel_sword': EquippableItem(
        'steel_sword', 'Espada de Aço', 'Uma espada de aço de boa qualidade',
        ItemType.WEAPON, ItemRarity.UNCOMMON, value=150,
        stat_bonuses={'ATK': 10}
    ),
    'legendary_sword': EquippableItem(
        'legendary_sword', 'Espada Lendária', 'Uma espada lendária com poder antigo',
        ItemType.WEAPON, ItemRarity.LEGENDARY, value=1000,
        stat_bonuses={'ATK': 25, 'SPD': 5}
    ),
    
    # Armaduras
    'leather_armor': EquippableItem(
        'leather_armor', 'Armadura de Couro', 'Armadura básica de couro',
        ItemType.ARMOR, ItemRarity.COMMON, value=40,
        stat_bonuses={'DEF': 3}
    ),
    'iron_armor': EquippableItem(
        'iron_armor', 'Armadura de Ferro', 'Armadura de ferro resistente',
        ItemType.ARMOR, ItemRarity.UNCOMMON, value=120,
        stat_bonuses={'DEF': 8}
    ),
    
    # Consumíveis
    'health_potion': ConsumableItem(
        'health_potion', 'Poção de Vida', 'Restaura 50 de HP',
        ItemRarity.COMMON, value=25,
        effect={'type': 'heal', 'value': 50}
    ),
    'greater_health_potion': ConsumableItem(
        'greater_health_potion', 'Poção de Vida Maior', 'Restaura 150 de HP',
        ItemRarity.UNCOMMON, value=75,
        effect={'type': 'heal', 'value': 150}
    ),
    'stamina_potion': ConsumableItem(
        'stamina_potion', 'Poção de Stamina', 'Restaura 50 de Stamina',
        ItemRarity.COMMON, value=30,
        effect={'type': 'restore_stamina', 'value': 50}
    ),
    
    # Materiais
    'copper_ore': Item(
        'copper_ore', 'Minério de Cobre', 'Minério bruto de cobre',
        ItemType.MATERIAL, ItemRarity.COMMON, value=10
    ),
    'iron_ore': Item(
        'iron_ore', 'Minério de Ferro', 'Minério bruto de ferro',
        ItemType.MATERIAL, ItemRarity.UNCOMMON, value=25
    ),
}

def get_item(item_id: str) -> Optional[Item]:
    """
    Retorna um item do banco de dados
    
    Args:
        item_id: ID do item
        
    Returns:
        Item ou None
    """
    if item_id in ITEM_DATABASE:
        item = ITEM_DATABASE[item_id]
        # Criar cópia para não modificar original
        if isinstance(item, EquippableItem):
            return EquippableItem(
                item.item_id, item.name, item.description,
                item.item_type, item.rarity, item.value, item.icon,
                item.stat_bonuses.copy()
            )
        elif isinstance(item, ConsumableItem):
            return ConsumableItem(
                item.item_id, item.name, item.description,
                item.rarity, item.value, item.icon,
                item.effect.copy()
            )
        else:
            return Item(
                item.item_id, item.name, item.description,
                item.item_type, item.rarity, item.value, item.icon
            )
    return None
