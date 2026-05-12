# Dragon Evolution RPG

Este é o repositório oficial do projeto **Dragon Evolution RPG**, um jogo de RPG de fantasia sombria desenvolvido com Pygame. Este projeto visa criar uma experiência imersiva com foco em narrativa, evolução de personagens e combate estratégico.

## 🚀 Visão Geral do Projeto

O **Dragon Evolution RPG** é um MMORPG clássico single player com visão top-down e arte pixelada 2D. O mundo é segmentado e o foco principal está na evolução do personagem, coleta de itens, quests e combate.

## 🔗 Links Essenciais

- **Hub Central do Projeto (Notion):** [Crônicas de Aethelgard: O Despertar das Sombras](https://www.notion.so/35a19930887e81e5902cee481424a889)
- **Planilha Mestre de Rastreamento (Google Sheets):** [RPG Project Master Tracker](https://docs.google.com/spreadsheets/d/1m7VqB81T9LXlxVBrFnb1V8o8ALejbStOUqw0Hd-K3NQ/edit)
- **Documento de Design de Jogo (GDD):** [GDD - Crônicas de Aethelgard](https://www.notion.so/35c19930887e8116b203c04c8d9397b5)

## 📂 Estrutura do Repositório

```
dragon-evolution-rpg/
├── main.py             # Ponto de entrada principal do jogo
├── requirements.txt    # Dependências do projeto
└── src/
    ├── __pycache__/    # Cache de módulos Python
    ├── combat/         # Lógica de combate
    ├── enemy/          # Definições e comportamento de inimigos
    ├── inventory/      # Sistema de inventário
    ├── loot/           # Geração e gerenciamento de itens
    ├── player/         # Lógica do jogador
    ├── progression/    # Sistema de progressão e level-up
    └── settings.py     # Configurações globais do jogo
```

## 🛠️ Como Contribuir

1. Clone o repositório:
   ```bash
   git clone https://github.com/danielnevesmartins-spec/dragon-evolution-rpg.git
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute o jogo:
   ```bash
   python main.py
   ```

## 📋 Roadmap

O roadmap detalhado pode ser encontrado no [Hub Central do Projeto no Notion](https://www.notion.so/35a19930887e81e5902cee481424a889). As próximas fases incluem:

- **Fase 2: Expansão de Mundo (Em Progresso)**
  - Integração com Tiled Maps
  - Sistema de Quests e NPCs
  - Respawn de monstros
- **Fase 3: Polimento e UX (Pendente)**
  - Melhoria estética de assets
  - Sistema de Auto-Play
  - Remoção de opção de Save

## 📝 Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes. (Nota: O arquivo LICENSE ainda não foi criado, mas será adicionado em breve.)
