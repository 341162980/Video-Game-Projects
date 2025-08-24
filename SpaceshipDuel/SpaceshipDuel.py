import pygame
pygame.font.init() 
pygame.mixer.init() #sound effect library

WIDTH, HEIGHT = 700,450
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  #window dimensions
pygame.display.set_caption("Fighter game")  #window name
FPS = 60  

SPACE = pygame.transform.scale(pygame.image.load("space.png"), (WIDTH, HEIGHT))  #load in background
BORDER = pygame.Rect(348, 0, 4, 450)

SPACESHIP_WIDTH = 50
SPACESHIP_HEIGHT = 40
SHIP_V = 5      #spaceship velocity

YELLOW_SPACESHIP_IMAGE = pygame.image.load('spaceship_yellow.png')
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 90)  #spaceship rotation and resizing

RED_SPACESHIP_IMAGE = pygame.image.load('spaceship_red.png')
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH,SPACESHIP_HEIGHT)), 270)

BULL_V = 7      #bullet velocity
MAX_BULL = 3       #max amount of bullets on screen at once

YELLOW_HIT = pygame.USEREVENT + 1       #event that a ship is hit
RED_HIT = pygame.USEREVENT + 2

HEALTH_FONT = pygame.font.SysFont("comicsans", 30)      #font for health 
WINNER_FONT = pygame.font.SysFont('comicsans', 80)

BULLET_HIT_SOUND = pygame.mixer.Sound("Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Gun+Silencer.mp3")

def draw(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp):
    WIN.blit(SPACE, (0,0))  #draw background
    pygame.draw.rect(WIN, "black", BORDER)  #border creation

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))   #blit: projects an image over window
    WIN.blit(RED_SPACESHIP, (red.x,red.y))

    #score/health
    red_hp_txt = HEALTH_FONT.render("Health: " + str(red_hp), 1, "red")   #display red ship hp
    yellow_hp_txt = HEALTH_FONT.render("Health: " + str(yellow_hp), 1, "yellow")   #display yellow ship hp
    WIN.blit(red_hp_txt, (WIDTH - red_hp_txt.get_width() - 10, 10))     
    WIN.blit(yellow_hp_txt, (10, 10))

    #draw bullets
    for bul in red_bullets:
        pygame.draw.rect(WIN, "red", bul)
    for bul in yellow_bullets:
        pygame.draw.rect(WIN, "yellow", bul)

    pygame.display.update()

def yellow_move(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - SHIP_V>=0:    #left for yellow
        yellow.x -= SHIP_V
    if keys_pressed[pygame.K_d] and yellow.x + SHIP_V + SPACESHIP_WIDTH<=BORDER.x:    #right for yellow
        yellow.x += SHIP_V
    if keys_pressed[pygame.K_w] and yellow.y - SHIP_V >=0:    #up for yellow
        yellow.y -= SHIP_V
    if keys_pressed[pygame.K_s] and yellow.y + SHIP_V + yellow.height <= HEIGHT - 10:    #down for yellow
        yellow.y += SHIP_V

def red_move(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - SHIP_V >= BORDER.x + BORDER.width:    #left for red
        red.x -= SHIP_V
    if keys_pressed[pygame.K_RIGHT] and red.x + SHIP_V + red.width -15< WIDTH:    #right for red
        red.x += SHIP_V
    if keys_pressed[pygame.K_UP] and red.y - SHIP_V >=0:    #up for red
        red.y -= SHIP_V
    if keys_pressed[pygame.K_DOWN] and red.y + SHIP_V + red.height <= HEIGHT - 10:    #down for red
        red.y += SHIP_V

def handle_bullets(yellow_bullets, red_bullets, yellow,red):

    for bul in yellow_bullets:
        bul.x += BULL_V
        if red.colliderect(bul):        #red is hit
            pygame.event.post(pygame.event.Event(RED_HIT))      #handles when red is hit
            yellow_bullets.remove(bul)  #remove bullet from screen
        elif bul.x > WIDTH:     #if bullet goes off screen, remove
            yellow_bullets.remove(bul)

    for bul in red_bullets:
        bul.x -= BULL_V
        if yellow.colliderect(bul):        #yellow is hit
            pygame.event.post(pygame.event.Event(YELLOW_HIT))      #handles when yellow is hit
            red_bullets.remove(bul)  #remove bullet from screen
        elif bul.x<0:           #if bullet goes off screen, remove
            red_bullets.remove(bul)

def draw_winner(text):      #function displaying winner
    if text =="Yellow Wins!":
        draw_text = WINNER_FONT.render(text,1,"yellow")
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(7000)
    if text =="Red Wins!":
        draw_text = WINNER_FONT.render(text,1,"red")
        WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2))
        pygame.display.update()
        pygame.time.delay(7000)

def main():     
    yellow = pygame.Rect(50, 180, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)     #hitbox of spaceship
    red = pygame.Rect(610, 180, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)     #hitbox of spaceship

    yellow_bullets = []
    red_bullets = []

    red_hp = 20
    yellow_hp = 20

    clock = pygame.time.Clock()
    run = True
    while run:      #game loop

        clock.tick(FPS)     #controls speed of loop
        for event in pygame.event.get():     #loop through instances ("events") of game
            if event.type ==pygame.QUIT:        #quit game
                run = False
        
            #Bullets
            if event.type == pygame.KEYDOWN:
                if event.key ==pygame.K_LALT and len(yellow_bullets)<MAX_BULL:      #yellow shoots
                    y_bul = pygame.Rect(yellow.x+yellow.width-5, yellow.y + yellow.height//2 - 2, 10,5)  #bullet position + dimensions
                    yellow_bullets.append(y_bul)
                    BULLET_FIRE_SOUND.play()

                if event.key ==pygame.K_RALT and len(red_bullets)<MAX_BULL:      #red shoots
                    r_bul = pygame.Rect(red.x, red.y + red.height//2 - 2, 10,5)  #bullet position + dimensions
                    red_bullets.append(r_bul)
                    BULLET_FIRE_SOUND.play()

            #handle bullets hitting ships
            if event.type ==RED_HIT:
                red_hp -= 4
                BULLET_HIT_SOUND.play()
            if event.type ==YELLOW_HIT:
                yellow_hp -= 4
                BULLET_HIT_SOUND.play()
        
        #When someone wins
        winner_text = ""
        if red_hp <=0:
            pygame.time.delay(100)
            winner_text = "Yellow Wins!"
        if yellow_hp<=0:  
            pygame.time.delay(100)      
            winner_text = "Red Wins!"
        if winner_text!= "":
            draw(red, yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)  #force hp to show 0 HP
            pygame.display.update()
            draw_winner(winner_text)    #someone won
            break

        #Spaceship movement
        keys_pressed = pygame.key.get_pressed()     #tells which keys are pressed (allows simultaneous pressing)
        yellow_move(keys_pressed, yellow)
        red_move(keys_pressed, red)

        #Handles bullet movement
        handle_bullets(yellow_bullets, red_bullets, yellow,red)

        draw(red,yellow, red_bullets, yellow_bullets, red_hp, yellow_hp)
        
    pygame.quit()

if __name__ == "__main__":      #only runs function if file is run directly (not imported)
    main()