from enum import Enum
from typing import List, Dict
from src.core.quest.quest_objective import QuestObjective

class QuestStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    REWARDED = "rewarded"

class Quest:
    """Classe que representa uma missão no jogo."""
    def __init__(self, id: str, name: str, description: str, objectives: List[QuestObjective], rewards: Dict):
        self.id = id
        self.name = name
        self.description = description
        self.objectives = objectives
        self.rewards = rewards
        self.status = QuestStatus.NOT_STARTED

    def check_completion(self) -> bool:
        """Verifica se todos os objetivos foram concluídos."""
        if all(obj.is_completed for obj in self.objectives):
            if self.status == QuestStatus.IN_PROGRESS:
                self.status = QuestStatus.COMPLETED
                print(f"✨ Missão Concluída: {self.name}")
            return True
        return False

    def get_progress(self) -> float:
        """Retorna o progresso total da quest (0.0 a 1.0)."""
        if not self.objectives:
            return 1.0
        completed_count = sum(1 for obj in self.objectives if obj.is_completed)
        return completed_count / len(self.objectives)
