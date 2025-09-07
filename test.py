import pygame
pygame.init()

screen = pygame.display.set_mode((640, 480))
light = pygame.image.load('circle.png').convert_alpha()  # Make sure alpha is preserved

running = True
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    screen.fill(pygame.Color('Red'))

    for x in range(0, 640, 20):
        pygame.draw.line(screen, pygame.Color('Green'), (x, 0), (x, 480), 3)

    filter_surface = pygame.Surface((640, 480), pygame.SRCALPHA)
    filter_surface.fill((128, 128, 128, 255))  # Grey with full alpha

    # Get mouse pos and adjust by 50
    mouse_x, mouse_y = pygame.mouse.get_pos()
    filter_surface.blit(light, (mouse_x - 50, mouse_y - 50))

    screen.blit(filter_surface, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    pygame.display.flip()

pygame.quit()
