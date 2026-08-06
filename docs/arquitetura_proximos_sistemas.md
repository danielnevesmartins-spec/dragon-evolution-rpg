# Arquitetura Técnica: Quests e Skills

Este documento detalha a arquitetura planejada para os sistemas de Quests e Skills, garantindo que sejam modulares e fáceis de integrar.

## 1. Sistema de Quests (Missões)

O sistema de quests será baseado em um gerenciador central que rastreia o progresso de múltiplas missões simultâneas.

### Estrutura da Classe `Quest`
- **ID:** Identificador único.
- **Nome e Descrição:** Informações para o jogador.
- **Estado:** `NOT_STARTED`, `IN_PROGRESS`, `COMPLETED`, `REWARDED`.
- **Objetivos:** Uma lista de `QuestObjective`.
- **Recompensas:** XP, Itens ou Atributos.

### Tipos de `QuestObjective`
- **KillObjective:** Derrotar um número específico de inimigos.
- **CollectObjective:** Coletar uma quantidade de itens.
- **TalkObjective:** Falar com um NPC específico.
- **ReachObjective:** Chegar a uma coordenada ou área do mapa.

### Gerenciador `QuestManager`
- Mantém a lista de quests ativas e concluídas.
- Escuta eventos do jogo (ex: inimigo derrotado, item coletado) para atualizar objetivos.
- Notifica a UI sobre mudanças no status das quests.

## 2. Sistema de Skills (Habilidades)

O sistema de skills permitirá a personalização do estilo de jogo do dragão através de habilidades ativas e passivas.

### Estrutura da Classe `Skill`
- **ID e Nome:** Identificadores.
- **Tipo:** `ACTIVE` (requer uso) ou `PASSIVE` (bônus constante).
- **Custo:** Consumo de MP ou Stamina.
- **Cooldown:** Tempo de espera entre usos.
- **Efeito:** Uma função ou objeto que define o que a skill faz (ex: causar dano em área, aumentar defesa).

### Evolução de Skills
- **Nível da Skill:** Permite aprimorar a eficácia da habilidade.
- **Requisitos:** Nível do jogador ou outras skills desbloqueadas.

### Integração com o Player
- O `Player` terá um `SkillManager` para gerenciar as habilidades aprendidas e equipadas.
- As skills ativas serão vinculadas a teclas de atalho (ex: 1, 2, 3, 4).

## 3. Próximos Passos de Implementação
1. Criar a estrutura de dados (classes base) para Quests e Objetivos.
2. Implementar o `QuestManager` e integrá-lo ao loop de eventos do jogo.
3. Desenvolver a interface de log de quests na UI.
4. Repetir o processo para o sistema de Skills, começando pelas habilidades passivas de atributos.
