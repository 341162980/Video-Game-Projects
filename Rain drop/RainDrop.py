import pygame
import time
import random
pygame.font.init()      #needed for fonts from pygame

#Create new window (for game)
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("EnderLife")     #name/caption of window

BG0 = pygame.image.load("Minecraft_background.jpg")     #background image
BG = pygame.transform.scale(BG0, (WIDTH,HEIGHT+130))

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 70

PLAYER_VEL = 5      #player velocity when moved

PROJ_WIDTH = 15       #projectile width
PROJ_HEIGHT = 35
PROJ_VEL = 4

FONT = pygame.font.SysFont("comicsans", 30)     #set a font

def draw(player, lapsed_time, projs):     #adds objects to screen
    WIN.blit(BG, (0,0), )      #blit: function used to draw background image on screen
    
    time_text = FONT.render(f"Time: {round(lapsed_time)}s", 1, "white")     #sets timer appearance
    WIN.blit(time_text, (10,10))        #sets position of timer 
    
    pygame.draw.rect(WIN, (0,0,0), player)      #creates player on window with color in rgb
    
    for proj in projs:      #add projectiles to window
        pygame.draw.rect(WIN, "blue", proj)
    
    pygame.display.update()     #adds new display

def main():     #function with main game logic
    run = True
    
    #create the player (rectangle with coordinates and player dimensions)
    player = pygame.Rect(480, HEIGHT - 130-PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)      
    
    clock = pygame.time.Clock() #clock object
    start_time = time.time()    #start time
    lapsed_time = 0
    
    #Projectiles
    proj_add_increment = 2500      #begin by sending 1 projectile every 2000 milisecs
    proj_count = 0      #tells us when to add next projectile
    projs = []       #where all projectiles on screen will be stored
    hit = False
    
    while run:      #main game loop
        
        proj_count += clock.tick(150)  #clock.tick regulates loop running speed
        
        lapsed_time = time.time() - start_time      #lapsed time: counter for game
        
        #Projectile instances (generation)
        if proj_count>proj_add_increment:       #add stars after 2000 milisecs
            
            for _ in range(3):      #add 3 stars
                proj_x = random.randint(0, WIDTH - PROJ_WIDTH)
                proj = pygame.Rect(proj_x, -PROJ_HEIGHT, PROJ_WIDTH, PROJ_HEIGHT)        #projectile begins off window
                projs.append(proj)
            
            proj_add_increment = max(400, proj_add_increment - 50)      #makes projectiles comes faster
            proj_count = 0
            
        
        for event in pygame.event.get():        #for every next instance of the loop running
            if event.type == pygame.QUIT:       #manually exits loop when window is closed
                run = False
                break
        
        #Handling player movement
        keys = pygame.key.get_pressed()     #gives dictionary of pressed keys by player
        
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >=0:     #left arrow key & establish boundaries for moving
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <=WIDTH:     #right arrow key & establish boundaries for moving
            player.x += PLAYER_VEL
        
        #Projectile movement
        for proj in projs[:]:       #create copy of list; projs out of screen are removed
            
            proj.y += PROJ_VEL
            if proj.y > HEIGHT:     #removes projs when out of screen
                projs.remove(proj)
            elif proj.y + proj.height >= player.y and proj.colliderect(player):       #when proj hits player
                projs.remove(proj)
                hit = True
                break
        
        #Handling Loss (collision)
        if hit:
            lost_text = FONT.render("You got hit after " + str(lapsed_time) + " seconds. Exiting game.", 1, "white")
            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2 - lost_text.get_height()/2) )      #display loss
            pygame.display.update()
            pygame.time.delay(7000)
            break
        
        draw(player, lapsed_time, projs)      #add objects to screen
    
    pygame.quit()   #quit game when loop ends

if __name__ == "__main__":      #run file (doesn't auto run when imported)
    main() 