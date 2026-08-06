# Sistema de Quests (Missões)

Este documento descreve o funcionamento do sistema de missões implementado no Dragon Evolution RPG.

## 1. Visão Geral
O sistema de quests permite que o jogador aceite, rastreie e complete missões com objetivos específicos, recebendo recompensas como XP e itens ao finalizar.

## 2. Estrutura Técnica

### 2.1. Objetivos (`QuestObjective`)
Existem diferentes tipos de objetivos que podem ser combinados em uma única missão:
- **KillObjective:** Rastreia a derrota de inimigos específicos.
- **CollectObjective:** Rastreia a coleta de itens específicos.
- **TalkObjective:** Rastreia a interação com NPCs.
- **ReachObjective:** Rastreia a chegada a locais específicos (planejado).

### 2.2. Estados da Quest (`QuestStatus`)
- `NOT_STARTED`: Missão disponível mas não aceita.
- `IN_PROGRESS`: Jogador está trabalhando nos objetivos.
- `COMPLETED`: Todos os objetivos foram atingidos, aguardando entrega.
- `REWARDED`: Recompensas entregues e missão finalizada.

### 2.3. Gerenciamento (`QuestManager`)
Integrado à classe `Player`, o gerenciador:
- Notifica o progresso dos objetivos através de eventos do jogo (`notify_kill`, `notify_collect`, etc).
- Verifica automaticamente a conclusão da missão.
- Entrega recompensas ao jogador.

## 3. Interface de Usuário (UI)
As missões ativas são exibidas no canto superior direito da tela, mostrando o nome da missão e o progresso detalhado de cada objetivo em tempo real.

## 4. Como Adicionar Novas Quests
Novas quests podem ser inicializadas no método `_init_quests` da classe `Game` em `main.py`, definindo os objetivos e recompensas desejados.
