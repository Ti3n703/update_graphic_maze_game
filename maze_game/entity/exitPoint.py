import pygame


class Exit_Point:
    def __init__(self, game):
        self.size = game.size
        self.game =game 
        self.exit_pos = [self.game.size - 1, self.game.size - 1]
        self.exit_color =game.exit_color
        self.CELL_SIZE = game.CELL_SIZE 
        self.screen_w = game.screen1.width
        self.screen_h = game.screen1.height

    
    def draw_exit_point(self):
        maze_w = self.size * self.CELL_SIZE
        maze_h = self.size * self.CELL_SIZE
        offset_x = (self.screen_w - maze_w) // 2
        offset_y = (self.screen_h - maze_h) // 2
        pixel_x= offset_x + self.exit_pos[0]*self.CELL_SIZE+self.CELL_SIZE//2
        pixel_y = offset_y+ self.exit_pos[1]*self.CELL_SIZE +self.CELL_SIZE//2
        exit_img = pygame.image.load('image/exit.png')
        exit_img = pygame.transform.scale(exit_img,((exit_img.get_width()*0.5), (exit_img.get_height()*0.5)))
        rect = exit_img.get_rect(center=(pixel_x, pixel_y ))
        self.game.screen.blit(exit_img,rect)