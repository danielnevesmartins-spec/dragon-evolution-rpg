from enum import Enum

class ObjectiveType(Enum):
    KILL = "kill"
    COLLECT = "collect"
    TALK = "talk"
    REACH = "reach"

class QuestObjective:
    """Classe base para objetivos de quest."""
    def __init__(self, description: str, target_amount: int = 1):
        self.description = description
        self.target_amount = target_amount
        self.current_amount = 0
        self.is_completed = False

    def update_progress(self, amount: int = 1):
        """Atualiza o progresso do objetivo."""
        if not self.is_completed:
            self.current_amount += amount
            if self.current_amount >= self.target_amount:
                self.current_amount = self.target_amount
                self.is_completed = True
            return True
        return False

    def get_progress_text(self) -> str:
        """Retorna o texto de progresso (ex: 2/5)."""
        return f"{self.description} ({self.current_amount}/{self.target_amount})"

class KillObjective(QuestObjective):
    """Objetivo de derrotar inimigos."""
    def __init__(self, enemy_name: str, target_amount: int):
        super().__init__(f"Derrotar {enemy_name}", target_amount)
        self.type = ObjectiveType.KILL
        self.enemy_name = enemy_name

class CollectObjective(QuestObjective):
    """Objetivo de coletar itens."""
    def __init__(self, item_name: str, target_amount: int):
        super().__init__(f"Coletar {item_name}", target_amount)
        self.type = ObjectiveType.COLLECT
        self.item_name = item_name

class TalkObjective(QuestObjective):
    """Objetivo de falar com um NPC."""
    def __init__(self, npc_name: str):
        super().__init__(f"Falar com {npc_name}", 1)
        self.type = ObjectiveType.TALK
        self.npc_name = npc_name
