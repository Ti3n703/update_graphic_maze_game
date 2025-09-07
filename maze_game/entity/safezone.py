import pygame
import random
from graphic import safezone_animation
from graphic.effect import Spot_Light

class Safe_Zone:
    def __init__(self, game):
        self.safe_zone_list,self.important_safe_zone_list = create_safezone()
        self.visited_safe_zone = []
        self.safe_zone_pos = [0,0]
        self.player = game.player 
        self.screen = game.screen
        self.maze = game.maze
        self.sz_color = game.sz_color
        self.screen_w = game.screen1.width
        self.screen_h = game.screen1.height
        self.CELL_SIZE = game.CELL_SIZE
        self.size = game.size
        self.animation = safezone_animation.Safe_zone_Animation()
        self.animation2 = safezone_animation.Safe_zone_Animation()
        self.dt = 0 
    def draw_safe_zone(self):
        maze_w = self.size * self.CELL_SIZE
        maze_h = self.size * self.CELL_SIZE
        offset_x = (self.screen_w - maze_w) // 2
        offset_y = (self.screen_h - maze_h) // 2
        im_sz_nf = pygame.image.load('image/important_sz_nf.png')
        for sz in self.important_safe_zone_list:
            pixel_x= offset_x + sz[0]*self.CELL_SIZE+self.CELL_SIZE//2
            pixel_y = offset_y+ sz[1]*self.CELL_SIZE +self.CELL_SIZE//2
            safe_zone_img_brazier = self.animation.update_safe_zone_frame(self.dt,'brazier', 'large')
            if sz in self.visited_safe_zone:
                rect_brazier =safe_zone_img_brazier.get_rect(center = (pixel_x, pixel_y))
                self.screen.blit(safe_zone_img_brazier,rect_brazier)
            else:
                rect_brazier = im_sz_nf.get_rect(center = (pixel_x, pixel_y))
                self.screen.blit(im_sz_nf,rect_brazier) 
        for sz in self.safe_zone_list:
            pixel_x= offset_x + sz[0]*self.CELL_SIZE+self.CELL_SIZE//2
            pixel_y = offset_y+ sz[1]*self.CELL_SIZE +self.CELL_SIZE//2
            safe_zone_img_candle = self.animation2.update_safe_zone_frame(self.dt,'candle','small') 
            rect_candle = safe_zone_img_candle.get_rect(center=(pixel_x, pixel_y ))
            self.screen.blit(safe_zone_img_candle,rect_candle) 
        
        # Add random safe zones up to count
    def player_is_in_safe_zone(self):

        if tuple(self.player.player_pos) in self.important_safe_zone_list: 
            self.visited_safe_zone.append(tuple(self.player.player_pos))
            return True
        else:
            return False
    
    def update_safe_zone(self, dt):
        self.player_is_in_safe_zone()
        for i in self.visited_safe_zone:
            print(i)
        self.dt = dt
        self.draw_safe_zone()



class important_safe_zone(Safe_Zone):
    def __init__(self):
        super().__init__(Safe_Zone)
        self.type = 'important'

def create_safezone():  # count is the number of additional safe zones to create
    safe_zone_list = set()
    important_safe_zone_list = set()

    #(0-5,0,5)
    safe_zone_list.add((0,0))
    safe_zone_list.add((2,3))
    safe_zone_list.add((5,2))
    important_safe_zone_list.add((5,2))
    #(5-10,0-5)
    safe_zone_list.add((7,3))
    safe_zone_list.add((10,1))
    important_safe_zone_list.add((10,1))
    #(10-15,0-5)
    safe_zone_list.add((13,3))
    safe_zone_list.add((15,1))
    important_safe_zone_list.add((15,1))
    #(15-20,0-5)
    safe_zone_list.add((17,4))
    safe_zone_list.add((19,0))
    important_safe_zone_list.add((19,0))
    #(0-5,5-10)
    safe_zone_list.add((1,7))
    safe_zone_list.add((4,8))
    important_safe_zone_list.add((4,8))
    #(5-10,5-10)
    safe_zone_list.add((7,7))
    safe_zone_list.add((10,9))
    important_safe_zone_list.add((10,9))
    #(10-15,5-10  )
    safe_zone_list.add((15,6))
    safe_zone_list.add((12,7))
    important_safe_zone_list.add((12,7))
    #(15-20, 5-10)
    safe_zone_list.add((17,10))
    important_safe_zone_list.add((17,10))
    safe_zone_list.add((19,5))
    #(0-5,10-15)
    safe_zone_list.add((1,10))
    important_safe_zone_list.add((1,10))
    safe_zone_list.add((4,14))

    #(5-10,10-15)
    safe_zone_list.add((5,11))
    important_safe_zone_list.add((5,11))
    safe_zone_list.add((8,13))
    #(10-15,10-15)
    safe_zone_list.add((10,11))
    important_safe_zone_list.add((10,11))
    safe_zone_list.add((13,14))
    
    #(15-20,10-15)
    safe_zone_list.add((15,11))
    important_safe_zone_list.add((15,11))
    safe_zone_list.add((19,14))

    #(0-5,15-20)
    safe_zone_list.add((1,15))
    important_safe_zone_list.add((1,15))
    safe_zone_list.add((4,19))

    #(5-10,15-20)
    safe_zone_list.add((5,16))
    important_safe_zone_list.add((5,16))
    safe_zone_list.add((8,19))
    #(10-15,15-20)
    safe_zone_list.add((10,17))
    important_safe_zone_list.add((10,17))
    safe_zone_list.add((13,19))
                                    
    #(15-20,15-20)
    safe_zone_list.add((15,16))
    important_safe_zone_list.add((15,16))
    safe_zone_list.add((19,19))

    return safe_zone_list, important_safe_zone_list
        