#File with helper functions
import pygame
pygame.font.init()      #needed for fonts from pygame

def scale_image(img, factor):      #function which automatically scales images
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

def rot_image(win, image, top_left, angle):        #function which rotates images
    rotated_image = pygame.transform.rotate(image,angle)      #rotates img by top left corner
    new_rect= rotated_image.get_rect(center = image.get_rect(topleft = top_left).center) #rotates img without changing x,y position    
    
    win.blit(rotated_image, new_rect.topleft)   #add image to window
    
def blit_text_center(win, font, text):   #prints text in middle of window
    render = font.render(text, 1, "green")
    win.blit(render, (win.get_width()/2 - render.get_width()/2 , win.get_height()/2 - render.get_height()/2 - 30))