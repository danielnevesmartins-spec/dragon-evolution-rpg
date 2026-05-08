"""
🎁 Loot Table System - Sistema de Tabelas de Loot
Define drop tables para inimigos e regiões
"""

import random
from typing import List, Tuple, Optional
from .item import Item, ItemRarity, get_item

class LootEntry:
    """Entrada em uma tabela de loot"""
    
    def __init__(self, item_id: str, chance: float, quantity_min: int = 1, 
                 quantity_max: int = 1):
        """
        Inicializa entrada de loot
        
        Args:
            item_id: ID do item
            chance: Chance de drop (0-1)
            quantity_min: Quantidade mínima
            quantity_max: Quantidade máxima
        """
        self.item_id = item_id
        self.chance = chance
        self.quantity_min = quantity_min
        self.quantity_max = quantity_max
    
    def roll(self) -> Optional[Tuple[str, int]]:
        """
        Tenta fazer o roll do loot
        
        Returns:
            Tupla (item_id, quantidade) ou None
        """
        if random.random() < self.chance:
            quantity = random.randint(self.quantity_min, self.quantity_max)
            return (self.item_id, quantity)
        return None

class LootTable:
    """Tabela de loot para um inimigo/região"""
    
    def __init__(self, name: str):
        """
        Inicializa tabela de loot
        
        Args:
            name: Nome da tabela
        """
        self.name = name
        self.entries: List[LootEntry] = []
    
    def add_entry(self, item_id: str, chance: float, 
                  quantity_min: int = 1, quantity_max: int = 1):
        """
        Adiciona entrada à tabela
        
        Args:
            item_id: ID do item
            chance: Chance de drop
            quantity_min: Quantidade mínima
            quantity_max: Quantidade máxima
        """
        entry = LootEntry(item_id, chance, quantity_min, quantity_max)
        self.entries.append(entry)
    
    def roll(self) -> List[Tuple[str, int]]:
        """
        Faz roll da tabela de loot
        
        Returns:
            Lista de (item_id, quantidade)
        """
        loot = []
        for entry in self.entries:
            result = entry.roll()
            if result:
                loot.append(result)
        return loot
    
    def __repr__(self) -> str:
        return f"LootTable({self.name}, entries={len(self.entries)})"

# Definição de tabelas de loot por tipo de inimigo
LOOT_TABLES = {
    'goblin': LootTable('Goblin Loot'),
    'orc': LootTable('Orc Loot'),
    'skeleton': LootTable('Skeleton Loot'),
}

# Configurar tabelas de loot
# Goblin
LOOT_TABLES['goblin'].add_entry('copper_ore', 0.5, 1, 3)
LOOT_TABLES['goblin'].add_entry('health_potion', 0.2, 1, 1)
LOOT_TABLES['goblin'].add_entry('iron_sword', 0.05)

# Orc
LOOT_TABLES['orc'].add_entry('iron_ore', 0.6, 1, 2)
LOOT_TABLES['orc'].add_entry('health_potion', 0.3, 1, 2)
LOOT_TABLES['orc'].add_entry('iron_armor', 0.1)
LOOT_TABLES['orc'].add_entry('steel_sword', 0.05)

# Skeleton
LOOT_TABLES['skeleton'].add_entry('copper_ore', 0.4, 1, 2)
LOOT_TABLES['skeleton'].add_entry('stamina_potion', 0.25, 1, 1)
LOOT_TABLES['skeleton'].add_entry('leather_armor', 0.08)

class LootDrop:
    """Representa um drop de loot no chão"""
    
    def __init__(self, x: float, y: float, item: Item):
        """
        Inicializa drop de loot
        
        Args:
            x: Posição X
            y: Posição Y
            item: Item dropado
        """
        self.x = x
        self.y = y
        self.item = item
        self.pickup_timer = 0
        self.pickup_delay = 0.5  # segundos antes de poder pegar
        self.lifetime = 300  # segundos antes de desaparecer
        self.time_alive = 0
    
    def update(self, dt: float):
        """Atualiza o drop"""
        self.time_alive += dt
        if self.pickup_timer < self.pickup_delay:
            self.pickup_timer += dt
    
    def can_pickup(self) -> bool:
        """Verifica se pode pegar o item"""
        return self.pickup_timer >= self.pickup_delay and self.time_alive < self.lifetime
    
    def is_expired(self) -> bool:
        """Verifica se expirou"""
        return self.time_alive >= self.lifetime
    
    def draw(self, surface):
        """Desenha o drop"""
        import pygame
        
        # Desenhar item como quadrado colorido
        color = self.item.get_rarity_color()
        pygame.draw.rect(surface, color, (self.x - 5, self.y - 5, 10, 10))
        pygame.draw.rect(surface, (255, 255, 255), (self.x - 5, self.y - 5, 10, 10), 1)
    
    def __repr__(self) -> str:
        return f"LootDrop({self.item.name} at ({self.x}, {self.y}))"

class LootManager:
    """Gerencia drops de loot"""
    
    def __init__(self):
        """Inicializa gerenciador de loot"""
        self.drops: List[LootDrop] = []
    
    def spawn_loot(self, x: float, y: float, enemy_type: str) -> List[LootDrop]:
        """
        Spawna loot de um inimigo
        
        Args:
            x: Posição X
            y: Posição Y
            enemy_type: Tipo de inimigo
            
        Returns:
            Lista de drops criados
        """
        if enemy_type not in LOOT_TABLES:
            return []
        
        loot_table = LOOT_TABLES[enemy_type]
        loot_rolls = loot_table.roll()
        
        drops = []
        for item_id, quantity in loot_rolls:
            for _ in range(quantity):
                item = get_item(item_id)
                if item:
                    item.quantity = 1
                    # Adicionar offset aleatório para não stacking perfeito
                    offset_x = random.uniform(-10, 10)
                    offset_y = random.uniform(-10, 10)
                    drop = LootDrop(x + offset_x, y + offset_y, item)
                    self.drops.append(drop)
                    drops.append(drop)
        
        return drops
    
    def update(self, dt: float):
        """Atualiza todos os drops"""
        for drop in self.drops[:]:
            drop.update(dt)
            
            # Remover se expirou
            if drop.is_expired():
                self.drops.remove(drop)
    
    def pickup_loot(self, player_pos: Tuple[float, float], 
                    pickup_range: float = 50) -> List[Item]:
        """
        Pega loot próximo ao player
        
        Args:
            player_pos: Posição do player
            pickup_range: Raio de pickup
            
        Returns:
            Lista de itens pegados
        """
        import math
        
        picked_items = []
        
        for drop in self.drops[:]:
            if not drop.can_pickup():
                continue
            
            # Calcular distância
            distance = math.sqrt((drop.x - player_pos[0])**2 + 
                               (drop.y - player_pos[1])**2)
            
            if distance <= pickup_range:
                picked_items.append(drop.item)
                self.drops.remove(drop)
        
        return picked_items
    
    def draw(self, surface):
        """Desenha todos os drops"""
        for drop in self.drops:
            drop.draw(surface)
    
    def clear(self):
        """Limpa todos os drops"""
        self.drops.clear()
    
    def __repr__(self) -> str:
        return f"LootManager(drops={len(self.drops)})"
