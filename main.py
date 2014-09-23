import sys
import pygame

background_color = (255, 255, 255)
WIDTH = 800
HEIGHT = 600
surface = pygame.display.set_mode((WIDTH, HEIGHT))

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
    pygame.display.flip()
