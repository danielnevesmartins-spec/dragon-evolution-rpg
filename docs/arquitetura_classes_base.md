# Arquitetura de Classes Base - Dragon Evolution RPG

Este documento detalha a arquitetura inicial das classes base para o projeto Dragon Evolution RPG, focando em modularidade e extensibilidade. As classes principais são `Entity`, `Item` e `Map`.

## 1. Classe `Entity`

A classe `Entity` servirá como a base para todos os objetos interativos no jogo que possuem uma presença física e podem se mover ou interagir com o ambiente. Isso inclui o jogador, NPCs e inimigos.

### Propriedades Principais:

*   `id` (UUID): Identificador único da entidade.
*   `name` (String): Nome da entidade.
*   `position` (Tuple[int, int]): Coordenadas (x, y) da entidade no mapa.
*   `health` (int): Pontos de vida atuais da entidade.
*   `max_health` (int): Pontos de vida máximos da entidade.
*   `speed` (int): Velocidade de movimento da entidade.
*   `sprite` (pygame.Surface): Representação visual da entidade.
*   `rect` (pygame.Rect): Retângulo de colisão da entidade.

### Métodos Principais:

*   `__init__(self, id, name, position, health, speed, sprite)`: Construtor da entidade.
*   `move(self, dx, dy)`: Move a entidade por `dx` e `dy` unidades.
*   `take_damage(self, amount)`: Reduz a saúde da entidade.
*   `heal(self, amount)`: Aumenta a saúde da entidade.
*   `update(self, dt)`: Lógica de atualização da entidade por frame.
*   `render(self, screen)`: Desenha a entidade na tela.

## 2. Classe `Item`

A classe `Item` é a base para todos os objetos que podem ser coletados, usados ou equipados pelos jogadores. Isso inclui consumíveis, equipamentos, chaves, etc.

### Propriedades Principais:

*   `id` (UUID): Identificador único do item.
*   `name` (String): Nome do item.
*   `description` (String): Descrição detalhada do item.
*   `icon` (pygame.Surface): Ícone visual do item.
*   `stackable` (bool): Indica se o item pode ser empilhado no inventário.
*   `value` (int): Valor monetário do item.

### Métodos Principais:

*   `__init__(self, id, name, description, icon, stackable=False, value=0)`: Construtor do item.
*   `use(self, target)`: Lógica de uso do item (a ser implementada por subclasses).
*   `get_info(self)`: Retorna informações formatadas sobre o item.

## 3. Classe `Map`

A classe `Map` gerenciará o ambiente do jogo, incluindo o carregamento de tiles, detecção de colisões e renderização do cenário. Será a base para diferentes áreas do mundo do jogo.

### Propriedades Principais:

*   `name` (String): Nome do mapa.
*   `width` (int): Largura do mapa em pixels.
*   `height` (int): Altura do mapa em pixels.
*   `tiles` (List[List[Tile]]): Matriz de tiles que compõem o mapa.
*   `collision_rects` (List[pygame.Rect]): Lista de retângulos para detecção de colisão.

### Métodos Principais:

*   `__init__(self, name, map_data_path)`: Construtor do mapa, carrega dados de um arquivo.
*   `load_map_data(self, path)`: Carrega os tiles e dados de colisão do mapa.
*   `is_collision(self, rect)`: Verifica se um retângulo colide com algum objeto do mapa.
*   `render(self, screen, camera_offset)`: Desenha o mapa na tela, considerando o offset da câmera.

## Relações entre as Classes

*   `Entity` interage com `Map` para movimento e colisão.
*   `Entity` pode possuir `Item`s (através de um inventário, por exemplo).
*   `Map` contém `Entity`s e `Item`s como parte de seu ambiente.

Esta arquitetura fornece uma base flexível para o desenvolvimento futuro do jogo, permitindo a criação de subclasses específicas para jogadores, inimigos, diferentes tipos de itens e mapas complexos.
