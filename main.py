print("Hello World")

import pygame

pygame.init()
window = pygame.display.set_mode((1280, 720), pygame.RESIZABLE | pygame.NOFRAME)
clock = pygame.time.Clock()

# Set the window to be transparent
pygame.display.set_caption("Transparent Window")
window.set_alpha(0)  # Set the window alpha to 0 for full transparency

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)


pygame.quit()
