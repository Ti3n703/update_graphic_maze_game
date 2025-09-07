from .get_frame_list import Load_Sprite_Sheet
import pygame
class Player_Animation:
    def __init__(self):
        self.timer_g =0 
        self.timer_p =0
        self.frame_rate =  10    #player
        self.p_run_img = pygame.image.load('image/run.png').convert_alpha() 
        self.p_idle_img = pygame.image.load('image/idle.png').convert_alpha()
        self.p_idle_sheet =Load_Sprite_Sheet(self.p_idle_img)
        self.p_run_sheet =Load_Sprite_Sheet(self.p_run_img)
        self.p_run_action_list = []
        self.p_idle_action_list = []
        self.player_animation()
        self.frame_index_p = 0 

    def update_player_frame(self,dt,dir, action = 'run' ):
        self.timer_p += dt
        # pick action list
        if action == "run":
            if dir == 'down':
                frame = self.p_run_action_list[0]  
            elif dir == 'left':
                frame = self.p_run_action_list[1]
            elif dir == 'right':
                frame = self.p_run_action_list[2]
            elif dir == 'up':
                frame = self.p_run_action_list[3]
            
        else:
            if dir == 'down':
                frame = self.p_idle_action_list[0]  
            elif dir == 'left':
                frame = self.p_idle_action_list[1]
            elif dir == 'right':
                frame = self.p_idle_action_list[2]
            elif dir == 'up':
                frame = self.p_idle_action_list[3]


        if self.timer_p >= self.frame_rate:
            self.timer_p = 0
            self.frame_index_p = (self.frame_index_p + 1) % len(frame)


        return frame[self.frame_index_p]

    def player_animation(self):
        animation_run_steps = [8,8,8,8]
        animation_idle_steps = [12,12,12,4]
        for anim_idx, frame_count in enumerate(animation_run_steps):
            temp_ani_list = []
            for frame in range(frame_count):
                temp_ani_list.append(self.p_run_sheet.get_image_horizontal(anim_idx, frame, 64, 64,1))
            self.p_run_action_list.append(temp_ani_list)

        for anim_idx, frame_count in enumerate(animation_idle_steps):
            temp_ani_list = []
            for frame in range(frame_count):
                temp_ani_list.append(self.p_idle_sheet.get_image_horizontal(anim_idx, frame, 64, 64,1))
            self.p_idle_action_list.append(temp_ani_list)
 

