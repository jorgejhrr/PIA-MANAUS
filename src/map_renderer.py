import pygame
import io
from PIL import Image

class MapRenderer:
    def __init__(self, google_maps):
        self.google_maps = google_maps
        self.current_map_image = None
        self.markers = []
        
    def load_map_for_location(self, location, nearby_routes=None):
        """Carrega mapa para uma localização"""
        location_coords = self.google_maps.geocode_address(location)
        locations = [location_coords]
        
        if nearby_routes:
            for route in nearby_routes[:3]:
                locations.append(route['location'])
        
        map_image_data = self.google_maps.get_static_map(locations)
        
        if map_image_data:
            self.current_map_image = self.convert_to_pygame_surface(map_image_data)
            self.markers = locations
            return True
        return False
    
    def convert_to_pygame_surface(self, image_data):
        """Converte dados de imagem para surface do Pygame"""
        try:
            image = Image.open(io.BytesIO(image_data))
            mode = image.mode
            size = image.size
            data = image.tobytes()
            
            pygame_image = pygame.image.fromstring(data, size, mode)
            return pygame_image
        except:
            return None
    
    def draw_map(self, surface, position):
        """Desenha o mapa na surface"""
        if self.current_map_image:
            surface.blit(self.current_map_image, position)
            
            # Desenhar legenda
            self.draw_legend(surface, position)
    
    def draw_legend(self, surface, position):
        """Desenha legenda para os marcadores"""
        font = pygame.font.SysFont('Arial', 14)
        legend_items = [
            ('A', 'Sua Localização'),
            ('B', 'Pontos de Ônibus')
        ]
        
        for i, (letter, description) in enumerate(legend_items):
            # Descrição
            desc_text = font.render(f"{letter}: {description}", True, (255, 255, 255))
            surface.blit(desc_text, (position[0] + 10, position[1] + 320 + i * 20))