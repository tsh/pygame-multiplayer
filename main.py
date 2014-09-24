import sys
import pygame

from client.Player import Player

background_color = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
surface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("hello")

player = Player()

RUNNING = True
while RUNNING:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        pass

    # Render
    surface.fill(background_color)
    surface.blit(player.sprite, (0,0))
    pygame.display.flip()
