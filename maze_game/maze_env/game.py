import platform
import random
from entity import Ghost, player, Safe_Zone, Exit_Point
from maze_env import Maze, Game_Screen, My_maze_path
import pygame
import numpy as np
from collections import deque
import utils.utilities as utilities

class Game:
    def __init__(self, size, render_mode="human"):
        self.display_cell_size = 25
        self.display_size = size * self.display_cell_size
        self.CELL_SIZE = 25
        self.obs_cell_size = 10
        self.obs_size = size * self.obs_cell_size
        self.WALL_THICKNESS = 4
        self.BG_COLOR = (23, 32, 38)
        self.WALL_COLOR = (141, 226, 46)
        self.player_color = (158, 124, 16)
        self.ghost_speed = 4
        self.exit_color = (185, 55, 93)
        self.player_movement_delay = 0
        self.steps = 0
        self.sz_color = (97, 55, 107)
        self.successful = 0
        self.total = 0
        self.size = size
        self.matrix_size = size * 2 - 1
        self.render_mode = render_mode
        self.metadata = {"render_modes": ["human", "rgb_array"], "render_fps": 30}
        self.screen1 = Game_Screen(self)
        self.screen = self.screen1.screen
        self.path = My_maze_path(self)
        self.path.create_path()
        self.path.add_random_edges()
        self.maze = Maze(self)
        self.player = player(self)
        self.safezone = Safe_Zone(self)
        self.safezone.create_safezone(self.size)
        self.ghost_update_interval = 0
        self.num_ghosts = 3  # Add 3 ghosts for challenge
        self.ghosts = []
        
        valid_positions = list(self.path.adjacency_list.keys())
        for i in range(self.num_ghosts):
            g = Ghost(self)
            # Place ghosts at random valid positions
            pos = random.choice(valid_positions)
            g.ghost_pos = [int(pos.split(',')[0]), int(pos.split(',')[1])]
            g.color = (225, 0, 0)
            self.ghosts.append(g)
        self.exit_point = Exit_Point(self)
        self.last_action = None
        self.visited = {}
        self.clock = pygame.time.Clock()
        self.bfs_cache = {}  # Cache for BFS results

    def _render_frame(self):
        self.screen.fill(self.BG_COLOR)
        self.maze.draw_final_maze(self.path)
        self.exit_point.draw_exit_point()
        self.safezone.draw_safe_zone()
        self.player.draw_player()
        for ghost in self.ghosts:
            ghost.update_ghost()
        pygame.display.flip()
        self.clock.tick(self.metadata["render_fps"])

    def render(self):
        if self.render_mode == "rgb_array":
            return self.get_observation()
        elif self.render_mode == "human":
            self._render_frame()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.close()
                    raise SystemExit("Window closed by user")
            return None

    def reset(self):
        self.path = My_maze_path(self)
        self.path.create_path()
        self.path.add_random_edges()
        self.maze = Maze(self)
        self.player = player(self)
        self.safezone = Safe_Zone(self)
        self.safezone.create_safezone(self.size)
        self.exit_point = Exit_Point(self)
        valid_positions = list(self.path.adjacency_list.keys())
        self.ghosts = []
        for i in range(self.num_ghosts):
            g = Ghost(self)
            pos = random.choice(valid_positions)
            g.ghost_pos = [int(pos.split(',')[0]), int(pos.split(',')[1])]
            g.color = (225, 0, 0)
            self.ghosts.append(g)
        self.steps = 0
        self.game_state = "playing"
        self.last_action = None
        self.visited = {}
        self.bfs_cache = {}  # Reset cache
        start_pos = tuple(self.player.player_pos)
        self.visited[start_pos] = 1
        if self.render_mode == "human":
            self._render_frame()
        return self.get_observation(), {}

    def get_observation(self):
        def convert_path_to_dir(path):
            if path is None or len(path) < 2:
                return 4  # stay
            curr = [int(x) for x in path[0].split(',')]
            next_ = [int(x) for x in path[1].split(',')]
            dx = next_[0] - curr[0]
            dy = next_[1] - curr[1]
            if dx == 1:
                return 3  # right
            elif dx == -1:
                return 2  # left
            elif dy == 1:
                return 1  # down
            elif dy == -1:
                return 0  # up
            return 4  # stay

        px, py = self.player.player_pos
        player_pos_key = f'{px},{py}'
        adj = self.path.adjacency_list.get(player_pos_key, {})
        left_wall = 0 if f'{px-1},{py}' in adj else 1
        right_wall = 0 if f'{px+1},{py}' in adj else 1
        up_wall = 0 if f'{px},{py-1}' in adj else 1
        down_wall = 0 if f'{px},{py+1}' in adj else 1

        next_great_dir = 0
        ghost_dis_list = [utilities.mahattan(self.player.player_pos, ghost.ghost_pos) for ghost in self.ghosts]
        ghost_dis_list = ghost_dis_list if ghost_dis_list else [float(self.size * 2)] * 3
        ghost_dis_list.sort()
        while len(ghost_dis_list) < 3:
            ghost_dis_list.append(float(self.size * 2))
        nearest_ghost = ghost_dis_list[0]
        is_in_safe_zone =0

        if nearest_ghost <10:
            safezone_pos_list = [tuple(sz) for sz in self.safezone.safe_zone_list]
            min_safezone_dist = float('inf')
            nearest_safezone_key = None
            for sz_pos in safezone_pos_list:
                dist = utilities.mahattan(self.player.player_pos, sz_pos)
                if dist < min_safezone_dist:
                    min_safezone_dist = dist
                    nearest_safezone_key = f'{sz_pos[0]},{sz_pos[1]}'
            
            if nearest_safezone_key is not None:
                cache_key = (player_pos_key, nearest_safezone_key)
                if cache_key not in self.bfs_cache:
                    self.bfs_cache[cache_key] = self.path.bfs(player_pos_key, nearest_safezone_key)
                path_to_safezone = self.bfs_cache[cache_key]
                dir_nearest_safe = convert_path_to_dir(path_to_safezone) if path_to_safezone else 4
            else:
                dir_nearest_safe = 4

            if tuple(self.player.player_pos) in safezone_pos_list:
                dir_nearest_safe = 4
                is_in_safe_zone = 1
            next_great_dir = dir_nearest_safe
        else:
            exit_pos_key = f'{self.exit_point.exit_pos[0]},{self.exit_point.exit_pos[1]}'
            cache_key = (player_pos_key, exit_pos_key)
            if cache_key not in self.bfs_cache:
                self.bfs_cache[cache_key] = self.path.bfs(player_pos_key, exit_pos_key)
            path_to_exit = self.bfs_cache[cache_key]
            dir_exit = convert_path_to_dir(path_to_exit) if path_to_exit else 4
            next_great_dir = dir_exit
        

        return np.array([
            next_great_dir,
            is_in_safe_zone,
           
        ], dtype=np.float32)
    def running(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
        close()

    

    def close(self):
        pygame.quit()
if __name__ == '__main__':
    game = Game(20)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        game.screen.fill()
        game.maze.draw_final_maze(game.path)

    
