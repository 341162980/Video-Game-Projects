import pygame
import time
import random
pygame.font.init()      #needed for fonts from pygame

#Create new window (for game)
WIDTH, HEIGHT = 800, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("SpaceFighters")     #name/caption of window

BG0 = pygame.image.load("background-black.png")     #background image
BG = pygame.transform.scale(BG0, (WIDTH,HEIGHT))
FPS = 80

#Spaceships
RED_SPACESHIP = pygame.image.load("pixel_ship_red_small.png")
GREEN_SPACESHIP = pygame.image.load("pixel_ship_green_small.png")
BLUE_SPACESHIP = pygame.image.load("pixel_ship_blue_small.png")
YELLOW_SPACESHIP = pygame.image.load("pixel_ship_yellow.png")        #player ship

P_VEL = 7     #player velocity
E_VEL = 1       #enemy velocity
L_VEL = 4       #laser velocity

#Bullets (laser)
RED_LASER = pygame.image.load("pixel_laser_red.png")
GREEN_LASER = pygame.image.load("pixel_laser_green.png")
BLUE_LASER = pygame.image.load("pixel_laser_blue.png")
YELLOW_LASER = pygame.image.load("pixel_laser_yellow.png")

FONT = pygame.font.SysFont("comicsans", 40)     #set a font
LOST_FONT = pygame.font.SysFont("comicsans", 80)     #set a font

class Ship:     #abstract class for ship which will be inherited by character ship and enemy ships
    
    COOLDOWN = 30       #0.5 sec cooldown
    def __init__(self, x, y, hp = 100):      #default ship has 100 hp
        #class attributes
        self.x = x
        self.y = y
        self.health = hp
        self.ship_image = None
        self.laser_image = None
        self.lasers = []
        self.cool_down_counter = 0      #prevent spamming lasers
    
    def draw_ship(self, window):
        window.blit(self.ship_image, (self.x, self.y))  #draws ship
        
        #draw lasers
        for laser in self.lasers:
            laser.laser_draw(window)
    
    def get_width(self):        #gets width of ship image
        return self.ship_image.get_width()
    
    def get_height(self):        #gets height of ship image
        return self.ship_image.get_height()

    def cooldown(self):     #handles shooting cool down
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter =0
        elif self.cool_down_counter > 0:        #if cooldown>0 and not past cool down time
            self.cool_down_counter += 1

    def shoot(self):    #function for shooting
        if self.cool_down_counter ==0:      #if cool down is 0, then you can shoot
            laser = Laser(self.x,self.y,self.laser_image)     #shoot laser
            self.lasers.append(laser)
            self.cool_down_counter = 1
    
    def move_lasers(self,vel, obj):    #method moving lasers & checks for collision with player
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):  #if enemy laser hits player, player loses hp
                obj.health -= 10
                self.lasers.remove(laser)

class Player(Ship):     #Player class; inherits from Ship class
    
    def __init__(self, x, y, hp=100):
        super().__init__(x,y,hp)       #"super" means it uses the parent class "Ship"
        self.ship_image = YELLOW_SPACESHIP
        self.laser_image = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_image)        #for pixel perfect collisions
        self.max_health = hp            #max health = starting health
    
    def move_lasers(self,vel, objs):    #method moving lasers & checks for collision with enemies
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else: 
                for obj in objs:
                    if laser.collision(obj) and obj.y >= 0:  #if player laser hits enemy on screen, enemy dies
                        obj.health -= 10
                        objs.remove(obj)
                        if laser in self.lasers:
                            self.lasers.remove(laser)
    
    def draw_ship(self, window):      #override draw function to add health bar
        super().draw_ship(window)
        self.healthbar(window)
    
    def healthbar(self, window):        #method for healthbar
        pygame.draw.rect(window, "red", (self.x,self.y+self.ship_image.get_height()+10, self.ship_image.get_width(), 10))
        pygame.draw.rect(window, "green", (self.x,self.y+self.ship_image.get_height()+10, self.ship_image.get_width() * (self.health/self.max_health), 10))
        

class Enemy(Ship):  #Enemy class; inherits from Ship class
    #dictionary for enemy ship type
    COLOR_MAP = {"red": (RED_SPACESHIP, RED_LASER), 
                "green": (GREEN_SPACESHIP, GREEN_LASER),
                "blue": (BLUE_SPACESHIP, BLUE_LASER)}      
    
    def __init__(self, x, y,color, hp=100):     #enemy ships have different colors
        super().__init__(x, y, hp)      #inherits from "Ship" class
        self.ship_image, self.laser_image = self.COLOR_MAP[color]   #retrieve enemy ship type image and laser
        self.mask = pygame.mask.from_surface(self.ship_image) #for pixel perfect collisions

    def move(self,vel):     #enemy ship movement
        self.y += vel
        
    def shoot(self):    #function for shooting (overriden previous version)
        if self.cool_down_counter ==0:      #if cool down is 0, then you can shoot
            laser = Laser(self.x - 20,self.y,self.laser_image)     #shoot laser, x position modified
            self.lasers.append(laser)
            self.cool_down_counter = 1

class Laser:            #represents 1 laser object (bullet)
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
    
    def laser_draw(self,window):
        window.blit(self.image, (self.x, self.y))
        
    def move(self, vel):    #method for laser movement
        self.y += vel
    
    def off_screen(self, height):   #method checking if laser is off screen
        return not (self.y<=height, self.y>=0)
    
    def collision(self,obj):        #checks if object collides with laser
        return collide(obj, self)

def collide(obj1, obj2):        #function which checks if collision occurs (pixel on pixel)
    offset_x = obj2.x - obj1.x  #distance between objects 
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None   #check for collision

def main():     #function with main game logic
    run = True
    clock = pygame.time.Clock() #clock object
    lost = False
    lost_count = 0
    
    level = 0   
    lives = 5
    
    player = Player(300,580)
    enemies = []        #list of enemies on screen
    wave_length = 2
    
    def draw():     #adds objects to screen (function in another function; can only be called within "main")
        WIN.blit(BG, (0,0))     #background
        
        #level and lives text
        lives_text = FONT.render(f"Level: {level}", 1, "yellow")
        level_text = FONT.render(f"Lives: {lives}", 1, "yellow")
        WIN.blit(level_text, (20,10))
        WIN.blit(lives_text, (WIDTH - level_text.get_width() - 20,10))
        
        for enemy in enemies:
            enemy.draw_ship(WIN)     #uses draw function from "Ship" class
        
        player.draw_ship(WIN)       #draw player
        
        if lost:        #Lost display
            lost_label = LOST_FONT.render("You lost!", 1, (255,0,0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2,300))  
        
        pygame.display.update()     #adds new display
    
    while run:      #main game loop
        clock.tick(FPS)  #clock.tick regulates loop running speed
        draw()
        
        if lives<=0 or player.health ==0:       #losing scenario
            lost = True
            lost_count +=1
            if lost_count> FPS*5:       #quit game 5 secs after losing 
                run = False
            continue    #freezes screen until 5 secs
        
        if len(enemies) ==0:        #increase level once all enemies in 1 wave are defeated
            level +=1
            if wave_length<40:
                wave_length += 3        #increase enemies per wave as level increases
            
            for i in range(wave_length):    #spawn enemies (position, type, hp)
                enemy = Enemy(random.randrange(50,WIDTH-75), random.randrange(-1500,-100)
                    ,random.choice(["red","green","blue"]), random.choice([100,200,300]))
                enemies.append(enemy)
        
        for event in pygame.event.get():        #for every next instance of the loop running
            if event.type == pygame.QUIT:       #manually exits loop when window is closed
                run = False
                break
        
        keys = pygame.key.get_pressed()     
        #Player movement
        if keys[pygame.K_LEFT] and player.x - P_VEL > 0:
            player.x -= P_VEL
        if keys[pygame.K_RIGHT] and player.x + P_VEL + player.get_width()< WIDTH:
            player.x += P_VEL
        if keys[pygame.K_UP] and player.y - P_VEL >0:
            player.y -= P_VEL
        if keys[pygame.K_DOWN] and player.y + P_VEL  + player.get_height() + 15< HEIGHT:
            player.y += P_VEL
        if keys[pygame.K_SPACE]:        #space bar shoots lasers for player
            player.shoot()
        
        for enemy in enemies[:]:
            enemy.move(E_VEL) #enemy ship movement
            enemy.move_lasers(L_VEL, player)     #checks if enemy lasers hit player
            
            if random.randrange(0,240) ==1 and enemy.y >= 0:        #how often enemy shoots
                enemy.shoot()
            
            if collide(enemy,player):       #scenario where ships collide
                player.health -= 10
                enemies.remove(enemy)
            
            #remove enemy once it goes off page and decrement lives
            elif enemy.y + enemy.get_height() > HEIGHT:       
                lives -= 1
                enemies.remove(enemy)
        
        player.move_lasers(-L_VEL, enemies)      #checks if player lasers hit enemy
            
def main_menu():        #function for main menu
    title_font = pygame.font.SysFont("comicsans", 50)   #font for title message
    run = True
    while run:
        WIN.blit(BG, (0,0))
        title_label = title_font.render("Press the mouse to begin.", 1, "white")   #title message
        WIN.blit(title_label, (WIDTH/2 - title_label.get_width()/2, 300))
        pygame.display.update()
        
        for event in pygame.event.get():        #game terminates when browser's closed
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:    #if we press mouse, start game
                main()
    
    pygame.quit()
main_menu()