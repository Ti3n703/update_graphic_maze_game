import pygame
class Load_Sprite_Sheet:
    def __init__(self, sheet):
        self.sheet = sheet

    def get_image_horizontal(self, action,frame, width, height,scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.fill((0,0,0,0))
        image.blit(self.sheet, (-1,0), ((frame*width), action*height, width, height))
        scaled_img = pygame.transform.scale(image,(int(image.get_width()*scale), int(image.get_height()*scale)))
        return image
    def get_image_vertical(self, action,frame, width, height,scale):
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.fill((0,0,0,0))
        image.blit(self.sheet, (-1,0), ((action*width), frame*height, width, height))
        image= pygame.transform.scale(image,(int(image.get_width()*scale), int(image.get_height()*scale)))
        return image

    
    