import pygame
import time
import math
#import helper functions from other file
from helper import scale_image, rot_image , blit_text_center     
pygame.font.init()      #needed for fonts from pygame

#LOAD IMAGES:
GRASS = scale_image(pygame.image.load("grass.jpg"), 2.5)
TRACK = scale_image(pygame.image.load("track.png"), 0.85)
TRACK_BORDER =  scale_image(pygame.image.load("track-border.png"), 0.85)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)        #mask (for pixel perfect collisions)
FINISH = scale_image(pygame.image.load("finish.png"), 0.85)
FINISH_MASK = pygame.mask.from_surface(FINISH)      #mask for finish line (for pixel perfect collisions)
FINISH_POSITION = (125,250) #position of finish line
RED_CAR = scale_image(pygame.image.load("red-car.png"), 0.55)
GREEN_CAR = scale_image(pygame.image.load("green-car.png"), 0.55)
GREY_CAR = scale_image(pygame.image.load("grey-car.png"), 0.55)
PURPLE_CAR = scale_image(pygame.image.load("purple-car.png"), 0.55)
WHITE_CAR = scale_image(pygame.image.load("white-car.png"), 0.55)
all_cars = [RED_CAR, GREEN_CAR, GREY_CAR, PURPLE_CAR, WHITE_CAR]

#Create new window (for game)
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("KACHOOOWWW")     #name/caption of window

FPS = 80
PATH = [(168, 116), (112, 66), (56, 121), (50, 431), (292, 684),    #path for cpu
        (360, 659), (365, 512), (476, 440), (562, 514), (575, 664), 
        (660, 664), (690, 385), (644, 343), (421, 327), (374, 289), 
        (425, 244), (654, 245), (685, 158), (659, 61), (304, 70), 
        (264, 122), (262, 345), (220, 374), (161, 345), (163, 258)]

FONT = pygame.font.SysFont("comicsans", 30)     #set a font

class GameInfo:     #class defining game info; levels
    LEVELS = 10
    
    def __init__(self, Level = 1):      #start at lvl 1
        self.level = Level
        self.started = False        #don't start yet
        self.level_start_time = 0       #tract time in cur level
    
    def next_level(self):       #function increasing lvls
        self.level += 1
        self.started = False
    
    def reset(self):        #function resetting all settings
        self.level = 1
        self.started = False
        self.level_start_time = 0
    
    def game_finished(self):        #completed game
        return self.level > self.LEVELS
    
    def start_level(self):      #start game
        self.started = True
        self.level_start_time = time.time()
    
    def get_level_time(self):   #tracks time elapsed in a lvl
        if not self.started:        #game hasn't started, no time apssed
            return 0
        return time.time() - self.level_start_time 

#Menu to select car before game starts
def select_car(win, font, car_images, title_text):
    selected_car = None

    while selected_car is None:
        win.fill((0, 0, 0))  # dark background

        title_surface = font.render(title_text, True, "green")       #Title text
        win.blit(title_surface, (WIDTH // 2 - title_surface.get_width() // 2, 50))

        # Draw cars
        car_positions = []
        start_x = 100
        y_pos = HEIGHT // 2
        spacing = 150

        for i, car_img in enumerate(car_images):    #line up cars
            x = start_x + i * spacing
            win.blit(car_img, (x, y_pos))
            car_positions.append((x, y_pos, car_img))  # store pos and image

        pygame.display.update()

        # if window's closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            #if car is clicked
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for x, y, img in car_positions:
                    rect = pygame.Rect(x, y, img.get_width(), img.get_height())
                    if rect.collidepoint(mx, my):
                        selected_car = img
                        break

    return selected_car


# Player car selection
player_car = select_car(WIN, FONT, all_cars, "Select your player car")

# Remove chosen car so CPU can't pick same
cpu_choices = [c for c in all_cars if c != player_car]

# CPU car selection
cpu_car = select_car(WIN, FONT, cpu_choices, "Select CPU car")

class AbstractCar:      #abstract class; base class for both player and cpu car

    def __init__(self, max_vel, rot_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0        #beginning velocity
        self.rot_vel = rot_vel
        self.angle = 0      #starting angle of car; changes as it rotates
        self.x, self.y = self.START_POS
        self.acceleration = 0.1     
        
    def rotate(self, left=False, right = False):        #function handling rotate
        if left:
            self.angle += self.rot_vel
        elif right:
            self.angle -= self.rot_vel
    
    def draw(self,win):     #draw car function; calls helper to rotate car
        rot_image(win,self.img, (self.x, self.y), self.angle)
    
    def move_forward(self):       #manages vel of car based on acceleration
        self.vel = min(self.vel + self.acceleration, self.max_vel)  #limits vel
        self.move()     #call move function
        
    def move_backward(self):       #manages vel of car based on acceleration (backwards movement)
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)  #limits vel (slower backward)
        self.move()     #call move function
    
    def move(self):     #function controlling movement
        radians = math.radians(self.angle)          #convert direction car facing from angle to radians
        vertical = math.cos(radians) * self.vel    #y-velocity
        horizontal = math.sin(radians) * self.vel   #x-velocity
        
        self.y -= vertical
        self.x -= horizontal
    
    def collide(self,mask,x=0,y=0):     #checks for collisions 
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)         #find point of intersection
        return poi      #poi = None if there's no collision
    
    def reset(self):        #resets position of car once race is finished
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


class PlayerCar(AbstractCar):       #player car class which inherits all features from abstract class
    IMG = player_car
    START_POS = (175, 200)
    
    def reduce_speed(self):     #reduces speed of car when key not pressed (for player only)
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()  
    
    def bounce(self):       #for when car hits border
        self.vel = -self.vel    #make car bounce backward
        self.move()

class ComputerCar(AbstractCar):     #class for computer car
    IMG = cpu_car
    START_POS = (150,200)
    
    def __init__(self, max_vel, rot_vel, path = []):       #override init function; add or change some features
        super().__init__(max_vel, rot_vel)
        self.path = path    #list of points cpu moves to
        self.current_point = 0
        self.vel = max_vel
    
    def draw_points(self,win):          #function which can draw points in path
        for point in self.path:
            pygame.draw.circle(win, "red", point, 5)
    
    def draw(self,win):     #override original draw method
        super().draw(win)
        #self.draw_points(win)       #draws all path points
    
    def update_path_point(self):        #make sure cpu updates current point when we reach one
        target = self.path[self.current_point]
        rect = pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())     #make rect for img
        if rect.collidepoint(*target):   #checks if img collides with point
            self.current_point += 1     #move to next point after we hit it
    
    def move(self):     #controls direction of movement for cpu
        if self.current_point >= len(self.path):    #make sure we have point to move too
            return
        self.calculate_angle()      #method altering angle of car
        self.update_path_point()    #see if we need to move to next point
        super().move()      #call overriden move method
    
    def calculate_angle(self):  #method altering angle of car
        
        #find displacement between target and current point
        target_x, target_y = self.path[self.current_point]
        x_diff = target_x - self.x
        y_diff = target_y - self.y
        
        if y_diff ==0:      #manually set angle if y_diff = 0, avoid 0 div error
            desired_radian_angle = math.pi/2
        else:           #get angle between car and next point
            desired_radian_angle = math.atan(x_diff/y_diff)
        
        if target_y> self.y:        #gets rid of equivalent angle value issue
            desired_radian_angle += math.pi
        
        #helps decide which direction cpu turns     
        difference_in_angle = self.angle - math.degrees(desired_radian_angle)  
        if difference_in_angle >= 180:      #chose optimal direction to turn
            difference_in_angle -= 360
        if difference_in_angle>0:
            self.angle -= min(self.rot_vel, abs(difference_in_angle))
        else:
            self.angle += min(self.rot_vel, abs(difference_in_angle))
        
    def next_level(self, Level):       #function which updates cpu speed per level
        self.reset()
        self.vel = self.max_vel + (Level - 1) * 0.12
        self.current_point = 0
    
        

def draw(win, images, player_car, computer_car, game_info):     #drawing function
    for img, pos in images:
        win.blit(img, pos)
    
    level_text = FONT.render(f"Level {game_info.level}", 1, "green")    #text for level
    win.blit(level_text, (10, HEIGHT - level_text.get_height() - 70))
    
    time_text = FONT.render(f"Time: {round(game_info.get_level_time(),1)}s", 1, "green")    #text for level
    win.blit(time_text, (10, HEIGHT - time_text.get_height() - 40))
    
    vel_text = FONT.render(f"Velocity: {round(player_car.vel, 1)}px/s", 1, "green")    #text for level
    win.blit(vel_text, (10, HEIGHT - vel_text.get_height() - 10))
    
    player_car.draw(win)        #draw car
    computer_car.draw(win)      #draw cpu car
    pygame.display.update()

def move_player(player_car):        #function handling player movement
    keys = pygame.key.get_pressed() 
    moved = False       #variable checking if gas ("up" arrow) is pressed
    
    if keys[pygame.K_LEFT]:         #car rotation using left/right arrow keys
        player_car.rotate(left = True)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right = True)
    if keys[pygame.K_UP]:       #move forward
        moved = True
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        moved = True
        player_car.move_backward()
    
    if not moved:       #reduce speed when up arrow isn't pressed
        player_car.reduce_speed()

def handle_collision(player_car, computer_car, game_info):     #function handling all collisions, with border & finish line
    
    if player_car.collide(TRACK_BORDER_MASK) != None:       #check for collision
        player_car.bounce()
    
    computer_finish_poi_collide = computer_car.collide(FINISH_MASK, 125,250)       #variable checking if cpu hit finish line
    if computer_finish_poi_collide != None:
        blit_text_center(WIN, FONT, "You lost. Game resetting...")  #reset game if cpu wins
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()      #reset positions if race finishes
        #computer_car.reset()
        computer_car.next_level(1)  #reset cpu to lvl 1 speed
        
    player_finish_poi_collide = player_car.collide(FINISH_MASK, 125,250)       #variable checking if player hit finish line
    if player_finish_poi_collide!= None:     #check if we hit finish line
        
        if player_finish_poi_collide[1] ==0:       #going backwards into finish line
            player_car.bounce()
        else:               #crossed finish line
            game_info.next_level()  #update level
            player_car.reset()      #reset positions if race finishes
            computer_car.next_level(game_info.level)     #update cpu speed for next lvl

run = True
clock = pygame.time.Clock() #clock object
images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POSITION), (TRACK_BORDER, (0,0))]   #list of tuples with images and their positions
player_car = PlayerCar(4,4)     #instance of player car
computer_car = ComputerCar(2,5, PATH) #instance of cpu car

game_info = GameInfo()

while run:      #main game loop
    clock.tick(FPS)  #clock.tick regulates loop running speed
    draw(WIN, images, player_car, computer_car, game_info)

    while not game_info.started:    #if current level hasn't started yet
        blit_text_center(WIN, FONT, f"Press any key to start level {game_info.level}!")
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if event.type == pygame.KEYDOWN:    #start level if any key is pressed
                game_info.start_level()
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
        
    computer_car.move()     #move cpu car    
    move_player(player_car)     #function for player movement
    
    handle_collision(player_car, computer_car, game_info)      #function handling all collisions

    if game_info.game_finished():   #once all 10 levels are completed
        blit_text_center(WIN, FONT, "You won. Wow!")  #reset game if player wins
        pygame.display.update()
        pygame.time.wait(5000)
        game_info.reset()
        player_car.reset()      #reset positions if race finishes
        computer_car.next_level(1)
#print(computer_car.path)   #prints computer path
pygame.quit()


"""if event.type == pygame.MOUSEBUTTONDOWN:        #adds points to path by clicking
            pos = pygame.mouse.get_pos()
            computer_car.path.append(pos)
    """
    


