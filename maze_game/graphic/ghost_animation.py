import pygame
from .get_frame_list import Load_Sprite_Sheet
class Ghost_Animation:
    def __init__(self):
        self.g_run_img = pygame.image.load('image/slime_run.png').convert_alpha()
        self.g_walk_img = pygame.image.load('image/slime_walk.png').convert_alpha()
        self.g_run_sheet = Load_Sprite_Sheet(self.g_run_img)
        self.g_walk_sheet = Load_Sprite_Sheet(self.g_walk_img)
        self.g_run_action_list = []
        self.g_walk_action_list = []
        self.ghost_animation()
        #frame index
        self.frame_index_g = 0 
        self.frame_rate =  10    
        self.timer_g = 0

    def ghost_animation(self):
        animation_run_steps = [8,8,8,8]
        animation_walk_steps = [8,8,8,8]
        for anim_idx, frame_count in enumerate(animation_run_steps):
            temp_ani_list = []
            for frame in range(frame_count):
                temp_ani_list.append(self.g_run_sheet.get_image_horizontal(anim_idx,frame,64,64,1))
            self.g_run_action_list.append(temp_ani_list)

        for anim_idx, frame_count in enumerate(animation_walk_steps):
            temp_ani_list = []
            for frame in range(frame_count):
                temp_ani_list.append(self.g_walk_sheet.get_image_horizontal(anim_idx,frame,64,64,1))
            self.g_walk_action_list.append(temp_ani_list)
    def update_ghost_frame(self,dt,dir, action = 'run' ):
        self.timer_g += dt
        # pick action list
        if action == "run":
            if dir == 'down':
                frame = self.g_run_action_list[0]  
            elif dir == 'left':
                frame = self.g_run_action_list[1]
            elif dir == 'right':
                frame = self.g_run_action_list[2]
            elif dir == 'up':
                frame = self.g_run_action_list[3]
            
        else:
            if dir == 'down':
                frame = self.g_walk_action_list[0]  
            elif dir == 'left':
                frame = self.g_walk_action_list[1]
            elif dir == 'right':
                frame = self.g_walk_action_list[2]
            elif dir == 'up':
                frame = self.g_walk_action_list[3]


        if self.timer_g >= self.frame_rate:
            self.timer_g = 0
            self.frame_index_g = (self.frame_index_g + 1) % len(frame)

        return frame[self.frame_index_g]

           
        
        











    




        


