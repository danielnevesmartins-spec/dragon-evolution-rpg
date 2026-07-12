"""
🎮 Dragon Evolution RPG - Configurações Globais
Arquivo central com todas as configurações do jogo
"""

import os
from enum import Enum

# ============================================
# CONFIGURAÇÕES DE TELA
# ============================================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
FULLSCREEN = False
RESIZABLE = True
VSYNC = True

# ============================================
# CONFIGURAÇÕES DE CORES
# ============================================
class Colors(Enum):
    """Paleta de cores do jogo"""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    CYAN = (0, 255, 255)
    MAGENTA = (255, 0, 255)
    DARK_GRAY = (64, 64, 64)
    LIGHT_GRAY = (192, 192, 192)
    DARK_RED = (139, 0, 0)
    DARK_GREEN = (0, 100, 0)
    DARK_BLUE = (0, 0, 139)
    ORANGE = (255, 165, 0)
    PURPLE = (128, 0, 128)
    PINK = (255, 192, 203)
    BROWN = (165, 42, 42)

# ============================================
# CONFIGURAÇÕES DE JOGO
# ============================================
GAME_TITLE = "🐉 Dragon Evolution RPG"
GAME_VERSION = "v0.0.0"
GAME_STATE = "Planejamento"

# Diretórios
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC_DIR = os.path.join(BASE_DIR, 'src')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
DATA_DIR = os.path.join(BASE_DIR, 'data')
SAVE_DIR = os.path.join(BASE_DIR, 'save')
MAPS_DIR = os.path.join(BASE_DIR, 'maps')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')

# ============================================
# CONFIGURAÇÕES DE PLAYER
# ============================================
PLAYER_SPEED = 200  # pixels/segundo
PLAYER_DASH_SPEED = 400  # pixels/segundo
PLAYER_DASH_DURATION = 0.3  # segundos
PLAYER_DASH_COOLDOWN = 1.0  # segundos
PLAYER_INITIAL_HP = 100
PLAYER_INITIAL_STAMINA = 100

# ============================================
# CONFIGURAÇÕES DE COMBATE
# ============================================
ATTACK_COOLDOWN = 0.5  # segundos
ATTACK_RANGE = 50  # pixels
ATTACK_DAMAGE_BASE = 10
CRIT_CHANCE = 0.15  # 15%
CRIT_MULTIPLIER = 1.5

# ============================================
# CONFIGURAÇÕES DE INIMIGOS
# ============================================
MAX_ENEMIES_SIMULTANEOUS = 20
ENEMY_SPAWN_DISTANCE = 300  # pixels da câmera
ENEMY_DESPAWN_DISTANCE = 500  # pixels da câmera
ENEMY_PATROL_RANGE = 200  # pixels
ENEMY_CHASE_RANGE = 150  # pixels
ENEMY_ATTACK_RANGE = 40  # pixels

# ============================================
# CONFIGURAÇÕES DE XP E LEVEL
# ============================================
XP_PER_KILL_BASE = 50
LEVEL_UP_XP_BASE = 100  # XP necessário para level 1
LEVEL_UP_XP_MULTIPLIER = 1.1  # Cada level requer 10% mais XP

# ============================================
# CONFIGURAÇÕES DE MAPA
# ============================================
TILE_SIZE = 32

# ============================================
# CONFIGURAÇÕES DE LOOT
# ============================================
class ItemRarity(Enum):
    """Raridade de itens"""
    COMMON = 1
    UNCOMMON = 2
    RARE = 3
    EPIC = 4
    LEGENDARY = 5

LOOT_DROP_CHANCE = 0.3  # 30% de chance de dropar loot

# ============================================
# CONFIGURAÇÕES DE EVOLUÇÃO
# ============================================
class DragonStage(Enum):
    """Estágios de evolução do dragão"""
    EGG = 0
    HATCHLING = 1
    JUVENILE = 2
    ADULT = 3
    ANCIENT = 4

class DragonElement(Enum):
    """Elementos do dragão"""
    FIRE = "fire"
    ICE = "ice"
    LIGHTNING = "lightning"
    NATURE = "nature"
    DARKNESS = "darkness"

# ============================================
# CONFIGURAÇÕES DE DEBUG
# ============================================
DEBUG = True
SHOW_FPS = True
SHOW_HITBOXES = False
SHOW_COLLISION_BOXES = False
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL

# ============================================
# CONFIGURAÇÕES DE ÁUDIO
# ============================================
MUSIC_VOLUME = 0.7
SOUND_VOLUME = 0.8
ENABLE_AUDIO = True

# ============================================
# CONFIGURAÇÕES DE PERFORMANCE
# ============================================
USE_OBJECT_POOLING = True
MAX_PARTICLES = 1000
ENABLE_VSYNC = True
ENABLE_FULLSCREEN_OPTIMIZATION = True

# ============================================
# FUNÇÃO DE VALIDAÇÃO
# ============================================
def validate_config():
    """Valida as configurações do jogo"""
    assert SCREEN_WIDTH > 0, "Largura da tela deve ser > 0"
    assert SCREEN_HEIGHT > 0, "Altura da tela deve ser > 0"
    assert FPS > 0, "FPS deve ser > 0"
    assert 0 <= CRIT_CHANCE <= 1, "Crit chance deve estar entre 0 e 1"
    assert CRIT_MULTIPLIER > 1, "Crit multiplier deve ser > 1"
    assert MAX_ENEMIES_SIMULTANEOUS > 0, "Max inimigos deve ser > 0"
    print("✓ Configurações validadas com sucesso!")

if __name__ == "__main__":
    validate_config()
    print(f"🎮 {GAME_TITLE} - {GAME_VERSION}")
    print(f"Resolução: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"FPS: {FPS}")
    print(f"Estado: {GAME_STATE}")
