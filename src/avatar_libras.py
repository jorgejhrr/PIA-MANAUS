import pygame
import random

class AvatarLibras:
    def __init__(self):
        print("✅ Avatar Libras inicializado")
        self.frame = 0
        self.sequencia_ativa = False
        
    def iniciar_sequencia(self, texto):
        print(f"👐 Avatar mostrando: {texto}")
        self.sequencia_ativa = True
        self.frame = 0
        
    def atualizar(self):
        self.frame += 1
        if self.frame > 100:
            self.frame = 0
        
    def desenhar(self, screen, x, y, w, h):
        # Desenhar avatar simples
        pygame.draw.rect(screen, (70, 70, 120), (x, y, w, h))
        
        # Cabeça
        pygame.draw.circle(screen, (200, 200, 255), (x + w//2, y + h//3), 40)
        
        # Olhos
        olho_offset = 15 + 5 * abs((self.frame % 40) - 20) / 20  # Animação suave
        pygame.draw.circle(screen, (0, 0, 0), (x + w//2 - 15, y + h//3), 8)
        pygame.draw.circle(screen, (0, 0, 0), (x + w//2 + 15, y + h//3), 8)
        
        # Boca
        mouth_y = y + h//3 + 15
        if self.sequencia_ativa:
            mouth_open = 5 + 3 * (self.frame % 20) / 20
            pygame.draw.arc(screen, (0, 0, 0), 
                           (x + w//2 - 20, mouth_y - 10, 40, 20), 
                           0, 3.14, 3)
        else:
            pygame.draw.arc(screen, (0, 0, 0), 
                           (x + w//2 - 15, mouth_y, 30, 10), 
                           3.14, 6.28, 2)
        
        # Braços (animação de libras)
        braco_altura = 20 + 10 * abs((self.frame % 30) - 15) / 15
        pygame.draw.rect(screen, (200, 200, 255), (x + w//2 - 60, y + h//2, 30, 80))
        pygame.draw.rect(screen, (200, 200, 255), (x + w//2 + 30, y + h//2, 30, 80))
        
        # Tronco
        pygame.draw.rect(screen, (100, 100, 200), (x + w//2 - 30, y + h//2, 60, 80))
        
        # Texto
        fonte = pygame.font.SysFont('Arial', 16)
        texto = fonte.render("AVATAR LIBRAS - TRADUZINDO", True, (255, 255, 255))
        screen.blit(texto, (x + 10, y + 10))
        
        fonte_pequena = pygame.font.SysFont('Arial', 12)
        status = fonte_pequena.render(f"Frame: {self.frame}", True, (200, 200, 200))
        screen.blit(status, (x + 10, y + 30))