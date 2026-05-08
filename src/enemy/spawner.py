"""
🎯 Enemy Spawner - Sistema de Spawn de Inimigos
Gerencia spawn, despawn e limite de inimigos
"""

import random
import math
from typing import List, Tuple
from .enemy import Enemy

class EnemySpawner:
    """Gerencia spawn de inimigos"""
    
    def __init__(self, settings):
        """
        Inicializa o spawner
        
        Args:
            settings: Objeto de configurações
        """
        self.settings = settings
        self.enemies: List[Enemy] = []
        self.spawn_timer = 0
        self.spawn_interval = 2.0  # segundos
        self.spawn_distance = settings.ENEMY_SPAWN_DISTANCE
        self.despawn_distance = settings.ENEMY_DESPAWN_DISTANCE
        self.max_enemies = settings.MAX_ENEMIES_SIMULTANEOUS
        
        # Tipos de inimigos disponíveis
        self.enemy_types = [
            "goblin",
            "orc",
            "skeleton"
        ]
    
    def update(self, dt: float, player):
        """
        Atualiza o spawner
        
        Args:
            dt: Delta time
            player: Referência ao player
        """
        # Atualizar spawn timer
        self.spawn_timer += dt
        
        # Tentar spawnar novo inimigo
        if self.spawn_timer >= self.spawn_interval and len(self.enemies) < self.max_enemies:
            self.spawn_enemy(player)
            self.spawn_timer = 0
        
        # Atualizar inimigos
        for enemy in self.enemies[:]:
            enemy.update(dt, player)
            
            # Verificar se deve despawnar
            if self.should_despawn(enemy, player):
                self.enemies.remove(enemy)
    
    def spawn_enemy(self, player):
        """
        Spawna um novo inimigo
        
        Args:
            player: Referência ao player
        """
        player_pos = player.get_center()
        
        # Escolher ângulo aleatório
        angle = random.uniform(0, 2 * math.pi)
        
        # Calcular posição de spawn
        spawn_x = player_pos[0] + math.cos(angle) * self.spawn_distance
        spawn_y = player_pos[1] + math.sin(angle) * self.spawn_distance
        
        # Escolher tipo de inimigo
        enemy_type = random.choice(self.enemy_types)
        
        # Calcular nível baseado no player
        player_level = getattr(player, 'level', 1)
        enemy_level = max(1, player_level + random.randint(-1, 1))
        
        # Criar inimigo
        enemy = Enemy(spawn_x, spawn_y, enemy_type, enemy_level, self.settings)
        self.enemies.append(enemy)
    
    def should_despawn(self, enemy: Enemy, player) -> bool:
        """
        Verifica se um inimigo deve ser despawnado
        
        Args:
            enemy: Inimigo a verificar
            player: Referência ao player
            
        Returns:
            True se deve despawnar
        """
        # Não despawnar se ainda está vivo e perto
        if enemy.is_alive():
            player_pos = player.get_center()
            enemy_pos = enemy.get_center()
            
            distance = math.sqrt((player_pos[0] - enemy_pos[0])**2 + 
                               (player_pos[1] - enemy_pos[1])**2)
            
            if distance < self.despawn_distance:
                return False
        
        # Despawnar se está morto ou muito longe
        return True
    
    def get_enemies_in_range(self, pos: Tuple[float, float], 
                            radius: float) -> List[Enemy]:
        """
        Retorna inimigos em um raio
        
        Args:
            pos: Posição central
            radius: Raio de busca
            
        Returns:
            Lista de inimigos no raio
        """
        enemies_in_range = []
        
        for enemy in self.enemies:
            if not enemy.is_alive():
                continue
            
            enemy_pos = enemy.get_center()
            distance = math.sqrt((pos[0] - enemy_pos[0])**2 + 
                               (pos[1] - enemy_pos[1])**2)
            
            if distance <= radius:
                enemies_in_range.append(enemy)
        
        return enemies_in_range
    
    def draw(self, surface):
        """
        Desenha todos os inimigos
        
        Args:
            surface: Surface para desenhar
        """
        for enemy in self.enemies:
            enemy.draw(surface)
    
    def get_alive_count(self) -> int:
        """Retorna quantidade de inimigos vivos"""
        return sum(1 for enemy in self.enemies if enemy.is_alive())
    
    def clear(self):
        """Limpa todos os inimigos"""
        self.enemies.clear()
    
    def __repr__(self) -> str:
        """Representação em string"""
        alive = self.get_alive_count()
        return f"EnemySpawner(enemies={len(self.enemies)}, alive={alive}, max={self.max_enemies})"
