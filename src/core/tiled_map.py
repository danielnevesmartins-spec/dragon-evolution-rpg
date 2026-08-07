import pygame
import pytmx
import pyscroll
from src.settings import SCREEN_WIDTH, SCREEN_HEIGHT

class TiledMap:
    """Classe para carregar e renderizar mapas do Tiled (.tmx)."""

    def __init__(self, filename: str):
        # Carregar os dados do Tiled
        tm = pytmx.util_pygame.load_pygame(filename, pixelalpha=True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmx_data = tm

        # Configurar o pyscroll para renderização eficiente
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(
            map_data, (SCREEN_WIDTH, SCREEN_HEIGHT), clamp_camera=True
        )
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer)

        # Lista de retângulos de colisão
        self.collision_rects = []
        self._load_collision_data()

    def _load_collision_data(self):
        """Extrai dados de colisão das camadas e propriedades do Tiled."""
        for layer in self.tmx_data.visible_layers:
            if isinstance(layer, pytmx.TiledTileLayer):
                for x, y, gid in layer:
                    tile = self.tmx_data.get_tile_properties_by_gid(gid)
                    if tile and tile.get("collision"):
                        rect = pygame.Rect(
                            x * self.tmx_data.tilewidth,
                            y * self.tmx_data.tileheight,
                            self.tmx_data.tilewidth,
                            self.tmx_data.tileheight
                        )
                        self.collision_rects.append(rect)
            
            # Também suporta Object Layers para colisões personalizadas
            elif isinstance(layer, pytmx.TiledObjectGroup):
                for obj in layer:
                    if obj.properties.get("collision") or layer.name == "Collision":
                        rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                        self.collision_rects.append(rect)

    def is_collision(self, rect: pygame.Rect) -> bool:
        """Verifica se um retângulo colide com algum obstáculo do mapa."""
        # Limites do mapa
        if rect.left < 0 or rect.right > self.width or rect.top < 0 or rect.bottom > self.height:
            return True
            
        # Otimização: Filtrar apenas retângulos próximos ao alvo (buffer de 64 pixels)
        search_area = rect.inflate(64, 64)
        
        # Obstáculos internos
        for collision_rect in self.collision_rects:
            if search_area.colliderect(collision_rect):
                if rect.colliderect(collision_rect):
                    return True
        return False

    def update(self, target_rect: pygame.Rect):
        """Atualiza a câmera para seguir um alvo."""
        self.group.center(target_rect.center)

    def render(self, screen: pygame.Surface):
        """Desenha o mapa na tela."""
        self.group.draw(screen)
