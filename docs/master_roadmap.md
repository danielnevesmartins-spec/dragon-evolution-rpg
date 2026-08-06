# Master Roadmap: Dragon Evolution RPG

## 1. Visão Geral do Projeto

O Dragon Evolution RPG é um jogo de RPG top-down 2D com pixel art, focado na evolução de um dragão, exploração de um mundo segmentado, combate estratégico, sistema de itens e quests. O objetivo é criar uma experiência imersiva e recompensadora para o jogador, com foco na progressão do personagem e na narrativa.

## 2. Módulos Concluídos (Core Systems)

O Módulo 1, **Core Systems**, está 100% concluído e serve como a espinha dorsal do jogo. Ele inclui:

*   **Arquitetura de Classes Base:** `Entity`, `Player`, `Enemy`, `Item`, `Inventory` e `NPC` foram implementadas, fornecendo uma base modular e extensível para o jogo.
*   **Movimentação e Colisão:** O jogador e os inimigos possuem movimentação fluida e um sistema de colisão robusto, unificado na classe `Entity` e integrado com o `TiledMap`.
*   **Sistema de Combate:** Mecânicas de ataque do jogador (com hitbox e cooldown), IA de perseguição e ataque para inimigos, e um sistema de dano funcional com feedback visual.
*   **Sistema de Inventário:** Gerenciamento de itens com slots limitados e empilhamento, permitindo a coleta de `CollectibleItem` no mapa.
*   **Sistema de Status e Level Up:** Atributos primários (Força, Agilidade, Inteligência) que influenciam status derivados (HP, MP, Stamina), e um sistema de XP e Level Up com progressão de atributos e cura automática.
*   **Interface de Usuário (UI) Básica:** Exibição de status do jogador (HP, MP, XP, Nível, Inventário) e feedback visual para Level Up e dano recebido.
*   **Testes Automatizados:** Cobertura de testes unitários para as principais funcionalidades, garantindo a estabilidade do código.

## 3. Próximas Fases do Desenvolvimento

### 3.1. Módulo 2: Mapas e NPCs (50% Concluído)

Esta fase está em andamento e foca na criação de um mundo mais dinâmico e interativo.

*   **Carregamento de Mapas Tiled:** Suporte completo para arquivos `.tmx` do Tiled Map Editor, permitindo a criação de mapas complexos com múltiplas camadas e propriedades de colisão.
*   **NPCs Interativos:** Implementação de uma classe base para NPCs com sistema de diálogo simples, permitindo que o jogador interaja com personagens no mundo.
*   **Próximos Passos:**
    *   **Sistema de Quests:** Desenvolver um sistema robusto para gerenciar missões, objetivos, recompensas e estados de quests.
    *   **Tipos de NPCs:** Expandir a classe `NPC` para incluir diferentes tipos (comerciantes, curandeiros, etc.) com funcionalidades específicas.
    *   **Eventos de Mapa:** Adicionar gatilhos e eventos baseados em áreas do mapa ou interações com objetos.

### 3.2. Módulo 3: Habilidades e Magias

Foco na diversificação das opções de combate e utilidade para o jogador.

*   **Sistema de Habilidades:** Implementar uma árvore de habilidades ou um sistema de pontos para desbloquear e aprimorar habilidades ativas e passivas.
*   **Sistema de Magias:** Introduzir magias com diferentes efeitos (dano, cura, buffs/debuffs) e consumo de MP.
*   **Efeitos Visuais e Sonoros:** Criar efeitos visuais (VFX) e sonoros (SFX) para habilidades e magias.

### 3.3. Módulo 4: Inimigos e IA Avançada

Melhorar a experiência de combate com inimigos mais desafiadores e inteligentes.

*   **Tipos de Inimigos:** Criar diferentes classes de inimigos com atributos, sprites e padrões de ataque variados.
*   **IA Comportamental:** Desenvolver IA mais complexa, incluindo patrulha, evasão, uso de habilidades e coordenação entre inimigos.
*   **Boss Fights:** Implementar mecânicas únicas para chefes, com fases e ataques especiais.

### 3.4. Módulo 5: Interface de Usuário (UI) Avançada

Refinar a experiência do jogador com uma interface mais intuitiva e visualmente atraente.

*   **Menus:** Criar menus de inventário, habilidades, status e opções com design moderno.
*   **Barras de Vida/Mana:** Implementar barras de progresso visuais para HP, MP, Stamina e XP.
*   **Mini-mapa:** Adicionar um mini-mapa funcional para auxiliar na navegação.
*   **Log de Combate:** Exibir mensagens de combate (dano causado/recebido, status aplicados) em tempo real.

## 4. Qualidade e Otimização Contínua

*   **Performance:** Otimização constante do código para garantir alta taxa de quadros (FPS) e baixo consumo de recursos.
*   **Testes:** Manutenção e expansão da suíte de testes automatizados para cobrir novas funcionalidades.
*   **Documentação:** Atualização contínua da documentação técnica e do design do jogo no Notion.
*   **Feedback:** Incorporação de feedback do usuário para refinar a jogabilidade e a experiência geral.

Este roadmap será atualizado conforme o projeto avança e novas necessidades surgem. Ele serve como um guia para manter o desenvolvimento focado e alinhado com a visão original do Dragon Evolution RPG.
