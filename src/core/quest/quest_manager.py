from typing import List, Dict
from src.core.quest.quest import Quest, QuestStatus
from src.core.quest.quest_objective import ObjectiveType, KillObjective, CollectObjective, TalkObjective

class QuestManager:
    """Gerenciador central de missões."""
    def __init__(self, player):
        self.player = player
        self.all_quests: Dict[str, Quest] = {}
        self.active_quests: List[Quest] = []
        self.completed_quests: List[Quest] = []

    def add_quest(self, quest: Quest):
        """Adiciona uma quest ao banco de dados do jogo."""
        self.all_quests[quest.id] = quest

    def accept_quest(self, quest_id: str):
        """O jogador aceita uma quest."""
        if quest_id in self.all_quests:
            quest = self.all_quests[quest_id]
            if quest.status == QuestStatus.NOT_STARTED:
                quest.status = QuestStatus.IN_PROGRESS
                self.active_quests.append(quest)
                print(f"📜 Nova Missão Aceita: {quest.name}")
                return True
        return False

    def notify_kill(self, enemy_name: str):
        """Notifica o sistema que um inimigo foi derrotado."""
        for quest in self.active_quests:
            for obj in quest.objectives:
                if isinstance(obj, KillObjective) and obj.enemy_name == enemy_name:
                    obj.update_progress()
            quest.check_completion()

    def notify_collect(self, item_name: str, amount: int = 1):
        """Notifica o sistema que um item foi coletado."""
        for quest in self.active_quests:
            for obj in quest.objectives:
                if isinstance(obj, CollectObjective) and obj.item_name == item_name:
                    obj.update_progress(amount)
            quest.check_completion()

    def notify_talk(self, npc_name: str):
        """Notifica o sistema que o jogador falou com um NPC."""
        for quest in self.active_quests:
            for obj in quest.objectives:
                if isinstance(obj, TalkObjective) and obj.npc_name == npc_name:
                    obj.update_progress()
            quest.check_completion()

    def complete_quest(self, quest_id: str):
        """Entrega a quest e recebe recompensas."""
        for quest in self.active_quests:
            if quest.id == quest_id and quest.status == QuestStatus.COMPLETED:
                quest.status = QuestStatus.REWARDED
                self.active_quests.remove(quest)
                self.completed_quests.append(quest)
                
                # Dar recompensas
                if "xp" in quest.rewards:
                    self.player.gain_xp(quest.rewards["xp"])
                
                if "items" in quest.rewards:
                    for item in quest.rewards["items"]:
                        self.player.inventory.add_item(item)
                
                print(f"🎁 Recompensas recebidas pela missão: {quest.name}")
                return True
        return False
