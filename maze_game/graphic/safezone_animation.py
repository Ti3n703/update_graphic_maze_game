import pygame
from .get_frame_list import Load_Sprite_Sheet
class Safe_zone_Animation:
    def __init__(self):
        self.candle_img = pygame.image.load('image/candle_img.png').convert_alpha()
        self.brazier = pygame.image.load('image/brazier_img.png').convert_alpha()
        self.candle_sheet= Load_Sprite_Sheet(self.candle_img)
        self.brazier_sheet = Load_Sprite_Sheet(self.brazier)
        self.candle_animation_list = []
        self.brazier_animation_list = []
        self.safe_zone_animation()
        #frame index
        self.frame_index = 0 
        self.frame_rate = 5000
        self.timer = 0

    def safe_zone_animation(self):
        animation_candle_steps = [1,1,1]
        animation_brazier_steps = [6,6,6]
        for anim_idx, frame_count in enumerate(animation_candle_steps):
            temp_candle_ani_list = []
            for frame in range(frame_count):
                temp_candle_ani_list.append(self.candle_sheet.get_image_vertical(anim_idx,frame,32,32,1))
            self.candle_animation_list.append(temp_candle_ani_list)
        for anim_idx, frame_count in enumerate(animation_brazier_steps):
            temp_brazier_ani_list = []
            for frame in range(frame_count):
                temp_brazier_ani_list.append(self.brazier_sheet.get_image_vertical(anim_idx,frame,44,48,1))
            self.brazier_animation_list.append(temp_brazier_ani_list)

    def update_safe_zone_frame(self,dt,type,size):
        self.timer += dt
        # pick action list

        if type == "candle":
            if size== 'large':
                frame = self.candle_animation_list[0]  
            elif size == 'medium':
                frame = self.candle_animation_list[1]
            elif size == 'small':
                frame = self.candle_animation_list[2]
            
        elif type =='brazier':
            if size == 'small':
                frame = self.brazier_animation_list[0]  
            elif size == 'medium':
                frame = self.brazier_animation_list[1]
            elif size == 'large':
                frame = self.brazier_animation_list[2]
            elif size == 'medium-large':
                frame = self.brazier_animation_list[3]
        if self.timer >= self.frame_rate:
            self.timer = 0
            self.frame_index = (self.frame_index + 1) % len(frame)
        print(self.frame_index)
        return frame[self.frame_index]

           
        
        











    




        


