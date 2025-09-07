import pygame

class Game_Screen:
    def __init__(self,game):
        self.width = 1000
        self.height =1000 
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Maze Game")
        self.CELL_SIZE =  50 # Size of each cell in the maze
        self.background_color = ((0,0,0))
        self.size = game.size
    
    def fill(self, color):
        self.screen.fill(color)
    
    def flip(self):
        pygame.display.flip()
    def draw_background(self):
        self.screen.fill(self.background_color)
        back_ground_image = pygame.image.load('image/border.png').convert_alpha()
        img = pygame.image.load("image/border.png").convert_alpha()
        scaled_img = pygame.transform.scale(img, (img.get_width()*0.68,img.get_height()*0.68))
        width_img, height_image = scaled_img.get_width(), scaled_img.get_height()


        # get rect and center it
        rect = scaled_img.get_rect(center=(self.width//2, self.height//2))

        #rect = scaled_img.get_rect(center=(self.size*15+200, self.size*15+200))

        self.screen.blit(scaled_img,rect)

        