import pygame
class Spot_Light:
    def __init__(self,game):
        self.game= game
        self.width = self.height = game.CELL_SIZE *game.size 
        self.screen_w = self.screen_h = 1000
        self.screen = game.screen
        self.CELL_SIZE = game.CELL_SIZE
        self.size = game.size
        self.player_pos = game.player.player_pos


    def spot_light_effect(self,spot_list):
        light = pygame.image.load('circle.png').convert_alpha()  # Preserve alpha
        filter_surface = pygame.Surface((self.width-8, self.height-8), pygame.SRCALPHA)
        #filter_surface.fill((128, 128, 128, 255))  # Grey overlay
        filter_surface.fill((255,255,255,255))
        maze_w = self.size * self.CELL_SIZE
        maze_h = self.size * self.CELL_SIZE
        offset_x = (self.screen_w- maze_w) // 2
        offset_y = (self.screen_h- maze_h) // 2
        for _ in spot_list:
            x,y = _[0], _[1]
            light_rect = light.get_rect(center=(x,y))
            filter_surface.blit(light, light_rect)

            # Apply the spotlight effect
        self.screen.blit(filter_surface, (offset_x+8, offset_y+8), special_flags=pygame.BLEND_RGBA_SUB)
