"""
⚔️ Combat System - Sistema de Combate
Implementa ataque, dano, crítico e knockback
"""

import math
import random
from enum import Enum
from typing import Tuple, Optional

class AttackType(Enum):
    """Tipos de ataque"""
    BASIC = "basic"
    CHARGED = "charged"
    SKILL = "skill"

class Attack:
    """Representa um ataque"""
    
    def __init__(self, attacker, attack_type: AttackType, damage: float, 
                 knockback: float = 0, element: str = "normal"):
        """
        Inicializa um ataque
        
        Args:
            attacker: Entidade que está atacando
            attack_type: Tipo de ataque
            damage: Dano base
            knockback: Força do knockback
            element: Elemento do ataque
        """
        self.attacker = attacker
        self.attack_type = attack_type
        self.damage = damage
        self.knockback = knockback
        self.element = element
        self.hit = False

class CombatSystem:
    """Sistema de combate do jogo"""
    
    def __init__(self, settings):
        """
        Inicializa o sistema de combate
        
        Args:
            settings: Objeto de configurações
        """
        self.settings = settings
        self.active_attacks = []  # Ataques ativos no frame
    
    def calculate_damage(self, attacker, defender, attack: Attack) -> Tuple[int, bool]:
        """
        Calcula o dano de um ataque
        
        Args:
            attacker: Entidade atacante
            defender: Entidade defendendo
            attack: Objeto do ataque
            
        Returns:
            Tupla (dano_final, é_crítico)
        """
        # Dano base
        damage = attack.damage
        
        # Adicionar ATK do atacante
        if hasattr(attacker, 'stats'):
            damage += attacker.stats.get('ATK', 0)
        
        # Reduzir por DEF do defensor
        if hasattr(defender, 'stats'):
            defense = defender.stats.get('DEF', 0)
            damage = max(1, damage - defense * 0.5)
        
        # Verificar crítico
        is_crit = random.random() < self.settings.CRIT_CHANCE
        if is_crit:
            damage *= self.settings.CRIT_MULTIPLIER
        
        # Variação de dano (±10%)
        variation = random.uniform(0.9, 1.1)
        damage *= variation
        
        return int(damage), is_crit
    
    def apply_attack(self, attacker, defender, attack: Attack) -> dict:
        """
        Aplica um ataque a um defensor
        
        Args:
            attacker: Entidade atacante
            defender: Entidade defendendo
            attack: Objeto do ataque
            
        Returns:
            Dicionário com resultado do ataque
        """
        # Calcular dano
        damage, is_crit = self.calculate_damage(attacker, defender, attack)
        
        # Aplicar dano
        if hasattr(defender, 'take_damage'):
            defender.take_damage(damage)
        
        # Aplicar knockback
        if attack.knockback > 0:
            self.apply_knockback(attacker, defender, attack.knockback)
        
        # Retornar resultado
        result = {
            'damage': damage,
            'is_crit': is_crit,
            'attack_type': attack.attack_type,
            'element': attack.element,
            'defender_hp': getattr(defender, 'hp', 0)
        }
        
        return result
    
    def apply_knockback(self, attacker, defender, knockback_force: float):
        """
        Aplica knockback ao defensor
        
        Args:
            attacker: Entidade atacante
            defender: Entidade defendendo
            knockback_force: Força do knockback
        """
        if not hasattr(attacker, 'get_center') or not hasattr(defender, 'get_center'):
            return
        
        # Calcular direção do knockback
        attacker_pos = attacker.get_center()
        defender_pos = defender.get_center()
        
        dx = defender_pos[0] - attacker_pos[0]
        dy = defender_pos[1] - attacker_pos[1]
        
        distance = math.sqrt(dx**2 + dy**2)
        if distance == 0:
            return
        
        # Normalizar direção
        dx /= distance
        dy /= distance
        
        # Aplicar knockback
        if hasattr(defender, 'vx') and hasattr(defender, 'vy'):
            defender.vx = dx * knockback_force
            defender.vy = dy * knockback_force

class PlayerCombat:
    """Componente de combate do player"""
    
    def __init__(self, player, combat_system):
        """
        Inicializa combate do player
        
        Args:
            player: Objeto do player
            combat_system: Sistema de combate
        """
        self.player = player
        self.combat_system = combat_system
        self.settings = combat_system.settings
        
        # Ataque
        self.attack_cooldown = self.settings.ATTACK_COOLDOWN
        self.attack_cooldown_timer = 0
        self.attack_range = self.settings.ATTACK_RANGE
        self.attack_damage = self.settings.ATTACK_DAMAGE_BASE
        
        # Ataque carregado
        self.is_charging = False
        self.charge_timer = 0
        self.max_charge_time = 1.0  # segundos
        self.charge_damage_multiplier = 2.0
        
        # Stats do player
        self.stats = {
            'ATK': 10,
            'DEF': 5,
            'SPD': 8,
            'SP.ATK': 7,
            'SP.DEF': 6
        }
    
    def handle_attack_input(self, mouse_pos: Tuple[int, int], is_clicking: bool, 
                           is_holding: bool):
        """
        Processa entrada de ataque
        
        Args:
            mouse_pos: Posição do mouse
            is_clicking: Se clicou (início do clique)
            is_holding: Se está segurando
        """
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= 1/60  # Assumindo 60 FPS
            return
        
        if is_clicking:
            # Começar carregamento
            self.is_charging = True
            self.charge_timer = 0
        
        if is_holding and self.is_charging:
            # Aumentar carregamento
            self.charge_timer += 1/60
            self.charge_timer = min(self.charge_timer, self.max_charge_time)
        
        if not is_holding and self.is_charging:
            # Soltar ataque
            self.perform_attack(mouse_pos)
            self.is_charging = False
            self.charge_timer = 0
    
    def perform_attack(self, target_pos: Tuple[int, int]) -> Optional[Attack]:
        """
        Realiza um ataque
        
        Args:
            target_pos: Posição alvo do ataque
            
        Returns:
            Objeto do ataque ou None
        """
        if self.attack_cooldown_timer > 0:
            return None
        
        # Determinar tipo de ataque
        if self.charge_timer > 0.5:
            attack_type = AttackType.CHARGED
            damage_multiplier = 1.0 + (self.charge_timer / self.max_charge_time)
        else:
            attack_type = AttackType.BASIC
            damage_multiplier = 1.0
        
        # Calcular dano
        damage = self.attack_damage * damage_multiplier + self.stats['ATK']
        
        # Calcular knockback
        knockback = 100 * damage_multiplier
        
        # Criar ataque
        attack = Attack(
            self.player,
            attack_type,
            damage,
            knockback,
            element="normal"
        )
        
        # Iniciar cooldown
        self.attack_cooldown_timer = self.attack_cooldown
        
        return attack
    
    def get_charge_percentage(self) -> float:
        """Retorna percentual de carregamento (0-100)"""
        if not self.is_charging:
            return 0
        return (self.charge_timer / self.max_charge_time) * 100
    
    def update(self, dt: float):
        """Atualiza cooldown"""
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt

class EnemyCombat:
    """Componente de combate do inimigo"""
    
    def __init__(self, enemy, combat_system):
        """
        Inicializa combate do inimigo
        
        Args:
            enemy: Objeto do inimigo
            combat_system: Sistema de combate
        """
        self.enemy = enemy
        self.combat_system = combat_system
        self.settings = combat_system.settings
        
        # Ataque
        self.attack_cooldown = 1.0  # segundos
        self.attack_cooldown_timer = 0
        self.attack_range = self.settings.ENEMY_ATTACK_RANGE
        self.attack_damage = 5
        
        # Stats do inimigo
        self.stats = {
            'ATK': 5,
            'DEF': 2,
            'SPD': 6,
            'SP.ATK': 4,
            'SP.DEF': 3
        }
    
    def try_attack(self, target) -> Optional[Attack]:
        """
        Tenta atacar um alvo
        
        Args:
            target: Alvo do ataque
            
        Returns:
            Objeto do ataque ou None
        """
        if self.attack_cooldown_timer > 0:
            return None
        
        # Verificar distância
        if not hasattr(self.enemy, 'get_center') or not hasattr(target, 'get_center'):
            return None
        
        enemy_pos = self.enemy.get_center()
        target_pos = target.get_center()
        
        distance = math.sqrt((enemy_pos[0] - target_pos[0])**2 + 
                            (enemy_pos[1] - target_pos[1])**2)
        
        if distance > self.attack_range:
            return None
        
        # Criar ataque
        attack = Attack(
            self.enemy,
            AttackType.BASIC,
            self.attack_damage,
            50,
            element="normal"
        )
        
        # Iniciar cooldown
        self.attack_cooldown_timer = self.attack_cooldown
        
        return attack
    
    def update(self, dt: float):
        """Atualiza cooldown"""
        if self.attack_cooldown_timer > 0:
            self.attack_cooldown_timer -= dt
