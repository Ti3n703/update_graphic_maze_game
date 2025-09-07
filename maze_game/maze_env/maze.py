import random
import heapq
import numpy as np
from collections import deque
import pygame

class Maze:
    def __init__(self, game):
        self.size = game.size
        self.screen = game.screen
        self.CELL_SIZE = game.CELL_SIZE
        self.WALL_COLOR = game.WALL_COLOR
        self.WALL_THICKNESS = game.WALL_THICKNESS
        self.highlight_color = (255, 0, 0)
        self.path = game.path
        self.BG_COLOR = game.BG_COLOR
        self.screen_w = game.screen1.width
        self.screen_h = game.screen1.height

    def draw_maze(self, animate=True, delay=0.05):
        if animate:
            temp_path = My_maze_path(self.size)
            temp_path.add_grid(self.size)
            
            for cell1, cell2 in self.path.build_steps:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        quit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        animate = False
                        break
                if not animate:
                    break
                
                temp_path.add_edge(cell1, cell2, 1)
                
                self.screen.fill(self.BG_COLOR)
                self.draw_final_maze(temp_path)
                
                col, row = map(int, cell1.split(','))
                pixel_x = col * self.CELL_SIZE
                pixel_y = row * self.CELL_SIZE
                pygame.draw.rect(self.screen, self.highlight_color, (pixel_x, pixel_y, self.CELL_SIZE - 3, self.CELL_SIZE - 3))
                pygame.display.flip()
                pygame.time.delay(int(delay * 1000))

        self.draw_final_maze(self.path)
        
    def draw_final_maze(self, maze_path):
        # --- tính offset để center nguyên cái maze ---
        maze_w = self.size * self.CELL_SIZE
        maze_h = self.size * self.CELL_SIZE
        offset_x = (self.screen_w - maze_w) // 2
        offset_y = (self.screen_h - maze_h) // 2

        # vẽ border ngoài
        #pygame.draw.rect(self.screen, self.WALL_COLOR, 
                      #   (offset_x, offset_y, maze_w, maze_h), 
                      #   self.WALL_THICKNESS)

        landscape_wall_img = pygame.image.load('image/bottom_wall.png').convert_alpha()
       # landscape_wall_img = pygame.transform.scale(
       #     landscape_wall_img,
       #     (int(landscape_wall_img.get_width()), int(landscape_wall_img.get_height()))
       # )

        potrait_wall_img = pygame.image.load('image/straight_wall.png').convert_alpha()
        #potrait_wall_img = pygame.transform.scale(
            #potrait_wall_img,
            #(int(potrait_wall_img.get_width()), int(potrait_wall_img.get_height()))
        #)

        #floor
        floor_image = pygame.image.load('image/floor.png').convert_alpha()

        for row in range(self.size):
            for col in range(self.size):
                current = f"{col},{row}"
                pixel_x = offset_x + col * self.CELL_SIZE
                pixel_y = offset_y + row * self.CELL_SIZE
                rect_floor = floor_image.get_rect(topleft = (pixel_x,pixel_y))
                self.screen.blit(floor_image,rect_floor)

        for row in range(self.size):
            for col in range(self.size):
                current = f"{col},{row}"
                pixel_x = offset_x + col * self.CELL_SIZE
                pixel_y = offset_y + row * self.CELL_SIZE

                # check top wall
                top_neighbor = f"{col},{row-1}"
                if  top_neighbor not in maze_path.adjacency_list.get(current, {}):
                    rect = landscape_wall_img.get_rect(topleft=(pixel_x, pixel_y ))
                    self.screen.blit(landscape_wall_img, rect)
                if col == self.size-1:
                    rect = landscape_wall_img.get_rect(topleft=(pixel_x+self.CELL_SIZE, pixel_y ))
                    self.screen.blit(potrait_wall_img, rect)



                # check left wall 
                right_neighbor = f"{col-1},{row}"
                if col - 1 < self.size and right_neighbor not in maze_path.adjacency_list.get(current, {}):
                    rect = potrait_wall_img.get_rect(topleft=(pixel_x , pixel_y))
                    self.screen.blit(potrait_wall_img, rect)
                if row == self.size-1:
                    rect = landscape_wall_img.get_rect(topleft=(pixel_x, pixel_y+self.CELL_SIZE ))
                    self.screen.blit(landscape_wall_img, rect)
            
        
   
    
class My_maze_path:
    def __init__(self, game):
        self.adjacency_list = {}
        self.build_steps = []
        self.size = game.size
      
        self.map = np.zeros((self.size*2-1, self.size*2-1))
        self.expanded_matrix = np.zeros((self.size*2-1, self.size*2-1))
        self.shortest_distance = {}
    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = {}

    def add_edge(self, from_node, to_node, weight=1):
        self.add_vertex(from_node)
        self.add_vertex(to_node)
        self.adjacency_list[from_node][to_node] = weight
        self.adjacency_list[to_node][from_node] = weight
        self.build_steps.append((from_node, to_node))

    def _prim(self, start_vertex, size):
        visited = set()
        min_heap = [(0, start_vertex, None)]
        
        while min_heap and len(visited) < size * size:
            weight, current_vertex, parent_vertex = heapq.heappop(min_heap)
            
            if current_vertex in visited:
                continue
                
            visited.add(current_vertex)
            if parent_vertex:
                self.add_edge(parent_vertex, current_vertex, weight)
            
            col, row = map(int, current_vertex.split(','))
            
            for dcol, drow in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                next_col, next_row = col + dcol, row + drow
                neighbor_vertex = f"{next_col},{next_row}"
                
                if 0 <= next_row < size and 0 <= next_col < size and neighbor_vertex not in visited:
                    edge_weight = random.randint(1, 10)
                    heapq.heappush(min_heap, (edge_weight, neighbor_vertex, current_vertex))

    def _dijkstra_path(self, start_vertex, end_vertex):
        distances = {vertex: float('infinity') for vertex in self.adjacency_list}
        distances[start_vertex] = 0
        priority_queue = [(0, start_vertex)]
        previous_vertices = {vertex: None for vertex in self.adjacency_list}

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue
            
            if current_vertex == end_vertex:
                path = []
                while previous_vertices[current_vertex]:
                    path.insert(0, current_vertex)
                    current_vertex = previous_vertices[current_vertex]
                path.insert(0, start_vertex)
                return path

            for neighbor, weight in self.adjacency_list[current_vertex].items():
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_vertices[neighbor] = current_vertex
                    heapq.heappush(priority_queue, (distance, neighbor))
        return None

    def add_grid(self, size):
        for row in range(size):
            for col in range(size):
                self.add_vertex(f'{col},{row}')

    def get_potential_connection(self, vertex, size):
        connections = []
        col, row = map(int, vertex.split(','))
        if col > 0:
            connections.append(f"{col-1},{row}")
        if col < size - 1:
            connections.append(f"{col+1},{row}")
        if row > 0:
            connections.append(f"{col},{row-1}")
        if row < size - 1:
            connections.append(f"{col},{row+1}")
        random.shuffle(connections)
        return connections

    def add_random_edges(self):
        potential_edges = []
        for row in range(self.size):
            for col in range(self.size):
                vertex = f"{col},{row}"
                for neighbor in self.get_potential_connection(vertex, self.size):
                    if neighbor not in self.adjacency_list.get(vertex, {}):
                        edge = tuple(sorted((vertex, neighbor)))
                        if edge not in potential_edges:
                            potential_edges.append(edge)
        
        random.shuffle(potential_edges)
        extra_edges_count = int(len(potential_edges) * 0.3)
        
        for i in range(min(extra_edges_count, len(potential_edges))):
            u, v = potential_edges[i]
            self.add_edge(u, v, random.randint(1, 5))

    def create_path(self, algorithm='prim'):
        self.add_grid(self.size)
        if algorithm == 'prim':
            self._prim('0,0', self.size)
        else:
            raise ValueError(f"Unknown algorithm: {algorithm}")

    def bfs(self, node, target):
        visited = {}  
        queue = deque()    

        visited[node] = None
        queue.append(node)
        
        while queue:
            m = queue.popleft() 
            if m == target:  # Bingo!
               
                path = []
                while m:
                    path.append(m)
                    m = visited[m]  # Walk back
                return path[::-1]  # Reverse it
            for neighbour in self.adjacency_list[m]:
                if neighbour not in visited:
                    visited[neighbour] = m  # Remember where we came from
                    queue.append(neighbour) 
            








