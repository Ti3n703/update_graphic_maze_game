import pygame
import math
from graphic.player_animation import Player_Animation


class player:
    def __init__(self, game):
        self.color = game.player_color
        self.player_pos = [0, 0]  # Lưu vị trí dưới dạng [x, y]
        self.target_pixel_pos = [0.0,0.0]
        self.pixel_pos = [0.0,0.0]
        self.speed =  5   
        self.maze = game.maze
        self.screen = game.screen
        self.path = game.path
        self.move_delay = game.player_movement_delay
        self.CELL_SIZE = game.CELL_SIZE
        self.move_counter = 0
        self.size = game.size
        self.screen_w = game.screen1.width
        self.screen_h = game.screen1.height
        self.moving = False
        self.dir = 'right'
        self.last_dir = 'right'
        self.state = 'exit'
        self.animation =Player_Animation()
        self.dt = 0

    def _get_player_pos(self):
        return self.player_pos[0], self.player_pos[1]

    def _move_up(self):
        self.player_pos[1] -= 1
        self.target_pixel_pos[1] -= self.CELL_SIZE 

    def _move_down(self):
        self.player_pos[1] += 1
        self.target_pixel_pos[1] +=self.CELL_SIZE

    def _move_left(self):
        self.player_pos[0] -= 1
        self.target_pixel_pos[0] -= self.CELL_SIZE

    def _move_right(self):
        self.player_pos[0] += 1
        self.target_pixel_pos[0] += self.CELL_SIZE

    def _check_valid_move(self, x, y):
        cur_x, cur_y = self.player_pos[0], self.player_pos[1]
        new_x, new_y = cur_x + x, cur_y + y

        if not (0 <= new_x < self.maze.size and 0 <= new_y < self.maze.size):
            return False

        cur_player_pos_str = f"{cur_x},{cur_y}"
        new_player_pos_str = f"{new_x},{new_y}"

        if new_player_pos_str in self.path.adjacency_list.get(cur_player_pos_str, {}):
            return True
        return False

    def check_event(self):
        if self.moving:
            return
        

        keys = pygame.key.get_pressed()
        
        # Kiểm tra và di chuyển theo một hướng mỗi khung hình
        if keys[pygame.K_UP] and self._check_valid_move(0, -1):
            self.moving = True 
            self._move_up()
            self.dir = 'up'
        elif keys[pygame.K_DOWN] and self._check_valid_move(0, 1):
            self.moving = True 
            self._move_down()
            self.dir = 'down'
        elif keys[pygame.K_LEFT] and self._check_valid_move(-1, 0):
            self.moving = True 
            self._move_left()
            self.dir = 'left'
        elif keys[pygame.K_RIGHT] and self._check_valid_move(1, 0):
            self.moving = True 
            self._move_right()
            self.dir = 'right'



    def update_movement(self):
    # move pixel position toward target
        if self.moving == True:
            dx = self.target_pixel_pos[0] - self.pixel_pos[0]
            dy = self.target_pixel_pos[1] - self.pixel_pos[1]

            dist = math.hypot(dx, dy)
            if dist > 0:
                step_x = self.speed * dx / dist
                step_y = self.speed * dy / dist

                if abs(step_x) > abs(dx): step_x = dx
                if abs(step_y) > abs(dy): step_y = dy

                self.pixel_pos[0] += step_x
                self.pixel_pos[1] += step_y
            else:
                self.last_dir = self.dir
                self.moving = False

    def draw_player(self):
        if self.moving == True:
            frame = self.animation.update_player_frame(self.dt,self.dir,'run')
        
        else:
            frame = self.animation.update_player_frame(self.dt,self.last_dir,'idle')

        
        maze_w = self.size * self.CELL_SIZE
        maze_h = self.size * self.CELL_SIZE
        offset_x = (self.screen_w - maze_w) // 2
        offset_y = (self.screen_h - maze_h) // 2
        pixel_x= offset_x + self.pixel_pos[0]+self.CELL_SIZE//2
        pixel_y = offset_y+ self.pixel_pos[1]+self.CELL_SIZE//2
        rect = frame.get_rect(center=(pixel_x, pixel_y ))
        self.screen.blit(frame,rect)

    def update_player(self,dt):
        self.dt = dt
        self.check_event()
        self.update_movement()
        self.draw_player()
