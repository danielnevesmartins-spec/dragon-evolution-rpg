"""
📈 Level System - Sistema de Nível e Experiência
Gerencia XP, level up e progressão de stats
"""

from typing import Dict, List

class LevelSystem:
    """Sistema de nível e experiência"""
    
    def __init__(self, settings):
        """
        Inicializa o sistema de nível
        
        Args:
            settings: Objeto de configurações
        """
        self.settings = settings
        
        # Configurações de XP
        self.xp_per_kill_base = settings.XP_PER_KILL_BASE
        self.level_up_xp_base = settings.LEVEL_UP_XP_BASE
        self.level_up_xp_multiplier = settings.LEVEL_UP_XP_MULTIPLIER
    
    def calculate_xp_for_level(self, level: int) -> int:
        """
        Calcula XP necessário para atingir um nível
        
        Args:
            level: Nível alvo
            
        Returns:
            XP necessário
        """
        if level <= 1:
            return 0
        
        xp = self.level_up_xp_base
        for i in range(1, level):
            xp = int(xp * self.level_up_xp_multiplier)
        
        return xp
    
    def calculate_xp_to_next_level(self, current_level: int, current_xp: int) -> int:
        """
        Calcula XP necessário para o próximo nível
        
        Args:
            current_level: Nível atual
            current_xp: XP atual
            
        Returns:
            XP necessário para próximo nível
        """
        next_level_xp = self.calculate_xp_for_level(current_level + 1)
        current_level_xp = self.calculate_xp_for_level(current_level)
        
        xp_needed = next_level_xp - current_level_xp
        xp_progress = current_xp - current_level_xp
        
        return max(0, xp_needed - xp_progress)
    
    def get_xp_percentage(self, current_level: int, current_xp: int) -> float:
        """
        Calcula percentual de XP para o próximo nível
        
        Args:
            current_level: Nível atual
            current_xp: XP atual
            
        Returns:
            Percentual (0-100)
        """
        current_level_xp = self.calculate_xp_for_level(current_level)
        next_level_xp = self.calculate_xp_for_level(current_level + 1)
        
        xp_needed = next_level_xp - current_level_xp
        xp_progress = current_xp - current_level_xp
        
        if xp_needed == 0:
            return 0
        
        return (xp_progress / xp_needed) * 100
    
    def calculate_xp_reward(self, enemy_level: int, player_level: int) -> int:
        """
        Calcula XP recompensado por matar um inimigo
        
        Args:
            enemy_level: Nível do inimigo
            player_level: Nível do player
            
        Returns:
            XP recompensado
        """
        base_xp = self.xp_per_kill_base + (enemy_level * 10)
        
        # Bônus/penalidade por diferença de nível
        level_diff = enemy_level - player_level
        
        if level_diff > 0:
            # Inimigo mais forte = mais XP
            multiplier = 1.0 + (level_diff * 0.2)
        elif level_diff < -5:
            # Inimigo muito mais fraco = menos XP
            multiplier = 0.1
        else:
            # Inimigo mais fraco = menos XP
            multiplier = 1.0 + (level_diff * 0.05)
        
        return int(base_xp * multiplier)

class PlayerProgression:
    """Gerencia progressão do player"""
    
    def __init__(self, level_system: LevelSystem):
        """
        Inicializa progressão do player
        
        Args:
            level_system: Sistema de nível
        """
        self.level_system = level_system
        
        # Atributos
        self.level = 1
        self.xp = 0
        self.skill_points = 0
        
        # Stats base
        self.base_stats = {
            'HP': 100,
            'ATK': 10,
            'DEF': 5,
            'SPD': 8,
            'SP.ATK': 7,
            'SP.DEF': 6
        }
        
        # Stats atuais (com bônus)
        self.stats = self.base_stats.copy()
        
        # Histórico de level ups
        self.level_up_history: List[Dict] = []
    
    def add_xp(self, amount: int) -> List[int]:
        """
        Adiciona XP ao player
        
        Args:
            amount: Quantidade de XP
            
        Returns:
            Lista de níveis conquistados
        """
        self.xp += amount
        levels_gained = []
        
        # Verificar level ups
        while True:
            next_level_xp = self.level_system.calculate_xp_for_level(self.level + 1)
            
            if self.xp >= next_level_xp:
                self.level_up()
                levels_gained.append(self.level)
            else:
                break
        
        return levels_gained
    
    def level_up(self):
        """Realiza um level up"""
        self.level += 1
        self.skill_points += 1
        
        # Aumentar stats
        stat_increases = {
            'HP': 10,
            'ATK': 2,
            'DEF': 1,
            'SPD': 1,
            'SP.ATK': 1,
            'SP.DEF': 1
        }
        
        for stat, increase in stat_increases.items():
            self.stats[stat] += increase
        
        # Registrar no histórico
        self.level_up_history.append({
            'level': self.level,
            'xp': self.xp,
            'stats': self.stats.copy()
        })
    
    def get_stat(self, stat_name: str) -> int:
        """
        Retorna valor de um stat
        
        Args:
            stat_name: Nome do stat
            
        Returns:
            Valor do stat
        """
        return self.stats.get(stat_name, 0)
    
    def get_all_stats(self) -> Dict[str, int]:
        """Retorna todos os stats"""
        return self.stats.copy()
    
    def get_xp_info(self) -> Dict:
        """Retorna informações de XP"""
        xp_to_next = self.level_system.calculate_xp_to_next_level(self.level, self.xp)
        xp_percentage = self.level_system.get_xp_percentage(self.level, self.xp)
        
        return {
            'level': self.level,
            'xp': self.xp,
            'xp_to_next': xp_to_next,
            'xp_percentage': xp_percentage,
            'skill_points': self.skill_points
        }
    
    def __repr__(self) -> str:
        """Representação em string"""
        xp_info = self.get_xp_info()
        return f"PlayerProgression(level={self.level}, xp={self.xp}, xp_to_next={xp_info['xp_to_next']}, skill_points={self.skill_points})"
