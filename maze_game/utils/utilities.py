import pygame
def mahattan(pos1,pos2):
    x1,y1 = pos1[0], pos1[1]
    x2,y2 = pos2[0], pos2[1]
    return abs(x2-x1) + abs(y2-y1)
    

