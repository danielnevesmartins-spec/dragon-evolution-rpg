import pygame

class Map:
    """Classe base para gerenciar o ambiente do jogo."""

    def __init__(self, name: str, width: int, height: int, tile_size: int = 32):
        self.name = name
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.tiles = []  # Representa a matriz de tiles
        self.collision_rects = [] # Lista de retângulos para colisão

        # Exemplo de inicialização de tiles e colisões (pode ser carregado de arquivo)
        self._initialize_dummy_map()

    def _initialize_dummy_map(self):
        """Inicializa um mapa de exemplo para testes."""
        # Cria um mapa simples 10x10
        for y in range(self.height // self.tile_size):
            row = []
            for x in range(self.width // self.tile_size):
                # Adiciona algumas colisões de exemplo
                if (x == 0 or x == (self.width // self.tile_size) - 1 or
                    y == 0 or y == (self.height // self.tile_size) - 1):
                    self.collision_rects.append(pygame.Rect(x * self.tile_size, y * self.tile_size, self.tile_size, self.tile_size))
                row.append(0) # Tile vazio
            self.tiles.append(row)

    def is_collision(self, rect: pygame.Rect) -> bool:
        """Verifica se um retângulo colide com algum objeto do mapa."""
        for collision_rect in self.collision_rects:
            if rect.colliderect(collision_rect):
                return True
        return False

    def render(self, screen: pygame.Surface, camera_offset: tuple[int, int]):
        """Desenha o mapa na tela, considerando o offset da câmera."""
        # Renderiza tiles (apenas um exemplo visual simples)
        for y, row in enumerate(self.tiles):
            for x, tile_id in enumerate(row):
                tile_rect = pygame.Rect(x * self.tile_size - camera_offset[0],
                                        y * self.tile_size - camera_offset[1],
                                        self.tile_size, self.tile_size)
                if tile_id == 0: # Exemplo de tile vazio (chão)
                    pygame.draw.rect(screen, (50, 50, 50), tile_rect)
                # Adicione mais lógica de renderização de tiles aqui

        # Renderiza colisões para debug
        for collision_rect in self.collision_rects:
            debug_rect = pygame.Rect(collision_rect.x - camera_offset[0],
                                     collision_rect.y - camera_offset[1],
                                     collision_rect.width, collision_rect.height)
            pygame.draw.rect(screen, (255, 0, 0), debug_rect, 1) # Borda vermelha para colisões
