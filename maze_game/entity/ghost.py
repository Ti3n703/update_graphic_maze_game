# ghost.py
import utils
import random
import pygame
import math
from graphic.ghost_animation import Ghost_Animation

class Ghost:
    def __init__(self,game):
        # Vị trí ban đầu của ma, giờ là góc dưới bên phải
        self.size = game.size
        self.screen_w = game.screen1.width
        self.screen_h = game.screen1.height
        self.ghost_pos = [game.size - 1, game.size - 1]
        self.ghost_pos_key = f'{self.ghost_pos[0]},{self.ghost_pos[1]}'
        self.color = (255, 0, 0)
        self.target = None
        self.state = "roaming"
        self.maze = game.maze
        self.screen = game.screen
        self.player = game.player
        self.player_pos_key = f'{self.player.player_pos[0]},{self.player.player_pos[1]}'
        self.path = game.path
        self.safe_zone = game.safezone
        self.move_delay = game.ghost_speed

        self.move_counter = 0
        self.CELL_SIZE = game.CELL_SIZE
        #init animation
        self.target_pixel_pos = [float(game.size-1)*self.CELL_SIZE,float(game.size-1)*self.CELL_SIZE]
        self.pixel_pos = [float(game.size-1)*self.CELL_SIZE,float(game.size-1)*self.CELL_SIZE]
        self.speed = 1
        self.moving = False
        self.dir = 'down'
        self.animation = Ghost_Animation()
        self.dt = 0

    def draw_ghost(self):
        if self.state == 'chase' or self.state == 'scare':
            frame = self.animation.update_ghost_frame(self.dt,self.dir,'run')
        else:
            frame = self.animation.update_ghost_frame(self.dt, self.dir, 'walk')
        maze_w = self.size * self.CELL_SIZE
        maze_h = self.size * self.CELL_SIZE
        offset_x = (self.screen_w - maze_w) // 2
        offset_y = (self.screen_h - maze_h) // 2
        pixel_x= offset_x + self.pixel_pos[0]+self.CELL_SIZE//2
        pixel_y = offset_y+ self.pixel_pos[1]+self.CELL_SIZE//2
        rect = frame.get_rect(center=(pixel_x, pixel_y ))
        self.screen.blit(frame,rect)
        
            

    def chase_target(self):
        """Di chuyển ma về phía mục tiêu theo đường ngắn nhất."""
        start = f"{self.ghost_pos[0]},{self.ghost_pos[1]}"
        path_to_target = self.path._dijkstra_path(start, self.target)
        if self.moving == False:
            # Di chuyển đến bước tiếp theo trên đường đi
            self.moving = True 
            if path_to_target and len(path_to_target) > 1:
                x, y = map(int, path_to_target[1].split(','))
                if x - self.ghost_pos[0] == 1:
                    self.target_pixel_pos[0] += self.CELL_SIZE 
                elif x - self.ghost_pos[0] == -1:
                    self.target_pixel_pos[0] -= self.CELL_SIZE 
                elif y - self.ghost_pos[1] ==1:
                    self.target_pixel_pos[1] += self.CELL_SIZE
                elif y- self.ghost_pos[1] ==-1:
                    self.target_pixel_pos[1] -= self.CELL_SIZE
                self.ghost_pos = [x, y]
            else: # Nếu không tìm thấy đường đi hoặc đã đến nơi, chọn một hướng ngẫu nhiên để di chuyển
                # Trong trường hợp này, hành vi "roam" mới sẽ được kích hoạt bởi update_ghost
                self.target = None
        else:
            self.moving = True



            
    def check_event(self):
        """
        Cập nhật logic và vị trí của ma trong mỗi khung hình.
        Đây là hàm chính để xử lý hành vi của ma.
        """
        distance_path = utils.utilities.mahattan(self.ghost_pos, self.player.player_pos)
        self.move_counter += 1
        if self.move_counter < self.move_delay:
            return
        
        self.move_counter = 0
        
        px, py = self.player.player_pos[0], self.player.player_pos[1]
        player_pos = f"{px},{py}"
        
        # Cập nhật trạng thái của ma
        if self.safe_zone.player_is_in_safe_zone() and distance_path <2:
            self.state = 'scare'
        elif self.safe_zone.player_is_in_safe_zone() and distance_path >3:
            self.state = 'roaming'
        elif self.safe_zone.player_is_in_safe_zone() == False:
            self.state = 'roaming' if distance_path >5 else 'chasing'
        
        # Thực hiện hành động dựa trên trạng thái
        if self.state == 'roaming':
            self.speed = 1
            # Nếu ma không có mục tiêu hoặc đã đến mục tiêu, chọn một điểm ngẫu nhiên mới
            if self.target is None or self.ghost_pos == list(map(int, self.target.split(','))):
                x = random.randint(0, self.maze.size - 1)
                y = random.randint(0, self.maze.size - 1)
                self.target = f"{x},{y}"
            
            # Di chuyển đến mục tiêu ngẫu nhiên
            self.chase_target()
            #chasing player
        elif self.state == 'chasing':  # 'chasing'
            self.speed = 5
            target1 = f'{self.player.player_pos[0]+1},{self.player.player_pos[1]}'
            target2 = f'{self.player.player_pos[0]-1},{self.player.player_pos[1]}'
            target3 = f'{self.player.player_pos[0]},{self.player.player_pos[1]}'
            target4 = f'{self.player.player_pos[0]},{self.player.player_pos[1]+1}'
            target5 = f'{self.player.player_pos[0]},{self.player.player_pos[1]-1}'
            options =[target1,target2,target3,target4,target5]
            self.target = random.choice(options)
            self.chase_target()
        else:
            #scare when player in safezone
            #make ghost run away
            self.speed = 7
            target = self.player_pos_key
            if self.ghost_pos[0] < self.player.player_pos[0]:
                if self.ghost_pos[1] < self.player.player_pos[1]:

                    x = random.randint(0,self.ghost_pos[0])
                    y = random.randint(0,self.ghost_pos[1])
                    target = f'{x},{y}'
                else:

                    x = random.randint(0,self.ghost_pos[0])
                    y = random.randint(self.ghost_pos[1],self.maze.size)
                    target = f'{x},{y}'
            else:

                if self.ghost_pos[1] < self.player.player_pos[1]:
                    while self.player.player_pos  in self.path._dijkstra_path(self.ghost_pos_key, target):
                        x = random.randint(self.ghost_pos[0],self.maze.size)
                        y = random.randint(0,self.ghost_pos[1])
                        target = f'{x},{y}'
                else:
                    while self.player.player_pos  in self.path._dijkstra_path(self.ghost_pos_key, target):
                        x = random.randint(self.ghost_pos[0],self.maze.size)
                        y = random.randint(self.ghost_pos[1],self.maze.size)
                        target = f'{x},{y}'
            self.target = target
            self.chase_target()

    # animation for ghost
    def update_movement(self):
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
                self.moving = False
        
    def update_ghost(self,dt):
        self.dt = dt
        self.check_event()
        self.update_movement()
        self.draw_ghost()
    
